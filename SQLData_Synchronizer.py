import copy
import pymysql
from dbutils.pooled_db import PooledDB
import datetime

'''
本地数据库与82服务器数据库同步
'''

class SQL_Synchronizer():
    def __init__(self):
        # 连接82服务器数据库
        try:
            self.ret_pool = PooledDB(pymysql, 1, host='10.6.1.82', user='furnace', passwd='furnace', db='GPfixleng',
                                     port=3306)
            self.ret_conn = self.ret_pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
            self.ret_cursor = self.ret_conn.cursor()
            print("82服务器数据库连接成功")
        except Exception as e:
            print("连接82服务器数据库失败:", e)

        # 连接本地数据库
        try:
            self.loc_pool = PooledDB(pymysql, 1, host='localhost', user='root', passwd='123', db='steelfixlength',
                                     port=3306)  # 5为连接池里的最少连接数
            self.loc_conn = self.loc_pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
            self.loc_cursor = self.loc_conn.cursor()
            print("本地数据库连接成功")
        except Exception as e:
            print("连接本地数据库失败:", e)

        # 抓取82服务器数据库sql,采用最后10个进行对比
        self.readRetMySql_sql = "SELECT * FROM `productiondata` ORDER BY IDtime desc "
        self.sqldata_time = datetime.datetime.strptime("2000-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")  # 初始化时间

        self.Run()

    # 读取数据库
    def readMysqlValue(self, sql, mode=1):
        # 读本地数据库
        if mode == 1:
            try:
                self.loc_cursor.execute(sql)
                self.loc_conn.commit()
                data = self.loc_cursor.fetchall()
            except Exception as e:
                print("读取数据库失败:", e)
            else:
                return data
        # 读82服务器数据库
        elif mode == 2:
            try:
                self.ret_cursor.execute(sql)
                self.ret_conn.commit()
                data = self.ret_cursor.fetchall()
            except Exception as e:
                print("读取数据库失败:", e)
            else:
                return data

    # 读出的数据库数据拆分
    def sqlValueSplit(self, data):
        if data is None or len(data) < 1:
            return

        for i in range(len(data)):
            try:
                sqlheader = "INSERT INTO `productiondata` (FlowNum,FurNum,FixLength,Team,SteelType,RealWeight,Weighing,SetWeight,IDtime,adjustment,density,theoryWeight) values ("
                sqlbody = "'" + str(data[i][0]) + "','" + str(data[i][1]) + "','" + str(data[i][2]) + "','" + str(
                    data[i][3]) + "','" + str(data[i][4]) + "','" + str(data[i][5]) + "','" + str(
                    data[i][6]) + "','" + str(data[i][7]) + "','" + str(data[i][8]) + "','" + str(
                    data[i][9]) + "','" + str(data[i][10]) + "','" + str(data[i][11]) + "')"
                sql = sqlheader + sqlbody
                # print(sql)
                self.ret_cursor.execute(sql)
                self.ret_conn.commit()
                print("插入82服务器数据库成功")
            except Exception as e:
                print("插入82服务器数据库失败:", e)

    # 插入数据库
    def insertMysqlValue(self, sqlfield, sqlvalue, mode=2):
        if mode == 1:
            try:
                sql = "replace into productiondata (" + str(sqlfield) + ")value(" + str(sqlvalue) + ")"
                # print(sql)
                self.ret_cursor.execute(sql)
                self.ret_conn.commit()
            except Exception as e:
                print("插入本地数据库失败:", e)
        elif mode == 2:
            try:
                sql = "replace into productiondata (" + str(sqlfield) + ")value(" + str(sqlvalue) + ")"
                # print(sql)
                self.ret_cursor.execute(sql)
                self.ret_conn.commit()
            except Exception as e:
                print("插入82服务器数据库失败:", e)

    # 查看数据
    def datashow(self, data, i=0):
        print("第%i行数据" % i)
        print('流号', data[i][0])  # 流号
        print('炉号', data[i][1])  # 炉号
        print('定长', data[i][2])  # 定长
        print('班组', data[i][3])  # 班组
        print('钢种', data[i][4])  # 钢种
        print('真实重量', data[i][5])  # 真实重量
        print('是否称重', data[i][6])  # 是否称重
        print('设定重量', data[i][7])  # 设定重量
        print('时间', data[i][8])  # 取得的时间
        print('微调值', data[i][9])  # 微调值
        print('密度', data[i][10])  # 密度
        print('理论重量', data[i][11])  # 理论重量

    # 数据库比较
    def ret_contrast_loc(self, data):
        for i in range(len(data)):
            # 组合SQL语法,将读取的数据顺序放入，查看是否有相同数据
            sqlheader = "SELECT * FROM `productiondata` WHERE 1=1 "
            bodysql_FlowNum = "and FlowNum = '" + str(data[i][0]) + "' "
            bodysql_FurNum = "and FurNum = '" + str(data[i][1]) + "' "
            bodysql_FixLength = "and FixLength = '" + str(data[i][2]) + "' "
            bodysql_Team = "and Team = '" + str(data[i][3]) + "' "
            bodysql_SteelType = "and SteelType = '" + str(data[i][4]) + "' "
            bodysql_RealWeight = "and RealWeight = '" + str(data[i][5]) + "' "
            bodysql_Weighing = "and Weighing = '" + str(data[i][6]) + "' "
            bodysql_SetWeight = "and SetWeight = '" + str(data[i][7]) + "' "
            bodysql_IDtime = "and IDtime = '" + str(data[i][8]) + "' "
            bodysql_adjustment = "and adjustment = '" + str(data[i][9]) + "' "
            bodysql_density = "and density = '" + str(data[i][10]) + "' "
            bodysql_theoryWeight = "and theoryWeight = '" + str(data[i][11]) + "' "
            footsql = ";"
            sql = sqlheader + bodysql_FlowNum + bodysql_FurNum + bodysql_FixLength + bodysql_Team + bodysql_SteelType + bodysql_RealWeight + bodysql_Weighing + bodysql_SetWeight + bodysql_IDtime + bodysql_adjustment + bodysql_density + bodysql_theoryWeight + footsql
            # print(sql)
            loc_data = self.readMysqlValue(sql, mode=1)
            # print("数据", loc_data, len(loc_data))
            # 判断有相同数据
            if len(loc_data) >= 1:
                print("有一样，数据时间为：", str(data[i][8]))

                # 根据时间，读取所有大于这个的时间数据
                bodysql_IDtime = "and IDtime > '" + str(data[i][8]) + "' "
                sql = sqlheader + bodysql_IDtime
                contrast_data = self.readMysqlValue(sql, mode=1)
                print("搜索大于这时间的数据:", contrast_data)
                print("搜索出来的数量:", len(contrast_data))
                if len(contrast_data) > 0:
                    self.sqlValueSplit(contrast_data)
                else:
                    print("当前无最新数据")

                # 触发开始后续插入数据库

                break
        else:
            print("没有找到一样的")
            contrast_data = self.readMysqlValue(self.readRetMySql_sql, mode=1)
            # 整体数据库重新插入
            self.sqlValueSplit(contrast_data)

    def Run(self):
        if self.readMysqlValue(self.readRetMySql_sql):  # 判断数据不为空
            data = self.readMysqlValue(self.readRetMySql_sql, mode=2)  # 读取82服务器数据库,最后n行数据
            # print("得到数据%s\n列数%i " % (data, len(data)))
            self.ret_contrast_loc(data)  # 搜索对比是否有一样的

            # 关闭连接池
            self.loc_conn.close()
            self.loc_cursor.close()
            self.ret_conn.close()
            self.ret_cursor.close()
        else:
            print('获取的82服务器数据库为空')


if __name__ == '__main__':
    SQL_Synchronizer()
