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

import matplotlib.pylab as plt, numpy as np
from matplotlib import font_manager

myFont = font_manager.FontProperties(fname='/Library/Fonts/Songti.ttc')
titleSize = 14
tipSize = 12

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
    plt.cla()
    plt.clf()
    plt.close()
    print 'drawPieChart',title,'over'

def drawNBarChart(data_label_colors, xindex, xlabel, ylabel, title):
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
                    
    ax.yaxis.grid(True, which='major') #y坐标轴的网格使用主刻度  
    plt.xlabel(xlabel, fontproperties=myFont, size=titleSize)
    plt.ylabel(ylabel, fontproperties=myFont, size=titleSize)
    plt.title(title, fontproperties=myFont, size=titleSize)
    plt.xticks(index + (len(data_label_colors)/2.)*bar_width, xindex, fontproperties=myFont, size=tipSize)
    plt.legend(prop=font_manager.FontProperties(fname='/Library/Fonts/Songti.ttc', size=tipSize))
    
    plt.tight_layout()
    plt.savefig(cur_file_dir+'/'+title+'.png', format='png')
    plt.cla()
    plt.clf()
    plt.close()
    print 'drawNBarChart',title,'over'
    
def drawLineChart(pd_series, title, xlabel, ylabel, xticks, xticklabels):
    ax = pd_series.plot(figsize=(14,8))
    #for label in ax.get_xticklabels(): #xtick
    #    label.set_fontproperties(myFont)
    for label in ax.get_yticklabels(): #ytick
        label.set_fontproperties(myFont)
    for label in ax.get_label(): # legend
        label.set_fontproperties(myFont)
    ax.set_title(title, fontproperties=myFont, size=titleSize)
    ax.set_xlabel(xlabel, fontproperties=myFont, size=tipSize)
    ax.set_ylabel(ylabel, fontproperties=myFont, size=tipSize)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels, fontproperties=myFont, size=tipSize)
    ax.xaxis.grid(True, which='major') #x坐标轴的网格使用主刻度  
    ax.yaxis.grid(True, which='major') #y坐标轴的网格使用主刻度  
    #ax.yaxis.grid(True, which='minor') #y坐标轴的网格使用次刻度  
    plt.savefig(cur_file_dir+'/'+title+'.png', format='png')
    plt.cla()
    plt.clf()
    plt.close()
    print 'drawLineChart',title,'over'
    
