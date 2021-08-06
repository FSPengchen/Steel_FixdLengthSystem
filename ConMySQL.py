import copy
import pymysql
from dbutils.pooled_db import PooledDB
import datetime

from clickhouse_driver import Client
import Log

from tkinter import messagebox

'''

转炉引用结构函数

'''

clickhouse_user = 'guest1'
clickhouse_pwd = '0ecadf'
clickhouse_host_sq = '10.6.80.18'
clickhouse_database = 'sensor'
client = Client(host=clickhouse_host_sq, user=clickhouse_user,
                database=clickhouse_database, password=clickhouse_pwd)
#
# pool = PooledDB(pymysql, 1, host='127.0.0.1', user='root', passwd='123', db='convert', port=3306)
# conn = pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
# cursor = conn.cursor()
#
# log = Log.Logger('all.log', level='warning')
#
# # 插入数据库
# def mysqlReplaceInto(sqlfield, sqlvalue):
#     '''
#     :param sqlfield: "inDate,heatNo,wateScrap_begin"
#     :param sqlvalue: str("'" + smeltv1['inDate'] +"','"+ str(smeltv1['heatNo']) +"','"+ smeltv1['wateScrap_begin'] + "'")
#     :return: 写入数据库
#     '''
#     try:
#         sql = "replace into smeltinfo (" + str(sqlfield) + ")value(" + str(sqlvalue) + ")"
#         print(sql)
#         cursor.execute(sql)
#         conn.commit()
#     except Exception as e:
#         log.logger.warning(e)
#     else:
#         return
#
#
# # 根据日期与炉号 判断更新数据
# def mysqlUpData(inDate, heatNo, value):
#     '''
#     :param inDate: 日期   20210628
#     :param heatNo: 炉号   809132
#     :param value:  "wateScrap = "+ str(smeltv1['wateScrap']) +""
#     :return:
#     '''
#     try:
#         sql = "UPDATE smeltinfo SET " + str(value) + " WHERE inDate = '" + str(inDate) + "'"
#         print(sql)
#         cursor.execute(sql)
#         conn.commit()
#     except Exception as e:
#         log.logger.warning(e)
#         print(e)
#     else:
#         return

try:
    # pool = PooledDB(pymysql, 1, host='10.6.1.82', user='furnace', passwd='furnace', db='GPfixleng', port=3306)
    pool = PooledDB(pymysql, 1, host='localhost', user='root', passwd='123', db='steelfixlength',
                    port=3306)  # 5为连接池里的最少连接数

    conn = pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
    cursor = conn.cursor()
except Exception as e:
    print(e)

log = Log.Logger('all.log', level='warning')


# 插入数据库
def CutToSQL(sqlfield, sqlvalue):
    '''
    :param sqlfield: "inDate,heatNo,wateScrap_begin"
    :param sqlvalue: str("'" + smeltv1['inDate'] +"','"+ str(smeltv1['heatNo']) +"','"+ smeltv1['wateScrap_begin'] + "'")
    :return: 写入数据库
    '''
    try:
        sql = "replace into productiondata (" + str(sqlfield) + ")value(" + str(sqlvalue) + ")"
        # print(sql)
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        log.logger.warning(e)
    else:
        return
