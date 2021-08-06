# 标准类
import datetime
import sys
from tkinter import messagebox
import numpy
import pymysql
from dbutils.pooled_db import PooledDB
import Config

# 配置文件
config_ini = Config.Config(path=r"E:\PycharmProjects\FixedLengthSystem", pathconfig='config.ini')
config_fur = Config.Config(path=r"E:\PycharmProjects\FixedLengthSystem", pathconfig='FurNum.ini')
# 配置数据库信息
pool = PooledDB(pymysql, 1, host='localhost', user='root', passwd='123', db='steelfixlength', port=3306)  # 5为连接池里的最少连接数
conn = pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
cursor = conn.cursor()
'''
dbapi ：数据库接口
mincached ：启动时开启的空连接数量
maxcached ：连接池最大可用连接数量
maxshared ：连接池最大可共享连接数量
maxconnections ：最大允许连接数量
blocking ：达到最大数量时是否阻塞
maxusage ：单个连接最大复用次数
setsession ：用于传递到数据库的准备会话，如 [”set name UTF-8″] 。
'''


# 新增钢种名称及密度
# SQL_addSteelType('钢种名称','钢种密度',value1='22',value2=13.5)
def SQL_addSteelType(steelName, steelDensity, **kwargs):
    sql = "replace into steeltype (" + str(steelName) + "," + str(steelDensity) + ") value('" + str(
        kwargs['value1']) + "'," + str(kwargs['value2']) + ")"
    cursor.execute(sql)
    conn.commit()


def SQL_readSteeltype():
    sql = "SELECT * FROM `steeltype`"
    cursor.execute(sql)
    conn.commit()
    repairEndhoursAllvalue = cursor.fetchall()

    if len(repairEndhoursAllvalue) > 0:
        value = repairEndhoursAllvalue
        return value
    elif len(repairEndhoursAllvalue) == 0:
        print("数据为空")
        value = 0
        return value
    else:
        print("数据异常")


def SQL_delSteeltype(steeltypename):
    sql = "DELETE FROM `steeltype` WHERE `钢种名称` =  '" + str(steeltypename) + "'"
    cursor.execute(sql)
    conn.commit()


def SQL_updataSteeltype(steeltypename, steeltypedensity):
    sql = "UPDATE `steeltype` set `钢种密度` ='" + str(steeltypedensity) + "' where `钢种名称` = '" + str(steeltypename) + "'"
    cursor.execute(sql)
    conn.commit()