def drawBarAXBarChart(bar1_series, bar2_series, title, xlabel, y_bar1_label, y_bar2_label, xticklabels, bar1_label, bar2_label):
    n_groups = xticklabels.size
    fig, ax = plt.subplots(dpi=100, figsize=(16,8))

    index = np.arange(n_groups)
    bar_width = 0.25

    opacity = 0.4
    error_config = {'ecolor': '0.3'}
    def autolabel(ax, rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.005*height,
                    '%d' % int(height),
                    ha='center', va='bottom', fontproperties=myFont, size=tipSize-1)
    rects = plt.bar(index, bar1_series, bar_width,
                    alpha=opacity,
                    color='b',
                    error_kw=error_config,
                    label=bar1_label)
    autolabel(ax,rects)              
    plt.xlabel(xlabel, fontproperties=myFont, size=titleSize)
    plt.ylabel(y_bar1_label, fontproperties=myFont, size=titleSize, color='b')
    for label in ax.get_yticklabels():
        label.set_color('b')
    plt.title(title, fontproperties=myFont, size=titleSize)
    plt.xticks(index + (1/2.)*bar_width, xticklabels, fontproperties=myFont, size=tipSize)
    plt.legend(prop=font_manager.FontProperties(fname='/Library/Fonts/Songti.ttc', size=tipSize))
    
    print 'drawNBarChart',title,'1 over'
    ax1 = ax.twinx()
    rects1 = plt.bar(index+1*bar_width, bar2_series, bar_width,
                    alpha=opacity,
                    color='r',
                    error_kw=error_config,
                    label=bar2_label, axes=ax1)
    autolabel(ax1,rects1)              
    for label in ax1.get_yticklabels():
        label.set_color('r')
    plt.ylabel(y_bar2_label, fontproperties=myFont, size=titleSize, color='r')
    plt.xticks(index + (2/2.)*bar_width, xticklabels, fontproperties=myFont, size=tipSize)
    plt.legend((rects, rects1), (bar1_label, bar2_label),prop=font_manager.FontProperties(fname='/Library/Fonts/Songti.ttc', size=tipSize))
    
    plt.tight_layout()
    
    plt.savefig(cur_file_dir+'/'+title+'.png', format='png')
    plt.cla()
    plt.clf()
    plt.close()
    print 'drawNBarChart',title,'2 over'
    
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
            province_city = pd.Series(province_city_all['USER_CNT'].values, index=province_city_all['PROVINCE']+' '+province_city_all['CITY'], name=hname+u'用户地域分布')
            drawPieChart(province_city[1:10], province_city[1:10].index, province_city.name+u'（第二位至第十位）')
            drawNBarChart([(province_city[0:10], hname, 'b')], province_city[0:10].index, u'市级', u'用户数量', province_city.name+u'（第一位至第十位）')
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
    
    ######### 使用产品时间 ##########
    sqls = [('''
    SELECT CONCAT_WS(':',SUBSTRING_INDEX(SUBSTRING_INDEX(VISIT_TIME,' ',-1),':',2),'00') AS VISIT_TIME, COUNT(*) AS CNT FROM qyw.qyw_4th_visit GROUP BY SUBSTRING_INDEX(SUBSTRING_INDEX(VISIT_TIME,' ',-1),':',2) ORDER BY VISIT_TIME;
    ''',8,u'日均操作时间分布（分钟级）',u'操作时间',u'操作数量'),('''
    SELECT CONCAT_WS(':',SUBSTRING_INDEX(VISIT_TIME,':',2),'00') AS VISIT_TIME, COUNT(*) AS CNT FROM qyw.qyw_4th_visit GROUP BY SUBSTRING_INDEX(VISIT_TIME,':',2) ORDER BY VISIT_TIME;
    ''',1,u'八日操作时间总分布（分钟级）',u'操作时间',u'操作数量'),('''
    SELECT CONCAT_WS(':',SUBSTRING_INDEX(SUBSTRING_INDEX(VISIT_TIME,' ',-1),':',2),'00') AS VISIT_TIME, COUNT(DISTINCT USER_ID) AS CNT FROM qyw.qyw_4th_visit GROUP BY SUBSTRING_INDEX(SUBSTRING_INDEX(VISIT_TIME,' ',-1),':',2) ORDER BY VISIT_TIME;
    ''',8,u'日均在线用户时间分布（分钟级）',u'操作时间',u'用户数量'),('''
    SELECT CONCAT_WS(':',SUBSTRING_INDEX(VISIT_TIME,':',2),'00') AS VISIT_TIME, COUNT(DISTINCT USER_ID) AS CNT FROM qyw.qyw_4th_visit GROUP BY SUBSTRING_INDEX(VISIT_TIME,':',2) ORDER BY VISIT_TIME;
    ''',1,u'八日在线用户总分布（分钟级）',u'操作时间',u'用户数量')]
    for sql, divided, title, xlabel, ylabel in sqls:
        df_frame = pd.read_sql(sql, con=conn)
        df_series = pd.Series(df_frame['CNT'].values/divided, index=df_frame['VISIT_TIME'], name=title)
        visit_times = []
        cns = []
        xticklabels = []
        if divided == 1:
            for i in xrange(8,16):
                visit_day = '2016-03-'
                if i < 10:
                    visit_day += '0'+str(i)+' '
                else:
                    visit_day += str(i) + ' '
                isXtick = True
                for j in xrange(0,24):
                    if j < 10:
                        visit_hour = '0'+str(j)+':'
                    else:
                        visit_hour = str(j) + ':'
                    if  j != 0:
                        isXtick = False
                    for k in xrange(0,60):
                        if k < 10:
                            visit_min = '0'+str(k)+':'
                        else:
                            visit_min = str(k) + ':'
                        if  k != 0:
                            isXtick = False
                        visit_sec = '00'
                        visit_time = visit_day+visit_hour+visit_min+visit_sec
                        if isXtick:
                            xticklabels.append(visit_time)
                        cn = 0
                        try:
                            cn = df_series[visit_time]
                            visit_times.append(visit_time)
                            cns.append(cn)
                        except KeyError:
                            visit_times.append(visit_time)
                            cns.append(cn)
        elif divided == 8:
            for j in xrange(0,24):
                if j < 10:
                    visit_hour = '0'+str(j)+':'
                else:
                    visit_hour = str(j) + ':'
                isXtick = True
                if j % 3 != 0:
                    isXtick = False
                for k in xrange(0,60):
                    if k < 10:
                        visit_min = '0'+str(k)+':'
                    else:
                        visit_min = str(k) + ':'
                    if k != 0:
                        isXtick = False
                    visit_sec = '00'
                    visit_time = visit_hour+visit_min+visit_sec
                    if isXtick:
                        xticklabels.append(visit_time)
                    cn = 0
                    try:
                        cn = df_series[visit_time]
                        visit_times.append(visit_time)
                        cns.append(cn)
                    except KeyError:
                        visit_times.append(visit_time)
                        cns.append(cn)
        df_new_series = pd.Series(cns, index=visit_times, name=title)
        drawLineChart(df_new_series, df_new_series.name, xlabel, ylabel, np.linspace(0, len(df_new_series), len(xticklabels)), xticklabels)
    ########## 用户消费金额分析 #########
    df_amount = pd.read_sql('''SELECT t1.USER_ID, t1.VISIT_TIME, t2.MEANS, COUNT(*) AS VISIT_CNT, AVG(AMOUNT) AS AVG FROM qyw.qyw_4th_visit_pay_base AS t1 INNER JOIN (SELECT VISIT_OP, GROUP_CONCAT(MEAN) AS MEANS, GROUP_CONCAT(CATEGORY) AS CATEGORIES, COUNT(*) FROM qyw.qyw_4th_business_dict GROUP BY VISIT_OP) AS t2 ON t1.VISIT_OP=t2.VISIT_OP GROUP BY t1.USER_ID, t1.VISIT_TIME, t1.VISIT_OP ORDER BY t1.USER_ID, t1.VISIT_TIME;
        ''', con=conn)
    ### 消费金额 vs. 操作 ###
    sr_op_cnt = df_amount.groupby(['MEANS'])['VISIT_CNT'].sum()
    sr_op_sum = df_amount.groupby(['MEANS'])['AVG'].sum()
    sr_op_mean = sr_op_sum / sr_op_cnt
    drawPieChart(sr_op_cnt, sr_op_cnt.index, u'主要的支付类操作占比（操作数量）')
    drawPieChart(sr_op_mean, sr_op_mean.index, u'主要的支付类操作涉及平均金额')
    drawBarAXBarChart(sr_op_cnt, sr_op_mean, u'主要的支付类操作频次vs.平均金额', u'支付类操作', u'操作数量', u'平均金额', sr_op_cnt.index, u'操作频次', u'平均消费')
    ### 用户消费平均情况 ###
    df_cnt = pd.DataFrame({'USER_ID':df_amount.groupby(['USER_ID'])['AVG'].count().index,'COUNT':df_amount.groupby(['USER_ID'])['AVG'].count()}, columns=['USER_ID','COUNT'])
    df_mean = pd.DataFrame({'USER_ID':df_amount.groupby(['USER_ID'])['AVG'].mean().index,'MEAN':df_amount.groupby(['USER_ID'])['AVG'].mean()}, columns=['USER_ID','MEAN'])
    df_merge = pd.merge(df_cnt, df_mean, on='USER_ID')
    sr_amount = df_merge.groupby(['MEAN'])['USER_ID'].count().sort_values(ascending=False)
    amount_users = [sr_amount[sr_amount.index > 10].sum(), sr_amount[sr_amount.index <= 10].sum()-sr_amount[sr_amount.index <= 5].sum(), sr_amount[sr_amount.index <= 5].sum()]
    amount_users_index = [u'大于10元', u'介于10元至5元之间', u'小于5元'];
    sr_user_amount = pd.Series(amount_users, index=amount_users_index)
    sr_user_amount.title=u'用户消费金额总分布'
    drawPieChart(sr_user_amount, sr_user_amount.index, sr_user_amount.title)
    sr_amount.index = map(lambda x: round(x,2), sr_amount.index)
    drawNBarChart([(sr_amount[:10].values, u'Top10平均消费指数', 'b')], sr_amount[:10].index, u'平均消费金额', u'消费人数', u'Top10用户平均消费指数')
except:
    pass
finally:
    conn.close()