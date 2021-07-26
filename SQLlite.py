#标准类
import sys
from tkinter import messagebox
import numpy
import pymysql
from dbutils.pooled_db import PooledDB

pool = PooledDB(pymysql, 1, host='localhost', user='root', passwd='123', db='steelfixlength', port=3306)  # 5为连接池里的最少连接数
conn = pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
cursor = conn.cursor()


#新增钢种名称及密度
# SQL_addSteelType('钢种名称','钢种密度',value1='22',value2=13.5)
def SQL_addSteelType(steelName,steelDensity,**kwargs):

    sql = "replace into steeltype ("+ str(steelName) +","+ str(steelDensity) +") value('"+str(kwargs['value1'])+"',"+ str(kwargs['value2'])+")"
    cursor.execute(sql)
    conn.commit()


def SQL_readSteeltype():
    sql ="SELECT * FROM `steeltype`"
    cursor.execute(sql)
    conn.commit()
    repairEndhoursAllvalue = cursor.fetchall()

    if len(repairEndhoursAllvalue) > 0 :
        value = repairEndhoursAllvalue
        return value
    elif len(repairEndhoursAllvalue) == 0:
        print("数据为空")
        value = 0
        return value
    else:
        print("数据异常")

def SQL_delSteeltype(steeltypename):
    sql ="DELETE FROM `steeltype` WHERE `钢种名称` =  '"+ str(steeltypename) +"'"
    cursor.execute(sql)
    conn.commit()


def SQL_updataSteeltype(steeltypename,steeltypedensity):
    sql = "UPDATE `steeltype` set `钢种密度` ='"+ str(steeltypedensity) +"' where `钢种名称` = '"+ str(steeltypename) +"'"
    cursor.execute(sql)
    conn.commit()
