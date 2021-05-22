import pymssql
from PyQt5.QtWidgets  import QApplication,QMainWindow,QPushButton,QPlainTextEdit,QTextBrowser,QMessageBox,QDialog
from PyQt5.Qt import *
from PyQt5.QtGui import QIcon,QIntValidator
import sys
import datetime
import time
import threading        #线程
from enum import Enum       #枚举
from sklearn import svm
import cv2
import HslCommunication
import ConsolePLC
from apscheduler.schedulers.blocking import BlockingScheduler   #线程定时器
import configparser     #ini配置文件
import logging  #日志文件
import os




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
import Config






class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent = None):
        super(MainWindow,self).__init__(parent)  # 调用父类QWidget中的init方法
        self.setupUi(self)

        tm = QTime.currentTime()    #获取当前时间
        dd = QDate.currentDate()    #获取当前日期
        strText = tm.toString("hh:mm:ss")
        logging.info("正常开始,datetime = " + strText)

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
        self.Act_Class.triggered.connect(self.slot_SetTeam)
        self.Act_LocNo.triggered.connect(self.slot_SetLocNo)
        self.Act_Exit.triggered.connect(self.close) #菜单栏
        self.Act_SetAlgorithm.triggered.connect(self.slot_SetAlgorithm_triggered)   #菜单栏
        self.Act_SetSteelData.triggered.connect(self.slot_SetSteelData)   #菜单栏 定尺管理

        self.Btn_Exit.clicked.connect(self.slot_close)
        self.Btn_Exit.clicked.connect(self.close)

        '''恢复上次关闭数据_初始化config.ini -> init'''
        config_ini = Config.Config()
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





        config_ini.writeValue('init', 'smtp_vserver','sss')


        '''时间刷新'''
        self.timer = QTimer()    #设定时间周期
        self.timer.timeout.connect(self.slot_timeOut)
        self.timer.setInterval(200)     #设置定时周期，超出周期启动timeout函数
        self.timer.start()  #启动


        '''视频开始'''

        self.open_flag = False
        self.Camera = cv2.VideoCapture(0)
        #self.painter = QPainter(self)
        self.open_flag = bool(1 - self.open_flag)



    def paintEvent(self, a0: QtGui.QPaintEvent):
        if self.open_flag:
            ret, frame = self.Camera.read()

            '''尝试1'''
            # frame = cv2.resize(frame, (800, 600), interpolation=cv2.INTER_AREA)
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            #
            # self.Qframe = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3,
            #                      QImage.Format_RGB888)
            #
            # self.labelCamera.setPixmap(QPixmap.fromImage(self.Qframe))
            # self.update()
            '''尝试1结束'''

            '''尝试2'''
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 转换为灰度图
            # ret, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)  #二值阀图像，更好的边缘检测
            # binary, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            # img = cv2.drawContours(frame, contours, -1, (0, 0, 255), 2)
            #
            # self.Qframe = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3,
            #                      QImage.Format_RGB888)
            #
            # self.labelCamera.setPixmap(QPixmap.fromImage(self.Qframe))
            # self.update()
            '''尝试2结束'''
        #高斯去噪
        # blurred = cv2.GaussianBlur(gray, (9, 9),0)

            '''尝试3'''
            frame = cv2.resize(frame, (800, 600), interpolation=cv2.INTER_AREA)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            self.Qframe = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3,
                                 QImage.Format_RGB888)

            self.labelCamera.setPixmap(QPixmap.fromImage(self.Qframe))
            self.update()
            '''尝试3结束'''

            img4 = frame[0:150, 0:640]  # 裁剪坐标为[y0:y1, x0:x1]
            cv2.imshow("4", img4)
            img3 = frame[150:300, 0:640]  # 裁剪坐标为[y0:y1, x0:x1]
            cv2.imshow("3", img3)
            img2 = frame[300:450, 0:640]  # 裁剪坐标为[y0:y1, x0:x1]
            cv2.imshow("2", img2)
            img1 = frame[450:600, 0:640]  # 裁剪坐标为[y0:y1, x0:x1]
            gray = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (9, 9), 0)
            ret, thresh = cv2.threshold(blurred, 240, 255, cv2.THRESH_BINARY)  # 二值阀图像，更好的边缘检测
            binary, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  #轮廓
            img1 = cv2.drawContours(img1, contours, -1, (0, 0, 255), 2)  # -1 全部轮廓画出来

            #print("一共有多少个" + str(len(contours)))
            for i in range(0,len(contours)):
                cnt = contours[i]
                # if cv2.contourArea(cnt) > 10.0 :
                #     print("第" + str(i) + "个是大于要求")
                #     print(contours[i])

            # cv2.imshow("1", img1)

        '''视频结束'''

    #关闭保持数据
    def slot_close(self,event):
        config_ini = Config.Config()
        config_ini.writeValue('init', 'smtp_vserver', 'sss')
        config_ini.writeValue('init', 'Lab_talRoot', '11')
        config_ini.writeValue('init', 'Lab_talTon', '11')

        # result = QtWidgets.QMessageBox.question(self, "标题", "亲，你确定想关闭我?别后悔！！！'_'",
        #                                         QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        # if (result == QtWidgets.QMessageBox.Yes):
        #     event.accept()
        #     # 通知服务器的代码省略，这里不是重点...
        # else:
        #     event.ignore()



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
        self.Btn_SetFurNoNo.clicked.connect(self.close)
        self.Btn_SetFurNoYes.clicked.connect(self.slot_ChangeLocNo)
        self.Btn_SetFurNoYes.clicked.connect(self.close)

    def slot_ChangeLocNo(self):                               #????????????????????限制输入
        LocNotext = self.LabInput_SetFurNo.toPlainText()
        window.Btn_FurNo.setText(LocNotext)

