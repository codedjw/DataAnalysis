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
sv_file_dir = cur_file_dir + '/' + u'统计结果';

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
    plt.savefig(sv_file_dir+'/'+title+'.png', format='png')
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
    plt.savefig(sv_file_dir+'/'+title+'.png', format='png')
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
    plt.savefig(sv_file_dir+'/'+title+'.png', format='png')
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
    
    plt.savefig(sv_file_dir+'/'+title+'.png', format='png')
    plt.cla()
    plt.clf()
    plt.close()
    print 'drawNBarChart',title,'2 over'
    
import pandas as pd, MySQLdb

conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='qyw', charset='utf8')
try:
    df_new_user = pd.read_sql('''
    SELECT * FROM qyw_4th_event_new_user;
    ''',
    con=conn)
    
    df_old_user = pd.read_sql('''
    SELECT * FROM qyw_4th_event_old_user;
    ''',
    con=conn)
except:
    pass
finally:
    conn.close()