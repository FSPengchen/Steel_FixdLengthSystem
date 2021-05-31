#标准类
import pymssql
from PyQt5.QtWidgets  import QApplication,QMainWindow,QPushButton,QPlainTextEdit,QTextBrowser,QMessageBox,QDialog
from PyQt5.Qt import *
from PyQt5.QtGui import QIcon,QIntValidator
import sys
import datetime
import time
import threading        #线程
from enum import Enum       #枚举

from dbutils.pooled_db import PooledDB
from sklearn import svm
import cv2
import HslCommunication
from apscheduler.schedulers.blocking import BlockingScheduler   #线程定时器
import os
import pymysql


#引用类
import ConsolePLC
import Log
import Config
import ConMySQL



#画面类
from UI_MainPage import *
import UI_SetFurNo
import UI_SetLocNo
import UI_SetFixLeng
from UI_SetTeam import *
import UI_SetTeam
import UI_ProductionData
import UI_ProductionDataQuery
import UI_SetCamera
import UI_SetAlgorithm
import UI_SetSteelData


list_SteelData = []

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent = None):
        super(MainWindow,self).__init__(parent)  # 调用父类QWidget中的init方法
        self.setupUi(self)

        tm = QTime.currentTime()    #获取当前时间
        dd = QDate.currentDate()    #获取当前日期
        strText = tm.toString("hh:mm:ss")

        #self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  隐藏窗口
        self.setFixedSize(1510, 1017)


        #self.Btn_FurNo.clicked.connect(self.slot_SetFurNo)     #按钮-设置炉号
        self.Btn_LocNo.clicked.connect(self.slot_SetLocNo)    #按钮-设置连铸机号
        self.Btn_1aSetWeight.clicked.connect(self.slot_SetFixLeng)       #按钮-设置输入设定
        self.Btn_2aSetWeight.clicked.connect(self.slot_SetFixLeng)
        self.Btn_3aSetWeight.clicked.connect(self.slot_SetFixLeng)
        self.Btn_4aSetWeight.clicked.connect(self.slot_SetFixLeng)
        self.Btn_Class.clicked.connect(self.slot_SetTeam)       #按钮-设置班组
        self.Btn_dataManagement.clicked.connect(self.slot_ProductionData)   #按钮-数据管理
        self.Btn_videoParameter.clicked.connect(self.slot_Camera)       #按钮-视频参数调整

        self.Act_Exit.setShortcut(self.close())     #菜单栏
        self.Act_FurNo.triggered.connect(self.slot_SetFurNo)
        self.Act_LocNo.triggered.connect(self.slot_SetLocNo)
        self.Act_Exit.triggered.connect(self.close) #菜单栏
        self.Act_SetAlgorithm.triggered.connect(self.slot_SetAlgorithm_triggered)   #菜单栏
        self.Act_SetSteelData.triggered.connect(self.slot_SetSteelData)   #菜单栏 定尺管理
        self.Act_Help.triggered.connect(self.slot_Help)

        self.Btn_Exit.clicked.connect(self.slot_close)
        self.Btn_Exit.clicked.connect(self.close)

        '''恢复上次关闭数据_初始化config.ini -> init'''
        self.Btn_Class.setText((config_ini.readvalue('init', 'Btn_Class')))      #班次
        self.Lab_talRoot.setText((config_ini.readvalue('init', 'Lab_talRoot')))  #总记数
        self.Lab_talTon.setText((config_ini.readvalue('init', 'Lab_talTon')))    #总重量
        self.Btn_FurNo.setText((config_ini.readvalue('init','Btn_FurNo')))  #炉号
        self.Lab_1cSteels.setText((config_ini.readvalue('init', 'Lab_1cSteels')))  # 1流钢种
        self.Lab_2cSteels.setText((config_ini.readvalue('init', 'Lab_2cSteels')))  # 2流钢种
        self.Lab_3cSteels.setText((config_ini.readvalue('init', 'Lab_3cSteels')))  # 3流钢种
        self.Lab_4cSteels.setText((config_ini.readvalue('init', 'Lab_4cSteels')))  # 4流钢种
        self.Lab_1cSetLength.setText((config_ini.readvalue('init', 'Lab_1cSetLength')))  # 1流定尺
        self.Lab_2cSetLength.setText((config_ini.readvalue('init', 'Lab_2cSetLength')))  # 2流定尺
        self.Lab_3cSetLength.setText((config_ini.readvalue('init', 'Lab_3cSetLength')))  # 3流定尺
        self.Lab_4cSetLength.setText((config_ini.readvalue('init', 'Lab_4cSetLength')))  # 4流定尺
        self.Btn_1aSetWeight.setText((config_ini.readvalue('init', 'Btn_1aSetWeight')))  # 1流定重设置显示
        self.Btn_2aSetWeight.setText((config_ini.readvalue('init', 'Btn_2aSetWeight')))  # 2流定重设置显示
        self.Btn_3aSetWeight.setText((config_ini.readvalue('init', 'Btn_3aSetWeight')))  # 3流定重设置显示
        self.Btn_4aSetWeight.setText((config_ini.readvalue('init', 'Btn_4aSetWeight')))  # 4流定重设置显示
        self.Lab_1bRange.setText((config_ini.readvalue('init', 'Lab_1bRange')))  # 1流定重合格范围
        self.Lab_2bRange.setText((config_ini.readvalue('init', 'Lab_2bRange')))  # 2流定重合格范围
        self.Lab_3bRange.setText((config_ini.readvalue('init', 'Lab_3bRange')))  # 3流定重合格范围
        self.Lab_4bRange.setText((config_ini.readvalue('init', 'Lab_4bRange')))  # 4流定重合格范围
        self.Lab_1cSpecs.setText((config_ini.readvalue('init', 'Lab_1cSpecs')))  # 1流规格
        self.Lab_2cSpecs.setText((config_ini.readvalue('init', 'Lab_2cSpecs')))  # 2流规格
        self.Lab_3cSpecs.setText((config_ini.readvalue('init', 'Lab_3cSpecs')))  # 3流规格
        self.Lab_4cSpecs.setText((config_ini.readvalue('init', 'Lab_4cSpecs')))  # 4流规格
        self.Lab_1cSetPos.setText((config_ini.readvalue('init', 'Lab_1cSetPos')))  # 1流预夹
        self.Lab_2cSetPos.setText((config_ini.readvalue('init', 'Lab_2cSetPos')))  # 2流预夹
        self.Lab_3cSetPos.setText((config_ini.readvalue('init', 'Lab_3cSetPos')))  # 3流预夹
        self.Lab_4cSetPos.setText((config_ini.readvalue('init', 'Lab_4cSetPos')))  # 4流预夹
        self.Lab_1cCompensate.setText((config_ini.readvalue('init', 'Lab_1cCompensate')))  # 1流补偿
        self.Lab_2cCompensate.setText((config_ini.readvalue('init', 'Lab_2cCompensate')))  # 2流补偿
        self.Lab_3cCompensate.setText((config_ini.readvalue('init', 'Lab_3cCompensate')))  # 3流补偿
        self.Lab_4cCompensate.setText((config_ini.readvalue('init', 'Lab_4cCompensate')))  # 4流补偿
        self.Lab_1cCount.setText((config_ini.readvalue('init', 'Lab_1cCount')))  # 1流记数
        self.Lab_2cCount.setText((config_ini.readvalue('init', 'Lab_2cCount')))  # 2流记数
        self.Lab_3cCount.setText((config_ini.readvalue('init', 'Lab_3cCount')))  # 3流记数
        self.Lab_4cCount.setText((config_ini.readvalue('init', 'Lab_4cCount')))  # 4流记数


        config_ini.writeValue('init', 'smtp_vserver','sss') #测试  11810*160*160 预夹=500 定重目标=2333.0



        '''时间刷新'''
        self.timer = QTimer()    #设定时间周期
        self.timer.timeout.connect(self.slot_timeOut)
        self.timer.setInterval(200)     #设置定时周期，超出周期启动timeout函数
        self.timer.start()  #启动


        '''笔记本摄像头开始'''
    #
    #     self.open_flag = False
    #     self.Camera = cv2.VideoCapture(0)
    #     #self.painter = QPainter(self)
    #     self.open_flag = bool(1 - self.open_flag)
    #
    #     log.logger.info('程序正常开启运行')
    #
    # #笔记本摄像头
    # def paintEvent(self, a0: QtGui.QPaintEvent):
    #     if self.open_flag:
    #         ret, frame = self.Camera.read()
    #
    #         '''尝试1'''
    #         # frame = cv2.resize(frame, (800, 600), interpolation=cv2.INTER_AREA)
    #         # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #         #
    #         # self.Qframe = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3,
    #         #                      QImage.Format_RGB888)
    #         #
    #         # self.labelCamera.setPixmap(QPixmap.fromImage(self.Qframe))
    #         # self.update()
    #         '''尝试1结束'''
    #
    #         '''尝试2'''
    #         # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 转换为灰度图
    #         # ret, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)  #二值阀图像，更好的边缘检测
    #         # binary, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    #         # img = cv2.drawContours(frame, contours, -1, (0, 0, 255), 2)
    #         #
    #         # self.Qframe = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3,
    #         #                      QImage.Format_RGB888)
    #         #
    #         # self.labelCamera.setPixmap(QPixmap.fromImage(self.Qframe))
    #         # self.update()
    #         '''尝试2结束'''
    #     #高斯去噪
    #     # blurred = cv2.GaussianBlur(gray, (9, 9),0)
    #
    #         '''尝试3'''
    #         frame = cv2.resize(frame, (800, 600), interpolation=cv2.INTER_AREA)
    #         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #
    #         self.Qframe = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3,
    #                              QImage.Format_RGB888)
    #
    #         self.labelCamera.setPixmap(QPixmap.fromImage(self.Qframe))
    #         self.update()
    #         '''尝试3结束'''
    #
    #         img4 = frame[0:150, 0:640]  # 裁剪坐标为[y0:y1, x0:x1]
    #         #cv2.imshow("4", img4)
    #         img3 = frame[150:300, 0:640]  # 裁剪坐标为[y0:y1, x0:x1]
    #         #cv2.imshow("3", img3)
    #         img2 = frame[300:450, 0:640]  # 裁剪坐标为[y0:y1, x0:x1]
    #         #cv2.imshow("2", img2)
    #         img1 = frame[450:600, 0:640]  # 裁剪坐标为[y0:y1, x0:x1]
    #         gray = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    #         blurred = cv2.GaussianBlur(gray, (9, 9), 0)
    #         ret, thresh = cv2.threshold(blurred, 240, 255, cv2.THRESH_BINARY)  # 二值阀图像，更好的边缘检测
    #         binary, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  #轮廓
    #         img1 = cv2.drawContours(img1, contours, -1, (0, 0, 255), 2)  # -1 全部轮廓画出来
    #
    #         #print("一共有多少个" + str(len(contours)))
    #         for i in range(0,len(contours)):
    #             cnt = contours[i]
    #             # if cv2.contourArea(cnt) > 10.0 :
    #             #     print("第" + str(i) + "个是大于要求")
    #             #     print(contours[i])
    #
    #         # cv2.imshow("1", img1)
        '''笔记本摄像头结束'''

    #关闭保持数据
    def slot_close(self,event):
        try:
            config_ini.writeValue('init', 'smtp_vserver', 'sss')
            config_ini.writeValue('init', 'Lab_talRoot', window.Lab_talRoot.text()) #总根数写入配置文件
            config_ini.writeValue('init', 'Lab_talTon', window.Lab_talTon.text())   #总重量写入配置文件
        except Exception as e :
            print(e)



    def slot_timeOut(self):     #延时触发该函数   定时
        tm = QTime.currentTime()    #获取当前时间
        dd = QDate.currentDate()    #获取当前日期
        strText = tm.toString("hh:mm:ss")
        self.Lab_Time.setText(strText)
        self.Lab_DateDay.setText(dd.toString(Qt.DefaultLocaleLongDate))

    def slot_SetFurNo(self):    #设置炉号
        furno = FurNoPage()
        furno.exec_()
    def slot_SetLocNo(self):  #设置连铸机号
        locno = LocNoPage()
        locno.exec_()
    def slot_SetFixLeng(self):  #设置输入定尺
        Fixleng = FixLengPage()
        Fixleng.exec_()
    def slot_SetTeam(self):     #设置班组
        Team = TeamPage()
        Team.exec_()
    def slot_ProductionData(self):  #设置生产数据
        Data = ProductionDataPage()
        Data.exec_()
    def slot_Camera(self):      #视频参数调整
        camera = SetCameraPage()
        camera.exec_()
    def slot_SetAlgorithm_triggered(self):  #设置算法
        algorithm = AlgorithmPage()
        algorithm.exec_()
    def slot_SetSteelData(self):        #定尺管理
        steeldata = SetSteelDataPage()
        steeldata.exec_()
    def slot_Help(self):
        QtWidgets.QMessageBox.question(self, "帮助", "联系计控室",
                                                     QtWidgets.QMessageBox.Yes )

    # def closeEvent(self, event):
    #     result = QtWidgets.QMessageBox.question(self, "标题", "亲，你确定想关闭我?别后悔！！！'_'",
    #                                             QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    #     if (result == QtWidgets.QMessageBox.Yes):
    #         event.accept()
    #         # 通知服务器的代码省略，这里不是重点...
    #     else:
    #         event.ignore()

