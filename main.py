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


class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent = None):
        super(MainWindow,self).__init__(parent)  # 调用父类QWidget中的init方法
        self.setupUi(self)
        #self.Btn_FurNo.clicked.connect(self.slot_SetFurNo)     #按钮-设置炉号
        self.Btn_LocNo.clicked.connect(self.slot_SetLocNo)    #按钮-设置连铸机号
        self.Btn_1aSetWeight.clicked.connect(self.slot_SetFixLeng)       #按钮-设置输入设定
        self.Btn_2aSetWeight.clicked.connect(self.slot_SetFixLeng)
        self.Btn_3aSetWeight.clicked.connect(self.slot_SetFixLeng)
        self.Btn_4aSetWeight.clicked.connect(self.slot_SetFixLeng)
        self.Btn_Class.clicked.connect(self.slot_SetTeam)       #按钮-设置班组
        self.Btn_Operator.clicked.connect(self.slot_SetTeam)       #按钮-设置设置操作员
        self.Btn_dataManagement.clicked.connect(self.slot_ProductionData)   #按钮-数据管理
        self.Btn_videoParameter.clicked.connect(self.slot_Camera)       #按钮-视频参数调整

        self.Act_Exit.setShortcut(self.close())     #菜单栏
        self.Act_FurNo.triggered.connect(self.slot_SetFurNo)
        self.Act_Class.triggered.connect(self.slot_SetTeam)
        self.Act_LocNo.triggered.connect(self.slot_SetLocNo)
        self.Act_Exit.triggered.connect(self.close) #菜单栏
        self.Act_SetAlgorithm.triggered.connect(self.slot_SetAlgorithm_triggered)   #菜单栏

        '''时间刷新'''
        self.timer = QTimer()    #设定时间周期
        self.timer.timeout.connect(self.slot_timeOut)
        self.timer.setInterval(200)     #设置定时周期，超出周期启动timeout函数
        self.timer.start()  #启动


        '''视频开始'''

        self.open_flag = False
        self.video_stream = cv2.VideoCapture(0)
        self.painter = QPainter(self)
        self.open_flag = bool(1 - self.open_flag)

    def paintEvent(self, a0: QtGui.QPaintEvent):
        if self.open_flag:
            ret, frame = self.video_stream.read(
            '''尝试2'''
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 转换为灰度图
            ret, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)  #二值阀图像，更好的边缘检测
            binary, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            img = cv2.drawContours(frame, contours, -1, (0, 0, 255), 2)

            self.Qframe = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3,
                                 QImage.Format_RGB888)

            self.labelCamera.setPixmap(QPixmap.fromImage(self.Qframe))
            self.update()
            '''尝试2结束'''


        '''视频结束'''

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

class FurNoPage(QDialog,UI_SetFurNo.Ui_Dialog): #炉号
    def __init__(self,parent = None):
        super(FurNoPage,self).__init__(parent)
        self.setupUi(self)
        self.Btn_SetFurNoNo.clicked.connect(self.close)
        self.Btn_SetFurNoYes.clicked.connect(self.slot_ChangeLocNo)
        self.Btn_SetFurNoYes.clicked.connect(self.close)

    def slot_ChangeLocNo(self):                               #????????????????????限制输入
        LocNotext = self.LabInput_SetFurNo.toPlainText()
        window.Btn_FurNo.setText("炉号:" + LocNotext)

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
        self.Btn_FixLengYes.clicked.connect(self.close)
        self.Ceb_AllowEdit.stateChanged.connect(self.slot_editEnabled)
        self.Lne_FixWeiht.setEnabled(False)
        self.Lne_TheoryWeiht.setEnabled(False)
        self.Lne_Density.setEnabled(False)

    def slot_editEnabled(self,b):       #b勾选编辑
        self.Lne_FixWeiht.setEnabled(b)
        self.Lne_TheoryWeiht.setEnabled(b)
        self.Lne_Density.setEnabled(b)
        self.Lne_FixWeiht.setValidator(QIntValidator(0,300,self.Lne_FixWeiht))  #QIntValidator 整数的有效判断，范围0-300


class TeamPage(QDialog,UI_SetTeam.Ui_Dialog): #设置班组
    class TeamType(Enum):       #枚举 班组
        TeamType_Invalid = 0 #无效
        TeamType_Admin = 1 #管理员
        TeamType_User = 2   #普通用户
        TeamType_Guest = 3  #guest用户
        TeamType_Other = 4 #其他
        TeamType_Max = 5    #最大值

    def __init__(self,parent = None):
        super(TeamPage,self).__init__(parent)
        self.setupUi(self)
        self.Btn_TeamNo.clicked.connect(self.close)

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
    def __init__(self,parent = None):
        super(ProductionDataQueryPage,self).__init__(parent)
        self.setupUi(self)
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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # 创建一个应用程序对象
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())  # 0是正常退出
    cap.release()
    cv2.destroyAllWindows()
