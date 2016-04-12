#!/usr/bin/env python
# coding:utf-8

# 手机号码归属地查询API调用
import urllib2, json

def getAreaByPhoneNumV1(phone_num):
    if(phone_num):
        url = 'http://apis.baidu.com/apistore/mobilenumber/mobilenumber?phone='+phone_num
        req = urllib2.Request(url)
        
        req.add_header('apiKey', 'ff4f9a23b904e94356b0ee6a4d017009')
        resp = urllib2.urlopen(req)
        content = resp.read()
        if(content):
            decodejson = json.loads(content)
            if decodejson['errNum'] == 0:
                return (decodejson['retData']['province'], decodejson['retData']['city'])

def getAreaByPhoneNumV2(phone_num):
    if(phone_num):
        url = 'http://api.k780.com:88/?app=phone.get&phone='+phone_num+'&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json'
        req = urllib2.Request(url)
        
        resp = urllib2.urlopen(req)
        content = resp.read()
        if(content):
            decodejson = json.loads(content)
            if decodejson['success'] == '1':
                att = decodejson['result']['att'].split(',')
                if len(att) == 3:
                    return (att[1], att[2])
                elif len(att) == 2:
                    return (att[1], att[1])
                elif len(att) == 1:
                    return (att[0], att[0])

# 数据库访问
import MySQLdb

# Open database connection
conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='cop', charset='utf8')
# Prepare a cursor object using cursor() method
cur=conn.cursor()

try:
    # Execute the SQL command
    # cur.execute('SELECT * FROM qyw_4th_area')
    cur.execute('SELECT * FROM qyw_4th_area WHERE AREA = \'- -\' OR AREA LIKE \'%全国%\';')
    # Fetch all the rows in a list of lists
    results = cur.fetchall()
except MySQLdb.Error, e:
    print "MySQL Error %d: %s" % (e.args[0], e.args[1])


for row in results:
    phone_prefix = row[0]
    phone_areacode = row[1]
    phone_number = phone_prefix+'1234'
    # ret = getAreaByPhoneNumV1(phone_number)
    ret = getAreaByPhoneNumV2(phone_number)
    province = ret[0]
    city = ret[1]
    print province, city
    updateSql = 'UPDATE qyw_4th_area SET AREA=\''+province+' '+city+'\' WHERE PHONE_PREFIX=\''+phone_prefix+'\''
    print updateSql
    try:
        # Execute the SQL command
        cur.execute(updateSql)
        conn.commit()
    except:
        conn.rollback()

# disconnect from server
cur.close()
conn.close()