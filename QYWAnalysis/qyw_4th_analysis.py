#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: Jiawei Du
# email: jiaweidu.js@gmail.com
# added: 2016/03/31

import sys,os
#获取脚本文件的当前路径
def cur_file_dir():
     #获取脚本路径
     path = sys.path[0]
     #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)
#打印结果

cur_file_dir = cur_file_dir()

import matplotlib.pylab as plt
from matplotlib import font_manager

myFont = font_manager.FontProperties(fname='/Library/Fonts/Songti.ttc')
titleSize = 12
tipSize = 10

def drawPieChart(data, labels, title):
    fig = plt.figure(dpi=100, figsize=(8,8))
    # first axes
    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    patches, texts, autotexts = ax1.pie(data, labels=labels, autopct='%1.1f%%', colors=['yellowgreen', 'gold', 'lightskyblue', 'lightcoral'])
    plt.setp(autotexts, fontproperties=myFont, size=tipSize)
    plt.setp(texts, fontproperties=myFont, size=tipSize)
    ax1.set_title(title,fontproperties=myFont, size=titleSize)
    ax1.set_aspect(1)
    #plt.show()
    plt.savefig(cur_file_dir+'/'+title+'.png', format='png')
    print 'drawPieChart',title,'over'

def drawNBarChart(data_label_colors, xindex, xlabel, ylabel, title):
    import numpy as np
    n_groups = xindex.size
    fig, ax = plt.subplots(dpi=100, figsize=(14,8))

    index = np.arange(n_groups)
    bar_width = 0.35

    opacity = 0.4
    error_config = {'ecolor': '0.3'}
    
    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.005*height,
                    '%d' % int(height),
                    ha='center', va='bottom', fontproperties=myFont, size=tipSize-1)
    i = 0
    for data, label, color in data_label_colors:
        rects = plt.bar(index+i*bar_width, data, bar_width,
                    alpha=opacity,
                    color=color,
                    error_kw=error_config,
                    label=label)
        autolabel(rects)
        i += 1
                    
    plt.xlabel(xlabel, fontproperties=myFont, size=titleSize)
    plt.ylabel(ylabel, fontproperties=myFont, size=titleSize)
    plt.title(title, fontproperties=myFont, size=titleSize)
    plt.xticks(index + (len(data_label_colors)/2.)*bar_width, xindex, fontproperties=myFont, size=tipSize)
    plt.legend(prop=font_manager.FontProperties(fname='/Library/Fonts/Songti.ttc', size=tipSize))
    
    plt.tight_layout()
    plt.savefig(cur_file_dir+'/'+title+'.png', format='png')
    print 'drawNBarChart',title,'over'
    
import pandas as pd, MySQLdb

conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='qyw', charset='utf8')
try:
    ############ 用户地域分析 ###########
    df_province_city_hid_all = pd.read_sql('''
    SELECT HOSPITAL_ID, PROVINCE, CITY, COUNT(DISTINCT USER_ID) AS USER_CNT FROM (SELECT * FROM (SELECT * FROM qyw.qyw_4th_visit WHERE USER_ID > 0 ORDER BY USER_ID) AS t1 INNER JOIN (SELECT USER_ID AS CUS_ID, PROVINCE, CITY, BIRTHDAY, GENDER, REGISTER_DATE FROM qyw.qyw_4th_user ORDER BY CUS_ID) AS t2 ON t1.USER_ID = t2.CUS_ID) AS t3 WHERE PROVINCE IS NOT null AND CITY IS NOT null GROUP BY HOSPITAL_ID, PROVINCE, CITY ORDER BY HOSPITAL_ID, USER_CNT DESC;
    ''', con=conn)
    ###### pie charts ######
    # merge hospitals
    province_city_merge_all = df_province_city_hid_all.groupby(['PROVINCE', 'CITY'])['USER_CNT'].sum().reset_index().sort_values(['USER_CNT'],0,[False])
    province_city_merge = pd.Series(province_city_merge_all['USER_CNT'].values, index=province_city_merge_all['PROVINCE']+' '+province_city_merge_all['CITY'], name=u'用户地域总分布（第三位至第十二位）')
    drawPieChart(province_city_merge[2:12], province_city_merge[2:12].index, province_city_merge.name)
    # each hospital
    hospitals = [{270001:u'武汉市中心医院'}, {5510002:u'安徽省中医院'}]
    for hospital in hospitals:
        for hid, hname in hospital.items():
            province_city_all = df_province_city_hid_all[df_province_city_hid_all['HOSPITAL_ID'] == hid]
            province_city = pd.Series(province_city_all['USER_CNT'].values, index=province_city_all['PROVINCE']+' '+province_city_all['CITY'], name=hname+u'用户地域分布（第三位至第十二位）')
            drawPieChart(province_city[2:12], province_city[2:12].index, province_city.name)
    ###### n bar charts ######
    province_merge_all = df_province_city_hid_all.groupby(['HOSPITAL_ID','PROVINCE'])['USER_CNT'].sum().reset_index().sort_values(['PROVINCE','HOSPITAL_ID'],0,[True, False])
    province_merge_less = pd.merge(province_merge_all[province_merge_all['PROVINCE']!=u'安徽'], province_merge_all[province_merge_all['PROVINCE']!=u'湖北'])
    province_merge_list = [{u'典型医院用户地域分布（所有）':province_merge_all}, {u'典型医院用户地域分布（部分）':province_merge_less}]
    bar_colors = ['b', 'r']
    for province_merge in province_merge_list:
        for title, data in province_merge.items():
            province_merge_pivot = data.pivot('PROVINCE', 'HOSPITAL_ID', 'USER_CNT')
            province_merge_pivot = province_merge_pivot.fillna(0)
            data_label_colors = []
            i = 0
            for hospital in hospitals:
                for hid, hname in hospital.items():
                    data_label_colors.append((province_merge_pivot[hid], hname, bar_colors[i]))
                i += 1
            drawNBarChart(data_label_colors, province_merge_pivot.index, u'省份', u'用户数量', title)
    ########## 登录方式分析 ##########
    publicservice_hid_all = pd.read_sql('''
    SELECT CONCAT_WS('@', IF(t2.PUBLIC_SERVICE_MEAN IS null, '其他渠道', t2.PUBLIC_SERVICE_MEAN), t1.PUBLIC_SERVICE_TYPE) AS PUBLIC_SERVICE_TYPE, USER_CNT FROM (SELECT PUBLIC_SERVICE_TYPE, COUNT(DISTINCT USER_ID) AS USER_CNT FROM qyw.qyw_4th_visit WHERE PUBLIC_SERVICE_TYPE IS NOT null GROUP BY PUBLIC_SERVICE_TYPE) AS t1 LEFT JOIN (SELECT * FROM qyw.qyw_4th_public_service_type) AS t2 ON t1.PUBLIC_SERVICE_TYPE = t2.PUBLIC_SERVICE_TYPE;
    ''', con=conn)
    publicservice_hid = pd.Series(publicservice_hid_all['USER_CNT'].values, index=publicservice_hid_all['PUBLIC_SERVICE_TYPE'], name=u'用户登录方式分布')
    ####### pie charts ######
    publicservice_hid_main = publicservice_hid.sort_values(0,False)
    publicservice_hid_main.name = u'用户主要登录方式分布'
    drawPieChart(publicservice_hid_main[:4], publicservice_hid_main[:4].index, publicservice_hid_main.name+u'饼图')
    ####### n bar charts ######
    drawNBarChart([(publicservice_hid.values, u'登录方式', bar_colors[0])], publicservice_hid.index, u'登录方式', u'用户数量', publicservice_hid.name+u'柱状图')
except:
    pass
finally:
    conn.close()