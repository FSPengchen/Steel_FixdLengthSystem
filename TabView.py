import sys

import pymysql
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTableView, QDialog, QApplication, QTableWidgetItem, QAbstractItemView, QTableWidget
from dbutils.pooled_db import PooledDB
from UI_ProductionData import Ui_Dialog


class MyMain(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        TaW_ProductionData = QTableWidget(self)
        title = ['流号', '炉号', '定尺', '班次', '种类', '实际重量', '是否称重', '设定重量', '时间']
        TaW_ProductionData.setHorizontalHeaderLabels(title)

        sql = "SELECT * FROM `productiondata`"
        cursor.execute(sql)
        conn.commit()
        data = cursor.fetchall()
        print(data)
        self.rowNum = len(data)  # 获取查询到的行数
        self.columnNum = len(data[0])  # 获取查询到的列数
        self.TaW_ProductionData.setRowCount(self.rowNum)  # 设置表格行数
        self.TaW_ProductionData.setColumnCount(self.columnNum)  ## 设置表格列数
        self.TaW_ProductionData.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 禁止编辑

        for i, da in enumerate(data):
            for j in range(self.columnNum):
                self.itemContent = QTableWidgetItem(('%s') % (da[j]))
                self.TaW_ProductionData.setItem(i, j, self.itemContent)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pool = PooledDB(pymysql, 1, host='localhost', user='root', passwd='123', db='steelfixlength',
                    port=3306)  # 5为连接池里的最少连接数
    conn = pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
    cursor = conn.cursor()
    A1 = MyMain()
    A1.show()
    sys.exit(app.exec_())
