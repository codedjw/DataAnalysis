#!/usr/bin/env python
# coding:utf-8

import xlrd

xls_prefix = '/Users/dujiawei/Desktop/流程挖掘案例/趣医网/趣医网-第四阶段/用户日志/'
sql_prefix = '/Users/dujiawei/Desktop/流程挖掘案例/趣医网/趣医网-第四阶段/用户日志/SQL/'

names = ['业务字典']

xls_file = xls_prefix+names[0]
workbook = xlrd.open_workbook(xls_file+".xlsx")
print "There are {} sheets in the workbook".format(workbook.nsheets)
for bookSheet in workbook.sheets():
    print bookSheet.name
    sql_file = sql_prefix + names[0] + '.sql'
    sql_obj = open(sql_file, 'w')
    print xls_file, '->', sql_file
    # 行循环
    for row in xrange(bookSheet.nrows):
        if row > 0:
            sqlStr = 'INSERT INTO qyw_4th_business_dict(BUSINESS_CODE, MEAN, CATEGORY, VISIT_OP, COMMENTS) VALUES ('
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
                else:
                    sqlStr += '\''+cell_str+'\''+','
            sqlStr = sqlStr[:-1] + ');\n'
            #print sqlStr
            sql_obj.write(sqlStr)
    sql_obj.close()