class LocNoPage(QDialog,UI_SetLocNo.Ui_Dialog): #连铸机号
    def __init__(self,parent = None):
        super(LocNoPage,self).__init__(parent)
        self.setupUi(self)
        self.Btn_LocNoNo.clicked.connect(self.close)
        self.Btn_LocNoYes.clicked.connect(self.slot_ChangeLocNo)
        self.Btn_LocNoYes.clicked.connect(self.close)

    def slot_ChangeLocNo(self):                               #????????????????????限制输入
        LocNotext = self.LabInput_LocNo.toPlainText()
        window.Btn_LocNo.setText("铸机号:" + LocNotext + "#")


class FixLengPage(QDialog,UI_SetFixLeng.Ui_Dialog): #设置输入定尺
    def __init__(self,parent = None):
        super(FixLengPage,self).__init__(parent)
        self.setupUi(self)
        self.Btn_FixLengNo.clicked.connect(self.close)
        self.Btn_FixLengYes.clicked.connect(self.slot_SaveData)
        self.Ceb_AllowEdit.stateChanged.connect(self.slot_editEnabled)
        self.Btn_FixLengYes.clicked.connect(self.close)
        self.Lne_FixWeiht.setEnabled(False)
        self.Lne_TheoryWeiht.setEnabled(False)
        self.Lne_Density.setEnabled(False)

    def slot_editEnabled(self,b):       #b勾选编辑
        self.Lne_FixWeiht.setEnabled(b)
        self.Lne_TheoryWeiht.setEnabled(b)
        self.Lne_Density.setEnabled(b)
        self.Lne_FixWeiht.setValidator(QIntValidator(0,300,self.Lne_FixWeiht))  #QIntValidator 整数的有效判断，范围0-300

    def slot_SaveData(self):
        config_ini = Config.Config()

        window.Btn_1aSetWeight.setText(self.Lne_FixLength.text())  # 1流定重设置显示
        window.Btn_2aSetWeight.setText(self.Lne_FixLength.text())  # 2流定重设置显示
        window.Btn_3aSetWeight.setText(self.Lne_FixLength.text())  # 3流定重设置显示
        window.Btn_4aSetWeight.setText(self.Lne_FixLength.text())  # 4流定重设置显示
        config_ini.writeValue('savedata', 'Lne_FixLength', self.Lne_FixLength.text())
        config_ini.writeValue('init', 'Btn_1aSetWeight', self.Lne_FixLength.text())
        config_ini.writeValue('init', 'Btn_2aSetWeight', self.Lne_FixLength.text())
        config_ini.writeValue('init', 'Btn_3aSetWeight', self.Lne_FixLength.text())
        config_ini.writeValue('init', 'Btn_4aSetWeight', self.Lne_FixLength.text())


class TeamPage(QDialog,UI_SetTeam.Ui_Dialog): #设置班组

    def __init__(self,parent = None):
        super(TeamPage,self).__init__(parent)
        self.setupUi(self)
        self.Btn_TeamNo.clicked.connect(self.close)
        self.Btn_TeamYes.clicked.connect(self.slot_ChangeLocYes)
        self.Btn_TeamYes.clicked.connect(self.close)

    def slot_ChangeLocYes(self):                               #????????????????????限制输入
        Cbb_SetTeamText = self.Cbb_SetTeam.currentText()
        window.Btn_Class.setText(Cbb_SetTeamText)   #修改窗口显示班组
        config_ini = Config.Config()
        config_ini.writeValue('init', 'Btn_Class', Cbb_SetTeamText) #写入config.ini文件


class ProductionDataPage(QDialog,UI_ProductionData.Ui_Dialog):      #生产数据
    def __init__(self,parent = None):
        super(ProductionDataPage,self).__init__(parent)
        self.setupUi(self)
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

class SetCameraPage(QDialog,UI_SetCamera.Ui_Dialog):
    def __init__(self,parent = None):
        super(SetCameraPage,self).__init__(parent)
        self.setupUi(self)
        self.Btn_Exit.clicked.connect(self.close)

class SetSteelDataPage(QDialog,UI_SetSteelData.Ui_Dialog):

    class SteelType(Enum):  #钢种类型枚举
        SteelType_all = 0
        SteelType_one = 1
        SteelType_two = 2
        SteelType_three = 3
        SteelType_four = 4


    def __init__(self,parent = None):
        super(SetSteelDataPage,self).__init__(parent)
        self.setupUi(self)
        self.Btn_Exit.clicked.connect(self.close)
        '''**********************************************************'''
        # self.cb.addItem("全部",self.SteelType.SteelType_all)
        # #当前第1条
        # self.cb_lengthType.addItem("方钢")
        # self.cb_lengthType.setItemData(1,self.SteelType.SteelType_one)


class contPLC(ConsolePLC.siemens):      #PLC通讯
    def __init__(self):
        super(contPLC,self).__init__()

class linkDB():     #连接数据库
    def __init__(self):
        super(linkDB,self).__init__()

    def linkdb(self):
        # 数据库远程连接
        conn = pymssql.connect(host="192.168.2.23", user="sa",
                               password="Admin123", database="DATA", charset="utf8")

        # 使用cursor()方法获取操作游标
        cursor = conn.cursor()
        # 查询语句
        sql = 'select top 1 * Table_1 order by id desc'

        try:
            cursor.execute(sql)  # 游标
            result = cursor.fetchone()  # 查询
            print(result)
        except:

            print("连接数据库报错了！")
        # 关闭数据库连接


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
    # linkDB.linkdb() #数据库连接
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())  # 0是正常退出
    cap.release()
    cv2.destroyAllWindows()
