#!/usr/bin/env python
# coding:utf-8

import pandas as pd, numpy as np, matplotlib.pylab as plt
# 数据库访问
import MySQLdb, datetime

# Open database connection
conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='qyw', charset='utf8')

try:
    user_visits = pd.read_sql('''
    SELECT USER_ID, OPERATE_TIME, PAGE_NAME, ELEMENT_NAME FROM qyw.qyw_5th_visit ORDER BY USER_ID, OPERATE_TIME;
    ''', con=conn)
    user_visits.insert(0, 'CASE_ID','')
    unique_users = user_visits['USER_ID'].unique()
    for user_id in unique_users:
        single_user_visits = user_visits[user_visits['USER_ID'] == user_id].sort_values(['OPERATE_TIME'],0,[True])
        size = len(single_user_visits.index)
        start = single_user_visits.index[0]
        date = None
        cid = 0
        for index, row in single_user_visits.iterrows():
            start_operate_time = row['OPERATE_TIME']
            cur_date = start_operate_time.strftime('%Y-%m-%d')
            if not date:
                date = cur_date
            end_operate_time = start_operate_time
            next_date = cur_date
            if index < start+size-1:
                end_operate_time = single_user_visits.loc[index+1, 'OPERATE_TIME']
                next_date = end_operate_time.strftime('%Y-%m-%d')
            interval = end_operate_time - start_operate_time
            interval_secs = interval.total_seconds()
            case_id = str(row['USER_ID'])+'@'+date+'_'+str(cid)
            single_user_visits.ix[index, 'CASE_ID'] = case_id
            if interval_secs > 5*60:
                if date != next_date:
                    cid = 0
                    date = next_date
                else:
                    cid += 1
        single_user_visits.to_sql('qyw_5th_event', conn, flavor='mysql', if_exists='append', index=False)
except MySQLdb.Error, e:
    print "MySQL Error %d: %s" % (e.args[0], e.args[1])