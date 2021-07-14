#标准类
import sys
from tkinter import messagebox

from PyQt5 import QtPrintSupport
from pymouse.windows import PyMouse
import cv2
import numpy
import pymysql
from PyQt5.Qt import *
from PyQt5.QtGui import QIntValidator
from dbutils.pooled_db import PooledDB
import Config
# 引用类
import ConsolePLC
import Log
import SQLlite
import UI_ProductionData
import UI_SetSteelType
import UI_SetAlgorithm
import UI_SetCamera
import UI_SetFixLeng
import UI_SetFurNo
import UI_SetSteelData
import UI_SetTeam
import UI_AddSteelType
import UI_ChangeSteelTypeDensity
import UI_CheckSteelTypeDensity
import UI_ChangeFixLeng
import Main_Data
from UI_MainPage import *
from UI_SetTeam import *

# 画面类


'''
1.新增钢种未找到更新ListWight指令(完成)
2.删除钢种功能(完成)
3.修改钢种密度(完成)
4.更换钢种功能
5.增加坐标位置显示
6.打印功能
7.excel导出功能
8.修改定尺
9.查询钢种密度

'''


list_SteelData = []


global temp_changesteelDensityname  # 修改密度下的临时变量
global temp_changesteelFixleng      # 修改定尺下的定尺

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent = None):
        super(MainWindow,self).__init__(parent)  # 调用父类QWidget中的init方法
        self.setupUi(self)

        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏窗口
        self.setFixedSize(1280, 960)

        self.Btn_Class.clicked.connect(self.slot_SetTeam)       # 按钮-设置班组
        self.Btn_dataManagement.clicked.connect(self.slot_ProductionData)   # 按钮-数据管理
        self.Btn_videoParameter.clicked.connect(self.slot_Camera)       # 按钮-视频参数调整

        self.Act_Exit.setShortcut(self.close())     # 菜单栏
        self.Act_FurNo.triggered.connect(self.slot_SetFurNo)
        self.Act_Exit.triggered.connect(self.close)  # 菜单栏
        self.Act_SetAlgorithm.triggered.connect(self.slot_SetAlgorithm_triggered)   # 菜单栏
        self.Act_SetSteelData.triggered.connect(self.slot_SetSteelData)   # 菜单栏 定尺管理
        self.Act_SetTeam.triggered.connect(self.slot_SetTeam)   # 设备班组
        self.Act_Help.triggered.connect(self.slot_Help)  # 帮助
        self.Act_SetSteelType.triggered.connect(self.slot_SetSteelType)  # 钢种管理
        self.Btn_Exit.clicked.connect(self.slot_close)  # 退出
        # self.Btn_Exit.clicked.connect(self.close)

        self.autoShow()     # 主页面刷新
        self.center()   # 窗口居中


        self.myMouse = PyMouse()
        # 获取鼠标位置
        nowP = self.myMouse.position()
        print(nowP)
        self.main_CameraInit()  # 启动工业摄像头

        config_ini.writeValue('init', 'smtp_vserver','sss') # 测试  11810*160*160 预夹=500 定重目标=2333.0

        '''时间刷新'''
        self.timer = QTimer()    # 设定时间周期线程
        self.timer.timeout.connect(self.slot_timeOut)
        self.timer.setInterval(200)     # 设置定时周期，超出周期启动timeout函数
        self.timer.start()  # 启动

        '''笔记本摄像头开始'''

        # self.open_flag = False
        # self.Camera = cv2.VideoCapture(0)
        # #self.painter = QPainter(self)
        # self.open_flag = bool(1 - self.open_flag)
        #
        # log.logger.info('程序正常开启运行')

    # 笔记本摄像头
    # def paintEvent(self, a0: QtGui.QPaintEvent):
    #     if self.open_flag:
    #         ret, frame = self.Camera.read()
    #
    #         '''尝试1'''
    #         try:
    #             frame = cv2.resize(frame,(800,600), interpolation=cv2.INTER_AREA)
    #             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #
    #             self.Qframe = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3,
    #                                  QImage.Format_RGB888)
    #
    #             self.labelCamera.setPixmap(QPixmap.fromImage(self.Qframe))
    #             self.update()
    #         except Exception as e:
    #             # messagebox.showinfo("提示", e)
    #             print(e)
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


    '''工业相机开始'''

    def main_CameraInit(self):
    #     global hCamera,pFrameBuffer
    #     DevList = mvsdk.CameraEnumerateDevice()
    #     nDev = len(DevList)
    #     if nDev < 1:
    #         print("No camera was found!")
    #         messagebox.showinfo("提示", "未发现相机")
    #         return
    #
    #     DevInfo = DevList[0]
    #     print(DevInfo)
    #
    #     # 打开相机
    #     hCamera = 0
    #     try:
    #         hCamera = mvsdk.CameraInit(DevInfo, -1, -1)
    #     except mvsdk.CameraException as e:
    #         print("CameraInit Failed({}): {}".format(e.error_code, e.message))
    #         return
    #
    #     # 获取相机特性描述
    #     cap = mvsdk.CameraGetCapability(hCamera)
    #
    #     # 判断是黑白相机还是彩色相机
    #     monoCamera = (cap.sIspCapacity.bMonoSensor != 0)
    #
    #     # 黑白相机让ISP直接输出MONO数据，而不是扩展成R=G=B的24位灰度
    #     if monoCamera:
    #         mvsdk.CameraSetIspOutFormat(hCamera, mvsdk.CAMERA_MEDIA_TYPE_MONO8)
    #
    #     # 相机模式切换成连续采集
    #     mvsdk.CameraSetTriggerMode(hCamera, 0)
    #
    #     # 手动曝光，曝光时间30ms
    #     mvsdk.CameraSetAeState(hCamera, 0)
    #     mvsdk.CameraSetExposureTime(hCamera, 30 * 1000)
    #
    #     # 让SDK内部取图线程开始工作
    #     mvsdk.CameraPlay(hCamera)
    #
    #     # 计算RGB buffer所需的大小，这里直接按照相机的最大分辨率来分配
    #     FrameBufferSize = cap.sResolutionRange.iWidthMax * cap.sResolutionRange.iHeightMax * (1 if monoCamera else 3)
    #
    #     # 分配RGB buffer，用来存放ISP输出的图像
    #     # 备注：从相机传输到PC端的是RAW数据，在PC端通过软件ISP转为RGB数据（如果是黑白相机就不需要转换格式，但是ISP还有其它处理，所以也需要分配这个buffer）
    #     pFrameBuffer = mvsdk.CameraAlignMalloc(FrameBufferSize, 16)
    #
    # def paintEvent(self, a0: QtGui.QPaintEvent):
    #     try:
    #         pRawData, FrameHead = mvsdk.CameraGetImageBuffer(hCamera, 200)
    #         mvsdk.CameraImageProcess(hCamera, pRawData, pFrameBuffer, FrameHead)
    #         mvsdk.CameraReleaseImageBuffer(hCamera, pRawData)
    #
    #         # 此时图片已经存储在pFrameBuffer中，对于彩色相机pFrameBuffer=RGB数据，黑白相机pFrameBuffer=8位灰度数据
    #         # 把pFrameBuffer转换成opencv的图像格式以进行后续算法处理
    #         frame_data = (mvsdk.c_ubyte * FrameHead.uBytes).from_address(pFrameBuffer)
    #         frame = np.frombuffer(frame_data, dtype=np.uint8)
    #         frame = frame.reshape((FrameHead.iHeight, FrameHead.iWidth,
    #                                1 if FrameHead.uiMediaType == mvsdk.CAMERA_MEDIA_TYPE_MONO8 else 3))
    #
    #         frame = cv2.resize(frame, (1050, 550), interpolation=cv2.INTER_AREA)
    #         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #
    #         self.Qframe = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3,
    #                              QImage.Format_RGB888)
    #
    #         self.labelCamera.setPixmap(QPixmap.fromImage(self.Qframe))
    #         self.update()
    #
    #
    #         # img4 = frame[0:137, 0:1050]  # 裁剪坐标为[y0:y1, x0:x1]
    #         # cv2.imshow("4", img4)
    #         # img3 = frame[138:274, 0:1050]  # 裁剪坐标为[y0:y1, x0:x1]
    #         # cv2.imshow("3", img3)
    #         # img2 = frame[275:411, 0:1050]  # 裁剪坐标为[y0:y1, x0:x1]
    #         # cv2.imshow("2", img2)
    #         # img1 = frame[412:550, 0:1050]  # 裁剪坐标为[y0:y1, x0:x1]
    #         # # cv2.imshow("1",img1)
    #         # gray = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    #         # blurred = cv2.GaussianBlur(gray, (9, 9), 0)
    #         # ret, thresh = cv2.threshold(blurred, 240, 255, cv2.THRESH_BINARY)  # 二值阀图像，更好的边缘检测
    #         # # binary, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  #轮廓
    #         # contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #         # img1 = cv2.drawContours(img1, contours, -1, (0, 0, 255), 2)  # -1 全部轮廓画出来
    #         # print("一共有多少个" + str(len(contours)))
    #         #
    #         # for i in range(0,len(contours)):
    #         #     cnt = contours[i]
    #         #     if cv2.contourArea(cnt) > 10.0 :
    #         #         print("第" + str(i) + "个是大于要求")
    #         #         print(contours[i])
    #         #
    #         # cv2.imshow("1", img1)
    #
    #
    #
    #     except mvsdk.CameraException as e:
    #         if e.error_code != mvsdk.CAMERA_STATUS_TIME_OUT:
    #             print("CameraGetImageBuffer failed({}): {}".format(e.error_code, e.message))


        # 照片查看
        # self.labelCamera.resize(900,550)
        frame = cv2.imread(
        r"E:\PycharmProjects\FixedLengthSystem\pictrue\1.bmp")
        frame = cv2.resize(frame, (900, 600), interpolation=cv2.INTER_AREA)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        img1 = frame[190:240, 200:900]  # 裁剪坐标为[y0:y1, x0:x1]
        colors = (255, 0, 0)
        cv2.rectangle(frame, (200, 190), (900, 240), colors, 2)
        print("img1:",img1)
        cv2.imshow("1", img1)

        # self.Qframe = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3,
        #                      QImage.Format_RGB888)
        # self.labelCamera_1.setPixmap(QPixmap.fromImage(self.Qframe))


        img2 = frame[240:310, 200:900]  # 裁剪坐标为[y0:y1, x0:x1]

        colors = (255, 0, 0)
        cv2.rectangle(frame, (200, 240), (900, 310), colors, 2)
        cv2.imshow("2", img2)
        # self.Qframe = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3,
        #                      QImage.Format_RGB888)
        # self.labelCamera_1.setPixmap(QPixmap.fromImage(self.Qframe))

        img3 = frame[310:380, 200:900]  # 裁剪坐标为[y0:y1, x0:x1]
        colors = (255, 0, 0)
        cv2.rectangle(frame, (200, 310), (900, 380), colors, 2)
        cv2.imshow("3", img3)
        # self.Qframe = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3,
        #                      QImage.Format_RGB888)
        # self.labelCamera_1.setPixmap(QPixmap.fromImage(self.Qframe))

        img4 = frame[380:460, 200:1000]  # 裁剪坐标为[y0:y1, x0:x1]
        colors = (255, 0, 0)
        cv2.rectangle(frame, (200, 380), (1000, 460), colors, 2)


        gray = cv2.cvtColor(img4, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (9, 9), 0)
        ret, thresh = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY)  # 二值阀图像，更好的边缘检测
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 轮廓
        img4 = cv2.drawContours(img4, contours, -1, (0, 0, 255), 3)  # -1 全部轮廓画出来
        kernel = numpy.ones((3, 3), numpy.uint8)
        img4 = cv2.erode(img4, kernel, iterations=1)

        print("一共有多少个" + str(len(contours)))
        for i in range(0,len(contours)):
            cnt = contours[i]
            print(cv2.contourArea(cnt))
            if cv2.contourArea(cnt) > 100.0 :
                print("第" + str(i + 1) + "个是大于要求")
                # print(contours[i])
        cv2.imshow("4", img4)


        self.Qframe = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3,
                             QImage.Format_RGB888)
        self.labelCamera.setPixmap(QPixmap.fromImage(self.Qframe))

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (9, 9), 0)
        ret, thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)  # 二值阀图像，更好的边缘检测
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  #轮廓
        frame = cv2.drawContours(frame, contours, -1, (0, 0, 255), 2)  # -1 全部轮廓画出来
        print("一共有多少个" + str(len(contours)))

        frameone = frame[380:460, 200:1000]
        print('frameone:',frameone,type(frameone))

        self.Qframe = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3,
                             QImage.Format_RGB888)
        print(self.Qframe,type(self.Qframe))
        self.labelCamera.setPixmap(QPixmap.fromImage(self.Qframe))

    '''工业相机结束'''
    # 主页面刷新
    def autoShow(self):
        '''恢复上次关闭数据_初始化config.ini -> init'''
        self.Btn_Class.setText((config_ini.readvalue('init', 'Btn_Class')))  # 班次
        self.Lab_talRoot.setText((config_ini.readvalue('init', 'Lab_talRoot')))  # 总记数
        self.Lab_talTon.setText((config_ini.readvalue('init', 'Lab_talTon')))  # 总重量
        self.Btn_FurNo.setText("炉号:  " + str((config_fur.readvalue('FurListData1','lne_setfurno'))))  # 炉号
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
        self.statuShow('数据读取中',5)

    # 状态栏显示函数
    def statuShow(self,showString,showTime):
        '''
        :param showString:需要在状态栏显示的内容
        :param showTime: 显示的时间*秒
        :return: 状态栏显示
        '''
        # 下面的状态栏
        self.status = self.statusBar()
        # 状态栏消息的消息
        # self.status.showMessage('只存在5秒的消息', 5000)
        self.status.showMessage(showString,showTime * 1000)

    # 窗口居中
    def center(self):
        # 获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()
        # 计算中间位置
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    # 关闭保持数据
    def slot_close(self,event):
        try:
            config_ini.writeValue('init', 'smtp_vserver', 'sss')
            config_ini.writeValue('init', 'Lab_talRoot', window.Lab_talRoot.text())  # 总根数写入配置文件
            config_ini.writeValue('init', 'Lab_talTon', window.Lab_talTon.text())   # 总重量写入配置文件
        except Exception as e :
            print(e)
        else:
            app = QApplication.instance()
            # 退出应用程序
            app.quit()


    def slot_timeOut(self):     # 延时触发该函数   定时
        tm = QTime.currentTime()    # 获取当前时间
        dd = QDate.currentDate()    # 获取当前日期
        strText = tm.toString("hh:mm:ss")
        self.Lab_Time.setText(strText)
        self.Lab_DateDay.setText(dd.toString(Qt.DefaultLocaleLongDate))

    def slot_SetFurNo(self):    # 设置炉号
        furno = FurNoPage()
        furno.exec_()

    def slot_SetFixLeng(self):  # 设置输入定尺
        Fixleng = FixLengPage()
        Fixleng.exec_()

    def slot_SetTeam(self):     # 设置班组
        Team = TeamPage()
        Team.exec_()

    def slot_ProductionData(self):  # 设置生产数据
        Data = ProductionDataPage()
        Data.exec_()

    def slot_Camera(self):      # 视频参数调整
        camera = SetCameraPage()
        camera.exec_()

    def slot_SetAlgorithm_triggered(self):  # 设置算法
        algorithm = AlgorithmPage()
        algorithm.exec_()

    def slot_SetSteelData(self):        # 定尺管理
        steeldata = SetSteelDataPage()
        steeldata.exec_()

    def slot_SetSteelType(self):    # 钢种管理
        steeltypeManage = SetSteelTypePage()
        steeltypeManage.exec_()

    def slot_Help(self):
        QtWidgets.QMessageBox.question(self, "帮助", "联系计控室",
                                                     QtWidgets.QMessageBox.Yes )

