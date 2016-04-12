#!/usr/bin/env python
# coding:utf-8

import xlrd

xls_prefix = '/Users/dujiawei/Desktop/流程挖掘案例/趣医网/趣医网-第四阶段/用户日志/'
sql_prefix = '/Users/dujiawei/Desktop/流程挖掘案例/趣医网/趣医网-第四阶段/用户日志/SQL/'

names = ['用户信息']

sqlHead = '''/*
 Navicat Premium Data Transfer

 Source Server         : mysqlcoon
 Source Server Type    : MySQL
 Source Server Version : 50625
 Source Host           : localhost
 Source Database       : cop

 Target Server Type    : MySQL
 Target Server Version : 50625
 File Encoding         : utf-8

 Date: 03/29/2016 13:08:48 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `qyw_4th_user`
-- ----------------------------
DROP TABLE IF EXISTS `qyw_4th_user`;
CREATE TABLE `qyw_4th_user` (
  `USER_ID` int(11) DEFAULT NULL,
  `GENDER` int(11) DEFAULT NULL,
  `BIRTHDAY` date DEFAULT NULL,
  `REGISTER_DATE` datetime DEFAULT NULL,
  `PHONE` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;

'''

xls_file = xls_prefix+names[0]
workbook = xlrd.open_workbook(xls_file+".xlsx")
print "There are {} sheets in the workbook".format(workbook.nsheets)
for bookSheet in workbook.sheets():
    print bookSheet.name
    sql_file = sql_prefix + names[0] + '.sql'
    sql_obj = open(sql_file, 'w')
    sql_obj.write(sqlHead)
    print xls_file, '->', sql_file
    # 行循环
    for row in xrange(bookSheet.nrows):
        if row > 0:
            sqlStr = 'INSERT INTO qyw_4th_user(USER_ID, GENDER, BIRTHDAY, REGISTER_DATE, PHONE) VALUES ('
            for col in xrange(bookSheet.ncols):
                cell = bookSheet.cell(row, col)
                cell_value = cell.value
                cell_str = ''
                # ctype :0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
                if cell.ctype == 1 or cell.ctype == 4:
                    cell_str = str(cell_value)
                elif cell.ctype == 2:
                    cell_str = str(int(cell_value))
                elif cell.ctype == 3:
                    cell_str = str(xlrd.xldate.xldate_as_datetime(cell_value, workbook.datemode))
                if cell.ctype == 0 or cell_value == '':
                    sqlStr += 'null'+','
                else:
                    sqlStr += '\''+cell_str+'\''+','
            sqlStr = sqlStr[:-1] + ');\n'
            print sqlStr
            sql_obj.write(sqlStr)
    sql_obj.close()