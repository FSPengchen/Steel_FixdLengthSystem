from dbutils.pooled_db import PooledDB
import pymysql


pool = PooledDB(pymysql, 2, host='10.6.1.35', user='sa', passwd='xgt', db='GPDATA', port=3306)  # 5为连接池里的最少连接数

conn = pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
cursor = conn.cursor()
sql = "SELECT * FROM GPmsg where [流号] ='1'  and [时间] >= '2021-04-01 00:03:29.000' and [连铸机号] = '1#' AND [是否称重] ='是'"
cursor.execute(sql)
conn.commit()
data = cursor.fetchall()