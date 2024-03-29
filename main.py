# coding=utf-8
# 标准类
import binascii
import datetime
import sys
import traceback
from tkinter import messagebox
import datetime
import time
from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json
import numpy as np
from PyQt5 import QtPrintSupport
import pandas as pd
import cv2
import numpy
import pymysql
import _thread
import threading
import socket
import binascii
from PyQt5.Qt import *
from PyQt5.QtGui import QIntValidator
from dbutils.pooled_db import PooledDB
import mvsdk
import math
from scipy import stats
from HslCommunication import SiemensS7Net
from HslCommunication import SiemensPLCS
from concurrent.futures import ThreadPoolExecutor
import SerialPortHelper
import Config
import logging
# import Casting_Region
# import requests, json

# 引用类

import Log
import SQLData_Synchronizer

try:
    import SQLlite
except Exception as e:
    print("数据库连接失败，请尝试启动数据库", e)

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
import UI_SetCalibrate
import Main_Data
import Frame_Cut_Temp

from UI_MainPage import *
from UI_SetTeam import *
import public_dict  # 引用公用数据类

# 画面类


'''
1.相机显示辨识度偏差较大
2.打印功能
3.连接PLC读写数据触发动作
4.测试现场实际对比长度，设置设定值

'''

# 调用公用数据
public = public_dict.public_dict


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)  # 调用父类QWidget中的init方法
        self.setupUi(self)

        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏窗口
        self.setFixedSize(1280, 960)

        self.Btn_Class.clicked.connect(self.slot_SetTeam)  # 按钮-设置班组
        self.Btn_dataManagement.clicked.connect(self.slot_ProductionData)  # 按钮-数据管理
        self.Btn_videoParameter.clicked.connect(self.slot_Camera)  # 按钮-视频参数调整
        self.Act_Exit.setShortcut(self.close())  # 菜单栏
        self.Act_FurNo.triggered.connect(self.slot_SetFurNo)
        self.Act_Exit.triggered.connect(self.close)  # 菜单栏
        self.Act_SetAlgorithm.triggered.connect(self.slot_SetAlgorithm_triggered)  # 菜单栏
        self.Act_SetSteelData.triggered.connect(self.slot_SetSteelData)  # 菜单栏 定尺管理
        self.Act_SetTeam.triggered.connect(self.slot_SetTeam)  # 设备班组
        self.Act_Calibrate.triggered.connect(self.slot_SetCalibrate)  # 设备班组
        self.Act_Help.triggered.connect(self.slot_Help)  # 帮助
        self.Act_SetSteelType.triggered.connect(self.slot_SetSteelType)  # 钢种管理
        self.Btn_Exit.clicked.connect(self.slot_close)  # 退出

        self.autoShow()  # 主页面刷新
        self.center()  # 窗口居中

        try:
            self.main_CameraInit()  # 启动工业摄像头
        except Exception as e:
            print("启动工业摄像头错误代码", e)
        finally:
            cv2.destroyAllWindows()

        config_ini.writeValue('init', 'smtp_vserver', 'sss')  # 测试  11810*160*160 预夹=500 定重目标=2333.0

        '''时间刷新'''
        self.timer = QTimer()  # 设定时间周期线程
        self.timer.timeout.connect(self.slot_timeOut)
        self.timer.setInterval(500)  # 设置定时周期，超出周期启动timeout函数
        self.timer.start()  # 启动

        self.Synchronizer_timer = QTimer()  # 设定时间周期线程
        self.Synchronizer_timer.timeout.connect(self.slot_Synchronizer_timer)
        self.Synchronizer_timer.setInterval(500000)  # 设置定时周期，超出周期启动timeout函数
        # self.Synchronizer_timer.start()  # 启动

        self.off_1f_timer = QTimer()  # 设定时间周期线程(切割点)
        self.off_1f_timer.timeout.connect(self.slot_off_1f_timer)
        self.off_1f_timer.setInterval(180000)  # 设置定时周期，超出周期启动timeout函数，3min
        # self.Synchronizer_timer.start()  # 启动

        self.off_2f_timer = QTimer()  # 设定时间周期线程(切割点)
        self.off_2f_timer.timeout.connect(self.slot_off_2f_timer)
        self.off_2f_timer.setInterval(180000)  # 设置定时周期，超出周期启动timeout函数，3min
        # self.Synchronizer_timer.start()  # 启动

        self.off_3f_timer = QTimer()  # 设定时间周期线程(切割点)
        self.off_3f_timer.timeout.connect(self.slot_off_3f_timer)
        self.off_3f_timer.setInterval(180000)  # 设置定时周期，超出周期启动timeout函数，3min
        # self.Synchronizer_timer.start()  # 启动

        self.off_4f_timer = QTimer()  # 设定时间周期线程(切割点)
        self.off_4f_timer.timeout.connect(self.slot_off_4f_timer)
        self.off_4f_timer.setInterval(180000)  # 设置定时周期，超出周期启动timeout函数，3min
        # self.Synchronizer_timer.start()  # 启动

    # 检测键盘回车按键
    def keyPressEvent(self, event):
        print("按下：" + str(event.key()))
        if (event.key() == Qt.Key_F1):
            print('F1')
            if public['selected_status_F1'] == False:
                public['selected_status_F1'] = True
                print('选定一流修改切割线')
            elif public['selected_status_F1'] == True:
                public['selected_status_F1'] = False
                print('取消一流修改切割线')

        if (event.key() == Qt.Key_F2):
            print('F2')
            if public['selected_status_F2'] == False:
                public['selected_status_F2'] = True
                print('选定二流修改切割线')
            elif public['selected_status_F2'] == True:
                public['selected_status_F2'] = False
                print('取消二流修改切割线')


        if (event.key() == Qt.Key_F3):
            print('F3')
            if public['selected_status_F3'] == False:
                public['selected_status_F3'] = True
                print('选定三流修改切割线')
            elif public['selected_status_F3'] == True:
                public['selected_status_F3'] = False
                print('取消三流修改切割线')

        if (event.key() == Qt.Key_F4):
            print('F4')
            if public['selected_status_F4'] == False:
                public['selected_status_F4'] = True
                print('选定四流修改切割线')
            elif public['selected_status_F4'] == True:
                public['selected_status_F4'] = False
                print('取消四流修改切割线')

        # Key_PageDown = 16777239
        # Key_PageUp = 16777238
        if (event.key() == Qt.Key_PageDown):
            print('左移动')
            if public['selected_status_F1'] == True:
                temp_setcutlimt_f1 = int(config_ini.readvalue('setcamre', 'setcutlimt_f1'))
                print('读取一流切割线坐标',temp_setcutlimt_f1)
                if temp_setcutlimt_f1 >= 5:
                    print('移动切割线')
                    temp_setcutlimt_f1 -= 1
                    config_ini.writeValue('setcamre', 'setcutlimt_f1', str(int(temp_setcutlimt_f1)))
                else:
                    QtWidgets.QMessageBox.question(self, "提示", "设置切割线过低",
                                                   QtWidgets.QMessageBox.Yes)
            if public['selected_status_F2'] == True:
                temp_setcutlimt_f2 = int(config_ini.readvalue('setcamre', 'setcutlimt_f2'))
                print('读取二流切割线坐标',temp_setcutlimt_f2)
                if temp_setcutlimt_f2 >= 5:
                    print('移动切割线')
                    temp_setcutlimt_f2 -= 1
                    config_ini.writeValue('setcamre', 'setcutlimt_f2', str(int(temp_setcutlimt_f2)))
                else:
                    QtWidgets.QMessageBox.question(self, "提示", "设置切割线过低",
                                                   QtWidgets.QMessageBox.Yes)
            if public['selected_status_F3'] == True:
                temp_setcutlimt_f3 = int(config_ini.readvalue('setcamre', 'setcutlimt_f3'))
                print('读取三流切割线坐标',temp_setcutlimt_f3)
                if temp_setcutlimt_f3 >= 5:
                    print('移动切割线')
                    temp_setcutlimt_f3 -= 1
                    config_ini.writeValue('setcamre', 'setcutlimt_f3', str(int(temp_setcutlimt_f3)))
                else:
                    QtWidgets.QMessageBox.question(self, "提示", "设置切割线过低",
                                                   QtWidgets.QMessageBox.Yes)
            if public['selected_status_F4'] == True:
                temp_setcutlimt_f4 = int(config_ini.readvalue('setcamre', 'setcutlimt_f4'))
                print('读取四流切割线坐标',temp_setcutlimt_f4)
                if temp_setcutlimt_f4 >= 5:
                    print('移动切割线')
                    temp_setcutlimt_f4 -= 1
                    config_ini.writeValue('setcamre', 'setcutlimt_f4', str(int(temp_setcutlimt_f4)))
                else:
                    QtWidgets.QMessageBox.question(self, "提示", "设置切割线过低",
                                                   QtWidgets.QMessageBox.Yes)

        if (event.key() == Qt.Key_PageUp):
            print('右移动')
            if public['selected_status_F1'] == True:
                temp_setcutlimt_f1 = int(config_ini.readvalue('setcamre', 'setcutlimt_f1'))
                print('读取一流切割线坐标',temp_setcutlimt_f1)
                if temp_setcutlimt_f1 <= 855:
                    print('移动切割线')
                    temp_setcutlimt_f1 += 1
                    config_ini.writeValue('setcamre', 'setcutlimt_f1', str(int(temp_setcutlimt_f1)))
                else:
                    QtWidgets.QMessageBox.question(self, "提示", "设置切割线过低",
                                                   QtWidgets.QMessageBox.Yes)
            if public['selected_status_F2'] == True:
                temp_setcutlimt_f2 = int(config_ini.readvalue('setcamre', 'setcutlimt_f2'))
                print('读取二流切割线坐标',temp_setcutlimt_f2)
                if temp_setcutlimt_f2 <= 855:
                    print('移动切割线')
                    temp_setcutlimt_f2 += 1
                    config_ini.writeValue('setcamre', 'setcutlimt_f2', str(int(temp_setcutlimt_f2)))
                else:
                    QtWidgets.QMessageBox.question(self, "提示", "设置切割线过低",
                                                   QtWidgets.QMessageBox.Yes)
            if public['selected_status_F3'] == True:
                temp_setcutlimt_f3 = int(config_ini.readvalue('setcamre', 'setcutlimt_f3'))
                print('读取三流切割线坐标',temp_setcutlimt_f3)
                if temp_setcutlimt_f3 <= 855:
                    print('移动切割线')
                    temp_setcutlimt_f3 += 1
                    config_ini.writeValue('setcamre', 'setcutlimt_f3', str(int(temp_setcutlimt_f3)))
                else:
                    QtWidgets.QMessageBox.question(self, "提示", "设置切割线过低",
                                                   QtWidgets.QMessageBox.Yes)
            if public['selected_status_F4'] == True:
                temp_setcutlimt_f4 = int(config_ini.readvalue('setcamre', 'setcutlimt_f4'))
                print('读取四流切割线坐标',temp_setcutlimt_f4)
                if temp_setcutlimt_f4 <= 855:
                    print('移动切割线')
                    temp_setcutlimt_f4 += 1
                    config_ini.writeValue('setcamre', 'setcutlimt_f4', str(int(temp_setcutlimt_f4)))
                else:
                    QtWidgets.QMessageBox.question(self, "提示", "设置切割线过低",
                                                   QtWidgets.QMessageBox.Yes)




        # # 举例
        # if (event.key() == Qt.Key_Escape):
        #     print('测试：ESC')
        # if (event.key() == Qt.Key_A):
        #     print('测试：A')
        # if (event.key() == Qt.Key_1):
        #     print('测试：1')
        # if (event.key() == Qt.Key_Enter):
        #     print('测试：Enter')
        # if (event.key() == Qt.Key_Space):
        #     print('测试：Space')

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("鼠标左键点击")
        elif event.button() == Qt.RightButton:
            print("鼠标右键点击")
        elif event.button() == Qt.MidButton:
            print("鼠标中键点击")


    # 复位一流PLC切割点
    def slot_off_1f_timer(self):
        # plc_1f.WriteBool("M50.0", False)
        public['action_cut_1f'] = False
        print('复位一流PLC切割点')
        self.off_1f_timer.stop()
        # public['1f_rset_count_end'] = True
        # time.sleep(1)
        # public['1f_rset_count_end'] = False

    # 复位二流PLC切割点
    def slot_off_2f_timer(self):
        # plc_2f.WriteBool("M50.0", False)
        public['action_cut_2f'] = False
        print('复位二流PLC切割点')
        self.off_2f_timer.stop()
        # public['2f_rset_count_end'] = True
        # time.sleep(1)
        # public['2f_rset_count_end'] = False

    # 复位三流PLC切割点
    def slot_off_3f_timer(self):
        # plc_3f.WriteBool("M50.0", False)
        public['action_cut_3f'] = False
        print('复位三流PLC切割点')
        self.off_3f_timer.stop()
        public['3f_rset_count_end'] = True
        time.sleep(1)
        public['3f_rset_count_end'] = False

    # 复位四流PLC切割点
    def slot_off_4f_timer(self):
        # plc_4f.WriteBool("M50.0", False)
        public['action_cut_4f'] = False
        print('复位四流PLC切割点')
        self.off_4f_timer.stop()
        public['4f_rset_count_end'] = True
        time.sleep(1)
        public['4f_rset_count_end'] = False

    # 鼠标位置坐标显示
    def mouseMoveEvent(self, event):
        self.Labtxt_coordinate_X.setText("X:" + str(int(event.x()) - 30))
        self.Labtxt_coordinate_Y.setText("Y:" + str(int(event.y()) - 157))

    '''工业相机开始'''

    def main_CameraInit(self):
        global hCamera, pFrameBuffer
        DevList = mvsdk.CameraEnumerateDevice()
        nDev = len(DevList)
        if nDev < 1:
            print("No camera was found!")
            QtWidgets.QMessageBox.question(self, "提示", "未发现相机",
                                           QtWidgets.QMessageBox.Yes)
            return

        DevInfo = DevList[0]
        # 打开相机
        hCamera = 0
        try:
            hCamera = mvsdk.CameraInit(DevInfo, -1, -1)
        except mvsdk.CameraException as e:
            print("CameraInit Failed({}): {}".format(e.error_code, e.message))
            return

        # 获取相机特性描述
        cap = mvsdk.CameraGetCapability(hCamera)

        # 判断是黑白相机还是彩色相机
        monoCamera = (cap.sIspCapacity.bMonoSensor != 0)

        # 黑白相机让ISP直接输出MONO数据，而不是扩展成R=G=B的24位灰度
        if monoCamera:
            mvsdk.CameraSetIspOutFormat(hCamera, mvsdk.CAMERA_MEDIA_TYPE_MONO8)

        # 相机模式切换成连续采集
        mvsdk.CameraSetTriggerMode(hCamera, 0)

        # 手动曝光，曝光时间30ms
        mvsdk.CameraSetAeState(hCamera, int(config_ini.readvalue('setcamre', 'camerasetaestate')))
        print(config_ini.readvalue('setcamre', 'camerasetaestate'))
        mvsdk.CameraSetExposureTime(hCamera, int(config_ini.readvalue('setcamre', 'camerasetexposuretime')) * 1000)

        # 让SDK内部取图线程开始工作
        mvsdk.CameraPlay(hCamera)

        # 计算RGB buffer所需的大小，这里直接按照相机的最大分辨率来分配
        FrameBufferSize = cap.sResolutionRange.iWidthMax * cap.sResolutionRange.iHeightMax * (1 if monoCamera else 3)

        # 分配RGB buffer，用来存放ISP输出的图像
        # 备注：从相机传输到PC端的是RAW数据，在PC端通过软件ISP转为RGB数据（如果是黑白相机就不需要转换格式，但是ISP还有其它处理，所以也需要分配这个buffer）
        pFrameBuffer = mvsdk.CameraAlignMalloc(FrameBufferSize, 16)

    def paintEvent(self, a0: QtGui.QPaintEvent):
        try:
            DevList = mvsdk.CameraEnumerateDevice()
            nDev = len(DevList)
            if nDev > 0:
                try:
                    pRawData, FrameHead = mvsdk.CameraGetImageBuffer(hCamera, 200)
                    mvsdk.CameraImageProcess(hCamera, pRawData, pFrameBuffer, FrameHead)
                    mvsdk.CameraReleaseImageBuffer(hCamera, pRawData)

                    # 此时图片已经存储在pFrameBuffer中，对于彩色相机pFrameBuffer=RGB数据，黑白相机pFrameBuffer=8位灰度数据
                    # 把pFrameBuffer转换成opencv的图像格式以进行后续算法处理
                    frame_data = (mvsdk.c_ubyte * FrameHead.uBytes).from_address(pFrameBuffer)
                    frame = np.frombuffer(frame_data, dtype=np.uint8)
                    self.frame = frame.reshape((FrameHead.iHeight, FrameHead.iWidth,
                                                1 if FrameHead.uiMediaType == mvsdk.CAMERA_MEDIA_TYPE_MONO8 else 3))
                except Exception as e:
                    print("相机错误代码：", e)
            else:
                # 照片查看
                self.labelCamera.resize(900, 480)  # 存放图片位置
                self.frame = cv2.imread(
                    "pictrue\\FT-G2F202-Snapshot-20210928072740-3204056805986.bmp")

            if int(config_ini.readvalue('setcamre', 'flip')) < 2:  # 判断标识是否翻转
                self.frame = cv2.flip(self.frame,
                                      int(config_ini.readvalue('setcamre', 'flip')))  # 图像翻转 0：水平翻转 1,2,3等 垂直翻转 -1-2 全翻转
            frame_cut = self.frameCut()  # 调用图片修改

            self.Qframe = QImage(frame_cut.data, frame_cut.shape[1], frame_cut.shape[0], frame_cut.shape[1] * 3,
                                 QImage.Format_RGB888)
            self.labelCamera.setPixmap(QPixmap.fromImage(self.Qframe))

            self.update()  # 更新绘制图像


        except mvsdk.CameraException as e:
            if e.error_code != mvsdk.CAMERA_STATUS_TIME_OUT:
                print("CameraGetImageBuffer failed({}): {}".format(e.error_code, e.message))

    def frameCut(self):
        try:
            # 相机拍摄图像分割
            config_ini.writeValue('setcamre', 'camre_x', str(self.frame.shape[1]))  # 将相机分辨率存入
            config_ini.writeValue('setcamre', 'camre_y', str(self.frame.shape[0]))  # 将相机分辨率存入
            frame_cut_x0 = config_ini.readvalue('setcamre', 'frame_cut_x0')  # 读取存入设定的裁剪坐标
            frame_cut_x1 = config_ini.readvalue('setcamre', 'frame_cut_x1')  # 读取存入设定的裁剪坐标
            frame_cut_y0 = config_ini.readvalue('setcamre', 'frame_cut_y0')
            frame_cut_y1 = config_ini.readvalue('setcamre', 'frame_cut_y1')

            cv2.rectangle(self.frame, (int(frame_cut_x0), int(frame_cut_y0)), (int(frame_cut_x1), int(frame_cut_y1)),
                          (255, 0, 0), 1)  # 画矩形

            # cv2.imshow("Original picture", self.frame)  # 展示原图
            # 分割后图像
            frame_cut = self.frame[int(frame_cut_y0):int(frame_cut_y1),
                        int(frame_cut_x0):int(frame_cut_x1)]  # 裁剪坐标为[y0:y1, x0:x1]

            frame_cut = cv2.resize(frame_cut, (
            int((config_ini.readvalue('setcamre', 'reframe_x'))), int((config_ini.readvalue('setcamre', 'reframe_y')))),
                                   interpolation=cv2.INTER_AREA)  # 重新定义显示尺寸
            frame_cut = cv2.cvtColor(frame_cut, cv2.COLOR_BGR2RGB)  # 重新定义显示通道

            # 1流实例化图像处理

            if str(config_ini.readvalue('setcamre', 'ceb_threshold_auto_1f')) == 'True':
                threshold_ratio_switch_F1 = 1
            elif str(config_ini.readvalue('setcamre', 'ceb_threshold_auto_1f')) == 'False':
                threshold_ratio_switch_F1 = 0


            frameCut_return_f1 = Frame_Cut_Temp.frameCut(
                frame_cut=frame_cut,
                cut_y0=float(config_ini.readvalue('setcamre', 'frame_cut_y0_f1')),
                cut_y1=float(config_ini.readvalue('setcamre', 'frame_cut_y1_f1')),
                cut_x0=float(config_ini.readvalue('setcamre', 'frame_cut_x0_f1')),
                cut_x1=float(config_ini.readvalue('setcamre', 'frame_cut_x1_f1')),
                fixlength=int(config_ini.readvalue('init', 'lab_1csetlength')),
                temp_Lne_Frame_cut_Y1=int(public['temp_Lne_Frame_cut_Y1_F1']),
                temp_Lne_Frame_cut_Y0=public['temp_Lne_Frame_cut_Y0_F1'],
                frame_cut_angle=config_ini.readvalue('setcamre', 'frame_cut_f1_angle'),
                setcutlimt=config_ini.readvalue('setcamre', 'setcutlimt_f1'),
                threshold=int(config_ini.readvalue('setcamre', 'threshold_f1')),
                Start_Cut_state=public['Start_Cut_state_F1'],
                pullspeed=public['plc_1f_pullspeed'],
                threshold_ratio=0.4,
                threshold_ratio_switch=threshold_ratio_switch_F1,
                x_9=int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_11'))),
                x_11=int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12'))),
                x_13=int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_13'))),
                setcutlimt_selected_status = public['selected_status_F1'],
                # fixlength=int(window.Lab_1cSetLength.text())
            )


            window.Lab_1cState.setText(frameCut_return_f1['Lab_fcState'])
            # 一直触发切割信号，一直到图像中没有符合要求的图像
            public['Start_Cut_state_F1'] = frameCut_return_f1['Start_Cut_state']
            window.Lab_1cCompensate.setText(str(round(float(frameCut_return_f1['adjustment']), 2)))
            # print('图像返回数据',frameCut_return_f1)
            # 只有开始第一周期执行

            def slot_CutToSQL_1f():
                MainWindow.slot_CutToSQL(self,
                                         FurNum=str((config_fur.readvalue('FurListData1', 'lne_setfurno'))),
                                         FlowNum="1",  # 流号
                                         FixLength=str(window.Lab_1cSetLength.text()),  # 定尺长度
                                         Team=str(window.Btn_Class.text()),  # 班组
                                         SteelType=str(window.Lab_1cSteels.text()),  # 钢种
                                         RealWeight=str(public['sql_weighting_F1']),  # 真实重量
                                         Weighing=public['weighting_F1_state'],  # 是否称重
                                         SetWeight=str(window.Btn_1aSetWeight.text()),  # 设定重量
                                         IDtime=frame_cut_f1,  # 时间
                                         adjustment=str(public['temp_Lab_1cCompensate']),  # 补偿值
                                         density=str(SQLlite.SQL_readSteeldensity(self.Lab_1cSteels.text())),
                                         # 读取数据库里的钢种密度
                                         theoryWeight=str(window.Lab_1bWeight.text())  # 理论重量
                                         )

                # 判断称重是否在合格范围内，如超出范围，自动调整
                if 'True' == config_ini.readvalue('setcamre', 'Ceb_Correct_auto_f1'):
                    # self.Ceb_Threshold_auto_f1.stateChanged.connect(self.slot_Change_Threshold_auto_1f)
                    public['auto_adjustment_switch_F1'] = True
                else:
                    public['auto_adjustment_switch_F1'] = False


                # 实际重量 - 设定重量 > 最大范围值  重量超出
                if public['auto_adjustment_switch_F1'] == True and float(public['sql_weighting_F1']) - float(config_ini.readvalue('init', 'Btn_1aSetWeight')) > float(config_ini.readvalue('init', 'lab_1errrangeplus')) and public['sql_weighting_F1'] != 0 and public['weighting_F1_state'] != '否' and float(public['sql_weighting_F1']) >= float(1800) and float(public['sql_weighting_F1']) <= float(2500):
                    # 每个格为5公斤
                    geshu_weight = 5
                    # 重量转换格数

                    weight_turn_geshu_1f = (float(public['sql_weighting_F1']) - float(config_ini.readvalue('init', 'Btn_1aSetWeight'))) / geshu_weight
                    print('1流转换的格数', weight_turn_geshu_1f)
                    if abs(weight_turn_geshu_1f) <= 50:
                        if int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_11'))) > int(config_ini.readvalue('setcamre', 'setcutlimt_f1')) >= int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12'))) :    #11米到12米转换x坐标
                            turned_x = int(config_ini.readvalue('setcamre', 'setcutlimt_f1')) + ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12')))) / frameCut_return_f1['num']) * weight_turn_geshu_1f
                            aaaa = 1
                        elif int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12'))) > int(config_ini.readvalue('setcamre', 'setcutlimt_f1')) >= int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_13'))) and (weight_turn_geshu_1f - (((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12'))) - int(config_ini.readvalue('setcamre', 'setcutlimt_f1')))) / ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_13')))) / frameCut_return_f1['num']))) * ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12')))) / frameCut_return_f1['num']) > 0 : #(50 - frameCut_return_f2['setfixlength_geshu_x']) < weight_turn_geshu_2f :    #12米到13米转换x坐标情况1
                            turned_x = int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12'))) + ((weight_turn_geshu_1f - (((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12'))) - int(config_ini.readvalue('setcamre', 'setcutlimt_f1')))) / ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_13')))) / frameCut_return_f1['num']))) * ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12')))) / frameCut_return_f1['num'])) #(weight_turn_geshu_2f - 50 + (frameCut_return_f1['setfixlength_geshu_x'])) * ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12')))) / frameCut_return_f1['num'])
                            aaaa = 2
                        elif int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12'))) > int(config_ini.readvalue('setcamre', 'setcutlimt_f1')) >= int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_13'))) and (weight_turn_geshu_1f - (((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12'))) - int(config_ini.readvalue('setcamre', 'setcutlimt_f1')))) / ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_13')))) / frameCut_return_f1['num']))) * ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12')))) / frameCut_return_f1['num']) < 0 :#(50 - frameCut_return_f2['setfixlength_geshu_x']) >= weight_turn_geshu_2f :  #12米到13米转换x坐标情况2
                            turned_x = int(config_ini.readvalue('setcamre', 'setcutlimt_f1')) + ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_13')))) / frameCut_return_f1['num']) * weight_turn_geshu_1f
                            aaaa = 3
                        else:
                            turned_x = config_ini.readvalue('setcamre', 'setcutlimt_f1')
                            aaaa = 4
                        if 0 < int(turned_x):
                            config_ini.writeValue('setcamre', 'setcutlimt_f1', str(int(turned_x)))
                        print('一流偏重', weight_turn_geshu_1f, aaaa, turned_x, config_ini.readvalue('setcamre', 'setcutlimt_f1'))
                        with open('2233.txt', 'a+') as f:
                            f.writelines(
                                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ':' + '一流偏重,调整格式' + str(weight_turn_geshu_1f) + str(aaaa) + '调整位置' + str(turned_x) +'读取位置' +str(config_ini.readvalue('setcamre', 'setcutlimt_f1'))+ '\n')


                    # 写入切割设定X坐标

                    # 判断调整后是否 跨越12米线，跨越时，须调整X坐标比例，以及超出边界时，注意点。

                # 设定重量 - 实际重量 > 最小范围值  重量不足
                elif public['auto_adjustment_switch_F1'] == True and float(config_ini.readvalue('init', 'Btn_1aSetWeight')) - float(public['sql_weighting_F1']) > float(config_ini.readvalue('init', 'lab_1errrangeminus')) and public['sql_weighting_F1'] != 0 and public['weighting_F1_state'] != '否' and float(public['sql_weighting_F1']) >= float(1800) and float(public['sql_weighting_F1']) <= float(2500):
                    # 每个格为5公斤
                    geshu_weight = 5
                    # 重量转换格数
                    weight_turn_geshu_1f = (float(config_ini.readvalue('init', 'Btn_1aSetWeight')) - (float(public['sql_weighting_F1']))) / geshu_weight
                    print('1流调整格数', weight_turn_geshu_1f)
                    if abs(weight_turn_geshu_1f) <= 50:
                        if int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12'))) > int(config_ini.readvalue('setcamre', 'setcutlimt_f1')) >= int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_13'))) :    #12米到13米转换x坐标
                            turned_x = int(config_ini.readvalue('setcamre', 'setcutlimt_f1')) - ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_13')))) / frameCut_return_f1['num']) * weight_turn_geshu_1f
                            bbbb = 5
                        elif int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_11'))) > int(config_ini.readvalue('setcamre', 'setcutlimt_f1')) >= int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12'))) and (weight_turn_geshu_1f - (((int(config_ini.readvalue('setcamre', 'setcutlimt_f1'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12')))) / ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12')))) / frameCut_return_f1['num']))) * ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_13')))) / frameCut_return_f1['num']) > 0 :
                            turned_x = int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12'))) - ((weight_turn_geshu_1f - (((int(config_ini.readvalue('setcamre', 'setcutlimt_f1'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12')))) / ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12')))) / frameCut_return_f1['num']))) * ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_13')))) / frameCut_return_f1['num']))
                            bbbb = 6
                        elif int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_11'))) > int(config_ini.readvalue('setcamre', 'setcutlimt_f1')) >= int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12'))) and (weight_turn_geshu_1f - (((int(config_ini.readvalue('setcamre', 'setcutlimt_f1'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12')))) / ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12')))) / frameCut_return_f1['num']))) * ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_13')))) / frameCut_return_f1['num']) < 0 : #(frameCut_return_f1['setfixlength_geshu_x'] - 50) >= weight_turn_geshu_2f :
                            turned_x = int(config_ini.readvalue('setcamre', 'setcutlimt_f1')) - ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_13')))) / frameCut_return_f1['num']) * weight_turn_geshu_1f
                            bbbb = 7
                        else:
                            turned_x = config_ini.readvalue('setcamre', 'setcutlimt_f1')
                            bbbb = 8
                        if 0 < int(turned_x):
                            config_ini.writeValue('setcamre', 'setcutlimt_f1', str(int(turned_x)))
                        print('一流偏轻', weight_turn_geshu_1f, bbbb, turned_x, config_ini.readvalue('setcamre', 'setcutlimt_f1'))
                    with open('2233.txt', 'a+') as f:
                        f.writelines(
                            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ':' + '一流偏轻,调整格式' + str(
                                weight_turn_geshu_1f) + str(bbbb) + '调整位置' + str(turned_x) + '读取位置' + str(
                                config_ini.readvalue('setcamre', 'setcutlimt_f1')) + '\n')

                else:
                    pass

                # 清楚缓冲重量数
                public['Weight_1f_list'] = []   # 清理称重重量缓冲数据
                public['sql_weighting_F1'] = 0  # 写入数据后的重量清零，如还在称重中，等称重为0，并且完成称重标记清零
                public['weighting_F1_state'] = '否'  # 写入数据后的修改称重记录，如还在称重中，等称重为0，并且完成称重标记修改
                public['send_cut_1f_stat'] = False  # 从 切割信号 至 三分钟写入数据库 之间的标志位

            frameCut_Timer_f1_threading_1 = threading.Timer(180, slot_CutToSQL_1f)
            # frameCut_Timer_f2_threading_1 = threading.Timer(1, slot_CutToSQL_2f)
            # 触发切割信号（一个周期）
            # print(frameCut_return_f1['Start_Cut_state_F'])
            if frameCut_return_f1['Start_Cut_state_F'] == True and float(public['plc_1f_pullspeed']) >= 1.0 and float(public['temp_Lab_1bTemperature']) >= 550.0 and public['send_cut_1f_stat'] == False:
                print('1流切割')
                print('1流PLC连接状态：', plc_1f.ConnectServer().IsSuccess)
                # print('切割状态',frameCut_return_f1['Start_Cut_state_F'])
                # plc_1f.WriteBool("M50.0", True])  # 写入PLC切割变量点
                public['action_cut_1f'] = True
                self.off_1f_timer.start()  # 启动
                # frameCut_Timer_f2_threading_1.cancel() # 判断是否为激活状态，激活状态时，并直接执行SQL(重新写SQL写入)，取消线程或结束线程，，进入下个计时
                # public['weighting_F2_state'] = '否'
                # public['sql_weighting_F2'] = 0
                # 增加流次计数量
                config_ini.writeValue('init', 'Lab_1cCount',
                                      str(int(config_ini.readvalue('init', 'Lab_1cCount')) + 1))
                window.Lab_1cCount.setText(str(config_ini.readvalue('init', 'Lab_1cCount')))  # 1流记数

                config_ini.writeValue('init', 'Lab_talRoot',
                                      str(int(config_ini.readvalue('init', 'Lab_talRoot')) + 1))
                window.Lab_talRoot.setText((config_ini.readvalue('init', 'Lab_talRoot')))  # 总记数
                frame_cut_f1 = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
                public['temp_Lab_1cCompensate'] = frameCut_return_f1['adjustment']
                public['send_cut_1f_stat'] = True

                # 延时3分钟，触发写入SQL函数
                frameCut_Timer_f1_threading_1.start()

            # 判断称重状态
            if int(public['temp_Lab_1bWeight']) >= 2000:
                public['weighting_F1_state'] = '是'  # 写入数据库的
                public['Weight_1f_list_stat'] = True  # 正在称重及称过重的标记
                public['Weight_1f_list'].append(int(public['temp_Lab_1bWeight']))
                public['sql_weighting_F1'] = int(stats.mode(public['Weight_1f_list'])[0][0])
                print('1流正在有重量', int(public['temp_Lab_1bWeight']), public['sql_weighting_F1'])
                # print('2流称重数组', public['Weight_2f_list'])
                # 传给PLC  给M区变量1个值来判断切割

            # 重量称重完成判断：当重量为0，并且有称重过后的标记存在，即认为称重完成。
            elif int(public['temp_Lab_1bWeight']) == 0 and public['Weight_1f_list_stat'] == True:
                public['Weight_1f_list'] = []   # 清空缓冲的称重数组
                public['Weight_1f_list_stat'] = False  # 消除正在称重及称过重的标记

                # 1.当三分钟，写入完数据库后，未称重完成，待重量称重完成，即把是否称重改为否
                # 2.当三分钟前完成称重，让写入数据库函数保存，清处把是否称重改为否
                if public['send_cut_1f_stat'] == False:
                    public['weighting_F1_state'] = '否'

            else:
                # public['temp_Lab_2bWeight'] = 0
                pass

            # 2流实例化图像处理

            if str(config_ini.readvalue('setcamre', 'ceb_threshold_auto_2f')) == 'True':
                threshold_ratio_switch_F2 = 1
            elif str(config_ini.readvalue('setcamre', 'ceb_threshold_auto_2f')) == 'False':
                threshold_ratio_switch_F2 = 0

            frameCut_return_f2 = Frame_Cut_Temp.frameCut(
                frame_cut=frame_cut,
                cut_y0=float(config_ini.readvalue('setcamre', 'frame_cut_y0_f2')),
                cut_y1=float(config_ini.readvalue('setcamre', 'frame_cut_y1_f2')),
                cut_x0=float(config_ini.readvalue('setcamre', 'frame_cut_x0_f2')),
                cut_x1=float(config_ini.readvalue('setcamre', 'frame_cut_x1_f2')),
                fixlength=int(config_ini.readvalue('init', 'lab_2csetlength')),
                temp_Lne_Frame_cut_Y1=int(public['temp_Lne_Frame_cut_Y1_F2']),
                temp_Lne_Frame_cut_Y0=public['temp_Lne_Frame_cut_Y0_F2'],
                frame_cut_angle=config_ini.readvalue('setcamre', 'frame_cut_f2_angle'),
                setcutlimt=config_ini.readvalue('setcamre', 'setcutlimt_f2'),
                threshold=int(config_ini.readvalue('setcamre', 'threshold_f2')),
                Start_Cut_state=public['Start_Cut_state_F2'],
                pullspeed=public['plc_2f_pullspeed'],
                threshold_ratio=0.4,
                threshold_ratio_switch=threshold_ratio_switch_F2,
                x_9=int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_11'))),
                x_11=int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12'))),
                x_13=int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_13'))),
                setcutlimt_selected_status=public['selected_status_F2'],
            )

            window.Lab_2cState.setText(frameCut_return_f2['Lab_fcState'])
            # 一直触发切割信号，一直到图像中没有符合要求的图像
            public['Start_Cut_state_F2'] = frameCut_return_f2['Start_Cut_state']
            window.Lab_2cCompensate.setText(str(round(float(frameCut_return_f2['adjustment']), 2)))

            # print(frameCut_return_f1)
            # 只有开始第一周期执行
            def slot_CutToSQL_2f():
                MainWindow.slot_CutToSQL(self,
                                         FurNum=str((config_fur.readvalue('FurListData2', 'lne_setfurno'))),
                                         FlowNum="2",  # 流号
                                         FixLength=str(window.Lab_2cSetLength.text()),  # 定尺长度
                                         Team=str(window.Btn_Class.text()),  # 班组
                                         SteelType=str(window.Lab_2cSteels.text()),  # 钢种
                                         RealWeight=str(public['sql_weighting_F2']),  # 真实重量
                                         Weighing=public['weighting_F2_state'],  # 是否称重
                                         SetWeight=str(window.Btn_1aSetWeight.text()),  # 设定重量
                                         IDtime=frame_cut_f2,  # 时间
                                         adjustment=str(public['temp_Lab_2cCompensate']),  # 补偿值
                                         density=str(SQLlite.SQL_readSteeldensity(self.Lab_2cSteels.text())),
                                         # 读取数据库里的钢种密度
                                         theoryWeight=str(window.Lab_2bWeight.text())  # 理论重量
                                         )


                # 判断称重是否在合格范围内，如超出范围，自动调整
                if 'True' == config_ini.readvalue('setcamre', 'Ceb_Correct_auto_f2'):
                    # self.Ceb_Threshold_auto_f1.stateChanged.connect(self.slot_Change_Threshold_auto_1f)
                    public['auto_adjustment_switch_F2'] = True
                else:
                    public['auto_adjustment_switch_F2'] = False

                # public['sql_weighting_F2'] = 2420
                # public['weighting_F2_state'] = '是'

                # 实际重量 - 设定重量 > 最大范围值  重量超出
                if public['auto_adjustment_switch_F2'] == True and float(public['sql_weighting_F2']) - float(config_ini.readvalue('init', 'Btn_2aSetWeight')) > float(config_ini.readvalue('init', 'lab_2errrangeplus')) and public['sql_weighting_F2'] != 0 and public['weighting_F2_state'] != '否' and float(public['sql_weighting_F2']) >= float(1800) and float(public['sql_weighting_F2']) <= float(2500):
                    # 每个格为5公斤
                    geshu_weight = 5
                    # 重量转换格数

                    weight_turn_geshu_2f = (float(public['sql_weighting_F2']) - float(config_ini.readvalue('init', 'Btn_2aSetWeight'))) / geshu_weight
                    print('2流转换的格数', weight_turn_geshu_2f)
                    if abs(weight_turn_geshu_2f) <= 50:
                        if int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_11'))) > int(config_ini.readvalue('setcamre', 'setcutlimt_f2')) >= int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12'))) :    #11米到12米转换x坐标
                            turned_x = int(config_ini.readvalue('setcamre', 'setcutlimt_f2')) + ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12')))) / frameCut_return_f2['num']) * weight_turn_geshu_2f
                            aaaa = 1
                        elif int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12'))) > int(config_ini.readvalue('setcamre', 'setcutlimt_f2')) >= int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_13'))) and (weight_turn_geshu_2f - (((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12'))) - int(config_ini.readvalue('setcamre', 'setcutlimt_f2')))) / ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_13')))) / frameCut_return_f2['num']))) * ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12')))) / frameCut_return_f2['num']) > 0 : #(50 - frameCut_return_f2['setfixlength_geshu_x']) < weight_turn_geshu_2f :    #12米到13米转换x坐标情况1
                            turned_x = int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12'))) + ((weight_turn_geshu_2f - (((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12'))) - int(config_ini.readvalue('setcamre', 'setcutlimt_f2')))) / ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_13')))) / frameCut_return_f2['num']))) * ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12')))) / frameCut_return_f2['num'])) #(weight_turn_geshu_2f - 50 + (frameCut_return_f1['setfixlength_geshu_x'])) * ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12')))) / frameCut_return_f1['num'])
                            aaaa = 2
                        elif int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12'))) > int(config_ini.readvalue('setcamre', 'setcutlimt_f2')) >= int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_13'))) and (weight_turn_geshu_2f - (((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12'))) - int(config_ini.readvalue('setcamre', 'setcutlimt_f2')))) / ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_13')))) / frameCut_return_f2['num']))) * ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12')))) / frameCut_return_f2['num']) < 0 :#(50 - frameCut_return_f2['setfixlength_geshu_x']) >= weight_turn_geshu_2f :  #12米到13米转换x坐标情况2
                            turned_x = int(config_ini.readvalue('setcamre', 'setcutlimt_f2')) + ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_13')))) / frameCut_return_f2['num']) * weight_turn_geshu_2f
                            aaaa = 3
                        else:
                            turned_x = config_ini.readvalue('setcamre', 'setcutlimt_f2')
                            aaaa = 4
                        if 0 < int(turned_x):
                            config_ini.writeValue('setcamre', 'setcutlimt_f2', str(int(turned_x)))
                        print('二流偏重', weight_turn_geshu_2f, aaaa, turned_x, config_ini.readvalue('setcamre', 'setcutlimt_f2'))
                        with open('2233.txt', 'a+') as f:
                            f.writelines(
                                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ':' + '二流偏重,调整格式' + str(weight_turn_geshu_2f) + str(aaaa) + '调整位置' + str(turned_x) +'读取位置' +str(config_ini.readvalue('setcamre', 'setcutlimt_f2'))+ '\n')


                    # 写入切割设定X坐标

                    # 判断调整后是否 跨越12米线，跨越时，须调整X坐标比例，以及超出边界时，注意点。

                # 设定重量 - 实际重量 > 最小范围值  重量不足
                elif public['auto_adjustment_switch_F2'] == True and float(config_ini.readvalue('init', 'Btn_2aSetWeight')) - float(public['sql_weighting_F2']) > float(config_ini.readvalue('init', 'lab_2errrangeminus')) and public['sql_weighting_F2'] != 0 and public['weighting_F2_state'] != '否' and float(public['sql_weighting_F2']) >= float(1800) and float(public['sql_weighting_F2']) <= float(2500):
                    # 每个格为5公斤
                    geshu_weight = 5
                    # 重量转换格数
                    weight_turn_geshu_2f = (float(config_ini.readvalue('init', 'Btn_2aSetWeight')) - (float(public['sql_weighting_F2']))) / geshu_weight
                    print('2流调整格数', weight_turn_geshu_2f)
                    if abs(weight_turn_geshu_2f) <= 50:
                        if int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12'))) > int(config_ini.readvalue('setcamre', 'setcutlimt_f2')) >= int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_13'))) :    #12米到13米转换x坐标
                            turned_x = int(config_ini.readvalue('setcamre', 'setcutlimt_f2')) - ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_13')))) / frameCut_return_f2['num']) * weight_turn_geshu_2f
                            bbbb = 5
                        elif int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_11'))) > int(config_ini.readvalue('setcamre', 'setcutlimt_f2')) >= int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12'))) and (weight_turn_geshu_2f - (((int(config_ini.readvalue('setcamre', 'setcutlimt_f2'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12')))) / ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12')))) / frameCut_return_f2['num']))) * ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_13')))) / frameCut_return_f2['num']) > 0 :
                            turned_x = int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12'))) - ((weight_turn_geshu_2f - (((int(config_ini.readvalue('setcamre', 'setcutlimt_f2'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12')))) / ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12')))) / frameCut_return_f2['num']))) * ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_13')))) / frameCut_return_f2['num']))
                            bbbb = 6
                        elif int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_11'))) > int(config_ini.readvalue('setcamre', 'setcutlimt_f2')) >= int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12'))) and (weight_turn_geshu_2f - (((int(config_ini.readvalue('setcamre', 'setcutlimt_f2'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12')))) / ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12')))) / frameCut_return_f2['num']))) * ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_13')))) / frameCut_return_f2['num']) < 0 : #(frameCut_return_f1['setfixlength_geshu_x'] - 50) >= weight_turn_geshu_2f :
                            turned_x = int(config_ini.readvalue('setcamre', 'setcutlimt_f2')) - ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f2_13')))) / frameCut_return_f2['num']) * weight_turn_geshu_2f
                            bbbb = 7
                        else:
                            turned_x = config_ini.readvalue('setcamre', 'setcutlimt_f2')
                            bbbb = 8
                        if 0 < int(turned_x):
                            config_ini.writeValue('setcamre', 'setcutlimt_f2', str(int(turned_x)))
                        print('二流偏轻', weight_turn_geshu_2f, bbbb, turned_x, config_ini.readvalue('setcamre', 'setcutlimt_f2'))
                    with open('2233.txt', 'a+') as f:
                        f.writelines(
                            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ':' + '二流偏轻,调整格式' + str(
                                weight_turn_geshu_2f) + str(bbbb) + '调整位置' + str(turned_x) + '读取位置' + str(
                                config_ini.readvalue('setcamre', 'setcutlimt_f2')) + '\n')

                else:
                    pass

                # 清楚缓冲重量数
                public['Weight_2f_list'] = []   # 清理称重重量缓冲数据
                public['sql_weighting_F2'] = 0  # 写入数据后的重量清零，如还在称重中，等称重为0，并且完成称重标记清零
                public['weighting_F2_state'] = '否'  # 写入数据后的修改称重记录，如还在称重中，等称重为0，并且完成称重标记修改
                public['send_cut_2f_stat'] = False  # 从 切割信号 至 三分钟写入数据库 之间的标志位

            frameCut_Timer_f2_threading_1 = threading.Timer(180, slot_CutToSQL_2f)
            # frameCut_Timer_f2_threading_1 = threading.Timer(1, slot_CutToSQL_2f)
            # 触发切割信号（一个周期）
            # print(frameCut_return_f1['Start_Cut_state_F'])
            if frameCut_return_f2['Start_Cut_state_F'] == True and float(public['plc_2f_pullspeed']) >= 1.0 and float(public['temp_Lab_2bTemperature']) >= 550.0 and public['send_cut_2f_stat'] == False:
                print('2流切割')
                print('2流PLC连接状态：', plc_2f.ConnectServer().IsSuccess)
                # print('切割状态',frameCut_return_f1['Start_Cut_state_F'])
                # plc_1f.WriteBool("M50.0", True])  # 写入PLC切割变量点
                public['action_cut_2f'] = True
                self.off_2f_timer.start()  # 启动
                # frameCut_Timer_f2_threading_1.cancel() # 判断是否为激活状态，激活状态时，并直接执行SQL(重新写SQL写入)，取消线程或结束线程，，进入下个计时
                # public['weighting_F2_state'] = '否'
                # public['sql_weighting_F2'] = 0
                # 增加流次计数量
                config_ini.writeValue('init', 'Lab_2cCount',
                                      str(int(config_ini.readvalue('init', 'Lab_2cCount')) + 1))
                window.Lab_1cCount.setText(str(config_ini.readvalue('init', 'Lab_2cCount')))  # 1流记数

                config_ini.writeValue('init', 'Lab_talRoot',
                                      str(int(config_ini.readvalue('init', 'Lab_talRoot')) + 1))
                window.Lab_talRoot.setText((config_ini.readvalue('init', 'Lab_talRoot')))  # 总记数
                frame_cut_f2 = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
                public['temp_Lab_2cCompensate'] = frameCut_return_f2['adjustment']
                public['send_cut_2f_stat'] = True

                # 延时3分钟，触发写入SQL函数
                frameCut_Timer_f2_threading_1.start()

            # 判断称重状态
            if int(public['temp_Lab_2bWeight']) >= 2000:
                public['weighting_F2_state'] = '是'  # 写入数据库的
                public['Weight_2f_list_stat'] = True  # 正在称重及称过重的标记
                public['Weight_2f_list'].append(int(public['temp_Lab_2bWeight']))
                public['sql_weighting_F2'] = int(stats.mode(public['Weight_2f_list'])[0][0])
                print('2流正在有重量', int(public['temp_Lab_2bWeight']), public['sql_weighting_F2'])
                # print('2流称重数组', public['Weight_2f_list'])
                # 传给PLC  给M区变量1个值来判断切割

            # 重量称重完成判断：当重量为0，并且有称重过后的标记存在，即认为称重完成。
            elif int(public['temp_Lab_2bWeight']) == 0 and public['Weight_2f_list_stat'] == True:
                public['Weight_2f_list'] = []   # 清空缓冲的称重数组
                public['Weight_2f_list_stat'] = False  # 消除正在称重及称过重的标记

                # 1.当三分钟，写入完数据库后，未称重完成，待重量称重完成，即把是否称重改为否
                # 2.当三分钟前完成称重，让写入数据库函数保存，清处把是否称重改为否
                if public['send_cut_2f_stat'] == False:
                    public['weighting_F2_state'] = '否'

            else:
                # public['temp_Lab_2bWeight'] = 0
                pass
            # with open('2233.txt', 'a+') as f:
            #     f.writelines(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+ ':' + '2流重量' + str(public['temp_Lab_2bWeight']) +  str(public['sql_weighting_F2']) + '\n')



            # 3流实例化图像处理
            if str(config_ini.readvalue('setcamre', 'ceb_threshold_auto_3f')) == 'True':
                threshold_ratio_switch_F3 = 1
            elif str(config_ini.readvalue('setcamre', 'ceb_threshold_auto_3f')) == 'False':
                threshold_ratio_switch_F3 = 0

            frameCut_return_f3 = Frame_Cut_Temp.frameCut(
                frame_cut=frame_cut,
                cut_y0=float(config_ini.readvalue('setcamre', 'frame_cut_y0_f3')),
                cut_y1=float(config_ini.readvalue('setcamre', 'frame_cut_y1_f3')),
                cut_x0=float(config_ini.readvalue('setcamre', 'frame_cut_x0_f3')),
                cut_x1=float(config_ini.readvalue('setcamre', 'frame_cut_x1_f3')),
                fixlength=int(config_ini.readvalue('init', 'lab_3csetlength')),
                temp_Lne_Frame_cut_Y1=int(public['temp_Lne_Frame_cut_Y1_F3']),
                temp_Lne_Frame_cut_Y0=public['temp_Lne_Frame_cut_Y0_F3'],
                frame_cut_angle=config_ini.readvalue('setcamre', 'frame_cut_f3_angle'),
                setcutlimt=config_ini.readvalue('setcamre', 'setcutlimt_f3'),
                threshold=int(config_ini.readvalue('setcamre', 'threshold_f3')),
                Start_Cut_state=public['Start_Cut_state_F3'],
                pullspeed=public['plc_3f_pullspeed'],
                threshold_ratio=0.4,
                threshold_ratio_switch=threshold_ratio_switch_F3,
                x_9=int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_11'))),
                x_11=int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12'))),
                x_13=int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_13'))),
                setcutlimt_selected_status=public['selected_status_F3'],
            )

            window.Lab_3cState.setText(frameCut_return_f3['Lab_fcState'])
            # 一直触发切割信号，一直到图像中没有符合要求的图像
            public['Start_Cut_state_F3'] = frameCut_return_f3['Start_Cut_state']
            window.Lab_3cCompensate.setText(str(round(float(frameCut_return_f3['adjustment']), 2)))

            # 只有开始第一周期执行
            def slot_CutToSQL_3f():
                MainWindow.slot_CutToSQL(self,
                                         FurNum=str((config_fur.readvalue('FurListData2', 'lne_setfurno'))),
                                         FlowNum="3",  # 流号
                                         FixLength=str(window.Lab_3cSetLength.text()),  # 定尺长度
                                         Team=str(window.Btn_Class.text()),  # 班组
                                         SteelType=str(window.Lab_3cSteels.text()),  # 钢种
                                         RealWeight=str(public['sql_weighting_F3']),  # 真实重量
                                         Weighing=public['weighting_F3_state'],  # 是否称重
                                         SetWeight=str(window.Btn_3aSetWeight.text()),  # 设定重量
                                         IDtime=frame_cut_f3,  # 时间
                                         adjustment=str(public['temp_Lab_3cCompensate']),  # 补偿值
                                         density=str(SQLlite.SQL_readSteeldensity(self.Lab_3cSteels.text())),
                                         # 读取数据库里的钢种密度
                                         theoryWeight=str(window.Lab_3bWeight.text())  # 理论重量
                                         )

                # 判断称重是否在合格范围内，如超出范围，自动调整
                if 'True' == config_ini.readvalue('setcamre', 'Ceb_Correct_auto_f3'):
                    # self.Ceb_Threshold_auto_f1.stateChanged.connect(self.slot_Change_Threshold_auto_1f)
                    public['auto_adjustment_switch_F3'] = True
                else:
                    public['auto_adjustment_switch_F3'] = False
                # public['sql_weighting_F3'] = 2355
                # public['weighting_F3_state'] = '是'
                # 实际重量 - 设定重量 > 最大范围值  重量超出
                if public['auto_adjustment_switch_F3'] == True and float(public['sql_weighting_F3']) - float(config_ini.readvalue('init', 'Btn_3aSetWeight')) > float(config_ini.readvalue('init', 'lab_3errrangeplus')) and public['sql_weighting_F3'] != 0 and public['weighting_F3_state'] != '否' and float(public['sql_weighting_F3']) >= float(1800) and float(public['sql_weighting_F3']) <= float(2500):
                    # 每个格为5公斤
                    geshu_weight = 5
                    # 重量转换格数
                    weight_turn_geshu_3f = (float(public['sql_weighting_F3']) - float(config_ini.readvalue('init', 'Btn_3aSetWeight'))) / geshu_weight
                    print('转换的格数',weight_turn_geshu_3f)
                    if abs(weight_turn_geshu_3f) <= 50:
                        if int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_11'))) > int(config_ini.readvalue('setcamre', 'setcutlimt_f3')) >= int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12'))) :    #11米到12米转换x坐标
                            turned_x = int(config_ini.readvalue('setcamre', 'setcutlimt_f3')) + ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12')))) / frameCut_return_f3['num']) * weight_turn_geshu_3f
                            aaaa = 1
                        elif int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12'))) > int(config_ini.readvalue('setcamre', 'setcutlimt_f3')) >= int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_13'))) and (weight_turn_geshu_3f - (((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12'))) - int(config_ini.readvalue('setcamre', 'setcutlimt_f3')))) / ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_13')))) / frameCut_return_f3['num']))) * ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12')))) / frameCut_return_f3['num']) > 0 : #(50 - frameCut_return_f2['setfixlength_geshu_x']) < weight_turn_geshu_2f :    #12米到13米转换x坐标情况1
                            turned_x = int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12'))) + ((weight_turn_geshu_3f - (((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12'))) - int(config_ini.readvalue('setcamre', 'setcutlimt_f3')))) / ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_13')))) / frameCut_return_f3['num']))) * ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12')))) / frameCut_return_f3['num'])) #(weight_turn_geshu_2f - 50 + (frameCut_return_f1['setfixlength_geshu_x'])) * ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12')))) / frameCut_return_f1['num'])
                            aaaa = 2
                        elif int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12'))) > int(config_ini.readvalue('setcamre', 'setcutlimt_f3')) >= int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_13'))) and (weight_turn_gesh_3f - (((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12'))) - int(config_ini.readvalue('setcamre', 'setcutlimt_f3')))) / ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_13')))) / frameCut_return_f3['num']))) * ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12')))) / frameCut_return_f3['num']) < 0 :#(50 - frameCut_return_f2['setfixlength_geshu_x']) >= weight_turn_geshu_2f :  #12米到13米转换x坐标情况2
                            turned_x = int(config_ini.readvalue('setcamre', 'setcutlimt_f3')) + ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_13')))) / frameCut_return_f3['num']) * weight_turn_geshu_3f
                            aaaa = 3
                        else:
                            turned_x = config_ini.readvalue('setcamre', 'setcutlimt_f3')
                            aaaa = 4
                        if 0 < int(turned_x):
                            config_ini.writeValue('setcamre', 'setcutlimt_f3', str(int(turned_x)))
                        print('三流偏重', weight_turn_geshu_3f , aaaa , turned_x, config_ini.readvalue('setcamre', 'setcutlimt_f3'))
                        with open('2233.txt', 'a+') as f:
                            f.writelines(
                                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ':' + '三流偏重,调整格式' + str(weight_turn_geshu_3f) + str(aaaa) + '调整位置' + str(turned_x) +'读取位置' +str(config_ini.readvalue('setcamre', 'setcutlimt_f3'))+ '\n')


                    # 写入切割设定X坐标

                    # 判断调整后是否 跨越12米线，跨越时，须调整X坐标比例，以及超出边界时，注意点。

                # 设定重量 - 实际重量 > 最小范围值  重量不足
                elif public['auto_adjustment_switch_F3'] == True and float(config_ini.readvalue('init', 'Btn_3aSetWeight')) - float(public['sql_weighting_F3']) > float(config_ini.readvalue('init', 'lab_3errrangeminus')) and public['sql_weighting_F3'] != 0 and public['weighting_F3_state'] != '否' and float(public['sql_weighting_F3']) >= float(1800) and float(public['sql_weighting_F3']) <= float(2500):
                    # 每个格为5公斤
                    geshu_weight = 5
                    # 重量转换格数
                    weight_turn_geshu_3f = (float(config_ini.readvalue('init', 'Btn_3aSetWeight')) - (float(public['sql_weighting_F3']))) / geshu_weight
                    print('调整格数', weight_turn_geshu_3f)
                    if abs(weight_turn_geshu_3f) <= 50:
                        if int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12'))) > int(config_ini.readvalue('setcamre', 'setcutlimt_f3')) >= int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_13'))) :    #12米到13米转换x坐标
                            turned_x = int(config_ini.readvalue('setcamre', 'setcutlimt_f3')) - ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_13')))) / frameCut_return_f3['num']) * weight_turn_geshu_3f
                            bbbb = 5
                        elif int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_11'))) > int(config_ini.readvalue('setcamre', 'setcutlimt_f3')) >= int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12'))) and (weight_turn_geshu_3f - (((int(config_ini.readvalue('setcamre', 'setcutlimt_f3'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12')))) / ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12')))) / frameCut_return_f3['num']))) * ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_13')))) / frameCut_return_f3['num']) > 0 :
                            turned_x = int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12'))) - ((weight_turn_geshu_3f - (((int(config_ini.readvalue('setcamre', 'setcutlimt_f3'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12')))) / ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12')))) / frameCut_return_f3['num']))) * ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_13')))) / frameCut_return_f3['num']))
                            bbbb = 6
                        elif int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_11'))) > int(config_ini.readvalue('setcamre', 'setcutlimt_f3')) >= int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12'))) and (weight_turn_geshu_3f - (((int(config_ini.readvalue('setcamre', 'setcutlimt_f3'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12')))) / ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12')))) / frameCut_return_f3['num']))) * ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_13')))) / frameCut_return_f3['num']) < 0 : #(frameCut_return_f1['setfixlength_geshu_x'] - 50) >= weight_turn_geshu_3f :
                            turned_x = int(config_ini.readvalue('setcamre', 'setcutlimt_f3')) - ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f3_13')))) / frameCut_return_f3['num']) * weight_turn_geshu_3f
                            bbbb = 7
                        else:
                            turned_x = config_ini.readvalue('setcamre', 'setcutlimt_f3')
                            bbbb = 8
                        if 0 < int(turned_x):
                            config_ini.writeValue('setcamre', 'setcutlimt_f3', str(int(turned_x)))
                        print('二流偏轻' , weight_turn_geshu_3f , bbbb , turned_x, config_ini.readvalue('setcamre', 'setcutlimt_f1'))
                        with open('2233.txt', 'a+') as f:
                            f.writelines(
                                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ':' + '三流偏轻,调整格式' + str(
                                    weight_turn_geshu_3f) + str(bbbb) + '调整位置' + str(turned_x) + '读取位置' + str(
                                    config_ini.readvalue('setcamre', 'setcutlimt_f3')) + '\n')

                else:
                    pass

                # 清楚缓冲重量数
                public['Weight_3f_list'] = []
                public['sql_weighting_F3'] = 0
                public['weighting_F3_state'] = '否'
                public['send_cut_3f_stat'] = False

            frameCut_Timer_f3_threading_1 = threading.Timer(180, slot_CutToSQL_3f)
            # frameCut_Timer_f2_threading_1 = threading.Timer(1, slot_CutToSQL_3f)
            # 触发切割信号（一个周期）
            # print(frameCut_return_f1['Start_Cut_state_F'])
            if frameCut_return_f3['Start_Cut_state_F'] == True and float(public['plc_3f_pullspeed']) >=1.0 and float(public['temp_Lab_3bTemperature']) >= 550.0 and public['send_cut_3f_stat'] == False:
                print('3流切割')
                print('3流PLC连接状态：', plc_3f.ConnectServer().IsSuccess)
                # print('切割状态',frameCut_return_f3['Start_Cut_state_F'])
                # plc_3f.WriteBool("M50.0", True])  # 写入PLC切割变量点
                public['action_cut_3f'] = True
                self.off_3f_timer.start()  # 启动
                # frameCut_Timer_f3_threading_1.cancel() # 判断是否为激活状态，激活状态时，并直接执行SQL(重新写SQL写入)，取消线程或结束线程，，进入下个计时
                # public['weighting_F3_state'] = '否'
                # public['sql_weighting_F3'] = 0
                # 增加流次计数量
                config_ini.writeValue('init', 'Lab_3cCount',
                                      str(int(config_ini.readvalue('init', 'Lab_3cCount')) + 1))
                window.Lab_1cCount.setText(str(config_ini.readvalue('init', 'Lab_3cCount')))  # 1流记数

                config_ini.writeValue('init', 'Lab_talRoot',
                                      str(int(config_ini.readvalue('init', 'Lab_talRoot')) + 1))
                window.Lab_talRoot.setText((config_ini.readvalue('init', 'Lab_talRoot')))  # 总记数
                frame_cut_f3 = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
                public['temp_Lab_3cCompensate'] = frameCut_return_f3['adjustment']
                public['send_cut_3f_stat'] = True

                # 延时3分钟，触发写入SQL函数
                frameCut_Timer_f3_threading_1.start()

            # 判断称重状态
            if int(public['temp_Lab_3bWeight']) >= 500:
                public['Weight_3f_list_stat'] = True
                public['weighting_F3_state'] = '是'
                public['Weight_3f_list'].append(int(public['temp_Lab_3bWeight']))
                public['sql_weighting_F3'] = int(stats.mode(public['Weight_3f_list'])[0][0])
                print('3流正在有重量', int(public['temp_Lab_3bWeight']), public['sql_weighting_F3'])
                # print('3流称重数组', public['Weight_2f_list'])
                # 传给PLC  给M区变量1个值来判断切割
            elif int(public['temp_Lab_3bWeight']) == 0 and public['Weight_3f_list_stat'] == True:
                public['Weight_3f_list'] = []
                public['Weight_3f_list_stat'] = False
            else:
                # public['temp_Lab_3bWeight'] = 0
                pass




            # 4流实例化图像处理

            if str(config_ini.readvalue('setcamre', 'ceb_threshold_auto_4f')) == 'True':
                threshold_ratio_switch_F4 = 1
            elif str(config_ini.readvalue('setcamre', 'ceb_threshold_auto_4f')) == 'False':
                threshold_ratio_switch_F4 = 0


            frameCut_return_f4 = Frame_Cut_Temp.frameCut(
                frame_cut=frame_cut,
                cut_y0=float(config_ini.readvalue('setcamre', 'frame_cut_y0_f4')),
                cut_y1=float(config_ini.readvalue('setcamre', 'frame_cut_y1_f4')),
                cut_x0=float(config_ini.readvalue('setcamre', 'frame_cut_x0_f4')),
                cut_x1=float(config_ini.readvalue('setcamre', 'frame_cut_x1_f4')),
                fixlength=int(config_ini.readvalue('init', 'lab_4csetlength')),
                temp_Lne_Frame_cut_Y1=int(public['temp_Lne_Frame_cut_Y1_F4']),
                temp_Lne_Frame_cut_Y0=public['temp_Lne_Frame_cut_Y0_F4'],
                frame_cut_angle=config_ini.readvalue('setcamre', 'frame_cut_f4_angle'),
                setcutlimt=config_ini.readvalue('setcamre', 'setcutlimt_f4'),
                threshold=int(config_ini.readvalue('setcamre', 'threshold_f4')),
                Start_Cut_state=public['Start_Cut_state_F4'],
                pullspeed=public['plc_4f_pullspeed'],
                threshold_ratio=0.4,
                threshold_ratio_switch=threshold_ratio_switch_F4,
                x_9=int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_11'))),
                x_11=int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12'))),
                x_13=int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_13'))),
                setcutlimt_selected_status = public['selected_status_F4'],
                # fixlength=int(window.Lab_1cSetLength.text())
            )


            window.Lab_4cState.setText(frameCut_return_f4['Lab_fcState'])
            # 一直触发切割信号，一直到图像中没有符合要求的图像
            public['Start_Cut_state_F4'] = frameCut_return_f4['Start_Cut_state']
            window.Lab_4cCompensate.setText(str(round(float(frameCut_return_f4['adjustment']), 2)))
            # print(frameCut_return_f1)
            # 只有开始第一周期执行

            def slot_CutToSQL_4f():
                MainWindow.slot_CutToSQL(self,
                                         FurNum=str((config_fur.readvalue('FurListData1', 'lne_setfurno'))),
                                         FlowNum="4",  # 流号
                                         FixLength=str(window.Lab_4cSetLength.text()),  # 定尺长度
                                         Team=str(window.Btn_Class.text()),  # 班组
                                         SteelType=str(window.Lab_4cSteels.text()),  # 钢种
                                         RealWeight=str(public['sql_weighting_F4']),  # 真实重量
                                         Weighing=public['weighting_F4_state'],  # 是否称重
                                         SetWeight=str(window.Btn_4aSetWeight.text()),  # 设定重量
                                         IDtime=frame_cut_f4,  # 时间
                                         adjustment=str(public['temp_Lab_4cCompensate']),  # 补偿值
                                         density=str(SQLlite.SQL_readSteeldensity(self.Lab_4cSteels.text())),
                                         # 读取数据库里的钢种密度
                                         theoryWeight=str(window.Lab_4bWeight.text())  # 理论重量
                                         )


                # 判断称重是否在合格范围内，如超出范围，自动调整
                if 'True' == config_ini.readvalue('setcamre', 'Ceb_Correct_auto_f4'):
                    # self.Ceb_Threshold_auto_f1.stateChanged.connect(self.slot_Change_Threshold_auto_1f)
                    public['auto_adjustment_switch_F4'] = True
                else:
                    public['auto_adjustment_switch_F4'] = False
                # public['sql_weighting_F1'] = 2384
                # public['weighting_F1_state'] = '是'
                # 实际重量 - 设定重量 > 最大范围值  重量超出
                if public['auto_adjustment_switch_F4'] == True and float(public['sql_weighting_F4']) - float(config_ini.readvalue('init', 'Btn_4aSetWeight')) > float(config_ini.readvalue('init', 'lab_4errrangeplus')) and public['sql_weighting_F4'] != 0 and public['weighting_F4_state'] != '否' and float(public['sql_weighting_F4']) >= float(1800) and float(public['sql_weighting_F4']) <= float(2500):
                    # 每个格为5公斤
                    geshu_weight = 5
                    # 重量转换格数
                    weight_turn_geshu_4f = (float(public['sql_weighting_F4']) - float(config_ini.readvalue('init', 'Btn_4aSetWeight'))) / geshu_weight
                    if abs(weight_turn_geshu_4f) <= 50:
                        if int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_11'))) > int(config_ini.readvalue('setcamre', 'setcutlimt_f4')) >= int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12'))) :    #11米到12米转换x坐标
                            turned_x = int(config_ini.readvalue('setcamre', 'setcutlimt_f4')) + ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12')))) / frameCut_return_f4['num']) * weight_turn_geshu_4f
                            aaaa = 1
                        elif int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12'))) > int(config_ini.readvalue('setcamre', 'setcutlimt_f4')) >= int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_13'))) and (weight_turn_geshu_4f - (((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12'))) - int(config_ini.readvalue('setcamre', 'setcutlimt_f4')))) / ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_13')))) / frameCut_return_f4['num']))) * ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12')))) / frameCut_return_f4['num']) > 0 : #(50 - frameCut_return_f4['setfixlength_geshu_x']) < weight_turn_geshu_4f :    #12米到13米转换x坐标情况1
                            turned_x = int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12'))) + ((weight_turn_geshu_4f - (((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12'))) - int(config_ini.readvalue('setcamre', 'setcutlimt_f4')))) / ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_13')))) / frameCut_return_f4['num']))) * ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12')))) / frameCut_return_f4['num'])) #(weight_turn_geshu_4f - 50 + (frameCut_return_f4['setfixlength_geshu_x'])) * ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12')))) / frameCut_return_f4['num'])
                            aaaa = 2
                        elif int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12'))) > int(config_ini.readvalue('setcamre', 'setcutlimt_f4')) >= int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_13'))) and (weight_turn_geshu_4f - (((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12'))) - int(config_ini.readvalue('setcamre', 'setcutlimt_f4')))) / ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_13')))) / frameCut_return_f4['num']))) * ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12')))) / frameCut_return_f4['num']) < 0 :#(50 - frameCut_return_f4['setfixlength_geshu_x']) >= weight_turn_geshu_4f :  #12米到13米转换x坐标情况2
                            turned_x = int(config_ini.readvalue('setcamre', 'setcutlimt_f4')) + ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_13')))) / frameCut_return_f4['num']) * weight_turn_geshu_4f
                            aaaa = 3
                        else:
                            turned_x = config_ini.readvalue('setcamre', 'setcutlimt_f4')
                            aaaa = 4
                        if 0 < int(turned_x):
                            config_ini.writeValue('setcamre', 'setcutlimt_f4', str(int(turned_x)))
                        print('四流偏重', weight_turn_geshu_4f , aaaa , turned_x, config_ini.readvalue('setcamre', 'setcutlimt_f4'))
                        with open('2233.txt', 'a+') as f:
                            f.writelines(
                                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ':' + '一流偏重,调整格式' + str(
                                    weight_turn_geshu_4f) + str(aaaa) + '调整位置' + str(turned_x) + '读取位置' + str(
                                    config_ini.readvalue('setcamre', 'setcutlimt_f4')) + '\n')

                    # 写入切割设定X坐标

                    # 判断调整后是否 跨越12米线，跨越时，须调整X坐标比例，以及超出边界时，注意点。

                # 设定重量 - 实际重量 > 最小范围值  重量不足
                elif public['auto_adjustment_switch_F4'] == True and float(config_ini.readvalue('init', 'Btn_4aSetWeight')) - float(public['sql_weighting_F4']) > float(config_ini.readvalue('init', 'lab_4errrangeminus')) and public['sql_weighting_F4'] != 0 and public['weighting_F4_state'] != '否' and float(public['sql_weighting_F4']) >= float(1800) and float(public['sql_weighting_F4']) <= float(2500):
                    # 每个格为5公斤
                    geshu_weight = 5
                    # 重量转换格数
                    weight_turn_geshu_4f = (float(config_ini.readvalue('init', 'Btn_4aSetWeight')) - (float(public['sql_weighting_F4']))) / geshu_weight
                    print('调整格数' , weight_turn_geshu_4f)
                    if abs(weight_turn_geshu_4f) <= 50:
                        if int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12'))) > int(config_ini.readvalue('setcamre', 'setcutlimt_f4')) >= int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_13'))) :    #12米到13米转换x坐标
                            turned_x = int(config_ini.readvalue('setcamre', 'setcutlimt_f4')) - ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_13')))) / frameCut_return_f4['num']) * weight_turn_geshu_4f
                            bbbb = 5
                        elif int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_11'))) > int(config_ini.readvalue('setcamre', 'setcutlimt_f4')) >= int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12'))) and (weight_turn_geshu_4f - (((int(config_ini.readvalue('setcamre', 'setcutlimt_f4'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12')))) / ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12')))) / frameCut_return_f4['num']))) * ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_13')))) / frameCut_return_f4['num']) > 0 :
                            turned_x = int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12'))) - ((weight_turn_geshu_4f - (((int(config_ini.readvalue('setcamre', 'setcutlimt_f4'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12')))) / ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12')))) / frameCut_return_f4['num']))) * ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_13')))) / frameCut_return_f4['num']))
                            bbbb = 6
                        elif int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_11'))) > int(config_ini.readvalue('setcamre', 'setcutlimt_f4')) >= int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12'))) and (weight_turn_geshu_4f - (((int(config_ini.readvalue('setcamre', 'setcutlimt_f4'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12')))) / ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_11'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12')))) / frameCut_return_f4['num']))) * ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_13')))) / frameCut_return_f4['num']) < 0 : #(frameCut_return_f4['setfixlength_geshu_x'] - 50) >= weight_turn_geshu_4f :
                            turned_x = int(config_ini.readvalue('setcamre', 'setcutlimt_f4')) - ((int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12'))) - int((config_ini.readvalue('setcamre', 'frame_cut_x1_f4_13')))) / frameCut_return_f4['num']) * weight_turn_geshu_4f
                            bbbb = 7
                        else:
                            turned_x = config_ini.readvalue('setcamre', 'setcutlimt_f4')
                            bbbb = 8
                        if 0 < int(turned_x):
                            config_ini.writeValue('setcamre', 'setcutlimt_f4', str(int(turned_x)))
                        print('四流偏轻', weight_turn_geshu_4f , bbbb , turned_x, config_ini.readvalue('setcamre', 'setcutlimt_f4'))
                        with open('2233.txt', 'a+') as f:
                            f.writelines(
                                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ':' + '四流偏轻,调整格式' + str(
                                    weight_turn_geshu_4f) + str(bbbb) + '调整位置' + str(turned_x) + '读取位置' + str(
                                    config_ini.readvalue('setcamre', 'setcutlimt_f4')) + '\n')

                else:
                    pass

                # 清楚缓冲重量数
                public['Weight_4f_list'] = []
                public['sql_weighting_F4'] = 0
                public['weighting_F4_state'] = '否'
                public['send_cut_4f_stat'] = False

            frameCut_Timer_f4_threading_1 = threading.Timer(180, slot_CutToSQL_4f)

            # 触发切割信号（一个周期）
            if frameCut_return_f4['Start_Cut_state_F'] == True and float(public['plc_4f_pullspeed']) >=1.0 and float(public['temp_Lab_4bTemperature']) >= 550.0 and public['send_cut_4f_stat'] == False:
                print('4流切割')
                print('4流PLC连接状态：', plc_4f.ConnectServer().IsSuccess)
                # print('切割状态',frameCut_return_f4['Start_Cut_state_F'])
                # plc_4f.WriteBool("M50.0", True])  # 写入PLC切割变量点
                public['action_cut_4f'] = True
                self.off_4f_timer.start()  # 启动
                # frameCut_Timer_f4_threading_1.cancel() # 判断是否为激活状态，激活状态时，并直接执行SQL(重新写SQL写入)，取消线程或结束线程，，进入下个计时
                # public['weighting_F4_state'] = '否'
                # public['sql_weighting_F4'] = 0
                # 增加流次计数量
                config_ini.writeValue('init', 'Lab_4cCount',
                                      str(int(config_ini.readvalue('init', 'Lab_4cCount')) + 1))
                window.Lab_4cCount.setText(str(config_ini.readvalue('init', 'Lab_4cCount')))  # 1流记数

                config_ini.writeValue('init', 'Lab_talRoot',
                                      str(int(config_ini.readvalue('init', 'Lab_talRoot')) + 1))
                window.Lab_talRoot.setText((config_ini.readvalue('init', 'Lab_talRoot')))  # 总记数
                frame_cut_f4 = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
                public['temp_Lab_4cCompensate'] = frameCut_return_f4['adjustment']
                public['send_cut_4f_stat'] = True


                # 延时3分钟，触发写入SQL函数
                frameCut_Timer_f4_threading_1.start()

            # 判断称重状态
            if int(public['temp_Lab_4bWeight']) >= 500:
                public['Weight_4f_list_stat'] = True
                public['weighting_F4_state'] = '是'
                public['Weight_4f_list'].append(int(public['temp_Lab_4bWeight']))
                public['sql_weighting_F4'] = int(stats.mode(public['Weight_4f_list'])[0][0])
                print('4流正在有重量', int(public['temp_Lab_4bWeight']), public['sql_weighting_F4'])
                # print('4流称重数组', public['Weight_4f_list'])
                # 传给PLC  给M区变量1个值来判断切割
            elif int(public['temp_Lab_4bWeight']) == 0 and public['Weight_4f_list_stat'] == True:
                public['Weight_4f_list'] = []
                public['Weight_4f_list_stat'] = False
            else:
                # public['temp_Lab_4bWeight'] = 0
                pass



        except Exception as e:
            print("frameCut报错", e)

        else:
            return frame_cut

    '''工业相机结束'''

    # 主页面刷新

    def autoShow(self):
        '''恢复上次关闭数据_初始化config.ini -> init'''
        self.Btn_Class.setText((config_ini.readvalue('init', 'Btn_Class')))  # 班次
        # self.Lab_talRoot.setText((config_ini.readvalue('init', 'Lab_talRoot')))  # 总记数
        self.Lab_talTon.setText((config_ini.readvalue('init', 'Lab_talTon')))  # 总重量
        self.Btn_FurNo.setText("炉号:  " + str((config_fur.readvalue('FurListData1', 'lne_setfurno'))))  # 炉号
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
        public['temp_Lne_Frame_cut_Y0_F1'] = int(config_ini.readvalue('setcamre', 'frame_cut_y0_f1'))
        public['temp_Lne_Frame_cut_Y0_F2'] = int(config_ini.readvalue('setcamre', 'frame_cut_y0_f2'))
        public['temp_Lne_Frame_cut_Y0_F3'] = int(config_ini.readvalue('setcamre', 'frame_cut_y0_f3'))
        public['temp_Lne_Frame_cut_Y0_F4'] = int(config_ini.readvalue('setcamre', 'frame_cut_y0_f4'))
        public['temp_Lne_Frame_cut_Y1_F1'] = int(config_ini.readvalue('setcamre', 'frame_cut_y1_f1'))
        public['temp_Lne_Frame_cut_Y1_F2'] = int(config_ini.readvalue('setcamre', 'frame_cut_y1_f2'))
        public['temp_Lne_Frame_cut_Y1_F3'] = int(config_ini.readvalue('setcamre', 'frame_cut_y1_f3'))
        public['temp_Lne_Frame_cut_Y1_F4'] = int(config_ini.readvalue('setcamre', 'frame_cut_y1_f4'))
        self.Lab_talRoot.setText(str(
            int(config_ini.readvalue('init', 'Lab_1cCount')) + int(config_ini.readvalue('init', 'Lab_2cCount')) + int(
                config_ini.readvalue('init', 'Lab_3cCount')) + int(config_ini.readvalue('init', 'Lab_4cCount'))))
        self.statuShow('与PLC连接中', 5)
        self.flag_time500 = False

        # self.Lab_1aTrackValue.setText(str(S7_300.printReadResult(plc.ReadBool("DB2.0.0"))))

    # 状态栏显示函数
    def statuShow(self, showString, showTime):
        '''
        :param showString:需要在状态栏显示的内容
        :param showTime: 显示的时间*秒
        :return: 状态栏显示
        '''
        # 下面的状态栏
        self.status = self.statusBar()
        # 状态栏消息的消息
        # self.status.showMessage('只存在5秒的消息', 5000)
        self.status.showMessage(showString, showTime * 1000)

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
    def slot_close(self, event):
        try:
            config_ini.writeValue('init', 'smtp_vserver', 'sss')
            config_ini.writeValue('init', 'Lab_talRoot', window.Lab_talRoot.text())  # 总根数写入配置文件
            config_ini.writeValue('init', 'Lab_talTon', window.Lab_talTon.text())  # 总重量写入配置文件
        except Exception as e:
            print("主程序关闭文件保存错误代码：", e)
        else:
            app = QApplication.instance()
            # 退出应用程序
            app.quit()

    def slot_SetFurNo(self):  # 设置炉号
        furno = FurNoPage()
        furno.exec_()

    def slot_SetFixLeng(self):  # 设置输入定尺
        Fixleng = FixLengPage()
        Fixleng.exec_()

    def slot_SetTeam(self):  # 设置班组
        Team = TeamPage()
        Team.exec_()

    def slot_ProductionData(self):  # 设置生产数据
        Data = ProductionDataPage()
        Data.exec_()

    def slot_Camera(self):  # 视频参数调整
        camera = SetCameraPage()
        camera.exec_()

    def slot_SetAlgorithm_triggered(self):  # 设置算法
        algorithm = AlgorithmPage()
        algorithm.exec_()

    def slot_SetSteelData(self):  # 定尺管理
        steeldata = SetSteelDataPage()
        steeldata.exec_()

    def slot_SetSteelType(self):  # 钢种管理
        steeltypeManage = SetSteelTypePage()
        steeltypeManage.exec_()

    def slot_SetCalibrate(self):
        setcalibrate = SetCalibratePage()
        setcalibrate.exec_()

    def slot_CutToSQL(self, FlowNum, FurNum, FixLength, Team, SteelType, RealWeight, Weighing, SetWeight, IDtime,
                      adjustment, density, theoryWeight):
        sqlfield = "FlowNum,FurNum,FixLength,Team,SteelType,RealWeight,Weighing,SetWeight,IDtime,adjustment,density,theoryWeight"
        sqlvalue = "'" + str(FlowNum) + "','" + str(FurNum) + "','" + str(FixLength) + "','" + str(Team) + "','" + str(
            SteelType) + "','" + str(RealWeight) + "','" + str(Weighing) + "','" + str(SetWeight) + "','" + str(
            IDtime) + "','" + str(adjustment) + "','" + str(density) + "','" + str(theoryWeight) + "'"
        SQLlite.CutToSQL(sqlfield, sqlvalue)
        # print('触发一次', FlowNum, RealWeight, Weighing)
        print(time.strftime("%Y-%m-%d %H:%M:%S"), '写入数据库:{FlowNum}流，称重重量{RealWeight},是否称重:{Weighing}'.format(FlowNum=FlowNum, RealWeight=RealWeight, Weighing=Weighing))

    def slot_Help(self):
        QtWidgets.QMessageBox.question(self, "帮助", "联系计控室",
                                       QtWidgets.QMessageBox.Yes)

    def slot_timeOut(self):  # 延时触发该函数定时
        tm = QTime.currentTime()  # 获取当前时间
        dd = QDate.currentDate()  # 获取当前日期
        strText = tm.toString("hh:mm:ss")
        self.Lab_Time.setText(strText)
        self.Lab_DateDay.setText(dd.toString(Qt.DefaultLocaleLongDate))

        if self.flag_time500 == False :
            self.flag_time500 = True
        elif self.flag_time500 == True:
            self.flag_time500 = False

        # 记数数量大于当炉号根数时，减少炉号1列信息
        try:
            if int(window.Lab_talRoot.text()) >= int(config_fur.readvalue('FurListData1', 'lne_setfurnum')):
                # FurNoPage.slot_autoDelFurNum(self)
                temp_furnoPage = FurNoPage()
                temp_furnoPage.slot_autoDelFurNum()
                window.Lab_talRoot.setText('0')
                window.Lab_talTon.setText('0')
                window.Lab_1cCount.setText('0')
                window.Lab_2cCount.setText('0')
                window.Lab_3cCount.setText('0')
                window.Lab_4cCount.setText('0')

                # 保存该班组的总根数
                config_ini.writeValue('init', 'Lab_talRoot', '0')  # 写入总根数为0
                # 保持该班组的总重量
                config_ini.writeValue('init', 'Lab_talTon', '0')  # 写入总重量为0
                # 写入流次记数清零
                config_ini.writeValue('init', 'Lab_1cCount', '0')
                config_ini.writeValue('init', 'Lab_2cCount', '0')
                config_ini.writeValue('init', 'Lab_3cCount', '0')
                config_ini.writeValue('init', 'Lab_4cCount', '0')

        except Exception as e:
            print('计数错误', e)

        # 刷新页面
        window.Lab_1bWeight.setText(str(public['temp_Lab_1bWeight']))
        window.Lab_2bWeight.setText(str(public['temp_Lab_2bWeight']))
        window.Lab_3bWeight.setText(str(public['temp_Lab_3bWeight']))
        window.Lab_4bWeight.setText(str(public['temp_Lab_4bWeight']))
        window.Lab_1cWeight.setText(str(public['temp_Lab_1bWeight']))
        window.Lab_2cWeight.setText(str(public['temp_Lab_2bWeight']))
        window.Lab_3cWeight.setText(str(public['temp_Lab_3bWeight']))
        window.Lab_4cWeight.setText(str(public['temp_Lab_4bWeight']))
        window.Lab_1aTrackValue.setText(str(public['temp_Lab_1bWeight']))
        window.Lab_2aTrackValue.setText(str(public['temp_Lab_2bWeight']))
        window.Lab_3aTrackValue.setText(str(public['temp_Lab_3bWeight']))
        window.Lab_4aTrackValue.setText(str(public['temp_Lab_4bWeight']))
        window.Lab_1bTemperature.setText(str(round(float(public['temp_Lab_1bTemperature']), 2)))
        window.Lab_2bTemperature.setText(str(round(float(public['temp_Lab_1bTemperature']), 2)))
        window.Lab_3bTemperature.setText(str(round(float(public['temp_Lab_1bTemperature']), 2)))
        window.Lab_4bTemperature.setText(str(round(float(public['temp_Lab_1bTemperature']), 2)))



        if public['plc_public_IsSuccess'] == True:
            window.Lab_public_plc_state.setStyleSheet("background-color:green;\n"
                          "font: 10pt \"微软雅黑\";\n"
                          "color:black;")
        elif public['plc_public_IsSuccess'] == False:
            window.Lab_public_plc_state.setStyleSheet("background-color:red;\n"
                                                      "font: 10pt \"微软雅黑\";\n"
                                                      "color:black;")
        else:
            print('公共流通讯状态异常')

        if public['plc_1f_IsSuccess'] == True:
            window.Lab_1f_plc_state.setStyleSheet("background-color:green;\n"
                          "font: 10pt \"微软雅黑\";\n"
                          "color:black;")
        elif public['plc_1f_IsSuccess'] == False:
            window.Lab_1f_plc_state.setStyleSheet("background-color:red;\n"
                                                      "font: 10pt \"微软雅黑\";\n"
                                                      "color:black;")
        else:
            print('一流通讯状态异常')


        if public['plc_2f_IsSuccess'] == True:
            window.Lab_2f_plc_state.setStyleSheet("background-color:green;\n"
                          "font: 10pt \"微软雅黑\";\n"
                          "color:black;")
        elif public['plc_2f_IsSuccess'] == False:
            window.Lab_2f_plc_state.setStyleSheet("background-color:red;\n"
                                                      "font: 10pt \"微软雅黑\";\n"
                                                      "color:black;")
        else:
            print('二流通讯状态异常')

        if public['plc_3f_IsSuccess'] == True:
            window.Lab_3f_plc_state.setStyleSheet("background-color:green;\n"
                          "font: 10pt \"微软雅黑\";\n"
                          "color:black;")
        elif public['plc_3f_IsSuccess'] == False:
            window.Lab_3f_plc_state.setStyleSheet("background-color:red;\n"
                                                      "font: 10pt \"微软雅黑\";\n"
                                                      "color:black;")
        else:
            print('三流通讯状态异常')

        if public['plc_4f_IsSuccess'] == True:
            window.Lab_4f_plc_state.setStyleSheet("background-color:green;\n"
                          "font: 10pt \"微软雅黑\";\n"
                          "color:black;")
        elif public['plc_4f_IsSuccess'] == False:
            window.Lab_4f_plc_state.setStyleSheet("background-color:red;\n"
                                                      "font: 10pt \"微软雅黑\";\n"
                                                      "color:black;")
        else:
            print('四流通讯状态异常')

        if public['plc_cut_IsSuccess'] == True:
            window.Lab_cut_plc_state.setStyleSheet("background-color:green;\n"
                          "font: 10pt \"微软雅黑\";\n"
                          "color:black;")
        elif public['plc_cut_IsSuccess'] == False:
            window.Lab_cut_plc_state.setStyleSheet("background-color:red;\n"
                                                      "font: 10pt \"微软雅黑\";\n"
                                                      "color:black;")
        else:
            print('四流通讯状态异常')



        # 1流手自动
        if public['plc_weight_manual_F1'] == True:
            window.Lab_1cMode.setText('手动')
        elif public['plc_weight_auto_F1'] == True:
            window.Lab_1cMode.setText('自动')
        elif public['plc_weight_manual_F1'] == False or public['plc_weight_auto_F1'] == False:
            window.Lab_1cMode.setText('非手自动')
        else:
            window.Lab_1cMode.setText('异常')

        # 2流手自动
        if public['plc_weight_manual_F2'] == True:
            window.Lab_2cMode.setText('手动')
        elif public['plc_weight_auto_F2'] == True:
            window.Lab_2cMode.setText('自动')
        elif public['plc_weight_manual_F2'] == False or public['plc_weight_auto_F2'] == False:
            window.Lab_2cMode.setText('非手自动')
        else:
            window.Lab_2cMode.setText('异常')

        # 3流手自动
        if public['plc_weight_manual_F3'] == True:
            window.Lab_3cMode.setText('手动')
        elif public['plc_weight_auto_F3'] == True:
            window.Lab_3cMode.setText('自动')
        elif public['plc_weight_manual_F3'] == False or public['plc_weight_auto_F3'] == False:
            window.Lab_3cMode.setText('非手自动')
        else:
            window.Lab_3cMode.setText('异常')

        # 4流手自动
        if public['plc_weight_manual_F4'] == True:
            window.Lab_4cMode.setText('手动')
        elif public['plc_weight_auto_F4'] == True:
            window.Lab_4cMode.setText('自动')
        elif public['plc_weight_manual_F4'] == False or public['plc_weight_auto_F4'] == False:
            window.Lab_4cMode.setText('非手自动')
        else:
            window.Lab_4cMode.setText('异常')

        # 是否在称重信号
        if public['plc_weighting_F1'] == True:
            window.Lab_1aWeight.setStyleSheet("background-color:green;\n"
                                              "color:yellow;")
        else:
            window.Lab_1aWeight.setStyleSheet("background-color:black;\n"
                                              "color:yellow;")

        if public['plc_weighting_F2'] == True:
            window.Lab_1aWeight.setStyleSheet("background-color:green;\n"
                                              "color:yellow;")
        else:
            window.Lab_1aWeight.setStyleSheet("background-color:black;\n"
                                              "color:yellow;")

        if public['plc_weighting_F3'] == True:
            window.Lab_1aWeight.setStyleSheet("background-color:green;\n"
                                              "color:yellow;")
        else:
            window.Lab_1aWeight.setStyleSheet("background-color:black;\n"
                                              "color:yellow;")

        if public['plc_weighting_F4'] == True:
            window.Lab_1aWeight.setStyleSheet("background-color:green;\n"
                                              "color:yellow;")
        else:
            window.Lab_1aWeight.setStyleSheet("background-color:black;\n"
                                              "color:yellow;")

        window.Lab_1cSpeed.setText(str(round(float(public['plc_1f_pullspeed']), 2)))
        window.Lab_2cSpeed.setText(str(round(float(public['plc_2f_pullspeed']), 2)))
        window.Lab_3cSpeed.setText(str(round(float(public['plc_3f_pullspeed']), 2)))
        window.Lab_4cSpeed.setText(str(round(float(public['plc_4f_pullspeed']), 2)))

        # if public['plc_cut_IsSuccess'] == True :
        #     self.Lab_PLCTon.setText("PLC连接成功")
        #     self.Lab_PLCTon.setStyleSheet("background-color:green;\n"
        #                                   "font: 75 14pt \"微软雅黑\";\n"
        #                                   "color:yellow\n"
        #                                   "")
        # elif public['plc_cut_IsSuccess'] == False :
        #     self.Lab_PLCTon.setText("PLC连接失败")
        #     self.Lab_PLCTon.setStyleSheet("background-color:red;\n"
        #                                   "font: 75 14pt \"微软雅黑\";\n"
        #                                   "color:black\n"
        #                                   "")

    def slot_Synchronizer_timer(self):  # 本地数据库同步82服务器   定时
        try:
            SynchronizerRun = SQLData_Synchronizer.SQL_Synchronizer
            SynchronizerRun()
            print("数据库同步成功")
        except Exception as e:
            print("数据库同步失败", e)


class FurNoPage(QDialog, UI_SetFurNo.Ui_Dialog):  # 炉号
    def __init__(self, parent=None):
        super(FurNoPage, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.Lne_SetFurNum.setValidator(QIntValidator(0, 65535))  # 设置输入整形数字范围
        self.Lne_SetFurNo.setValidator(QDoubleValidator())  # 设置输入浮点数字范围
        try:
            # 显示列表信息
            for i in range(1, 11):
                Furstr = 'FurListData' + str(i)
                if int(config_fur.readvalue(Furstr, 'show')) == 1:  # 判断在第几个开始显示
                    a = "炉号" + config_fur.readvalue(Furstr, 'lne_setfurno')
                    b = "根数" + config_fur.readvalue(Furstr, 'lne_setfurnum')
                    self.LW_SetFurNo.addItem(a + b)
        except Exception as e:
            print('炉号显示异常:',e)

        self.Btn_Exit.clicked.connect(self.close)
        self.Btn_addFurNum.clicked.connect(self.slot_addFurNum)  # 增加项
        self.Btn_delFurNum.clicked.connect(self.slot_delFurNum)  # 删除项
        self.LW_SetFurNo.setSelectionMode(QAbstractItemView.SingleSelection)  # 单项处理
        self.LW_SetFurNo.itemClicked.connect(self.slot_SetFurNoItemCliked)  # 单击触发 提示
        self.LW_SetFurNo.currentItemChanged.connect(self.slot_SetFurNoItemDoubleClicked)  # 选中项前后字体变色

    # 炉号列表增加
    def slot_addFurNum(self):
        strNo = self.Lne_SetFurNo.text()
        strNum = self.Lne_SetFurNum.text()

        if len(strNo) > 0 and len(strNum) > 0:  # 判断是否输入
            # 修改配置文件
            for i in range(1, 11):
                Furstr = 'FurListData' + str(i)  # 配置文件中，名称
                if int(config_fur.readvalue(Furstr, 'show')) == 0:  #
                    config_fur.readvalue(Furstr, 'row')  # 获取未显示行数
                    config_fur.writeValue(Furstr, 'lne_setfurno', self.Lne_SetFurNo.text())
                    config_fur.writeValue(Furstr, 'lne_setfurnum', self.Lne_SetFurNum.text())
                    config_fur.writeValue(Furstr, 'show', '1')
                    self.LW_SetFurNo.addItem(
                        '炉号' + str(self.Lne_SetFurNo.text()) + '根数' + str(self.Lne_SetFurNum.text()))
                    # window.autoShow()
                    break
        else:
            QtWidgets.QMessageBox.question(self, "提示", "请全部输入！",
                                           QtWidgets.QMessageBox.Yes)

    # 炉号列表指定删除
    def slot_delFurNum(self):
        pItem = self.LW_SetFurNo.currentItem()  # 得到左侧列表选中项
        if pItem is None:
            return
        try:
            idx = self.LW_SetFurNo.row(pItem)  # 得到项的序号  所在行 idx =>int
            # print(pItem.text())  # 所选行的文本
            # Furstr = 'FurListData' + str(idx)  # 配置文件中，名称
            # print(idx)  #选择行数
            print(idx)
            self.LW_SetFurNo.takeItem(idx)
            if idx == 9:  # 当选择最后一列，直接隐藏
                config_fur.writeValue('FurListData10', 'show', '0')
                window.autoShow()
            else:
                for i in range(idx, 9):
                    j = 'FurListData' + str(i + 1)
                    k = 'FurListData' + str(i + 2)
                    config_fur.writeValue(j, 'lne_setfurno', config_fur.readvalue(k, 'lne_setfurno'))
                    config_fur.writeValue(j, 'lne_setfurnum', config_fur.readvalue(k, 'lne_setfurnum'))

                for s in range(idx + 1, 11):
                    l = 'FurListData' + str(s)  # 配置文件中，名称
                    if int(config_fur.readvalue(l, 'show')) == 0:
                        for j in range(s - 1, 11):
                            m = 'FurListData' + str(j)  # 配置文件中，名称
                            config_fur.writeValue(m, 'show', '0')
                            if j == 10:
                                window.autoShow()
                                return
                    elif int(config_fur.readvalue('FurListData10', 'show')) == 1:
                        config_fur.writeValue('FurListData10', 'show', '0')
                        window.autoShow()
                        return
        except Exception as e:
            print('炉号删除', e)

    # 炉号列表自动删第一行
    # 自动减炉号
    # furno = FurNoPage()
    # furno.slot_autoDelFurNum()
    def slot_autoDelFurNum(self):
        idx = 0
        if self.LW_SetFurNo.count() == 0:
            QtWidgets.QMessageBox.question(self, "提示", "炉号为空",
                                           QtWidgets.QMessageBox.Yes)
            return
        else:
            self.LW_SetFurNo.takeItem(idx)
            if idx == 9:  # 当选择最后一列，直接隐藏
                config_fur.writeValue('FurListData10', 'show', '0')
                window.autoShow()
            else:
                for i in range(idx, 9):
                    j = 'FurListData' + str(i + 1)
                    k = 'FurListData' + str(i + 2)
                    config_fur.writeValue(j, 'lne_setfurno', config_fur.readvalue(k, 'lne_setfurno'))
                    config_fur.writeValue(j, 'lne_setfurnum', config_fur.readvalue(k, 'lne_setfurnum'))

                for s in range(idx + 1, 11):
                    l = 'FurListData' + str(s)  # 配置文件中，名称
                    if int(config_fur.readvalue(l, 'show')) == 0:
                        for j in range(s - 1, 11):
                            m = 'FurListData' + str(j)  # 配置文件中，名称
                            config_fur.writeValue(m, 'show', '0')
                            if j == 10:
                                window.autoShow()
                                return
                    elif int(config_fur.readvalue('FurListData10', 'show')) == 1:
                        config_fur.writeValue('FurListData10', 'show', '0')
                        window.autoShow()
                        return

    def slot_SetFurNoItemCliked(self, item):
        ft = item.font()
        ft.setBold(True)
        item.setFont(ft)

    def slot_SetFurNoItemDoubleClicked(self, current, previous):  # current 新选中的项  previous之前选中的项
        # 将之前选中的字体粗体恢复
        if not (previous is None):
            ft = previous.font()
            ft.setBold(False)
            previous.setFont(ft)


class FixLengPage(QDialog, UI_SetFixLeng.Ui_Dialog):  # 设置输入定尺
    def __init__(self, parent=None):
        super(FixLengPage, self).__init__(parent)
        self.setupUi(self)

        # 输入限制
        self.Lne_FixLength.setValidator(QIntValidator(0, 65535))  # 设置输入整形数字范围
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

    def slot_editEnabled(self, b):  # b勾选编辑
        self.Lne_FixWeiht.setEnabled(b)
        self.Lne_TheoryWeiht.setEnabled(b)
        self.Lne_Density.setEnabled(b)
        self.Lne_FixWeiht.setValidator(QIntValidator(0, 50000, self.Lne_FixWeiht))  # QIntValidator 整数的有效判断，范围0-300

    def slot_SaveData(self):
        if len(self.Lne_FixLength.text()) > 0 \
                and len(self.Lne_FixWeiht.text()) > 0 \
                and len(self.Lne_Density.text()) > 0 \
                and len(self.Lne_ErrRangeMinus.text()) > 0 \
                and len(self.Lne_ErrRangePlus.text()) > 0 \
                and len(self.Lne_PreClampOffset.text()) > 0 \
                and len(self.Lne_TheoryWeiht.text()) > 0 \
                and len(self.Lne_LengthRangeMax.text()) > 0 \
                and len(self.Lne_WeightMax.text()) > 0:

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
                    print(row, form[0])
                    SQLname = str(self.Lne_FixLength.text()) + ' 预夹=' + str(
                        self.Lne_PreClampOffset.text()) + ' 定重目标=' + str(self.Lne_FixWeiht.text())
                    if SQLname in form[0]:
                        QtWidgets.QMessageBox.question(self, "提示", "有重复",
                                                       QtWidgets.QMessageBox.Yes)
                        return

            try:
                window.Btn_1aSetWeight.setText(self.Lne_FixLength.text())  # 1流定重设置显示
                window.Btn_2aSetWeight.setText(self.Lne_FixLength.text())  # 2流定重设置显示
                window.Btn_3aSetWeight.setText(self.Lne_FixLength.text())  # 3流定重设置显示
                window.Btn_4aSetWeight.setText(self.Lne_FixLength.text())  # 4流定重设置显示
                config_ini.writeValue('init', 'Btn_1aSetWeight', self.Lne_FixWeiht.text())
                config_ini.writeValue('init', 'Btn_2aSetWeight', self.Lne_FixWeiht.text())
                config_ini.writeValue('init', 'Btn_3aSetWeight', self.Lne_FixWeiht.text())
                config_ini.writeValue('init', 'Btn_4aSetWeight', self.Lne_FixWeiht.text())

                SQLname = str(self.Lne_FixLength.text()) + ' 预夹=' + str(
                    self.Lne_PreClampOffset.text()) + ' 定重目标=' + str(self.Lne_FixWeiht.text())

                # conn = pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
                # cursor = conn.cursor()
                cursor.execute("INSERT INTO fixsteeldata ("
                               "SteelName, "  # 定长名称
                               "FixLength,"  # 定长
                               "FixWeiht,"  # 定长重量
                               "Density,"  # 密度
                               "ErrRangeMinus,"  # 误差范围负
                               "ErrRangePlus,"  # 误差范围正
                               "PreClampOffset,"  # 预夹
                               "TheoryWeiht,"  # 理论重量
                               "LengthRangeMax,"  # 最大调节范围   
                               "WeightMax ) "  # 对应重量

                               " VALUES (" + "'" +
                               SQLname + "','" +
                               self.Lne_FixLength.text() + "','" +
                               self.Lne_FixWeiht.text() + "','" +
                               self.Lne_Density.text() + "','" +
                               self.Lne_ErrRangeMinus.text() + "','" +
                               self.Lne_ErrRangePlus.text() + "','" +
                               self.Lne_PreClampOffset.text() + "','" +
                               self.Lne_TheoryWeiht.text() + "','" +
                               self.Lne_LengthRangeMax.text() + "','" +
                               self.Lne_WeightMax.text() + "');")
                conn.commit()

            except Exception as e:
                print("数据库写入错误", e)
                QtWidgets.QMessageBox.question(self, "数据库写入错误", e,
                                               QtWidgets.QMessageBox.Yes)

            else:
                QtWidgets.QMessageBox.question(self, "提示", "添加成功",
                                               QtWidgets.QMessageBox.Yes)
                self.close()
        else:
            QtWidgets.QMessageBox.question(self, "提示", "请输入参数",
                                           QtWidgets.QMessageBox.Yes)


class TeamPage(QDialog, UI_SetTeam.Ui_Dialog):  # 设置班组

    def __init__(self, parent=None):
        super(TeamPage, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.Btn_TeamNo.clicked.connect(self.close)
        self.Btn_TeamYes.clicked.connect(self.slot_ChangeLocYes)
        self.Btn_TeamYes.clicked.connect(self.close)

    def slot_ChangeLocYes(self):  # ????????????????????限制输入
        Cbb_SetTeamText = self.Cbb_SetTeam.currentText()
        window.Btn_Class.setText(Cbb_SetTeamText)  # 修改窗口显示班组

        config_ini.writeValue('init', 'Btn_Class', Cbb_SetTeamText)  # 写入config.ini文件
        window.Lab_talRoot.setText('0')
        window.Lab_talTon.setText('0')
        window.Lab_1cCount.setText('0')
        window.Lab_2cCount.setText('0')
        window.Lab_3cCount.setText('0')
        window.Lab_4cCount.setText('0')

        # 保存该班组的总根数
        config_ini.writeValue('init', 'Lab_talRoot', '0')  # 写入总根数为0
        # 保持该班组的总重量
        config_ini.writeValue('init', 'Lab_talTon', '0')  # 写入总重量为0
        # 写入流次记数清零
        config_ini.writeValue('init', 'Lab_1cCount', '0')
        config_ini.writeValue('init', 'Lab_2cCount', '0')
        config_ini.writeValue('init', 'Lab_3cCount', '0')
        config_ini.writeValue('init', 'Lab_4cCount', '0')


class ProductionDataPage(QDialog, UI_ProductionData.Ui_Dialog):  # 生产数据
    def __init__(self, parent=None):
        super(ProductionDataPage, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        # self.Btn_PrintSupport.clicked.connect(self.slot_printSupport)   # 打印
        self.Btn_excelExport.clicked.connect(self.slot_excelExport)  # 导出excel
        self.Btn_Query.clicked.connect(self.slot_ReadSQLProductionDataQuery)  # 查询
        self.autoShow()
        # self.editor = QTextEdit('默认文本',self)
        # self.editor.setGeometry(20,60,260,200)

    def autoShow(self):
        self.Det_DateRangeFrom.setDate(QDate.currentDate())  # 默认当前日期
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
                window.statuShow(e, 5)

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
        SQLbody_DateTime = " and IDtime >= '" + str(selectDateTimeFrom) + "' and IDtime <= '" + str(
            selectDateTimeTo) + "'"

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
        SQLbody_LengRange = " and FixLength >= '" + str(selectLengRangeFrom) + "' and FixLength <= '" + str(
            selectLengRangeTo) + "'"

        selectsetWeightFrom = self.Lne_SetWeightFrom.text()  # 选择的重量目标开始范围
        selectsetWeightTo = self.Lne_SetWeightTo.text()  # 选择的重量目标结束范围
        SQLbody_setWeight = " and SetWeight >= '" + str(selectsetWeightFrom) + "' and SetWeight <= '" + str(
            selectsetWeightTo) + "'"
        sqlheader = "SELECT * FROM `productiondata` WHERE 1=1 "
        try:
            sql = "" + str(sqlheader) + "" + str(SQLbody_DateTime) + "" + str(SQLbody_selectFlow) + "" + str(
                SQLbody_selectTeam) + "" + str(SQLbody_selectSteelType) + "" + str(SQLbody_LengRange) + "" + str(
                SQLbody_setWeight) + ""
            print(sql)
            cursor.execute(sql)
            fixsteelSqldata = cursor.fetchall()

            try:
                if fixsteelSqldata:
                    self.TaW_ProductionData.clear()
                    # 设置名称列数
                    self.TaW_ProductionData.setRowCount(int(len(fixsteelSqldata)))
                    # 设置种类行数
                    self.TaW_ProductionData.setColumnCount(9)
                    # 设置水平方向的表头标签与垂直方向上的表头标签，注意必须在初始化行列之后进行，否则，没有效果
                    self.TaW_ProductionData.setHorizontalHeaderLabels(
                        ["流号", "炉号", "定尺", "班次", "钢种", "实际重量", "是否称重", "设置重量", "时间"])
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
                    # print(fixsteelSqldata)  # 数据库查询中的数据
                    excelData = []
                    for i in range(len(fixsteelSqldata)):
                        excelDataColumns = []  # 初始化excel行数据
                        for j in range(len(fixsteelSqldata[i])):
                            itemContent = "%s" % (fixsteelSqldata[i][j])
                            excelDataColumns.append(itemContent)  # 增加excel单行数据

                            # 为每个表格内添加数据
                            self.TaW_ProductionData.setItem(i, j, QTableWidgetItem(itemContent))
                        excelData.append(excelDataColumns)  # 增加excel数据
                        layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.df = pd.DataFrame(excelData,
                                           columns=['流号', '炉号', '定尺', '班次', '钢种', '实际重量', '是否称重', '设置重量', '时间', '调整值',
                                                    '密度', '理论重量'])
                    self.setLayout(layout)


            except Exception as e:
                window.statuShow(e, 5)
                print("查询生产数据现场错误代码：", e)
        except Exception as e:
            window.statuShow(e, 5)
            print("查询生产数据错误代码：", e)

    def slot_setweighten(self, b):
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
        printer = QtPrintSupport.QPrinter()
        # 画布绘制出来
        painter = QtGui.QPainter()
        # 绘制的目标重定向到打印机
        painter.begin(printer)
        # 获得可视的屏幕
        screen = self.editor.grab()
        painter.drawPixmap(10, 10, screen)
        painter.end()

    def slot_excelExport(self):
        try:
            self.df.to_excel('导出生产数据.xlsx', index=False)
        except Exception as e:
            print("excel 导出错误代码：", e)


class AlgorithmPage(QDialog, UI_SetAlgorithm.Ui_Dialog):
    def __init__(self, parent=None):
        super(AlgorithmPage, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.Lne_SetCutLimt_f1.setValidator(QIntValidator(0, 900))  # 设置输入整形数字范围
        self.Lne_SetCutLimt_f2.setValidator(QIntValidator(0, 900))  # 设置输入整形数字范围
        self.Lne_SetCutLimt_f3.setValidator(QIntValidator(0, 900))  # 设置输入整形数字范围
        self.Lne_SetCutLimt_f4.setValidator(QIntValidator(0, 900))  # 设置输入整形数字范围
        self.Btn_Yes.clicked.connect(self.slot_saveDate)
        self.Btn_No.clicked.connect(self.close)
        self.AutoShow()

    def AutoShow(self):
        self.Lne_SetCutLimt_f1.setText(config_ini.readvalue('setcamre', 'setcutlimt_f1'))
        self.Lne_SetCutLimt_f2.setText(config_ini.readvalue('setcamre', 'setcutlimt_f2'))
        self.Lne_SetCutLimt_f3.setText(config_ini.readvalue('setcamre', 'setcutlimt_f3'))
        self.Lne_SetCutLimt_f4.setText(config_ini.readvalue('setcamre', 'setcutlimt_f4'))

    def slot_saveDate(self):
        config_ini.writeValue('setcamre', 'setcutlimt_f1', str(self.Lne_SetCutLimt_f1.text()))
        config_ini.writeValue('setcamre', 'setcutlimt_f2', str(self.Lne_SetCutLimt_f2.text()))
        config_ini.writeValue('setcamre', 'setcutlimt_f3', str(self.Lne_SetCutLimt_f3.text()))
        config_ini.writeValue('setcamre', 'setcutlimt_f4', str(self.Lne_SetCutLimt_f4.text()))


class SetCameraPage(QDialog, UI_SetCamera.Ui_Dialog):
    def __init__(self, parent=None):
        super(SetCameraPage, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.Btn_Exit.clicked.connect(self.close)
        self.Btn_SaveData.clicked.connect(self.slot_savedate)
        self.Lne_Threshold_f1.setValidator(QIntValidator(0, 255))  # 设置输入整形数字范围
        self.Lne_Threshold_f2.setValidator(QIntValidator(0, 255))  # 设置输入整形数字范围
        self.Lne_Threshold_f3.setValidator(QIntValidator(0, 255))  # 设置输入整形数字范围
        self.Lne_Threshold_f4.setValidator(QIntValidator(0, 255))  # 设置输入整形数字范围
        self.Lne_SetCameraFlip.setValidator(QIntValidator(-1, 2))  # 设置输入整形数字范围
        self.Lne_Threshold_ratio_f1.setValidator(QDoubleValidator())  # 设置输入浮点数字范围
        self.Lne_Threshold_ratio_f2.setValidator(QDoubleValidator())  # 设置输入浮点数字范围
        self.Lne_Threshold_ratio_f3.setValidator(QDoubleValidator())  # 设置输入浮点数字范围
        self.Lne_Threshold_ratio_f4.setValidator(QDoubleValidator())  # 设置输入浮点数字范围
        self.Btn_CameraSetAeState_auto.clicked.connect(self.slot_CameraSetAeState_auto)
        self.Btn_CameraSetAeState_man.clicked.connect(self.slot_CameraSetAeState_man)
        self.horizontalSlider_Light.valueChanged.connect(self.valChange)
        self.Ceb_Threshold_auto_f1.stateChanged.connect(self.slot_Change_Threshold_auto_1f)  # 自动阈值比的开关及输入比例值的使能
        self.Ceb_Threshold_auto_f2.stateChanged.connect(self.slot_Change_Threshold_auto_2f)
        self.Ceb_Threshold_auto_f3.stateChanged.connect(self.slot_Change_Threshold_auto_3f)
        self.Ceb_Threshold_auto_f4.stateChanged.connect(self.slot_Change_Threshold_auto_4f)

        # self.Ceb_Correct_auto_f1.stateChanged.connect(self.slot_Change_Threshold_auto_1f)  # 自动阈值比的开关及输入比例值的使能
        # self.Ceb_Correct_auto_f2.stateChanged.connect(self.slot_Change_Threshold_auto_2f)
        # self.Ceb_Correct_auto_f3.stateChanged.connect(self.slot_Change_Threshold_auto_3f)
        # self.Ceb_Correct_auto_f4.stateChanged.connect(self.slot_Change_Threshold_auto_4f)

        self.horizontalSlider_Light.setMinimum(00)  # 最小值
        self.horizontalSlider_Light.setMaximum(280)  # 最大值
        self.horizontalSlider_Light.setSingleStep(1)  # 步长
        self.horizontalSlider_Light.setTickPosition(QSlider.TicksBelow)  # 设置刻度位置，在下方
        self.horizontalSlider_Light.setTickInterval(5)  # 设置刻度间隔
        self.autoShow()

    def autoShow(self):
        try:
            self.Ceb_Threshold_auto_f4.setTristate(True)
            self.Lne_Threshold_f1.setText(config_ini.readvalue('setcamre', 'threshold_f1'))
            self.Lne_Threshold_f2.setText(config_ini.readvalue('setcamre', 'threshold_f2'))
            self.Lne_Threshold_f3.setText(config_ini.readvalue('setcamre', 'threshold_f3'))
            self.Lne_Threshold_f4.setText(config_ini.readvalue('setcamre', 'threshold_f4'))
            self.Lne_Threshold_ratio_f1.setText(config_ini.readvalue('setcamre', 'threshold_auto_1f'))
            self.Lne_Threshold_ratio_f2.setText(config_ini.readvalue('setcamre', 'threshold_auto_2f'))
            self.Lne_Threshold_ratio_f3.setText(config_ini.readvalue('setcamre', 'threshold_auto_3f'))
            self.Lne_Threshold_ratio_f4.setText(config_ini.readvalue('setcamre', 'threshold_auto_4f'))

            self.Lne_SetCameraFlip.setText(config_ini.readvalue('setcamre', 'flip'))
            self.Lab_LightValue.setNum(int(config_ini.readvalue('setcamre', 'camerasetexposuretime')))
            self.horizontalSlider_Light.setValue(int(config_ini.readvalue('setcamre', 'camerasetexposuretime')))

            if int(config_ini.readvalue('setcamre', 'camerasetaestate')) == 1:
                self.Lab_CameraSetAeState.setText('自动模式')
            elif int(config_ini.readvalue('setcamre', 'camerasetaestate')) == 0:
                self.Lab_CameraSetAeState.setText('手动模式')
            else:
                print("错误")

            # 判断自动阈值比的开关及输入比例值的使能
            if 'True' == config_ini.readvalue('setcamre', 'Ceb_Threshold_auto_1f'):
                # self.Ceb_Threshold_auto_f1.stateChanged.connect(self.slot_Change_Threshold_auto_1f)
                self.Ceb_Threshold_auto_f1.setChecked(True)
            if 'True' == config_ini.readvalue('setcamre', 'Ceb_Threshold_auto_2f'):
                # self.Ceb_Threshold_auto_f2.stateChanged.connect(self.slot_Change_Threshold_auto_1f)
                self.Ceb_Threshold_auto_f2.setChecked(True)
            if 'True' == config_ini.readvalue('setcamre', 'Ceb_Threshold_auto_3f'):
                # self.Ceb_Threshold_auto_f3.stateChanged.connect(self.slot_Change_Threshold_auto_1f)
                self.Ceb_Threshold_auto_f3.setChecked(True)
            if 'True' == config_ini.readvalue('setcamre', 'Ceb_Threshold_auto_4f'):
                # self.Ceb_Threshold_auto_f4.stateChanged.connect(self.slot_Change_Threshold_auto_1f)
                self.Ceb_Threshold_auto_f4.setChecked(True)


            # 判断自动调整的使能
            if 'True' == config_ini.readvalue('setcamre', 'Ceb_Correct_auto_f1'):
                # self.Ceb_Threshold_auto_f1.stateChanged.connect(self.slot_Change_Threshold_auto_1f)
                self.Ceb_Correct_auto_f1.setChecked(True)
            if 'True' == config_ini.readvalue('setcamre', 'Ceb_Correct_auto_f2'):
                # self.Ceb_Threshold_auto_f2.stateChanged.connect(self.slot_Change_Threshold_auto_1f)
                self.Ceb_Correct_auto_f2.setChecked(True)
            if 'True' == config_ini.readvalue('setcamre', 'Ceb_Correct_auto_f3'):
                # self.Ceb_Threshold_auto_f3.stateChanged.connect(self.slot_Change_Threshold_auto_1f)
                self.Ceb_Correct_auto_f3.setChecked(True)
            if 'True' == config_ini.readvalue('setcamre', 'Ceb_Correct_auto_f4'):
                # self.Ceb_Threshold_auto_f4.stateChanged.connect(self.slot_Change_Threshold_auto_1f)
                self.Ceb_Correct_auto_f4.setChecked(True)

            # print(self.Ceb_Threshold_auto_f4.isChecked())  # 判断被选择中状态
            # print(self.Ceb_Threshold_auto_f4.checkState())  # 来判断当前状态

        except Exception as e:
            print("相机设置刷新错误代码：", e)

    # 调整亮度函数
    def valChange(self):
        self.Lab_LightValue.setNum(self.horizontalSlider_Light.value())  # 注意这里别setText 会卡死
        try:
            config_ini.writeValue('setcamre', 'camerasetexposuretime', str(self.horizontalSlider_Light.value()))
            mvsdk.CameraSetExposureTime(hCamera, int(config_ini.readvalue('setcamre', 'camerasetexposuretime')) * 1000)
            mvsdk.CameraSaveParameter(hCamera, 0)
            print(int(config_ini.readvalue('setcamre', 'camerasetexposuretime')) * 1000)
        except Exception as e:
            print("调整亮度函数错误:", e)
            QtWidgets.QMessageBox.question(self, "提示", "调整亮度函数错误",
                                           QtWidgets.QMessageBox.Yes)
        # self.Lab_LightValue.setFont(QFont("微软雅黑", self.horizontalSlider_Light.value()))

    # 调整亮度自动
    def slot_CameraSetAeState_auto(self):
        config_ini.writeValue('setcamre', 'camerasetaestate', '1')
        mvsdk.CameraSetAeState(hCamera, int(config_ini.readvalue('setcamre', 'camerasetaestate')))
        mvsdk.CameraSaveParameter(hCamera, 0)
        self.autoShow()

    # 调整亮度手动
    def slot_CameraSetAeState_man(self):
        config_ini.writeValue('setcamre', 'camerasetaestate', '0')
        mvsdk.CameraSetAeState(hCamera, int(config_ini.readvalue('setcamre', 'camerasetaestate')))
        mvsdk.CameraSaveParameter(hCamera, 0)
        self.autoShow()

    # 修改阈值比例输入的使能
    def slot_Change_Threshold_auto_1f(self, b):  # b勾选编辑
        self.Lne_Threshold_ratio_f1.setEnabled(b)
    def slot_Change_Threshold_auto_2f(self, b):  # b勾选编辑
        self.Lne_Threshold_ratio_f2.setEnabled(b)
    def slot_Change_Threshold_auto_3f(self, b):  # b勾选编辑
        self.Lne_Threshold_ratio_f3.setEnabled(b)
    def slot_Change_Threshold_auto_4f(self, b):  # b勾选编辑
        self.Lne_Threshold_ratio_f4.setEnabled(b)



    # 保存阈值
    def slot_savedate(self):
        try:
            if (0 <= int(self.Lne_Threshold_f1.text()) and int(self.Lne_Threshold_f1.text()) <= 255) and (
                    0 <= int(self.Lne_Threshold_f2.text()) and int(self.Lne_Threshold_f2.text()) <= 255) and (
                    0 <= int(self.Lne_Threshold_f3.text()) and int(self.Lne_Threshold_f3.text()) <= 255) and (
                    0 <= int(self.Lne_Threshold_f4.text()) and int(self.Lne_Threshold_f4.text()) <= 255) and len(
                    self.Lne_SetCameraFlip.text()) > 0:
                config_ini.writeValue('setcamre', 'threshold_f1', self.Lne_Threshold_f1.text())
                config_ini.writeValue('setcamre', 'threshold_f2', self.Lne_Threshold_f2.text())
                config_ini.writeValue('setcamre', 'threshold_f3', self.Lne_Threshold_f3.text())
                config_ini.writeValue('setcamre', 'threshold_f4', self.Lne_Threshold_f4.text())
                config_ini.writeValue('setcamre', 'flip', self.Lne_SetCameraFlip.text())
                config_ini.writeValue('setcamre', 'Ceb_Threshold_auto_1f', str(self.Ceb_Threshold_auto_f1.isChecked()))
                config_ini.writeValue('setcamre', 'Ceb_Threshold_auto_2f', str(self.Ceb_Threshold_auto_f2.isChecked()))
                config_ini.writeValue('setcamre', 'Ceb_Threshold_auto_3f', str(self.Ceb_Threshold_auto_f3.isChecked()))
                config_ini.writeValue('setcamre', 'Ceb_Threshold_auto_4f', str(self.Ceb_Threshold_auto_f4.isChecked()))
                config_ini.writeValue('setcamre', 'threshold_auto_1f', self.Lne_Threshold_ratio_f1.text())
                config_ini.writeValue('setcamre', 'threshold_auto_2f', self.Lne_Threshold_ratio_f2.text())
                config_ini.writeValue('setcamre', 'threshold_auto_3f', self.Lne_Threshold_ratio_f3.text())
                config_ini.writeValue('setcamre', 'threshold_auto_4f', self.Lne_Threshold_ratio_f4.text())

                config_ini.writeValue('setcamre', 'ceb_correct_auto_f1', str(self.Ceb_Correct_auto_f1.isChecked()))
                config_ini.writeValue('setcamre', 'ceb_correct_auto_f2', str(self.Ceb_Correct_auto_f2.isChecked()))
                config_ini.writeValue('setcamre', 'ceb_correct_auto_f3', str(self.Ceb_Correct_auto_f3.isChecked()))
                config_ini.writeValue('setcamre', 'ceb_correct_auto_f4', str(self.Ceb_Correct_auto_f4.isChecked()))

            else:
                QtWidgets.QMessageBox.question(self, "提示", "输入数值不正确",
                                               QtWidgets.QMessageBox.Yes)
        except Exception as e:
            print("调整曝光值拉条错误代码：", e)


class SetSteelTypePage(QDialog, UI_SetSteelType.Ui_Dialog):
    def __init__(self, parent=None):
        super(SetSteelTypePage, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        try:
            self.Btn_addSteelType.clicked.connect(self.slot_addSteelType)  # 新增钢种
            self.Btn_changeSteelDensity.clicked.connect(self.slot_changesteeldensity)  # 修改钢种密度
            self.Btn_Exit.clicked.connect(self.close)  # 退出
            self.Btn_delSteelType.clicked.connect(self.slot_delsteeltype)  # 删除项
            self.LW_SteelType.setSelectionMode(QAbstractItemView.SingleSelection)  # 单项处理
            self.LW_SteelType.itemClicked.connect(self.slot_SetFurNoItemCliked)  # 单击触发 提示
            self.LW_SteelType.currentItemChanged.connect(self.slot_setFurNoItemDoubleClicked)  # 选中项前后字体变色
            self.Btn_CheckSteelDensity.clicked.connect(self.slot_checkSteelDensity)  # 查看钢种密度
            self.Btn_changeSteelType.clicked.connect(self.slot_changeSteelType)  # 更换钢种
            self.autoShow()
        except Exception as e:
            print("钢坯钢种错误代码", e)

    def autoShow(self):
        # 读取config 钢种
        configSteelType = config_ini.readvalue('init', 'lab_1csteels')
        self.Lab_showSteelType.setText(str(configSteelType))
        self.LW_SteelType.clear()
        sql_sqlreadsteeltypevalue = SQLlite.SQL_readSteeltype()  # 读取数据库里的钢种信息
        if sql_sqlreadsteeltypevalue == 0:
            print("数据为空")
        else:
            # 显示出mysql中所有的钢种名称
            for sqlreadsteeltypevalue in range(len(sql_sqlreadsteeltypevalue)):
                self.LW_SteelType.addItem(sql_sqlreadsteeltypevalue[sqlreadsteeltypevalue][0])

    def slot_addSteelType(self):
        addsteeltype = AddSteelTypePage()
        if addsteeltype.exec_() == 0:
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
        SQLlite.SQL_delSteeltype(self.LW_SteelType.item(idx).text())  # 删除mysql中的数据
        print(self.LW_SteelType.item(idx).text())
        self.LW_SteelType.takeItem(idx)  # 移除选中的项

    def slot_changesteeldensity(self):
        # global temp_changesteelDensityname
        pItem = self.LW_SteelType.currentItem()  # 得到左侧列表选中项
        if pItem is None:
            QtWidgets.QMessageBox.question(self, "提示", "请选择钢种名称",
                                           QtWidgets.QMessageBox.Yes)
            return
        idx = self.LW_SteelType.row(pItem)  # 得到项的序号  所在行 idx =>int
        public['temp_changesteelDensityname'] = self.LW_SteelType.item(idx).text()
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

    def slot_SetFurNoItemCliked(self, item):  # 选中项触发字体变化  item
        ft = item.font()
        ft.setBold(True)
        item.setFont(ft)

    def slot_setFurNoItemDoubleClicked(self, current, previous):  # current 新选中的项  previous之前选中的项
        # 将之前选中的字体粗体恢复
        if not (previous is None):
            ft = previous.font()
            ft.setBold(False)
            previous.setFont(ft)


class AddSteelTypePage(QDialog, UI_AddSteelType.Ui_Dialog):  # 增加钢种类型页面
    def __init__(self, parent=None):
        super(AddSteelTypePage, self).__init__(parent)
        self.setupUi(self)

        try:
            self.Btn_No.clicked.connect(self.close)
            self.Lne_steelDensity.setValidator(QDoubleValidator())  # 设置输入浮点数字范围
            self.Btn_Yes.clicked.connect(self.slot_saveSteelType)
        except Exception as e:
            print("增加钢种种类错误代码:", e)

    # 新增钢种名称及密度
    def slot_saveSteelType(self):
        if len(self.Lne_steelName.text()) > 0 and len(self.Lne_steelDensity.text()) > 0 and float(
                self.Lne_steelDensity.text()) > 6:
            try:
                SQLlite.SQL_addSteelType('钢种名称', '钢种密度', value1=str(self.Lne_steelName.text()),
                                         value2=self.Lne_steelDensity.text())
                QtWidgets.QMessageBox.question(self, "提示", "添加成功",
                                               QtWidgets.QMessageBox.Yes)
                # 更新列表listwidget
                self.close()

            except Exception as e:
                QtWidgets.QMessageBox.question(self, "提示", e,
                                               QtWidgets.QMessageBox.Yes)
        elif len(self.Lne_steelName.text()) > 0 and len(self.Lne_steelDensity.text()) > 0 and float(
                self.Lne_steelDensity.text()) <= 6:
            QtWidgets.QMessageBox.question(self, "提示", "输入钢种密度过低",
                                           QtWidgets.QMessageBox.Yes)
        else:
            QtWidgets.QMessageBox.question(self, "提示", "请输入钢种名称及密度",
                                           QtWidgets.QMessageBox.Yes)


class ChangeSteelTypeDensityPage(QDialog, UI_ChangeSteelTypeDensity.Ui_Dialog):  # 修改钢种密度页面
    def __init__(self, parent=None):
        super(ChangeSteelTypeDensityPage, self).__init__(parent)
        self.setupUi(self)
        self.Lab_showSteelTypename.setText(public['temp_changesteelDensityname'])
        self.Lne_steelDensity.setValidator(QDoubleValidator())  # 设置输入浮点数字范围
        self.Btn_No.clicked.connect(self.close)
        self.Btn_Yes.clicked.connect(self.slot_changeSteelTypeDensity)

    def slot_changeSteelTypeDensity(self):
        # global temp_changesteelDensityname
        if len(self.Lne_steelDensity.text()) > 0 and float(self.Lne_steelDensity.text()) > 6:
            SQLlite.SQL_updataSteeltype(str(public['temp_changesteelDensityname']), self.Lne_steelDensity.text())
            QtWidgets.QMessageBox.question(self, "提示", "钢种密度修改成功",
                                           QtWidgets.QMessageBox.Yes)
            self.close()
        elif len(self.Lne_steelDensity.text()) == 0:
            QtWidgets.QMessageBox.question(self, "提示", "请输入密度",
                                           QtWidgets.QMessageBox.Yes)
        else:
            print("数据过小")
            QtWidgets.QMessageBox.question(self, "提示", "输入数据过小",
                                           QtWidgets.QMessageBox.Yes)


class CheckSteelTypeDensityPage(QDialog, UI_CheckSteelTypeDensity.Ui_Dialog):
    def __init__(self, parent=None):
        super(CheckSteelTypeDensityPage, self).__init__(parent)
        self.setupUi(self)
        try:
            self.Btn_Exit.clicked.connect(self.close)
            self.autoShow()
        except Exception as e:
            print("查看钢种密度错误代码：", e)

    def autoShow(self):
        try:
            self.TaW_CheckSteelDensity.clear()
            sql_sqlreadsteeltypevalue = SQLlite.SQL_readSteeltype()  # 读取数据库里的钢种信息
            if sql_sqlreadsteeltypevalue == 0:
                print("数据为空")
            else:
                # 显示出mysql中所有的钢种名称
                print('种类行长度:', len(sql_sqlreadsteeltypevalue))
                print('数据列长度:', len(sql_sqlreadsteeltypevalue[0]))
                # 设置名称列数
                self.TaW_CheckSteelDensity.setRowCount(int(len(sql_sqlreadsteeltypevalue)))
                # 设置种类行数
                self.TaW_CheckSteelDensity.setColumnCount(int(len(sql_sqlreadsteeltypevalue[0])))
                # 设置水平方向的表头标签与垂直方向上的表头标签，注意必须在初始化行列之后进行，否则，没有效果
                self.TaW_CheckSteelDensity.setHorizontalHeaderLabels(["钢种类型", "钢种密度"])
                # 禁止编辑
                self.TaW_CheckSteelDensity.setEditTriggers(QAbstractItemView.NoEditTriggers)
                # TODO 优化 2 设置水平方向表格为自适应的伸缩模式
                self.TaW_CheckSteelDensity.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

                self.TaW_CheckSteelDensity.setColumnWidth(0, 160)  # 将第一列的单元宽度设置为160
                self.TaW_CheckSteelDensity.setColumnWidth(1, 161)  # 将第二列的单元宽度设置为160
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
            print("刷新钢种密度错误代码：", e)


class SetSteelDataPage(QDialog, UI_SetSteelData.Ui_Dialog):

    def __init__(self, parent=None):
        super(SetSteelDataPage, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.Btn_Exit.clicked.connect(self.close)  # 退出
        self.Btn_addLength.clicked.connect(self.slot_addLength)  # 添加所选定尺
        self.Btn_delLength.clicked.connect(self.slot_delLength)  # 删除所选定尺
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
            # sql = 'SELECT * FROM `fixsteeldata`'
            sql = 'SELECT * FROM `fixsteeldata` ORDER BY fixlength ASC'
            cursor.execute(sql)
            # conn.commit()
            fixsteeldatadata = cursor.fetchall()

            if fixsteeldatadata:
                self.LW_lengthType.clear()
                for row, form in enumerate(fixsteeldatadata):
                    self.LW_lengthType.addItem(str(form[0]))

        except Exception as e:
            QtWidgets.QMessageBox.question(self, "提示", e,
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

            sql = "DELETE FROM fixsteeldata WHERE SteelName = '" + pItem.text() + "';"
            cursor.execute(sql)
            conn.commit()
            self.autoShow()

        except Exception as e:
            QtWidgets.QMessageBox.question(self, "提示", e,
                                           QtWidgets.QMessageBox.Yes)

    def slot_changelength(self):  # 修改定尺
        pItem = self.LW_lengthType.currentItem()
        if pItem is None:
            return
        idx = self.LW_lengthType.row(pItem)
        public['temp_changesteelFixleng'] = self.LW_lengthType.item(idx).text()
        changeSteelDate = ChangeFixLengPage()
        if changeSteelDate.exec_() == 0:
            self.autoShow()

    def slot_switchlength(self):  # 切换定尺
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
                        config_ini.writeValue('init', 'btn_1asetweight', str(switchlengdata[switchleng][2]))
                        config_ini.writeValue('init', 'btn_2asetweight', str(switchlengdata[switchleng][2]))
                        config_ini.writeValue('init', 'btn_3asetweight', str(switchlengdata[switchleng][2]))
                        config_ini.writeValue('init', 'btn_4asetweight', str(switchlengdata[switchleng][2]))
                        config_ini.writeValue('init', 'Lab_1cSetPos', str(switchlengdata[switchleng][7]))  # 预夹
                        config_ini.writeValue('init', 'Lab_2cSetPos', str(switchlengdata[switchleng][7]))
                        config_ini.writeValue('init', 'Lab_3cSetPos', str(switchlengdata[switchleng][7]))
                        config_ini.writeValue('init', 'Lab_4cSetPos', str(switchlengdata[switchleng][7]))

                        # 合格重量范围， 指定重量  设置重量- 偏差   设定重量 + 偏差
                        config_ini.writeValue('init', 'lab_1brange', str(
                            float(switchlengdata[switchleng][2]) - float(switchlengdata[switchleng][5])) + "~" + str(
                            (float(switchlengdata[switchleng][6])) + float(switchlengdata[switchleng][2])))
                        config_ini.writeValue('init', 'lab_2brange', str(
                            float(switchlengdata[switchleng][2]) - float(switchlengdata[switchleng][5])) + "~" + str(
                            (float(switchlengdata[switchleng][6])) + float(switchlengdata[switchleng][2])))
                        config_ini.writeValue('init', 'lab_3brange', str(
                            float(switchlengdata[switchleng][2]) - float(switchlengdata[switchleng][5])) + "~" + str(
                            (float(switchlengdata[switchleng][6])) + float(switchlengdata[switchleng][2])))
                        config_ini.writeValue('init', 'lab_4brange', str(
                            float(switchlengdata[switchleng][2]) - float(switchlengdata[switchleng][5])) + "~" + str(
                            (float(switchlengdata[switchleng][6])) + float(switchlengdata[switchleng][2])))
                        # 称重范围值
                        config_ini.writeValue('init', 'lab_1ErrRangeMinus', str(float(switchlengdata[switchleng][5])))
                        config_ini.writeValue('init', 'lab_1ErrRangePlus', str(float(switchlengdata[switchleng][6])))
                        config_ini.writeValue('init', 'lab_2ErrRangeMinus', str(float(switchlengdata[switchleng][5])))
                        config_ini.writeValue('init', 'lab_2ErrRangePlus', str(float(switchlengdata[switchleng][6])))
                        config_ini.writeValue('init', 'lab_3ErrRangeMinus', str(float(switchlengdata[switchleng][5])))
                        config_ini.writeValue('init', 'lab_3ErrRangePlus', str(float(switchlengdata[switchleng][6])))
                        config_ini.writeValue('init', 'lab_4ErrRangeMinus', str(float(switchlengdata[switchleng][5])))
                        config_ini.writeValue('init', 'lab_4ErrRangePlus', str(float(switchlengdata[switchleng][6])))



            except Exception as e:
                print("切换定尺错误代码：", e)
            else:
                window.autoShow()
        except Exception as e:
            QtWidgets.QMessageBox.question(self, "提示", e,
                                           QtWidgets.QMessageBox.Yes)

    def slot_takeItem(self):  # 删除定尺信息
        pItem = self.LW_lengthType.currentItem()
        if pItem is None:
            return
        idx = self.LW_lengthType.row(pItem)
        self.LW_lengthType.takeItem(idx)

    def slot_SetFurNoItemCliked(self, item):  # 选中项触发字体变化  item
        ft = item.font()
        ft.setBold(True)
        item.setFont(ft)

    def slot_setFurNoItemDoubleClicked(self, current, previous):  # current 新选中的项  previous之前选中的项
        # 将之前选中的字体粗体恢复
        if not (previous is None):
            ft = previous.font()
            ft.setBold(False)
            previous.setFont(ft)


class ChangeFixLengPage(QDialog, UI_ChangeFixLeng.Ui_Dialog):
    def __init__(self, parent=None):
        super(ChangeFixLengPage, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
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
            data = cursor.fetchall()
            for fixleng in range(len(data)):
                # 读取选中的信息，显示到页面
                if public['temp_changesteelFixleng'] == data[fixleng][0]:
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
            print("修改定重数据错误代码：", e)

    # 保存定尺修改内容
    def slot_saveChangeFixLengDate(self):

        try:
            sql = "SELECT * FROM `fixsteeldata` where SteelName = '" + str(public['temp_changesteelFixleng']) + "'"
            cursor.execute(sql)
            changefixleng = cursor.fetchall()
            print(changefixleng)
            print(changefixleng[0][1])
            if changefixleng:
                SQLname = str(self.Lab_ReadLeng.text()) + ' 预夹=' + str(
                    self.Lne_PreClampOffset.text()) + ' 定重目标=' + str(self.Lne_FixWeiht.text())

                sql = "UPDATE fixsteeldata SET SteelName = '" + str(SQLname) + "' , FixWeiht= " + str(
                    self.Lne_FixWeiht.text()) + ", Density= " + str(
                    self.Lne_Density.text()) + ", ErrRangeMinus= " + str(
                    self.Lne_ErrRangeMinus.text()) + ", ErrRangePlus= " + str(
                    self.Lne_ErrRangePlus.text()) + ", PreClampOffset = " + str(
                    self.Lne_PreClampOffset.text()) + ", TheoryWeiht = " + str(
                    self.Lne_TheoryWeiht.text()) + ", LengthRangeMax = " + str(
                    self.Lne_LengthRangeMax.text()) + " ,WeightMax = " + str(
                    self.Lne_WeightMax.text()) + " WHERE FixLength = '" + str(changefixleng[0][1]) + "'"
                print(sql)
                cursor.execute(sql)
                conn.commit()

        except Exception as e:
            print("修改保存定重数据错误代码:", e)
        finally:
            self.close()


class SetCalibratePage(QDialog, UI_SetCalibrate.Ui_Dialog):
    def __init__(self, parent=None):
        super(SetCalibratePage, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.Lne_Frame_cut_X0.setValidator(QIntValidator(0, 65535))  # 设置输入整形数字范围
        self.Lne_Frame_cut_Y0.setValidator(QIntValidator(0, 65535))  # 设置输入整形数字范围
        self.Lne_Frame_cut_X1.setValidator(QIntValidator(0, 65535))  # 设置输入整形数字范围
        self.Lne_Frame_cut_Y1.setValidator(QIntValidator(0, 65535))  # 设置输入整形数字范围
        self.Lne_ReFrame_X.setValidator(QIntValidator(0, 900))  # 设置输入整形数字范围
        self.Lne_ReFrame_Y.setValidator(QIntValidator(0, 480))  # 设置输入整形数字范围
        self.Lne_Frame_cut_X0_F1.setValidator(QIntValidator(0, 900))  # 设置输入整形数字范围
        self.Lne_Frame_cut_X1_F1.setValidator(QIntValidator(0, 900))  # 设置输入整形数字范围
        self.Lne_Frame_cut_Y0_F1.setValidator(QIntValidator(0, 480))  # 设置输入整形数字范围
        self.Lne_Frame_cut_Y1_F1.setValidator(QIntValidator(0, 480))  # 设置输入整形数字范围
        self.Lne_Frame_cut_X0_F2.setValidator(QIntValidator(0, 900))  # 设置输入整形数字范围
        self.Lne_Frame_cut_X1_F2.setValidator(QIntValidator(0, 900))  # 设置输入整形数字范围
        self.Lne_Frame_cut_Y0_F2.setValidator(QIntValidator(0, 480))  # 设置输入整形数字范围
        self.Lne_Frame_cut_Y1_F2.setValidator(QIntValidator(0, 480))  # 设置输入整形数字范围
        self.Lne_Frame_cut_X0_F3.setValidator(QIntValidator(0, 900))  # 设置输入整形数字范围
        self.Lne_Frame_cut_X1_F3.setValidator(QIntValidator(0, 900))  # 设置输入整形数字范围
        self.Lne_Frame_cut_Y0_F3.setValidator(QIntValidator(0, 480))  # 设置输入整形数字范围
        self.Lne_Frame_cut_Y1_F3.setValidator(QIntValidator(0, 480))  # 设置输入整形数字范围
        self.Lne_Frame_cut_X0_F4.setValidator(QIntValidator(0, 900))  # 设置输入整形数字范围
        self.Lne_Frame_cut_X1_F4.setValidator(QIntValidator(0, 900))  # 设置输入整形数字范围
        self.Lne_Frame_cut_Y0_F4.setValidator(QIntValidator(0, 480))  # 设置输入整形数字范围
        self.Lne_Frame_cut_Y1_F4.setValidator(QIntValidator(0, 480))  # 设置输入整形数字范围
        self.Lne_Frame_cut_F1_angle.setValidator(QIntValidator(10, 120))
        self.Lne_Frame_cut_F2_angle.setValidator(QIntValidator(10, 120))
        self.Lne_Frame_cut_F3_angle.setValidator(QIntValidator(10, 120))
        self.Lne_Frame_cut_F4_angle.setValidator(QIntValidator(10, 120))
        self.Lne_Frame_cut_X1_F1_11.setValidator(QIntValidator(0, 900))  # 设置输入整形数字范围
        self.Lne_Frame_cut_X1_F2_11.setValidator(QIntValidator(0, 900))  # 设置输入整形数字范围
        self.Lne_Frame_cut_X1_F3_11.setValidator(QIntValidator(0, 900))  # 设置输入整形数字范围
        self.Lne_Frame_cut_X1_F4_11.setValidator(QIntValidator(0, 900))  # 设置输入整形数字范围
        self.Lne_Frame_cut_X1_F1_12.setValidator(QIntValidator(0, 900))  # 设置输入整形数字范围
        self.Lne_Frame_cut_X1_F2_12.setValidator(QIntValidator(0, 900))  # 设置输入整形数字范围
        self.Lne_Frame_cut_X1_F3_12.setValidator(QIntValidator(0, 900))  # 设置输入整形数字范围
        self.Lne_Frame_cut_X1_F4_12.setValidator(QIntValidator(0, 900))  # 设置输入整形数字范围
        self.Lne_Frame_cut_X1_F1_13.setValidator(QIntValidator(0, 900))  # 设置输入整形数字范围
        self.Lne_Frame_cut_X1_F2_13.setValidator(QIntValidator(0, 900))  # 设置输入整形数字范围
        self.Lne_Frame_cut_X1_F3_13.setValidator(QIntValidator(0, 900))  # 设置输入整形数字范围
        self.Lne_Frame_cut_X1_F4_13.setValidator(QIntValidator(0, 900))  # 设置输入整形数字范围

        # self.Lne_Frame_cut_F4_angle.setValidator(QDoubleValidator())  # 设置输入浮点数字范围

        self.Lab_Camre_X.setText(config_ini.readvalue('setcamre', 'camre_x'))
        self.Lab_Camre_Y.setText(config_ini.readvalue('setcamre', 'camre_y'))
        self.Btn_SaveCutData.clicked.connect(self.slot_savesetcamrecutdata)
        self.Btn_SaveReData.clicked.connect(self.slot_savesetcamreredata)
        self.Btn_SaveFlowData.clicked.connect(self.slot_savesetflowdata)
        self.Btn_SaveProofreadingData.clicked.connect(self.slot_saveproofreadingdata)
        self.autoShow()

    def autoShow(self):
        self.Lne_Frame_cut_X0.setText(str(config_ini.readvalue('setcamre', 'frame_cut_x0')))
        self.Lne_Frame_cut_Y0.setText(str(config_ini.readvalue('setcamre', 'frame_cut_y0')))
        self.Lne_Frame_cut_X1.setText(str(config_ini.readvalue('setcamre', 'frame_cut_x1')))
        self.Lne_Frame_cut_Y1.setText(str(config_ini.readvalue('setcamre', 'frame_cut_y1')))
        self.Lne_ReFrame_X.setText(str(config_ini.readvalue('setcamre', 'reframe_x')))
        self.Lne_ReFrame_Y.setText(str(config_ini.readvalue('setcamre', 'reframe_y')))
        self.Lne_Frame_cut_X0_F1.setText(str(config_ini.readvalue('setcamre', 'frame_cut_x0_f1')))
        self.Lne_Frame_cut_Y0_F1.setText(str(config_ini.readvalue('setcamre', 'frame_cut_y0_f1')))
        self.Lne_Frame_cut_X1_F1.setText(str(config_ini.readvalue('setcamre', 'frame_cut_x1_f1')))
        self.Lne_Frame_cut_Y1_F1.setText(str(config_ini.readvalue('setcamre', 'frame_cut_y1_f1')))
        self.Lne_Frame_cut_X0_F2.setText(str(config_ini.readvalue('setcamre', 'frame_cut_x0_f2')))
        self.Lne_Frame_cut_Y0_F2.setText(str(config_ini.readvalue('setcamre', 'frame_cut_y0_f2')))
        self.Lne_Frame_cut_X1_F2.setText(str(config_ini.readvalue('setcamre', 'frame_cut_x1_f2')))
        self.Lne_Frame_cut_Y1_F2.setText(str(config_ini.readvalue('setcamre', 'frame_cut_y1_f2')))
        self.Lne_Frame_cut_X0_F3.setText(str(config_ini.readvalue('setcamre', 'frame_cut_x0_f3')))
        self.Lne_Frame_cut_Y0_F3.setText(str(config_ini.readvalue('setcamre', 'frame_cut_y0_f3')))
        self.Lne_Frame_cut_X1_F3.setText(str(config_ini.readvalue('setcamre', 'frame_cut_x1_f3')))
        self.Lne_Frame_cut_Y1_F3.setText(str(config_ini.readvalue('setcamre', 'frame_cut_y1_f3')))
        self.Lne_Frame_cut_X0_F4.setText(str(config_ini.readvalue('setcamre', 'frame_cut_x0_f4')))
        self.Lne_Frame_cut_Y0_F4.setText(str(config_ini.readvalue('setcamre', 'frame_cut_y0_f4')))
        self.Lne_Frame_cut_X1_F4.setText(str(config_ini.readvalue('setcamre', 'frame_cut_x1_f4')))
        self.Lne_Frame_cut_Y1_F4.setText(str(config_ini.readvalue('setcamre', 'frame_cut_y1_f4')))
        self.Lne_Frame_cut_F1_angle.setText(str(config_ini.readvalue('setcamre', 'frame_cut_f1_angle')))
        self.Lne_Frame_cut_F2_angle.setText(str(config_ini.readvalue('setcamre', 'frame_cut_f2_angle')))
        self.Lne_Frame_cut_F3_angle.setText(str(config_ini.readvalue('setcamre', 'frame_cut_f3_angle')))
        self.Lne_Frame_cut_F4_angle.setText(str(config_ini.readvalue('setcamre', 'frame_cut_f4_angle')))
        self.Lne_Frame_cut_X1_F1_11.setText(str(config_ini.readvalue('setcamre', 'frame_cut_x1_f1_11')))
        self.Lne_Frame_cut_X1_F2_11.setText(str(config_ini.readvalue('setcamre', 'frame_cut_x1_f2_11')))
        self.Lne_Frame_cut_X1_F3_11.setText(str(config_ini.readvalue('setcamre', 'frame_cut_x1_f3_11')))
        self.Lne_Frame_cut_X1_F4_11.setText(str(config_ini.readvalue('setcamre', 'frame_cut_x1_f4_11')))
        self.Lne_Frame_cut_X1_F1_12.setText(str(config_ini.readvalue('setcamre', 'frame_cut_x1_f1_12')))
        self.Lne_Frame_cut_X1_F2_12.setText(str(config_ini.readvalue('setcamre', 'frame_cut_x1_f2_12')))
        self.Lne_Frame_cut_X1_F3_12.setText(str(config_ini.readvalue('setcamre', 'frame_cut_x1_f3_12')))
        self.Lne_Frame_cut_X1_F4_12.setText(str(config_ini.readvalue('setcamre', 'frame_cut_x1_f4_12')))
        self.Lne_Frame_cut_X1_F1_13.setText(str(config_ini.readvalue('setcamre', 'frame_cut_x1_f1_13')))
        self.Lne_Frame_cut_X1_F2_13.setText(str(config_ini.readvalue('setcamre', 'frame_cut_x1_f2_13')))
        self.Lne_Frame_cut_X1_F3_13.setText(str(config_ini.readvalue('setcamre', 'frame_cut_x1_f3_13')))
        self.Lne_Frame_cut_X1_F4_13.setText(str(config_ini.readvalue('setcamre', 'frame_cut_x1_f4_13')))

    # 保存切割图片坐标
    def slot_savesetcamrecutdata(self):
        if int(self.Lne_Frame_cut_X0.text()) > int(self.Lab_Camre_X.text()) or int(self.Lne_Frame_cut_Y0.text()) > int(
                self.Lab_Camre_Y.text()) or int(self.Lne_Frame_cut_X1.text()) > int(self.Lab_Camre_X.text()) or int(
                self.Lne_Frame_cut_Y1.text()) > int(self.Lab_Camre_Y.text()):
            QtWidgets.QMessageBox.question(self, "提示", "输入范围超出",
                                           QtWidgets.QMessageBox.Yes)
        else:
            config_ini.writeValue('setcamre', 'frame_cut_x1', str(self.Lne_Frame_cut_X1.text()))
            config_ini.writeValue('setcamre', 'frame_cut_y1', str(self.Lne_Frame_cut_Y1.text()))
            if int(self.Lne_Frame_cut_X1. text()) > int(self.Lne_Frame_cut_X0.text()) and int(
                    self.Lne_Frame_cut_Y1.text()) > int(self.Lne_Frame_cut_Y0.text()):
                config_ini.writeValue('setcamre', 'frame_cut_x0', str(self.Lne_Frame_cut_X0.text()))
                config_ini.writeValue('setcamre', 'frame_cut_y0', str(self.Lne_Frame_cut_Y0.text()))
            else:
                QtWidgets.QMessageBox.question(self, "提示", "输入范围超出",
                                               QtWidgets.QMessageBox.Yes)

    # 保存重组图片尺寸
    def slot_savesetcamreredata(self):
        if int(self.Lne_ReFrame_X.text()) > 900 or int(self.Lne_ReFrame_Y.text()) > 480:
            QtWidgets.QMessageBox.question(self, "提示", "输入范围超出",
                                           QtWidgets.QMessageBox.Yes)
        else:
            config_ini.writeValue('setcamre', 'reframe_x', str(self.Lne_ReFrame_X.text()))
            config_ini.writeValue('setcamre', 'reframe_y', str(self.Lne_ReFrame_Y.text()))

    # 保存流点位坐标
    def slot_savesetflowdata(self):
        if float(self.Lne_Frame_cut_Y0_F1.text()) > float(self.Lne_Frame_cut_F1_angle.text()) and float(
                self.Lne_Frame_cut_Y0_F2.text()) > float(self.Lne_Frame_cut_F2_angle.text()) and float(
                self.Lne_Frame_cut_Y0_F3.text()) > float(self.Lne_Frame_cut_F3_angle.text()) and float(
                self.Lne_Frame_cut_Y0_F4.text()) > float(self.Lne_Frame_cut_F4_angle.text()) and float(
                self.Lne_Frame_cut_Y1_F1.text()) > float(self.Lne_Frame_cut_F1_angle.text()) and float(
                self.Lne_Frame_cut_Y1_F2.text()) > float(self.Lne_Frame_cut_F2_angle.text()) and float(
                self.Lne_Frame_cut_Y1_F3.text()) > float(self.Lne_Frame_cut_F3_angle.text()) and float(
                self.Lne_Frame_cut_Y1_F4.text()) > float(self.Lne_Frame_cut_F4_angle.text()):
            config_ini.writeValue('setcamre', 'frame_cut_x0_f1', str(self.Lne_Frame_cut_X0_F1.text()))
            config_ini.writeValue('setcamre', 'frame_cut_y0_f1', str(self.Lne_Frame_cut_Y0_F1.text()))
            config_ini.writeValue('setcamre', 'frame_cut_x1_f1', str(self.Lne_Frame_cut_X1_F1.text()))
            config_ini.writeValue('setcamre', 'frame_cut_y1_f1', str(self.Lne_Frame_cut_Y1_F1.text()))
            config_ini.writeValue('setcamre', 'frame_cut_x0_f2', str(self.Lne_Frame_cut_X0_F2.text()))
            config_ini.writeValue('setcamre', 'frame_cut_y0_f2', str(self.Lne_Frame_cut_Y0_F2.text()))
            config_ini.writeValue('setcamre', 'frame_cut_x1_f2', str(self.Lne_Frame_cut_X1_F2.text()))
            config_ini.writeValue('setcamre', 'frame_cut_y1_f2', str(self.Lne_Frame_cut_Y1_F2.text()))
            config_ini.writeValue('setcamre', 'frame_cut_x0_f3', str(self.Lne_Frame_cut_X0_F3.text()))
            config_ini.writeValue('setcamre', 'frame_cut_y0_f3', str(self.Lne_Frame_cut_Y0_F3.text()))
            config_ini.writeValue('setcamre', 'frame_cut_x1_f3', str(self.Lne_Frame_cut_X1_F3.text()))
            config_ini.writeValue('setcamre', 'frame_cut_y1_f3', str(self.Lne_Frame_cut_Y1_F3.text()))
            config_ini.writeValue('setcamre', 'frame_cut_x0_f4', str(self.Lne_Frame_cut_X0_F4.text()))
            config_ini.writeValue('setcamre', 'frame_cut_y0_f4', str(self.Lne_Frame_cut_Y0_F4.text()))
            config_ini.writeValue('setcamre', 'frame_cut_x1_f4', str(self.Lne_Frame_cut_X1_F4.text()))
            config_ini.writeValue('setcamre', 'frame_cut_y1_f4', str(self.Lne_Frame_cut_Y1_F4.text()))
            config_ini.writeValue('setcamre', 'frame_cut_f1_angle', str(self.Lne_Frame_cut_F1_angle.text()))
            config_ini.writeValue('setcamre', 'frame_cut_f2_angle', str(self.Lne_Frame_cut_F2_angle.text()))
            config_ini.writeValue('setcamre', 'frame_cut_f3_angle', str(self.Lne_Frame_cut_F3_angle.text()))
            config_ini.writeValue('setcamre', 'frame_cut_f4_angle', str(self.Lne_Frame_cut_F4_angle.text()))
            window.autoShow()
        else:
            QtWidgets.QMessageBox.question(self, "提示", "输入范围错误",
                                           QtWidgets.QMessageBox.Yes)

    def slot_saveproofreadingdata(self):
        if float(self.Lne_Frame_cut_X1_F1_11.text()) > float(self.Lne_Frame_cut_X1_F1_12.text()) and float(
                self.Lne_Frame_cut_X1_F1_11.text()) > float(self.Lne_Frame_cut_X1_F1_13.text()) and float(
                self.Lne_Frame_cut_X1_F1_12.text()) > float(self.Lne_Frame_cut_X1_F1_13.text()) and float(
                self.Lne_Frame_cut_X1_F2_11.text()) > float(self.Lne_Frame_cut_X1_F2_12.text()) and float(
                self.Lne_Frame_cut_X1_F2_11.text()) > float(self.Lne_Frame_cut_X1_F2_13.text()) and float(
                self.Lne_Frame_cut_X1_F2_12.text()) > float(self.Lne_Frame_cut_X1_F2_13.text()) and float(
                self.Lne_Frame_cut_X1_F3_11.text()) > float(self.Lne_Frame_cut_X1_F3_12.text()) and float(
                self.Lne_Frame_cut_X1_F3_11.text()) > float(self.Lne_Frame_cut_X1_F3_13.text()) and float(
                self.Lne_Frame_cut_X1_F3_12.text()) > float(self.Lne_Frame_cut_X1_F3_13.text()) and float(
                self.Lne_Frame_cut_X1_F4_11.text()) > float(self.Lne_Frame_cut_X1_F4_12.text()) and float(
                self.Lne_Frame_cut_X1_F4_11.text()) > float(self.Lne_Frame_cut_X1_F4_13.text()) and float(
                self.Lne_Frame_cut_X1_F4_12.text()) > float(self.Lne_Frame_cut_X1_F4_13.text()):
            config_ini.writeValue('setcamre', 'frame_cut_x1_f1_11', str(self.Lne_Frame_cut_X1_F1_11.text()))
            config_ini.writeValue('setcamre', 'frame_cut_x1_f2_11', str(self.Lne_Frame_cut_X1_F2_11.text()))
            config_ini.writeValue('setcamre', 'frame_cut_x1_f3_11', str(self.Lne_Frame_cut_X1_F3_11.text()))
            config_ini.writeValue('setcamre', 'frame_cut_x1_f4_11', str(self.Lne_Frame_cut_X1_F4_11.text()))
            config_ini.writeValue('setcamre', 'frame_cut_x1_f1_12', str(self.Lne_Frame_cut_X1_F1_12.text()))
            config_ini.writeValue('setcamre', 'frame_cut_x1_f2_12', str(self.Lne_Frame_cut_X1_F2_12.text()))
            config_ini.writeValue('setcamre', 'frame_cut_x1_f3_12', str(self.Lne_Frame_cut_X1_F3_12.text()))
            config_ini.writeValue('setcamre', 'frame_cut_x1_f4_12', str(self.Lne_Frame_cut_X1_F4_12.text()))
            config_ini.writeValue('setcamre', 'frame_cut_x1_f1_13', str(self.Lne_Frame_cut_X1_F1_13.text()))
            config_ini.writeValue('setcamre', 'frame_cut_x1_f2_13', str(self.Lne_Frame_cut_X1_F2_13.text()))
            config_ini.writeValue('setcamre', 'frame_cut_x1_f3_13', str(self.Lne_Frame_cut_X1_F3_13.text()))
            config_ini.writeValue('setcamre', 'frame_cut_x1_f4_13', str(self.Lne_Frame_cut_X1_F4_13.text()))

            window.autoShow()
        else:
            QtWidgets.QMessageBox.question(self, "提示", "输入范围错误",
                                           QtWidgets.QMessageBox.Yes)




class S7_300():
    # 以下是读取PLC数据的函数
    def printReadResult(result):
        if result.IsSuccess:
            # print(result.Content)
            return result.Content
        else:
            print("failed1  " + result.Message)
            return False

    # 以下是写PLC的程序
    def printWriteResult(result):
        if result.IsSuccess:
            print("success")
            pass
        else:
            print("failed2  " + result.Message)


class MyWidget(QWidget):
    def closeEvent(self, event):
        result = QtWidgets.QMessageBox.question(self, "标题", "亲，你确定想关闭我?别后悔！！！'_'",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if (result == QtWidgets.QMessageBox.Yes):
            event.accept()
            # 通知服务器的代码省略，这里不是重点...
        else:
            event.ignore()


# 串口通讯线程
def thread_SerialPort(name):
    try:
        while True:
            s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s1.bind(('', 20001))
            s1.listen(5)
            print("开始监听_余姚太平洋")
            conn, addr = s1.accept()
            print('conn:', conn)
            print('addr:', addr)
            time.sleep(0.3)
            weiht_flag = True
            while weiht_flag:
                data = conn.recv(1024)
                if len(data) != 13:
                    print('不等于13',len(data),data)
                    # with open('2233.txt', 'a+') as f:
                    #     f.writelines(
                    #         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ':' + '1传感器重量,不等于13,数据长度' + str(
                    #             len(data)) + '数据' + str(data) + '\n')

                if len(data) == 13:
                    weigth = int(data[3:8])
                    # print('1流,等于13', weigth, len(data), data)
                    m = int(data[9:10])
                    public['temp_Lab_1bWeight'] = weigth

                elif len(data) == 0:
                    print('等于0',len(data),data)
                    # with open('2233.txt', 'a+') as f:
                    #     f.writelines(
                    #         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ':' + '1传感器重量,不等于0和13,数据长度' + str(
                    #             len(data)) + '数据' + str(data) + '\n')
                    weiht_flag = False
                    s1.close()
                elif len(data) == 1:
                    print('等于1',len(data),data)
                    # with open('2233.txt', 'a+') as f:
                    #     f.writelines(
                    #         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ':' + '1传感器重量,等于1,数据长度' + str(
                    #             len(data)) + '数据' + str(data) + '\n')

                else:
                    print('不等于0,13其他', len(data), data)
                    # with open('2233.txt', 'a+') as f:
                    #     f.writelines(
                    #         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ':' + '1传感器重量,等于0,数据长度' + str(
                    #             len(data)) + '数据' + str(data) + '\n')

    except Exception as e:
        print('1流称重传感器异常',name,e)
        with open('2233.txt', 'a+') as f:
            f.writelines(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ':' + '1流称重传感器异常,数据长度' + str(
                    len(data)) + '数据' + str(data) + '\n')
    finally:
        _thread.start_new_thread(thread_SerialPort, ('SerialPort',), )



# 串口通讯线程
def thread_SerialPort_MED(port, name):
    try:
        while True:
            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s2.bind(('', int(port)))
            s2.listen(5)
            print("开始监听_MED", port, name)
            conn, addr = s2.accept()
            print('MED_conn:', conn)
            print('MED_addr:', addr)
            time.sleep(0.3)
            weiht_flag = True
            while weiht_flag:
                data = conn.recv(1024)
                if data:
                    # print(name, int((data[4:10])),len(data), data)
                    if len(data) == 144 or len(data) == 162 or len(data) == 18:
                        public[str(name)] = int((data[4:10]))
                        logging.info('重量:{}'.format(public[str(name)]))

                        # if int((data[4:10])) > 500:
                        #     print(name, int((data[4:10])))

                        # public['temp_Lab_2bWeight'] = int(2380) # 测试重量用
                        # public['temp_Lab_3bWeight'] = int(2380) # 测试重量用
                        # public['temp_Lab_4bWeight'] = int(2380) # 测试重量用
                        # print(name, '重量 ', int((data[4:10])))

                    else:
                        with open('2233.txt', 'a+') as f:
                            f.writelines(
                                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ':' + '2传感器重量不等于常用数据长度' + str(
                                    len(data)) + str(data) + '\n')

                else:
                    weiht_flag = False
                    s2.close()
    except Exception as e:
        print('MED称重异常',name,e)
        with open('2233.txt', 'a+') as f:
            f.writelines(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ':' + str(name) +'2传感器重量不等于常用数据长度' + str(
                    len(data)) + str(data) + e + '\n')
    finally:
        _thread.start_new_thread(thread_SerialPort_MED, (20002, 'temp_Lab_2bWeight'), )



# 切割PLC通讯线程
def thread_PLC_CUT_stat(name):
    PLC_stat_flag = True
    S7_300()
    time.sleep(0.1)
    while PLC_stat_flag:
        if plc_cut.ConnectServer().IsSuccess == True:
            public['plc_cut_IsSuccess'] = True
            # print("PLC连接成功")
            # 四流称重重量
            public['temp_Lab_1bTemperature'] = S7_300.printReadResult(plc_cut.ReadFloat("M20"))
            public['temp_Lab_2bTemperature'] = S7_300.printReadResult(plc_cut.ReadFloat("M20"))
            public['temp_Lab_3bTemperature'] = S7_300.printReadResult(plc_cut.ReadFloat("M20"))
            public['temp_Lab_4bTemperature'] = S7_300.printReadResult(plc_cut.ReadFloat("M20"))
            # 四流称重模式
            public['plc_weight_manual_F1'] = S7_300.printReadResult(plc_cut.ReadBool("M1.0"))
            public['plc_weight_auto_F1'] = S7_300.printReadResult(plc_cut.ReadBool("M1.1"))
            public['plc_weight_manual_F2'] = S7_300.printReadResult(plc_cut.ReadBool("M1.2"))
            public['plc_weight_auto_F2'] = S7_300.printReadResult(plc_cut.ReadBool("M1.3"))
            public['plc_weight_manual_F3'] = S7_300.printReadResult(plc_cut.ReadBool("M1.4"))
            public['plc_weight_auto_F3'] = S7_300.printReadResult(plc_cut.ReadBool("M1.5"))
            public['plc_weight_manual_F4'] = S7_300.printReadResult(plc_cut.ReadBool("M1.6"))
            public['plc_weight_auto_F4'] = S7_300.printReadResult(plc_cut.ReadBool("M1.7"))
            # 是否称重信号
            public['plc_weighting_F1'] = S7_300.printReadResult(plc_cut.ReadBool("M11.3"))
            public['plc_weighting_F2'] = S7_300.printReadResult(plc_cut.ReadBool("M21.3"))
            public['plc_weighting_F3'] = S7_300.printReadResult(plc_cut.ReadBool("M31.3"))
            public['plc_weighting_F4'] = S7_300.printReadResult(plc_cut.ReadBool("M41.3"))

        else:
            public['plc_cut_IsSuccess'] = False
            print("切割PLC连接失败")


# 连铸公用PLC通讯线程
def thread_PLC_public_stat(name):
    PLC_stat_flag = True
    S7_300()
    time.sleep(0.1)
    while PLC_stat_flag:
        if plc_public.ConnectServer().IsSuccess == True:
            public['plc_public_IsSuccess'] = True

        else:
            public['plc_public_IsSuccess'] = False
            print("连铸公共PLC连接失败")


# 连铸1流PLC通讯线程
def thread_PLC_1f_stat(name):
    PLC_stat_flag = True
    S7_300()
    time.sleep(0.1)
    while PLC_stat_flag:
        if plc_1f.ConnectServer().IsSuccess == True:
            # print('连接成功')
            public['plc_1f_IsSuccess'] = True
            # print('1',S7_300.printReadResult(plc_1f.ReadFloat("DB1.26.0")))
            # 读取拉速
            public['plc_1f_pullspeed'] = S7_300.printReadResult(plc_1f.ReadFloat("M224"))
            # print(S7_300.printReadResult(plc_1f.ReadFloat("M224")))
            # # time.sleep(1)
            # if public['1f_rset_count_end'] == True or public['action_cut_1f'] == True :
            plc_1f.WriteBool("M50.0", public['action_cut_1f'])
            # print('M50.0_f1', S7_300.printReadResult(plc_1f.ReadBool("M50.0")))  # 监听状态


        else:
            public['plc_1f_IsSuccess'] = False
            print("连铸1流PLC连接失败")


# 连铸2流PLC通讯线程
def thread_PLC_2f_stat(name):
    PLC_stat_flag = True
    S7_300()
    time.sleep(0.1)
    while PLC_stat_flag:
        if plc_2f.ConnectServer().IsSuccess == True:
            public['plc_2f_IsSuccess'] = True
            # print('2',S7_300.printReadResult(plc_2f.ReadFloat("DB1.26.0")))
            public['plc_2f_pullspeed'] = S7_300.printReadResult(plc_2f.ReadFloat("M224"))
            # print(S7_300.printReadResult(plc_2f.ReadFloat("M224")))
            # print(S7_300.printReadResult(plc_1f.ReadFloat("M224")))
            # # time.sleep(1)
            # if public['2f_rset_count_end'] == True or public['action_cut_2f'] == True:
            # if public['action_cut_2f'] == True:
            plc_2f.WriteBool("M50.0", public['action_cut_2f'])
            # print('M50.0_f2', S7_300.printReadResult(plc_2f.ReadBool("M50.0")))  # 监听状态
        else:
            public['plc_2f_IsSuccess'] = False
            print("连铸2流PLC连接失败")


# 连铸3流PLC通讯线程
def thread_PLC_3f_stat(name):
    PLC_stat_flag = True
    S7_300()
    time.sleep(0.1)
    while PLC_stat_flag:
        if plc_3f.ConnectServer().IsSuccess == True:
            public['plc_3f_IsSuccess'] = True
            # print('3',S7_300.printReadResult(plc_3f.ReadFloat("DB1.26.0")))
            public['plc_3f_pullspeed'] = S7_300.printReadResult(plc_3f.ReadFloat("M224"))

        else:
            public['plc_3f_IsSuccess'] = False
            print("连铸3流PLC连接失败")


# 连铸4流PLC通讯线程
def thread_PLC_4f_stat(name):
    PLC_stat_flag = True
    S7_300()
    time.sleep(0.1)
    while PLC_stat_flag:
        if plc_4f.ConnectServer().IsSuccess == True:
            public['plc_4f_IsSuccess'] = True
            # print('4',S7_300.printReadResult(plc_4f.ReadFloat("DB1.26.0")))
            public['plc_4f_pullspeed'] = S7_300.printReadResult(plc_4f.ReadFloat("M224"))

        else:
            public['plc_4f_IsSuccess'] = False
            print("连铸4流PLC连接失败")

# 称重重量数据上传至kafka
def upload_kafka_stat(name):
    producer = KafkaProducer(bootstrap_servers=['10.6.80.21:9092', '10.6.80.22:9092', '10.6.80.17:9092',
                                                '10.6.80.18:9092', '10.6.80.19:9092', '10.6.80.20:9092'],
                             key_serializer=str.encode, value_serializer=str.encode)

    while True:
        kafka_time = int(time.time())
        sendkafka_1f = str({0: 'b12ceda6', 1: kafka_time, 7: int(public['temp_Lab_1bWeight'])})
        sendkafka_2f = str({0: 'yraet5rr', 1: kafka_time, 7: int(public['temp_Lab_2bWeight'])})
        # print(sendkafka_1f,type(sendkafka_1f))

        sendkafka_3f = json.dumps({1: kafka_time, 7: public['temp_Lab_3bWeight']})
        sendkafka_4f = json.dumps({1: kafka_time, 7: public['temp_Lab_4bWeight']})

        temp_1Weight = producer.send('sensor-pc', key='b12ceda6', value=sendkafka_1f)
        temp_2Weight = producer.send('sensor-pc', key='yraet5rr', value=sendkafka_2f)
        # producer.send('sensor-pc', key='b12ceda6', value=sendkafka_3f)
        # producer.send('sensor-pc', key='yraet5rr', value=sendkafka_4f)

        logging.info('send:sensor-pc EID:b12ceda6,value:{}'.format(sendkafka_1f))
        logging.info('send:sensor-pc EID:yraet5rr,value:{}'.format(sendkafka_2f))
        logging.info('send:sensor-pc EID:b12ceda6,value:{}'.format(sendkafka_3f))
        # logging.info('send:sensor-pc EID:b12ceda6,value:{}'.format(sendkafka_4f))
        kafkasendNum = config_ini.readvalue('setcamre', 'kafkasendNum')
        kafkasendNum = int(kafkasendNum) + 2
        config_ini.writeValue('setcamre', 'kafkasendNum', str(kafkasendNum))

        # print(kafka_time, sendkafka_1f,sendkafka_2f)
        temp_1Weight.get(timeout=20)
        temp_2Weight.get(timeout=20)
        time.sleep(1)





if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)  # 创建一个应用程序对象

    try:
        # 日志
        log = Log.Logger('all.log')
        # 配置文件
        config_ini = Config.Config(path="..\FixedLengthSystem", pathconfig='config.ini')
        config_fur = Config.Config(path="..\FixedLengthSystem", pathconfig='FurNum.ini')
        # 连接本地数据库
        pool = PooledDB(pymysql, 1, host='localhost', user='root', passwd='123', db='steelfixlength',
                        port=3306)  # 5为连接池里的最少连接数
        conn = pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
        cursor = conn.cursor()


        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s > %(message)s',
                            datefmt='%Y/%m/%d %H:%M:%S',
                            filename='testlog.log',  # 日志存储文件
                            filemode='a'
                            )

        # 记录



        # 发送kafka存储记录
        # logging.basicConfig(level=logging.INFO,
        #                     format='%(asctime)s > %(message)s',
        #                     datefmt='%Y/%m/%d %H:%M:%S',
        #                     filename='sendkafkalog.log',  # 日志存储文件
        #                     filemode='a'
        #                     )
    except Exception as e:
        messagebox.showinfo("配置连接异常", e)

    try:
        # PLC链接
        plc_cut = SiemensS7Net(SiemensPLCS.S300, '192.168.0.21')
        plc_public = SiemensS7Net(SiemensPLCS.S300, '192.168.0.80')
        plc_1f = SiemensS7Net(SiemensPLCS.S300, '192.168.0.81')
        plc_2f = SiemensS7Net(SiemensPLCS.S300, '192.168.0.82')
        plc_3f = SiemensS7Net(SiemensPLCS.S300, '192.168.0.83')
        plc_4f = SiemensS7Net(SiemensPLCS.S300, '192.168.0.84')

    except Exception as e:
        messagebox.showinfo("连接问题", e)

    # 创建plc通讯实例延时，防止引用时报错


    # 线程管理
    _thread.start_new_thread(thread_SerialPort, ('SerialPort',), )
    _thread.start_new_thread(thread_SerialPort_MED, (20002, 'temp_Lab_2bWeight'), )
    _thread.start_new_thread(thread_SerialPort_MED, (20003, 'temp_Lab_3bWeight'), )
    # _thread.start_new_thread(thread_SerialPort_MED, (20004, 'temp_Lab_4bWeight'), )
    _thread.start_new_thread(thread_PLC_CUT_stat, ('PLC_CUT_stat',), )
    _thread.start_new_thread(thread_PLC_public_stat, ('PLC_public_stat',), )
    _thread.start_new_thread(thread_PLC_1f_stat, ('PLC_1f_stat',), )
    _thread.start_new_thread(thread_PLC_2f_stat, ('PLC_2f_stat',), )
    _thread.start_new_thread(thread_PLC_3f_stat, ('PLC_3f_stat',), )
    _thread.start_new_thread(thread_PLC_4f_stat, ('PLC_4f_stat',), )
    _thread.start_new_thread(upload_kafka_stat, ('upload_kafka',), )



    # 主函数调用实例化
    window = MainWindow()
    # window.showFullScreen()    #全屏

    window.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
    window.show()

    sys.exit(app.exec_())  # 0是正常退出
    serialPort.close()
    cursor.close()
    conn.close()
    cap.release()
    cv2.destroyAllWindows()