class FurNoPage(QDialog,UI_SetFurNo.Ui_Dialog): # 炉号
    def __init__(self,parent = None):
        super(FurNoPage,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.Lne_SetFurNum.setValidator(QIntValidator(0,65535)) # 设置输入整形数字范围
        self.Lne_SetFurNo.setValidator(QDoubleValidator())  # 设置输入浮点数字范围

        #显示 列表信息
        for i in range(1,11):
            Furstr = 'FurListData' + str(i)
            if int(config_fur.readvalue(Furstr, 'show')) == 1 :     #判断在第几个开始显示
                a = "炉号" + config_fur.readvalue(Furstr, 'lne_setfurno')
                b = "根数" + config_fur.readvalue(Furstr, 'lne_setfurnum')
                self.LW_SetFurNo.addItem( a + b )

        self.Btn_Exit.clicked.connect(self.close)
        self.Btn_addFurNum.clicked.connect(self.slot_addFurNum)     # 增加项
        self.Btn_delFurNum.clicked.connect(self.slot_delFurNum)     # 删除项
        self.LW_SetFurNo.setSelectionMode(QAbstractItemView.SingleSelection)     # 单项处理
        self.LW_SetFurNo.itemClicked.connect(self.slot_SetFurNoItemCliked)  # 单击触发 提示
        self.LW_SetFurNo.currentItemChanged.connect(self.slot_SetFurNoItemDoubleClicked)    # 选中项前后字体变色

    # 炉号列表增加
    def slot_addFurNum(self):
        strNo =self.Lne_SetFurNo.text()
        strNum = self.Lne_SetFurNum.text()

        if len(strNo) > 0 and len(strNum) > 0:  # 判断是否输入
            # 修改配置文件
            for i in range(1, 11):
                Furstr = 'FurListData' + str(i)     # 配置文件中，名称
                if int(config_fur.readvalue(Furstr, 'show')) == 0:  #
                    config_fur.readvalue(Furstr, 'row')     # 获取未显示行数
                    config_fur.writeValue(Furstr,'lne_setfurno',self.Lne_SetFurNo.text())
                    config_fur.writeValue(Furstr, 'lne_setfurnum', self.Lne_SetFurNum.text())
                    config_fur.writeValue(Furstr, 'show','1')
                    self.LW_SetFurNo.addItem('炉号' + str(self.Lne_SetFurNo.text()) +'根数'+ str(self.Lne_SetFurNum.text()))
                    window.autoShow()
                    break
        else:
            QtWidgets.QMessageBox.question(self, "提示", "请全部输入！",
                                           QtWidgets.QMessageBox.Yes)

    # 炉号列表指定删除
    def slot_delFurNum(self):
        pItem = self.LW_SetFurNo.currentItem()   # 得到左侧列表选中项
        if pItem is None:
            return
        idx = self.LW_SetFurNo.row(pItem)   # 得到项的序号  所在行 idx =>int
        # print(pItem.text())  # 所选行的文本
        # Furstr = 'FurListData' + str(idx)  # 配置文件中，名称
        # print(idx)  #选择行数
        print(idx)
        self.LW_SetFurNo.takeItem(idx)
        if idx == 9 :   #当选择最后一列，直接隐藏
            config_fur.writeValue('FurListData10', 'show', '0')
            window.autoShow()
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
                            window.autoShow()
                            return
                elif int(config_fur.readvalue('FurListData10', 'show')) == 1:
                    config_fur.writeValue('FurListData10', 'show', '0')
                    window.autoShow()
                    return

    #炉号列表自动删第一行
    # 自动减炉号
    # furno = FurNoPage()
    # furno.slot_autoDelFurNum()
    def slot_autoDelFurNum(self):
        idx = 0
        if self.LW_SetFurNo.count() == 0 :
            QtWidgets.QMessageBox.question(self, "提示", "炉号为空",
                                           QtWidgets.QMessageBox.Yes)
            return
        else:
            self.LW_SetFurNo.takeItem(idx)
            if idx == 9 :   #当选择最后一列，直接隐藏
                config_fur.writeValue('FurListData10', 'show', '0')
                window.autoShow()
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
                                window.autoShow()
                                return
                    elif int(config_fur.readvalue('FurListData10', 'show')) == 1:
                        config_fur.writeValue('FurListData10', 'show', '0')
                        window.autoShow()
                        return

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

class FixLengPage(QDialog,UI_SetFixLeng.Ui_Dialog): #设置输入定尺
    def __init__(self,parent = None):
        super(FixLengPage,self).__init__(parent)
        self.setupUi(self)

        #输入限制
        self.Lne_FixLength.setValidator(QIntValidator(0,65535)) #设置输入整形数字范围
        self.Lne_PreClampOffset.setValidator(QIntValidator(0, 65535))  # 设置输入整形数字范围
        self.Lne_TheoryWeiht.setValidator(QIntValidator(0, 65535))  # 设置输入整形数字范围
        self.Lne_Density.setValidator(QDoubleValidator())  # 设置输入浮点数字范围
        self.Lne_ErrRangeMinus.setValidator(QIntValidator(0, 65535))  # 设置输入整形数字范围
        self.Lne_ErrRangePlus.setValidator(QIntValidator(0, 65535))  # 设置输入整形数字范围
        self.Lne_LengthRangeMax.setValidator(QIntValidator(0, 65535))  # 设置输入整形数字范围
        self.Lne_WeightMax.setValidator(QIntValidator(0, 65535))  # 设置输入整形数字范围
        self.Lne_FixWeiht.setValidator(QIntValidator(0, 65535))  # 设置输入整形数字范围

        # 按钮
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.Btn_FixLengNo.clicked.connect(self.close)
        self.Ceb_AllowEdit.stateChanged.connect(self.slot_editEnabled)
        # self.Btn_FixLengYes.clicked.connect(self.close)
        self.Lne_FixWeiht.setEnabled(False)
        self.Lne_TheoryWeiht.setEnabled(False)
        self.Lne_Density.setEnabled(False)
        self.Btn_FixLengYes.clicked.connect(self.slot_SaveData)




    def slot_editEnabled(self,b):       #b勾选编辑
        self.Lne_FixWeiht.setEnabled(b)
        self.Lne_TheoryWeiht.setEnabled(b)
        self.Lne_Density.setEnabled(b)
        self.Lne_FixWeiht.setValidator(QIntValidator(0,50000,self.Lne_FixWeiht))  #QIntValidator 整数的有效判断，范围0-300

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

                # conn = pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
                # cursor = conn.cursor()
                sql = 'SELECT * FROM `fixsteeldata`'
                cursor.execute(sql)
                # conn.commit()
                data = cursor.fetchall()
                if data:
                    for row, form in enumerate(data):
                        # for column,item in enumerate(form[0]):
                        #     self.TW_lengthType.setItem(row,column,QTableWidgetItem(str(form[0])))
                        #     column += 1
                        #     print(row,form[0])
                        print(row,form[0])
                        SQLname = str(self.Lne_FixLength.text()) + ' 预夹=' + str(
                            self.Lne_PreClampOffset.text()) + ' 定重目标=' + str(self.Lne_FixWeiht.text())
                        if SQLname  in form[0]:
                            QtWidgets.QMessageBox.question(self, "提示", "有重复",
                                                           QtWidgets.QMessageBox.Yes)
                            return

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


                    # conn = pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
                    # cursor = conn.cursor()
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
                    QtWidgets.QMessageBox.question(self, "提示", "添加成功",
                                                   QtWidgets.QMessageBox.Yes)
                    self.close()
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
        self.Btn_PrintSupport.clicked.connect(self.slot_printSupport)   # 打印
        self.Btn_Query.clicked.connect(self.slot_ReadSQLProductionDataQuery)    # 查询
        self.autoShow()
        # self.editor = QTextEdit('默认文本',self)
        # self.editor.setGeometry(20,60,260,200)

    def autoShow(self):
        self.Det_DateRangeFrom.setDate(QDate.currentDate())     # 默认当前日期
        self.Det_DateRangeTo.setDate(QDate.currentDate())
        try:
            sql = 'SELECT * FROM `steeltype`'
            cursor.execute(sql)
            steeltypedata = cursor.fetchall()

            try:
                if steeltypedata:
                    self.cb_selectSteelType.clear()
                    self.cb_selectSteelType.addItem('全部')
                    for steeltypeNum in range(len(steeltypedata)):
                        self.cb_selectSteelType.addItem(str(steeltypedata[steeltypeNum][0]))
            except Exception as e:
                window.statuShow(e,5)

        except Exception as e:
            window.statuShow(e, 5)
            QtWidgets.QMessageBox.question(self, "提示", e,
                                           QtWidgets.QMessageBox.Yes)

    def slot_ReadSQLProductionDataQuery(self):
        self.TaW_ProductionData.clear()
        selectDayFrom = self.Det_DateRangeFrom.date().toString(Qt.ISODate)  # 选择的开始日期
        selectDayTo = self.Det_DateRangeTo.date().toString(Qt.ISODate)  # 选择的结束日期

        # print(self.Det_DateRangeFrom.date().toString(Qt.ISODate))   # 时间类型转换
        selectTimeFrom = self.Tet_TimeRangeFrom.text()  # 选择的开始时间
        selectTimeTo = self.Tet_TimeRangeTo.text()  # 选择的结束时间
        selectDateTimeFrom = str(selectDayFrom) + " " + str(selectTimeFrom)  # 拼接开始日期时间
        selectDateTimeTo = str(selectDayTo) + " " + str(selectTimeTo)  # 拼接结束日期时间
        SQLbody_DateTime = " and IDtime >= '"+ str(selectDateTimeFrom) + "' and IDtime <= '"+ str(selectDateTimeTo) + "'"

        # 流号
        if self.cb_selectFlow.currentText() == "全部":
            SQLbody_selectFlow = ""
        else:
            SQLbody_selectFlow = " and FlowNum = '" + self.cb_selectFlow.currentText() + "'"  # 选择的流号
        # 班次
        if self.cb_selectTeam.currentText() == "全部":
            SQLbody_selectTeam = ""
        else:
            SQLbody_selectTeam = " and Team = '" + self.cb_selectTeam.currentText() + "'"  # 选择的班组
        # 钢种
        if self.cb_selectSteelType.currentText() == "全部":
            SQLbody_selectSteelType = ""
        else:
            SQLbody_selectSteelType = " and SteelType = '" + self.cb_selectSteelType.currentText() + "'"  # 选择的钢种

        selectLengRangeFrom = self.Lne_LengRangeFrom.text()  # 选择的定尺开始范围
        selectLengRangeTo = self.Lne_LengRangeTo.text()  # 选择的定尺结束范围
        SQLbody_LengRange = " and FixLength >= '" + str(selectLengRangeFrom) + "' and FixLength <= '"+ str(selectLengRangeTo) + "'"

        selectsetWeightFrom = self.Lne_SetWeightFrom.text()  # 选择的重量目标开始范围
        selectsetWeightTo = self.Lne_SetWeightTo.text()  # 选择的重量目标结束范围
        SQLbody_setWeight = " and SetWeight >= '"+ str(selectsetWeightFrom) + "' and SetWeight <= '"+ str(selectsetWeightTo) + "'"
        sqlheader = "SELECT * FROM `productiondata` WHERE 1=1 "
        try:
            sql = "" + str(sqlheader) + "" + str(SQLbody_DateTime) + "" + str(SQLbody_selectFlow) + "" + str(SQLbody_selectTeam) + "" + str(SQLbody_selectSteelType) + "" + str(SQLbody_LengRange) + "" + str(SQLbody_setWeight) + ""
            cursor.execute(sql)
            fixsteelSqldata = cursor.fetchall()

            try:
                if fixsteelSqldata:
                    self.TaW_ProductionData.clear()
                    # 设置名称列数
                    self.TaW_ProductionData.setRowCount(int(len(fixsteelSqldata)))
                    # 设置种类行数
                    self.TaW_ProductionData.setColumnCount(int(len(fixsteelSqldata[0])))
                    # 设置水平方向的表头标签与垂直方向上的表头标签，注意必须在初始化行列之后进行，否则，没有效果
                    self.TaW_ProductionData.setHorizontalHeaderLabels(["流号", "炉号", "定尺", "班次", "钢种","实际重量", "是否称重", "设置重量", "时间"])
                    # 禁止编辑
                    self.TaW_ProductionData.setEditTriggers(QAbstractItemView.NoEditTriggers)
                    # TODO 优化 2 设置水平方向表格为自适应的伸缩模式
                    # self.TaW_ProductionData.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                    # 单元格内容居中
                    # self.TaW_ProductionData.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    # 单元格宽度
                    self.TaW_ProductionData.setColumnWidth(0, 80)  # 流号
                    self.TaW_ProductionData.setColumnWidth(1, 100)  # 炉号
                    self.TaW_ProductionData.setColumnWidth(2, 100)  # 定尺
                    self.TaW_ProductionData.setColumnWidth(3, 80)  # 班次
                    self.TaW_ProductionData.setColumnWidth(4, 100)  # 钢种
                    self.TaW_ProductionData.setColumnWidth(5, 100)  # 实际重量
                    self.TaW_ProductionData.setColumnWidth(6, 100)  # 是否称重
                    self.TaW_ProductionData.setColumnWidth(7, 100)  # 设置重量
                    self.TaW_ProductionData.setColumnWidth(8, 197)  # 时间
                    # 水平布局
                    layout = QHBoxLayout()
                    print(fixsteelSqldata)

                    for i in range(len(fixsteelSqldata)):
                        for j in range(len(fixsteelSqldata[i])):
                            itemContent = "%s" % (fixsteelSqldata[i][j])

                            # 为每个表格内添加数据
                            self.TaW_ProductionData.setItem(i, j, QTableWidgetItem(itemContent))
                        layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                    self.setLayout(layout)

            except Exception as e:
                window.statuShow(e,5)
                print(e)
        except Exception as e:
            window.statuShow(e, 5)
            print(e)


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

    def slot_printSupport(self):
        printer =  QtPrintSupport.QPrinter()
        #画布绘制出来
        painter = QtGui.QPainter()
        # 绘制的目标重定向到打印机
        painter.begin(printer)
        # 获得可视的屏幕
        screen = self.editor.grab()
        painter.drawPixmap(10,10,screen)
        painter.end()

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

class SetSteelTypePage(QDialog,UI_SetSteelType.Ui_Dialog):
    def __init__(self,parent = None):
        super(SetSteelTypePage,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        try:
            self.Btn_addSteelType.clicked.connect(self.slot_addSteelType)   #新增钢种
            self.Btn_changeSteelDensity.clicked.connect(self.slot_changesteeldensity)   #修改钢种密度
            self.Btn_Exit.clicked.connect(self.close)      #退出
            self.Btn_delSteelType.clicked.connect(self.slot_delsteeltype)  # 删除项
            self.LW_SteelType.setSelectionMode(QAbstractItemView.SingleSelection)  # 单项处理
            self.LW_SteelType.itemClicked.connect(self.slot_SetFurNoItemCliked)  # 单击触发 提示
            self.LW_SteelType.currentItemChanged.connect(self.slot_setFurNoItemDoubleClicked)  # 选中项前后字体变色
            self.Btn_CheckSteelDensity.clicked.connect(self.slot_checkSteelDensity)  # 查看钢种密度
            self.Btn_changeSteelType.clicked.connect(self.slot_changeSteelType) # 更换钢种
            self.autoShow()
        except Exception as e:
            print(e)

    def autoShow(self):
        # 读取config 钢种
        configSteelType = config_ini.readvalue('init', 'lab_1csteels')
        self.Lab_showSteelType.setText(str(configSteelType))
        self.LW_SteelType.clear()
        sql_sqlreadsteeltypevalue = SQLlite.SQL_readSteeltype()  # 读取数据库里的钢种信息
        if sql_sqlreadsteeltypevalue == 0 :
            print("数据为空")
        else:
            #显示出mysql中所有的钢种名称
            for sqlreadsteeltypevalue in range(len(sql_sqlreadsteeltypevalue)) :
                    self.LW_SteelType.addItem(sql_sqlreadsteeltypevalue[sqlreadsteeltypevalue][0])

    def slot_addSteelType(self):
        addsteeltype = AddSteelTypePage()
        if addsteeltype.exec_() == 0 :
            self.autoShow()

    def slot_checkSteelDensity(self):
        checksteeltypedensity = CheckSteelTypeDensityPage()
        checksteeltypedensity.exec_()

    def slot_delsteeltype(self):
        pItem = self.LW_SteelType.currentItem()  # 得到左侧列表选中项
        if pItem is None:
            QtWidgets.QMessageBox.question(self, "提示", "请选择钢种名称",
                                           QtWidgets.QMessageBox.Yes)
            return
        idx = self.LW_SteelType.row(pItem)  # 得到项的序号  所在行 idx =>int
        print(idx)
        SQLlite.SQL_delSteeltype(self.LW_SteelType.item(idx).text())    #删除mysql中的数据
        print(self.LW_SteelType.item(idx).text())
        self.LW_SteelType.takeItem(idx)  #移除选中的项

    def slot_changesteeldensity(self):
        global temp_changesteelDensityname
        pItem = self.LW_SteelType.currentItem()  # 得到左侧列表选中项
        if pItem is None:
            QtWidgets.QMessageBox.question(self, "提示", "请选择钢种名称",
                                           QtWidgets.QMessageBox.Yes)
            return
        idx = self.LW_SteelType.row(pItem)  # 得到项的序号  所在行 idx =>int
        temp_changesteelDensityname = self.LW_SteelType.item(idx).text()
        addsteeltype = ChangeSteelTypeDensityPage()
        addsteeltype.exec_()

    def slot_changeSteelType(self):
        pItem = self.LW_SteelType.currentItem()  # 得到左侧列表选中项
        if pItem is None:
            QtWidgets.QMessageBox.question(self, "提示", "请选择钢种名称",
                                           QtWidgets.QMessageBox.Yes)
            return
        idx = self.LW_SteelType.row(pItem)  # 得到项的序号  所在行 idx =>int
        # 写入config 里的钢种中
        config_ini.writeValue('init', 'lab_1csteels', str(self.LW_SteelType.item(idx).text()))
        config_ini.writeValue('init', 'lab_2csteels', str(self.LW_SteelType.item(idx).text()))
        config_ini.writeValue('init', 'lab_3csteels', str(self.LW_SteelType.item(idx).text()))
        config_ini.writeValue('init', 'lab_4csteels', str(self.LW_SteelType.item(idx).text()))
        self.autoShow()
        window.autoShow()

    def slot_SetFurNoItemCliked(self,item): # 选中项触发字体变化  item
        ft = item.font()
        ft.setBold(True)
        item.setFont(ft)

    def slot_setFurNoItemDoubleClicked(self,current,previous):  # current 新选中的项  previous之前选中的项
        # 将之前选中的字体粗体恢复
        if not (previous is None):
            ft = previous.font()
            ft.setBold(False)
            previous.setFont(ft)


class AddSteelTypePage(QDialog,UI_AddSteelType.Ui_Dialog): #增加钢种类型页面
    def __init__(self,parent = None):
        super(AddSteelTypePage,self).__init__(parent)
        self.setupUi(self)

        try:
            self.Btn_No.clicked.connect(self.close)
            self.Lne_steelDensity.setValidator(QDoubleValidator())  # 设置输入浮点数字范围
            self.Btn_Yes.clicked.connect(self.slot_saveSteelType)
        except Exception as e:
            print(e)

    # 新增钢种名称及密度
    def slot_saveSteelType(self):
        if len(self.Lne_steelName.text()) > 0 and len(self.Lne_steelDensity.text()) > 0 and float(self.Lne_steelDensity.text()) > 6 :
            try:
                SQLlite.SQL_addSteelType('钢种名称', '钢种密度', value1=str(self.Lne_steelName.text()),
                                         value2=self.Lne_steelDensity.text())
                QtWidgets.QMessageBox.question(self, "提示", "添加成功",
                                               QtWidgets.QMessageBox.Yes)
                #更新列表listwidget
                self.close()

            except Exception as e:
                QtWidgets.QMessageBox.question(self, "提示", e,
                                               QtWidgets.QMessageBox.Yes)
        elif len(self.Lne_steelName.text()) > 0 and len(self.Lne_steelDensity.text()) > 0 and float(self.Lne_steelDensity.text()) <= 6 :
            QtWidgets.QMessageBox.question(self, "提示", "输入钢种密度过低",
                                           QtWidgets.QMessageBox.Yes)
        else:
            QtWidgets.QMessageBox.question(self, "提示", "请输入钢种名称及密度",
                                           QtWidgets.QMessageBox.Yes)

class ChangeSteelTypeDensityPage(QDialog,UI_ChangeSteelTypeDensity.Ui_Dialog): #修改钢种密度页面
    def __init__(self,parent = None):
        super(ChangeSteelTypeDensityPage,self).__init__(parent)
        self.setupUi(self)
        self.Lab_showSteelTypename.setText(temp_changesteelDensityname)
        self.Lne_steelDensity.setValidator(QDoubleValidator())  # 设置输入浮点数字范围
        self.Btn_No.clicked.connect(self.close)
        self.Btn_Yes.clicked.connect(self.slot_changeSteelTypeDensity)


    def slot_changeSteelTypeDensity(self):
        global temp_changesteelDensityname
        if len(self.Lne_steelDensity.text()) > 0 and float(self.Lne_steelDensity.text()) > 6:
            SQLlite.SQL_updataSteeltype(str(temp_changesteelDensityname),self.Lne_steelDensity.text())
            QtWidgets.QMessageBox.question(self, "提示", "钢种密度修改成功",
                                           QtWidgets.QMessageBox.Yes)
            self.close()
        elif len(self.Lne_steelDensity.text()) == 0 :
            QtWidgets.QMessageBox.question(self, "提示", "请输入密度",
                                           QtWidgets.QMessageBox.Yes)
        else:
            print("数据过小")
            QtWidgets.QMessageBox.question(self, "提示", "输入数据过小",
                                           QtWidgets.QMessageBox.Yes)

class CheckSteelTypeDensityPage(QDialog,UI_CheckSteelTypeDensity.Ui_Dialog):
    def __init__(self,parent = None):
        super(CheckSteelTypeDensityPage,self).__init__(parent)
        self.setupUi(self)
        try:
            self.Btn_Exit.clicked.connect(self.close)
            self.autoShow()
        except Exception as e:
            print(e)

    def autoShow(self):
        try:
            self.TaW_CheckSteelDensity.clear()
            sql_sqlreadsteeltypevalue = SQLlite.SQL_readSteeltype()  # 读取数据库里的钢种信息
            if sql_sqlreadsteeltypevalue == 0:
                print("数据为空")
            else:
                # 显示出mysql中所有的钢种名称
                print('种类行长度:',len(sql_sqlreadsteeltypevalue))
                print('数据列长度:', len(sql_sqlreadsteeltypevalue[0]))
                # 设置名称列数
                self.TaW_CheckSteelDensity.setRowCount(int(len(sql_sqlreadsteeltypevalue)))
                # 设置种类行数
                self.TaW_CheckSteelDensity.setColumnCount(int(len(sql_sqlreadsteeltypevalue[0])))
                # 设置水平方向的表头标签与垂直方向上的表头标签，注意必须在初始化行列之后进行，否则，没有效果
                self.TaW_CheckSteelDensity.setHorizontalHeaderLabels(["钢种类型","钢种密度"])
                # 禁止编辑
                self.TaW_CheckSteelDensity.setEditTriggers(QAbstractItemView.NoEditTriggers)
                # TODO 优化 2 设置水平方向表格为自适应的伸缩模式
                self.TaW_CheckSteelDensity.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

                self.TaW_CheckSteelDensity.setColumnWidth(0,160)    # 将第一列的单元宽度设置为160
                self.TaW_CheckSteelDensity.setColumnWidth(1,161)    # 将第二列的单元宽度设置为160
                # 水平布局
                layout = QHBoxLayout()

                for i in range(len(sql_sqlreadsteeltypevalue)):
                    for j in range(len(sql_sqlreadsteeltypevalue[0])):
                        itemContent = "%s" % (sql_sqlreadsteeltypevalue[i][j])
                        # 为每个表格内添加数据
                        self.TaW_CheckSteelDensity.setItem(i, j, QTableWidgetItem(itemContent))
                self.setLayout(layout)


                # TODO 优化 4 设置表格整行选中
                # TableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

                # TODO 优化 5 将行与列的高度设置为所显示的内容的宽度高度匹配
                # QTableWidget.resizeColumnsToContents(TableWidget)
                # QTableWidget.resizeRowsToContents(TableWidget)

                # TODO 优化 6 表格头的显示与隐藏
                # TableWidget.verticalHeader().setVisible(False)
                # TableWidget.horizontalHeader().setVisible(False)

                # TOdo 优化7 在单元格内放置控件
                # comBox=QComboBox()
                # comBox.addItems(['男','女'])
                # comBox.addItem('未知')
                # comBox.setStyleSheet('QComboBox{margin:3px}')
                # TableWidget.setCellWidget(0,1,comBox)
                #
                # searchBtn=QPushButton('修改')
                # searchBtn.setDown(True)
                # searchBtn.setStyleSheet('QPushButton{margin:3px}')
                # TableWidget.setCellWidget(0,2,searchBtn)
        except Exception as e:
            print(e)

class SetSteelDataPage(QDialog,UI_SetSteelData.Ui_Dialog):

    def __init__(self,parent = None):
        super(SetSteelDataPage,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.Btn_Exit.clicked.connect(self.close)   # 退出
        self.Btn_addLength.clicked.connect(self.slot_addLength) # 添加所选定尺
        self.Btn_delLength.clicked.connect(self.slot_delLength) # 删除所选定尺
        self.Btn_chgLength.clicked.connect(self.slot_changelength)  # 修改所选定尺
        self.Btn_switchLength.clicked.connect(self.slot_switchlength)  # 切换所选定尺
        self.LW_lengthType.setSelectionMode(QAbstractItemView.SingleSelection)  # 单项处理
        self.LW_lengthType.itemClicked.connect(self.slot_SetFurNoItemCliked)  # 单击触发 提示
        self.LW_lengthType.currentItemChanged.connect(self.slot_setFurNoItemDoubleClicked)  # 选中项前后字体变色
        self.autoShow()
        '''**********************************************************'''

    # 数据库查询
    def autoShow(self):
        try:
            sql = 'SELECT * FROM `fixsteeldata`'
            cursor.execute(sql)
            # conn.commit()
            fixsteeldatadata =cursor.fetchall()

            if fixsteeldatadata:
                self.LW_lengthType.clear()
                for row,form in enumerate(fixsteeldatadata):
                    self.LW_lengthType.addItem(str(form[0]))

        except Exception as e:
            QtWidgets.QMessageBox.question(self, "提示",e,
                                           QtWidgets.QMessageBox.Yes)


    def slot_addLength(self):
        Fixleng = FixLengPage()
        if Fixleng.exec_() == 0:
            self.autoShow()


    def slot_delLength(self):
        try:
            pItem = self.LW_lengthType.currentItem()  # 得到左侧列表选中项
            if pItem is None:
                return
            idx = self.LW_lengthType.row(pItem)  # 得到项的序号  所在行 idx =>int
            # print(pItem.text())  # 所选行的文本
            # print(idx)  #选择行数
            self.LW_lengthType.takeItem(idx)

            sql = "DELETE FROM fixsteeldata WHERE SteelName = '" + pItem.text() +"';"
            cursor.execute(sql)
            conn.commit()
            self.autoShow()

        except Exception as e:
            QtWidgets.QMessageBox.question(self, "提示",e,
                                           QtWidgets.QMessageBox.Yes)

    def slot_changelength(self):    #修改定尺
        global temp_changesteelFixleng
        pItem = self.LW_lengthType.currentItem()
        if pItem is None:
            return
        idx = self.LW_lengthType.row(pItem)
        temp_changesteelFixleng = self.LW_lengthType.item(idx).text()
        changeSteelDate = ChangeFixLengPage()
        if changeSteelDate.exec_() == 0:
            self.autoShow()

    def slot_switchlength(self):    #切换定尺
        try:
            pItem = self.LW_lengthType.currentItem()  # 得到左侧列表选中项
            if pItem is None:
                return
            idx = self.LW_lengthType.row(pItem)  # 得到项的序号  所在行 idx =>int
            print(pItem.text())  # 所选行的文本
            try:
                sql = 'SELECT * FROM `fixsteeldata`'
                cursor.execute(sql)
                conn.commit()
                switchlengdata = cursor.fetchall()
                for switchleng in range(len(switchlengdata)):
                    # 读取选中的信息，显示到页面
                    if pItem.text() == switchlengdata[switchleng][0]:
                        print(str(switchlengdata[switchleng]))
                        # 写入config 里
                        # 定尺长度 文本
                        config_ini.writeValue('init', 'lab_1csetlength', str(switchlengdata[switchleng][1]))
                        config_ini.writeValue('init', 'lab_2csetlength', str(switchlengdata[switchleng][1]))
                        config_ini.writeValue('init', 'lab_3csetlength', str(switchlengdata[switchleng][1]))
                        config_ini.writeValue('init', 'lab_4csetlength', str(switchlengdata[switchleng][1]))
                        # 定尺长度,按钮
                        config_ini.writeValue('init', 'btn_1asetweight', str(switchlengdata[switchleng][1]))
                        config_ini.writeValue('init', 'btn_2asetweight', str(switchlengdata[switchleng][1]))
                        config_ini.writeValue('init', 'btn_3asetweight', str(switchlengdata[switchleng][1]))
                        config_ini.writeValue('init', 'btn_4asetweight', str(switchlengdata[switchleng][1]))
                        config_ini.writeValue('init', 'Lab_1cSetPos', str(switchlengdata[switchleng][7]))    # 预夹
                        config_ini.writeValue('init', 'Lab_2cSetPos', str(switchlengdata[switchleng][7]))
                        config_ini.writeValue('init', 'Lab_3cSetPos', str(switchlengdata[switchleng][7]))
                        config_ini.writeValue('init', 'Lab_4cSetPos', str(switchlengdata[switchleng][7]))

                        # 合格重量范围， 指定重量  设置重量- 偏差   设定重量 + 偏差
                        config_ini.writeValue('init', 'lab_1brange', str(float(switchlengdata[switchleng][2]) - float(switchlengdata[switchleng][5])) + "~" + str((float(switchlengdata[switchleng][6])) + float(switchlengdata[switchleng][2])))
                        config_ini.writeValue('init', 'lab_2brange', str(
                            float(switchlengdata[switchleng][2]) - float(switchlengdata[switchleng][5])) + "~" + str(
                            (float(switchlengdata[switchleng][6])) + float(switchlengdata[switchleng][2])))
                        config_ini.writeValue('init', 'lab_3brange', str(
                            float(switchlengdata[switchleng][2]) - float(switchlengdata[switchleng][5])) + "~" + str(
                            (float(switchlengdata[switchleng][6])) + float(switchlengdata[switchleng][2])))
                        config_ini.writeValue('init', 'lab_4brange', str(
                            float(switchlengdata[switchleng][2]) - float(switchlengdata[switchleng][5])) + "~" + str(
                            (float(switchlengdata[switchleng][6])) + float(switchlengdata[switchleng][2])))

            except Exception as e:
                print(e)
            else:
                window.autoShow()
        except Exception as e:
            QtWidgets.QMessageBox.question(self, "提示", e,
                                           QtWidgets.QMessageBox.Yes)

    def slot_takeItem(self):    # 删除定尺信息
        pItem = self.LW_lengthType.currentItem()
        if pItem is None:
            return
        idx = self.LW_lengthType.row(pItem)
        self.LW_lengthType.takeItem(idx)

    def slot_SetFurNoItemCliked(self,item): # 选中项触发字体变化  item
        ft = item.font()
        ft.setBold(True)
        item.setFont(ft)

    def slot_setFurNoItemDoubleClicked(self,current,previous):  # current 新选中的项  previous之前选中的项
        # 将之前选中的字体粗体恢复
        if not (previous is None):
            ft = previous.font()
            ft.setBold(False)
            previous.setFont(ft)

class ChangeFixLengPage(QDialog,UI_ChangeFixLeng.Ui_Dialog):
    def __init__(self,parent = None):
        super(ChangeFixLengPage,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        global temp_changesteelFixleng
        self.Lne_PreClampOffset.setValidator(QIntValidator(0, 65535))  # 设置输入整形数字范围
        self.Lne_TheoryWeiht.setValidator(QIntValidator(0, 65535))  # 设置输入整形数字范围
        self.Lne_Density.setValidator(QDoubleValidator())  # 设置输入浮点数字范围
        self.Lne_ErrRangeMinus.setValidator(QIntValidator(0, 65535))  # 设置输入整形数字范围
        self.Lne_ErrRangePlus.setValidator(QIntValidator(0, 65535))  # 设置输入整形数字范围
        self.Lne_LengthRangeMax.setValidator(QIntValidator(0, 65535))  # 设置输入整形数字范围
        self.Lne_WeightMax.setValidator(QIntValidator(0, 65535))  # 设置输入整形数字范围
        self.Lne_FixWeiht.setValidator(QIntValidator(0, 65535))  # 设置输入整形数字范围
        self.Btn_FixLengYes.clicked.connect(self.slot_saveChangeFixLengDate)
        self.Btn_FixLengNo.clicked.connect(self.close)
        try:
            sql = 'SELECT * FROM `fixsteeldata`'
            cursor.execute(sql)
            conn.commit()
            data =cursor.fetchall()
            for fixleng in range(len(data)):
                # 读取选中的信息，显示到页面
                if temp_changesteelFixleng == data[fixleng][0]:
                    self.Lab_ReadLeng.setText(str(data[fixleng][1]))
                    self.Lne_FixWeiht.setText(str(data[fixleng][2]))
                    self.Lne_Density.setText(str(data[fixleng][4]))
                    self.Lne_ErrRangeMinus.setText(str(data[fixleng][5]))
                    self.Lne_ErrRangePlus.setText(str(data[fixleng][6]))
                    self.Lne_PreClampOffset.setText(str(data[fixleng][7]))
                    self.Lne_TheoryWeiht.setText(str(data[fixleng][8]))
                    self.Lne_LengthRangeMax.setText(str(data[fixleng][9]))
                    self.Lne_WeightMax.setText(str(data[fixleng][10]))
        except Exception as e:
            print(e)

    # 保存定尺修改内容
    def slot_saveChangeFixLengDate(self):

        try:
            sql = "SELECT * FROM `fixsteeldata` where SteelName = '"+ str(temp_changesteelFixleng) + "'"
            cursor.execute(sql)
            changefixleng =cursor.fetchall()
            print(changefixleng)
            print(changefixleng[0][1])
            if changefixleng :
                SQLname = str(self.Lab_ReadLeng.text()) + ' 预夹=' + str(
                    self.Lne_PreClampOffset.text()) + ' 定重目标=' + str(self.Lne_FixWeiht.text())

                sql = "UPDATE fixsteeldata SET SteelName = '" + str(SQLname) + "' , FixWeiht= "+ str(self.Lne_FixWeiht.text()) + ", Density= "+ str(self.Lne_Density.text()) +", ErrRangeMinus= "+ str(self.Lne_ErrRangeMinus.text()) +", ErrRangePlus= "+ str(self.Lne_ErrRangePlus.text()) +", PreClampOffset = "+ str(self.Lne_PreClampOffset.text()) +", TheoryWeiht = "+ str(self.Lne_TheoryWeiht.text()) +", LengthRangeMax = "+ str(self.Lne_LengthRangeMax.text()) +" ,WeightMax = "+ str(self.Lne_WeightMax.text()) +" WHERE FixLength = '" + str(changefixleng[0][1]) + "'"
                print(sql)
                cursor.execute(sql)
                conn.commit()

        except Exception as e:
            print(e)
        finally:
            self.close()


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
    try:
        # 日志
        log = Log.Logger('all.log')
        # 配置文件
        config_ini = Config.Config(path = r"E:\PycharmProjects\FixedLengthSystem",pathconfig ='config.ini')
        config_fur = Config.Config(path = r"E:\PycharmProjects\FixedLengthSystem",pathconfig ='FurNum.ini')
        # 连接本地数据库
        pool = PooledDB(pymysql, 1, host='localhost', user='root', passwd='123', db='steelfixlength', port=3306)  # 5为连接池里的最少连接数
        conn = pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
        cursor = conn.cursor()

    except Exception as e:
        messagebox.showinfo("连接问题", e)

    # cv2.EVENT_MOUSEMOVE
    window = MainWindow()
    # window.showFullScreen()    #全屏
    window.show()

    sys.exit(app.exec_())  # 0是正常退出
    cursor.close()
    conn.close()
    cap.release()
    cv2.destroyAllWindows()
