#!/usr/bin/env python
# coding:utf-8

import xlrd, json

xls_prefix = '/Users/dujiawei/Desktop/流程挖掘案例/趣医网/趣医网-第四阶段/用户日志/'
sql_prefix = '/Users/dujiawei/Desktop/流程挖掘案例/趣医网/趣医网-第四阶段/用户日志/SQL/'

names = ['安徽省中医院_visit', '武汉市中心医院_visit']

for name in names:
    params = [{'op':0}, {'hospitalID':0}, {'isLogin':0}, {'operateUserSource':0}, {'APP_UUID':0}, {'IMEI_ID':0}, {'CHANNEL_ID':0}, {'PHONETYPE':0}]
    xls_file = xls_prefix + name +'.xlsx'
    workbook = xlrd.open_workbook(xls_file)
    print "There are {} sheets in the workbook".format(workbook.nsheets)
    for bookSheet in workbook.sheets():
        print bookSheet.name
        sql_file = sql_prefix + name + '.sql'
        sql_obj = open(sql_file, 'w')
        print xls_file, '->', sql_file
        # 行循环
        for row in xrange(bookSheet.nrows):
            if row > 0:
                sqlStr = 'INSERT INTO qyw_4th_user(USER_ID, VISIT_OP, VISIT_TIME, OP, HOSPITAL_ID, IS_LOGIN, USER_RESOURCE, APP_UUID, IMEI_ID, CHANNEL_ID, PHONETYPE) VALUES ('
                for col in xrange(bookSheet.ncols):
                    cell = bookSheet.cell(row, col)
                    cell_value = cell.value
                    cell_str = ''
                    # ctype :0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
                    if cell.ctype == 1 or cell.ctype == 4:
                        cell_str = str(cell_value.encode('utf8'))
                    elif cell.ctype == 2:
                        cell_str = str(int(cell_value))
                    elif cell.ctype == 3:
                        cell_str = str(xlrd.xldate.xldate_as_datetime(cell_value, workbook.datemode))
                    if cell.ctype == 0 or cell_value == '':
                        sqlStr += 'null'+','
                    elif col == 3:
                        # decode json
                        decodejson = json.loads(cell_str)
                        for param in params:
                            for k,v in param.items():
                                if(decodejson.has_key(k)):
                                    sqlStr += '\''+decodejson[k]+'\''+','
                                    param[k] += 1
                                else:
                                    sqlStr += 'null'+','
                    else:
                        sqlStr += '\''+cell_str+'\''+','
                sqlStr = sqlStr[:-1] + ');\n'
                sql_obj.write(sqlStr.encode('utf-8'))
        sql_obj.close()
    print params