class FurNoPage(QDialog,UI_SetFurNo.Ui_Dialog): #炉号
    def __init__(self,parent = None):
        super(FurNoPage,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.Lne_SetFurNum.setValidator(QIntValidator(0,65535)) #设置输入整形数字范围
        self.Lne_SetFurNo.setValidator(QDoubleValidator())  # 设置输入浮点数字范围

        #显示 列表信息
        for i in range(1,11):
            Furstr = 'FurListData' + str(i)
            if int(config_fur.readvalue(Furstr, 'show')) == 1 :     #判断在第几个开始显示
                a = "炉号" + config_fur.readvalue(Furstr, 'lne_setfurno')
                b = "根数" + config_fur.readvalue(Furstr, 'lne_setfurnum')
                self.LW_SetFurNo.addItem( a + b )

        self.Btn_Exit.clicked.connect(self.close)
        self.Btn_addFurNum.clicked.connect(self.slot_addFurNum)     #增加项
        self.Btn_delFurNum.clicked.connect(self.slot_delFurNum)     #删除项
        self.LW_SetFurNo.setSelectionMode(QAbstractItemView.SingleSelection)     #单项处理
        self.LW_SetFurNo.itemClicked.connect(self.slot_SetFurNoItemCliked)  #单击触发 提示
        self.LW_SetFurNo.currentItemChanged.connect(self.slot_SetFurNoItemDoubleClicked)    #选中项前后字体变色


    def slot_addFurNum(self):
        strNo =self.Lne_SetFurNo.text()
        strNum = self.Lne_SetFurNum.text()

        if len(strNo) > 0 and len(strNum) > 0:  #判断是否输入
            # 修改配置文件
            for i in range(1, 11):
                Furstr = 'FurListData' + str(i)     #配置文件中，名称
                if int(config_fur.readvalue(Furstr, 'show')) == 0:  #
                    config_fur.readvalue(Furstr, 'row')     #获取未显示行数
                    config_fur.writeValue(Furstr,'lne_setfurno',self.Lne_SetFurNo.text())
                    config_fur.writeValue(Furstr, 'lne_setfurnum', self.Lne_SetFurNum.text())
                    config_fur.writeValue(Furstr, 'show','1')
                    self.LW_SetFurNo.addItem('炉号' + str(self.Lne_SetFurNo.text()) +'根数'+ str(self.Lne_SetFurNum.text()))
                    break

            '''数据库插入'''
            #数据库插入

            # FurNumstr = '炉号:' + str(self.Lne_SetFurNo.text()) +'根数:'+ str(self.Lne_SetFurNum.text())
            # try:
            #     conn = pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
            #     cursor = conn.cursor()
            #     cursor.execute("INSERT INTO furnum(炉号, 根数, 完成标, 时间戳,序号)VALUES (%s,%s,%s,%s,%s)",
            #                    (strNo,strNum,0,QDateTime.currentDateTime().toString(("yyyy-MM-dd hh:mm:ss")),str(FurNumstr)))
            #     conn.commit()
            # except Exception as e:
            #     QtWidgets.QMessageBox.question(self, "提示",e,
            #                                    QtWidgets.QMessageBox.Yes)

        else:
            QtWidgets.QMessageBox.question(self, "提示", "请全部输入！",
                                           QtWidgets.QMessageBox.Yes)


    def slot_delFurNum(self):
        pItem = self.LW_SetFurNo.currentItem()   #得到左侧列表选中项
        if pItem is None:
            return
        idx = self.LW_SetFurNo.row(pItem)   #得到项的序号  所在行 idx =>int
        # print(pItem.text())  # 所选行的文本
        # Furstr = 'FurListData' + str(idx)  # 配置文件中，名称
        # print(idx)  #选择行数
        self.LW_SetFurNo.takeItem(idx)
        if idx == 9 :   #当选择最后一列，直接隐藏
            config_fur.writeValue('FurListData10', 'show', '0')
        else:
            for i in range(idx,9):
                j = 'FurListData' + str(i + 1)
                k = 'FurListData' + str(i + 2)
                config_fur.writeValue(j, 'lne_setfurno', config_fur.readvalue(k, 'lne_setfurno'))
                config_fur.writeValue(j, 'lne_setfurnum', config_fur.readvalue(k, 'lne_setfurnum'))

            for s in range(idx + 1, 11):
                l = 'FurListData' + str(s)  # 配置文件中，名称
                if int(config_fur.readvalue(l, 'show')) == 0  :
                    for j in range(s - 1,11):
                        m = 'FurListData' + str(j)  # 配置文件中，名称
                        config_fur.writeValue(m, 'show', '0')
                        if j == 10 :
                            return
                elif int(config_fur.readvalue('FurListData10', 'show')) == 1:
                    config_fur.writeValue('FurListData10', 'show', '0')
                    return





                #数据库删除
        # conn = pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
        # cursor = conn.cursor()
        # b = 233
        # cursor.execute("DELETE FROM furnum WHERE `序号` ='"+ str(b) +"'")
        # conn.commit()


    def slot_SetFurNoItemCliked(self,item):
        ft = item.font()
        ft.setBold(True)
        item.setFont(ft)

    def slot_SetFurNoItemDoubleClicked(self,current,previous):  #current 新选中的项  previous之前选中的项
        #将之前选中的字体粗体恢复
        if not (previous is None):
            ft = previous.font()
            ft.setBold(False)
            previous.setFont(ft)


class LocNoPage(QDialog,UI_SetLocNo.Ui_Dialog): #连铸机号
    def __init__(self,parent = None):
        super(LocNoPage,self).__init__(parent)
        self.setupUi(self)

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.Btn_LocNoNo.clicked.connect(self.close)
        self.Btn_LocNoYes.clicked.connect(self.slot_ChangeLocNo)
        self.Btn_LocNoYes.clicked.connect(self.close)

    def slot_ChangeLocNo(self):                               #????????????????????限制输入
        try:
            LocNotext = self.LabInput_LocNo.toPlainText()
            window.Btn_LocNo.setText("铸机号:" + LocNotext + "#")
        except Exception as e:
            print(e)


class FixLengPage(QDialog,UI_SetFixLeng.Ui_Dialog): #设置输入定尺
    def __init__(self,parent = None):
        super(FixLengPage,self).__init__(parent)
        self.setupUi(self)

        #输入限制
        self.Lne_FixLength.setValidator(QIntValidator(0,65535)) #设置输入整形数字范围
        self.Lne_PreClampOffset.setValidator(QIntValidator(0, 65535))  # 设置输入整形数字范围
        self.Lne_TheoryWeiht.setValidator(QIntValidator(0, 65535))  # 设置输入整形数字范围
        self.Lne_Density.setValidator(QIntValidator(0, 65535))  # 设置输入整形数字范围
        self.Lne_ErrRangeMinus.setValidator(QIntValidator(0, 65535))  # 设置输入整形数字范围
        self.Lne_ErrRangePlus.setValidator(QIntValidator(0, 65535))  # 设置输入整形数字范围
        self.Lne_LengthRangeMax.setValidator(QIntValidator(0, 65535))  # 设置输入整形数字范围
        self.Lne_WeightMax.setValidator(QIntValidator(0, 65535))  # 设置输入整形数字范围
        self.Lne_FixWeiht.setValidator(QDoubleValidator())  # 设置输入浮点数字范围


        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.Btn_FixLengNo.clicked.connect(self.close)
        self.Ceb_AllowEdit.stateChanged.connect(self.slot_editEnabled)
        #self.Btn_FixLengYes.clicked.connect(self.close)
        self.Lne_FixWeiht.setEnabled(False)
        self.Lne_TheoryWeiht.setEnabled(False)
        self.Lne_Density.setEnabled(False)
        self.Btn_FixLengYes.clicked.connect(self.slot_SaveData)




    def slot_editEnabled(self,b):       #b勾选编辑
        self.Lne_FixWeiht.setEnabled(b)
        self.Lne_TheoryWeiht.setEnabled(b)
        self.Lne_Density.setEnabled(b)
        self.Lne_FixWeiht.setValidator(QIntValidator(0,300,self.Lne_FixWeiht))  #QIntValidator 整数的有效判断，范围0-300

    def slot_SaveData(self):
        if len(self.Lne_FixLength.text()) > 0 \
                and len(self.Lne_FixWeiht.text()) > 0  \
                and len(self.Lne_Density.text()) > 0 \
                and len(self.Lne_ErrRangeMinus.text()) > 0 \
                and len(self.Lne_ErrRangePlus.text()) > 0 \
                and len(self.Lne_PreClampOffset.text()) > 0 \
                and len(self.Lne_TheoryWeiht.text()) > 0 \
                and len(self.Lne_LengthRangeMax.text()) > 0 \
                and len(self.Lne_WeightMax.text()) > 0 :
               try:
                    window.Btn_1aSetWeight.setText(self.Lne_FixLength.text())  # 1流定重设置显示
                    window.Btn_2aSetWeight.setText(self.Lne_FixLength.text())  # 2流定重设置显示
                    window.Btn_3aSetWeight.setText(self.Lne_FixLength.text())  # 3流定重设置显示
                    window.Btn_4aSetWeight.setText(self.Lne_FixLength.text())  # 4流定重设置显示
                    config_ini.writeValue('init', 'Btn_1aSetWeight', self.Lne_FixLength.text())
                    config_ini.writeValue('init', 'Btn_2aSetWeight', self.Lne_FixLength.text())
                    config_ini.writeValue('init', 'Btn_3aSetWeight', self.Lne_FixLength.text())
                    config_ini.writeValue('init', 'Btn_4aSetWeight', self.Lne_FixLength.text())

                    SQLname = str(self.Lne_FixLength.text()) + ' 预夹=' + str(self.Lne_PreClampOffset.text()) + ' 定重目标=' + str(self.Lne_FixWeiht.text())
                    print(SQLname)


                    conn = pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO fixsteeldata ("
                                   "SteelName, "    #定长名称
                                   "FixLength,"     #定长
                                   "FixWeiht,"      #定长重量
                                   "Density,"       #密度
                                   "ErrRangeMinus," #误差范围负
                                   "ErrRangePlus,"  #误差范围正
                                   "PreClampOffset,"    #预夹
                                   "TheoryWeiht,"   #理论重量
                                   "LengthRangeMax,"  #最大调节范围   
                                   "WeightMax ) "       #对应重量
                                   
                                   " VALUES ("+"'" +
                                   SQLname + "','" +
                                   self.Lne_FixLength.text()  +"','"+
                                   self.Lne_FixWeiht.text() +"','" +
                                   self.Lne_Density.text() +"','" +
                                   self.Lne_ErrRangeMinus.text() + "','"+
                                   self.Lne_ErrRangePlus.text() +"','" +
                                   self.Lne_PreClampOffset.text() +"','" +
                                   self.Lne_TheoryWeiht.text() +"','" +
                                   self.Lne_LengthRangeMax.text() + "','"+
                                   self.Lne_WeightMax.text() +"');")
                    conn.commit()

               except Exception as e :
                   print(e)
                   QtWidgets.QMessageBox.question(self, "错误",e,
                                                  QtWidgets.QMessageBox.Yes)

        else:
                    QtWidgets.QMessageBox.question(self, "提示", "请输入参数",
                                                   QtWidgets.QMessageBox.Yes)




class TeamPage(QDialog,UI_SetTeam.Ui_Dialog): #设置班组

    def __init__(self,parent = None):
        super(TeamPage,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.Btn_TeamNo.clicked.connect(self.close)
        self.Btn_TeamYes.clicked.connect(self.slot_ChangeLocYes)
        self.Btn_TeamYes.clicked.connect(self.close)

    def slot_ChangeLocYes(self):                               #????????????????????限制输入
        Cbb_SetTeamText = self.Cbb_SetTeam.currentText()
        window.Btn_Class.setText(Cbb_SetTeamText)   #修改窗口显示班组

        config_ini.writeValue('init', 'Btn_Class', Cbb_SetTeamText) #写入config.ini文件
        window.Lab_talRoot.setText('0')
        window.Lab_talTon.setText('0')

        #保存该班组的总根数
        #保持该班组的总重量
        config_ini.writeValue('init', 'Lab_talRoot', '0')  #写入总根数为0
        config_ini.writeValue('init', 'Lab_talTon', '0')   #写入总重量为0


class ProductionDataPage(QDialog,UI_ProductionData.Ui_Dialog):      #生产数据
    def __init__(self,parent = None):
        super(ProductionDataPage,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.Btn_Exit.clicked.connect(self.close)
        self.Btn_Query.clicked.connect(self.slot_ProductionDataQuery)   #按钮-查询生产数据

    def slot_ProductionDataQuery(self):
        dataaquery = ProductionDataQueryPage()
        dataaquery.exec_()

class ProductionDataQueryPage(QDialog,UI_ProductionDataQuery.Ui_Dialog):    #查询生产数据

    class SteelType(Enum):  #钢种类型枚举

        SteelType_all = 0
        SteelType_one = 1
        SteelType_two = 2
        SteelType_three = 3
        SteelType_four = 4

    def __init__(self,parent = None):
        super(ProductionDataQueryPage,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        #钢坯类型下拉列表
        #addItem 当前第0条
        self.cb_lengthType.addItem("全部",self.SteelType.SteelType_all)
        #当前第1条
        # self.cb_SteelType.addItem("方钢")
        # self.cb_SteelType.setItemData(1,self.SteelType.SteelType_one)

        # strList = ["2","3","4"]
        # self.cb_SteelType.addItem(strList)
        #在all之前插入一条记录，将在第0条之前插入，将''变为第0条
        #self.cb_SteelType.insertItem(0,"4",self.SteelType.SteelType_four)
        self.cb_SteelType.currentIndexChanged.connect(self.slot_cbSteelChanged)  #当变化时动作,触发记录动作


        self.Lne_LengRangeFrom.setEnabled(False)
        self.Lne_LengRangeTo.setEnabled(False)
        self.Tet_TimeRangeFrom.setEnabled(False)
        self.Tet_TimeRangeTo.setEnabled(False)
        self.Lne_SetWeight.setEnabled(False)
        self.Det_DateRangeFrom.setEnabled(False)
        self.Det_DateRangeTo.setEnabled(False)
        self.Ceb_SetWeightEn.stateChanged.connect(self.slot_setweighten)
        self.Ceb_LengRangeEn.stateChanged.connect(self.slot_lengrangeen)
        self.Ceb_TimeRangeEn.stateChanged.connect(self.slot_timerangeen)

    def slot_cbSteelChanged(self,index):    #index 下拉项
        str = self.cb_SteelType.currentText()
        print(str)
        steeltype = self.cb_SteelType.itemData(index)
        print(steeltype)
        #if steeltype == self.cb_SteelType.steel

    def slot_setweighten(self,b):
        self.Lne_SetWeight.setEnabled(b)
        self.Lne_SetWeight.setCursorPosition(0)  # 光标定位
    def slot_lengrangeen(self, b):
        self.Lne_LengRangeFrom.setEnabled(b)
        self.Lne_LengRangeTo.setEnabled(b)
    def slot_timerangeen(self, b):
        self.Tet_TimeRangeFrom.setEnabled(b)
        self.Tet_TimeRangeTo.setEnabled(b)
        self.Det_DateRangeFrom.setEnabled(b)
        self.Det_DateRangeTo.setEnabled(b)
        # self.Lne_DateRangeFrom.setInputMask("0000-00-00")
        # self.Lne_DateRangeToRangeTo.setInputMask("0000-00-00")
        # self.Lne_DateRangeToRangeTo.setText("0000-00-00")
        # self.Lne_DateRangeFrom.setText("0000-00-00")

class AlgorithmPage(QDialog,UI_SetAlgorithm.Ui_Dialog):
    def __init__(self,parent = None):
        super(AlgorithmPage,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

class SetCameraPage(QDialog,UI_SetCamera.Ui_Dialog):
    def __init__(self,parent = None):
        super(SetCameraPage,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.Btn_Exit.clicked.connect(self.close)

class SetSteelDataPage(QDialog,UI_SetSteelData.Ui_Dialog):


    def __init__(self,parent = None):
        super(SetSteelDataPage,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.Btn_Exit.clicked.connect(self.close)
        self.Btn_addLength.clicked.connect(self.slot_addLength)
        self.Btn_delLength.clicked.connect(self.slot_delLength)
        '''**********************************************************'''

        # 数据库查询

        try:
            conn = pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
            cursor = conn.cursor()
            sql = 'SELECT * FROM `fixsteeldata`'
            cursor.execute(sql)
            conn.commit()
            data =cursor.fetchall()

            # if data:
            #     # self.TW_lengthType.setRowCount(0)
            #     # self.TW_lengthType.insertRow(0)
            #     for row,form in enumerate(data):
            #         print(row,form[0])
            #         # for column,item in enumerate(form[0]):
            #         #     self.TW_lengthType.setItem(row,column,QTableWidgetItem(str(form[0])))
            #         #     column += 1
            #         #     print(row,form[0])
            #
            #         self.TW_lengthType.setItem(row, 0, QTableWidgetItem(str(form[0])))
            #         row_position = self.TW_lengthType.rowCount()
            #         print('row_position')
            #         print(row_position)
            #         self.TW_lengthType.insertRow(row_position)


            if data:
                for row,form in enumerate(data):
                    # for column,item in enumerate(form[0]):
                    #     self.TW_lengthType.setItem(row,column,QTableWidgetItem(str(form[0])))
                    #     column += 1
                    #     print(row,form[0])

                    self.LW_lengthType.addItem(str(form[0]))

        except Exception as e:
            QtWidgets.QMessageBox.question(self, "提示",e,
                                           QtWidgets.QMessageBox.Yes)

    def slot_addLength(self):
        Fixleng = FixLengPage()
        Fixleng.exec_()

    def slot_delLength(self):
        try:
            pItem = self.LW_lengthType.currentItem()  # 得到左侧列表选中项
            if pItem is None:
                return
            idx = self.LW_lengthType.row(pItem)  # 得到项的序号  所在行 idx =>int
            # print(pItem.text())  # 所选行的文本
            # print(idx)  #选择行数
            self.LW_lengthType.takeItem(idx)

            conn = pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
            cursor = conn.cursor()
            sql = "DELETE FROM fixsteeldata WHERE SteelName = '" + pItem.text() +"';"
            cursor.execute(sql)
            conn.commit()

        except Exception as e:
            QtWidgets.QMessageBox.question(self, "提示",e,
                                           QtWidgets.QMessageBox.Yes)

    def slot_changelength(self):    #修改
        pass

    def slot_switchlength(self):    #切换
        pass


        #self.LW_Left.itemClicked.connect(self.slot_leftItemCliked)  # 单击触发 提示

        self.Btn_addLength.clicked.connect(MainWindow.slot_SetFixLeng)
        self.Btn_delLength.clicked.connect(self.slot_takeItem)


    def slot_takeItem(self):    #删除定尺信息
        pItem = self.LW_lengthType.currentItem()
        if pItem is None:
            return
        idx = self.LW_lengthType.row(pItem)
        self.LW_lengthType.takeItem(idx)


class contPLC(ConsolePLC.siemens):      #PLC通讯
    def __init__(self):
        super(contPLC,self).__init__()


class MyWidget(QWidget):
    def closeEvent(self, event):
        result = QtWidgets.QMessageBox.question(self, "标题", "亲，你确定想关闭我?别后悔！！！'_'",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if (result == QtWidgets.QMessageBox.Yes):
            event.accept()
            # 通知服务器的代码省略，这里不是重点...
        else:
            event.ignore()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # 创建一个应用程序对象
    #日志
    log = Log.Logger('all.log')
    #配置文件
    config_ini = Config.Config(path = r"E:\PycharmProjects\FixedLengthSystem",pathconfig ='config.ini')
    config_fur = Config.Config(path = r"E:\PycharmProjects\FixedLengthSystem",pathconfig ='FurNum.ini')
    #连接本地数据库
    pool = PooledDB(pymysql, 1, host='localhost', user='root', passwd='123', db='steelfixlength', port=3306)  # 5为连接池里的最少连接数

    # conn = pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
    # cursor = conn.cursor()
    # b = 233
    # cursor.execute("DELETE FROM furnum WHERE `序号` ='" + str(b) + "'")
    # print(cursor)
    # conn.commit()


    window = MainWindow()
   # window.showFullScreen()    #全屏

    window.show()
    sys.exit(app.exec_())  # 0是正常退出

    cap.release()
    cv2.destroyAllWindows()
