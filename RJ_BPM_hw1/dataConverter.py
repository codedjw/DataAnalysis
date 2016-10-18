#!/usr/bin/env python
# coding:utf-8

import pandas as pd, MySQLdb

def load_excel_data(filename):
    data = pd.ExcelFile(filename)
    print data.sheet_names
    df = data.parse("Sheet1")
    return df
    
filename = '/Users/dujiawei/Downloads/data/'
try:
    conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='renji', charset='utf8')
    for i in xrange(30):
        subname = str(i+1)
        df = load_excel_data(filename+subname+'.xlsx')        
        df.to_sql('2016eventlog_'+subname,conn,flavor='mysql')
    conn.close()
except MySQLdb.Error,e:
    print e.args[1]
