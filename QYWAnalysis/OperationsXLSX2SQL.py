#!/usr/bin/env python
# coding:utf-8

import xlrd, json

xls_prefix = '/Users/dujiawei/Desktop/流程挖掘案例/趣医网/趣医网-第四阶段/用户日志/'
sql_prefix = '/Users/dujiawei/Desktop/流程挖掘案例/趣医网/趣医网-第四阶段/用户日志/SQL/'

hospitals = {'安徽省中医院_visit':'5510002', '武汉市中心医院_visit':'270001', '安徽省中医院_visit_no_params':'5510002', '武汉市中心医院_visit_no_params':'270001'}

for name, hid in hospitals.items():
    params = [{'OP':(['op'],0)}, {'HOSPITAL_ID':(['hospitalId','hospitalID','HOSPITAL_ID'],0)}, {'IS_LOGIN':(['isLogin'],0)}, {'USER_RESOURCE':(['operateUserSource'],0)}, {'APP_UUID':(['APP_UUID'],0)}, {'IMEI_ID':(['IMEI_ID'],0)}, {'CHANNEL_ID':(['CHANNEL_ID'],0)}, {'PHONETYPE':(['PHONETYPE'],0)}]
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
                sqlHead = 'INSERT INTO qyw_4th_visit(USER_ID,VISIT_OP,VISIT_TIME,'
                sqlTail = '('
                for col in xrange(bookSheet.ncols):
                    cell = bookSheet.cell(row, col)
                    cell_value = cell.value
                    cell_str = ''
                    # ctype :0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
                    if col < 3:
                        if cell.ctype == 1 or cell.ctype == 4:
                            cell_str = str(cell_value.encode('utf8'))
                        elif cell.ctype == 2:
                            cell_str = str(int(cell_value))
                        elif cell.ctype == 3:
                            cell_str = str(xlrd.xldate.xldate_as_datetime(cell_value, workbook.datemode))
                        if cell.ctype == 0 or cell.ctype == 5 or cell_value == '':
                            cell_str = 'null'
                        sqlTail += '\''+cell_str+'\''+','
                    elif col == 3:
                        cell_str = str(cell_value.encode('utf8'))
                        try:
                            # decode json
                            decodejson = json.loads(cell_str)
                            for param in params:
                                for k, (l, c) in param.items():
                                    find = False
                                    vv = ''
                                    for ll in l:
                                        if not find and decodejson.has_key(ll):
                                            vv = decodejson[ll]
                                            if k == 'HOSPITAL_ID' and decodejson[ll] != hid:
                                                continue
                                            else:
                                                find = True
                                    if not find and k == 'HOSPITAL_ID': # 保证在电子表格中的每一项都有HOSPITAL_ID
                                        vv = hid
                                    if find:
                                        sqlHead += k+','
                                        sqlTail += '\''+vv+'\''+','
                                        c += 1
                                        param[k] = (l,c)
                                        # v = (filedName, filedCnt) error：因为这样v就引用了一个新的tuple，不是之前的param[k]，且(filedName, filedCnt)没有绑定到param[k]上（只是绑定到了v上）
                                        # ref: http://www.educity.cn/wenda/571922.html
                        except:
                            sqlHead += 'HOSPITAL_ID'+','
                            sqlTail += '\''+hid+'\''+','
                            l, c = params[1]['HOSPITAL_ID']   # attention(hardcode)
                            c += 1
                            params[1]['HOSPITAL_ID'] = (l, c)  # attention(hardcode)
                sqlHead = sqlHead[:-1] + ') VALUES '
                sqlTail = sqlTail[:-1] + ');\n'
                sqlStr = sqlHead+sqlTail
                #print sqlStr
                sql_obj.write(sqlStr.encode('utf-8'))
        sql_obj.close()
    print params