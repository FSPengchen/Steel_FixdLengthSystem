
# from PyQt5.QtWidgets import QApplication,QMainWindow
# import sys
# from Ui_firstMainwindow import *

# class MyMainWindow(QMainWindow,Ui_MainWindow):
# 	# 这一部分感觉不好理解
#     def __init__(self,parent=None):
#         super(MyMainWindow, self).__init__(parent)
#         self.setupUi(self)
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     myWindow = MyMainWindow()
#     myWindow.show()
#     sys.exit(app.exec_())
# ————————————————
# 版权声明：本文为CSDN博主「努力中的熊」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/baidu_20313315/article/details/112956113


# from PyQt5.QtWidgets import QApplication,QMainWindow
# import sys
# from Ui_firstMainwindow import *
#
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     # 实例化一个主窗口
#     myWindow = QMainWindow()
#     # 实例化.ui转换后的py文件
#     ui_main_window = Ui_MainWindow()
#     # 调用转换后的py文件实例对象方法setupUi，并继承QMainwindow的实例对象（这里算不算多态我还说不太清楚）
#     ui_main_window.setupUi(myWindow)
#     # 展示窗口
#     myWindow.show()
#     sys.exit(app.exec_())
# ————————————————
# 版权声明：本文为CSDN博主「努力中的熊」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/baidu_20313315/article/details/112956113



#背后颜色调整
#self.Lab_Time.resize(100,100)
# self.Lab_Time.setText(_translate("MainWindow", "12时16分32秒"))
# self.Lab_Time.setStyleSheet('background-color:green;')
#
#
# from PyQt5.Qt import *
# import sys
#
#
# class Window(QWidget):
#     def __init__(self):
#         super().__init__()  # 调用父类QWidget中的init方法
#         self.setWindowTitle("软件名称")
#         self.resize(600, 500)
#         self.func_list()
#
#     def func_list(self):
#         self.func()
#
#     def func(self):
#         btn = QPushButton(self)
#         btn.setText("软件内容")
#         btn.resize(120, 30)
#         btn.move(100, 100)
#         btn.setStyleSheet('background-color:green;font-size:20px;')
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)  # 创建一个应用程序对象
#     # sys.argv可以接收用户命令行启动时所输入的参数，根据参数执行不同程序
#     # qApp 为全局对象
#     print(sys.argv)
#     print(app.arguments())
#     print(qApp.arguments())
#     # 以上三个输出结果是一样的
#     window = Window()
#
#     window.show()
#     sys.exit(app.exec_())  # 0是正常退出
#     # app.exec_()  进行循环
#     # sys.exit()   检测退出原因
#
# '''
# 1.创建一个应用程序
# 2.控件操作
# 3.执行应用，进入消息循环
# '''
# '''
# 1.创建控件
# window = QWidget()
# window = QPushButton()
# 2.设置控件
# window.resize(50,50)
# 3.展示控件
# window.show()
# '''


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'camerapage.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
#
# from PyQt5 import QtCore, QtGui, QtWidgets
#
# class Ui_CameraPage(object):
#  def setupUi(self, CameraPage):
#         CameraPage.setObjectName("CameraPage")
#         CameraPage.resize(855, 443)
#         self.layoutWidget = QtWidgets.QWidget(CameraPage)
#         self.layoutWidget.setGeometry(QtCore.QRect(30, 30, 757, 348))
#         self.layoutWidget.setObjectName("layoutWidget")
#         self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
#         self.gridLayout.setContentsMargins(8, 8, 8, 8)
#         self.gridLayout.setObjectName("gridLayout")
#         self.rightButton = QtWidgets.QPushButton(self.layoutWidget)
#         self.rightButton.setMinimumSize(QtCore.QSize(80, 80))
#         self.rightButton.setMaximumSize(QtCore.QSize(80, 80))
#         font = QtGui.QFont()
#         font.setPointSize(14)
#         self.rightButton.setFont(font)
#         self.rightButton.setObjectName("rightButton")
#         self.gridLayout.addWidget(self.rightButton, 1, 2, 1, 1)
#         self.leftButton = QtWidgets.QPushButton(self.layoutWidget)
#         self.leftButton.setMinimumSize(QtCore.QSize(80, 80))
#         self.leftButton.setMaximumSize(QtCore.QSize(80, 80))
#         font = QtGui.QFont()
#         font.setPointSize(14)
#         self.leftButton.setFont(font)
#         self.leftButton.setObjectName("leftButton")
#         self.gridLayout.addWidget(self.leftButton, 1, 0, 1, 1)
#         self.returnButton = QtWidgets.QPushButton(self.layoutWidget)
#         font = QtGui.QFont()
#         font.setPointSize(14)
#         self.returnButton.setFont(font)
#         self.returnButton.setObjectName("returnButton")
#         self.gridLayout.addWidget(self.returnButton, 4, 0, 1, 3)
#         self.cameraButton = QtWidgets.QPushButton(self.layoutWidget)
#         font = QtGui.QFont()
#         font.setPointSize(14)
#         self.cameraButton.setFont(font)
#         self.cameraButton.setObjectName("cameraButton")
#         self.gridLayout.addWidget(self.cameraButton, 3, 0, 1, 3)
#         self.cameraLabel = QtWidgets.QLabel(self.layoutWidget)
#         self.cameraLabel.setMinimumSize(QtCore.QSize(480, 320))
#         font = QtGui.QFont()
#         font.setPointSize(14)
#         self.cameraLabel.setFont(font)
#         self.cameraLabel.setObjectName("cameraLabel")
#         self.gridLayout.addWidget(self.cameraLabel, 0, 3, 5, 1)
#         self.upButton = QtWidgets.QPushButton(self.layoutWidget)
#         self.upButton.setMinimumSize(QtCore.QSize(80, 80))
#         self.upButton.setMaximumSize(QtCore.QSize(80, 80))
#         font = QtGui.QFont()
#         font.setPointSize(14)
#         self.upButton.setFont(font)
#         self.upButton.setObjectName("upButton")
#         self.gridLayout.addWidget(self.upButton, 0, 1, 1, 1)
#         self.downButton = QtWidgets.QPushButton(self.layoutWidget)
#         self.downButton.setMinimumSize(QtCore.QSize(80, 80))
#         self.downButton.setMaximumSize(QtCore.QSize(80, 80))
#         font = QtGui.QFont()
#         font.setPointSize(14)
#         self.downButton.setFont(font)
#         self.downButton.setObjectName("downButton")
#         self.gridLayout.addWidget(self.downButton, 2, 1, 1, 1)
#
#         self.retranslateUi(CameraPage)
#         QtCore.QMetaObject.connectSlotsByName(CameraPage)
#
#         def retranslateUi(self, CameraPage):
#                 _translate = QtCore.QCoreApplication.translate
#                 CameraPage.setWindowTitle(_translate("CameraPage", "摄像头界面"))
#         self.rightButton.setText(_translate("CameraPage", "右"))
#         self.leftButton.setText(_translate("CameraPage", "左"))
#         self.returnButton.setText(_translate("CameraPage", "返回"))
#         self.cameraButton.setText(_translate("CameraPage", "打开摄像头"))
#         self.cameraLabel.setText(_translate("CameraPage", "摄像头画面"))
#         self.upButton.setText(_translate("CameraPage", "上"))
#         self.downButton.setText(_translate("CameraPage", "下"))



# class Ui_MainWindow(QMainWindow):
#     import sys
#     from PyQt5.QtWidgets import QApplication, QMainWindow
#     if __name__ == '__main__':
#         app = QApplication(sys.argv)
#         mywindows = Ui_MainWindow()
#         ui_main_window = Ui_MainWindow()
#         ui_main_window.setupUi(mywindows)
#         mywindows.show()
#         sys.exit(app.exec_())
# #
import time
import threading
#
# def show_timestruct(t):
#     print( t.tm_year,'年：')
#     print('月：', t.tm_mon)
#
#     print('日：', t.tm_mday)
#
#     print('小时：', t.tm_hour)
#
#     print()
#     '分钟', t.tm_min
#     print()
#     '秒', t.tm_sec
#     print()
#     '星期：', t.tm_wday
#     print()
#     '一年的第 %s 天' % t.tm_yday
#     print()
#     '是否夏时令：', t.tm_isdst
#
#
# def thread_Timer():
#     print("该起床啦...5秒之后再次呼叫你起床...")
#
#     # 声明全局变量
#     global t1
#     # 创建并初始化线程
#     t1 = threading.Timer(5, thread_Timer)
#     # 启动线程
#     t1.start()
#
# if __name__ == "__main__":
#     # 创建并初始化线程
#     t1 = threading.Timer(5, thread_Timer)
#     # 启动线程
#     t1.start()
#     t = time.gmtime()
#     print(time.gmtime().tm_year)
#     show_timestruct(t)
#
#
#     print('时间：', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
#     print('时间：', time.strftime('%Y-%m-%d', time.localtime(time.time())))
#     print('时间：', time.strftime('%H:%M:%S', time.localtime(time.time())))
#     exec_count = 0
#
#
# '''每秒一次'''
# def heart_beat():
#     print(time.strftime('%Y-%m-%d %H:%M:%S'))
#     threading.Timer(1, heart_beat).start()
#
# heart_beat()


'''每秒一次'''
def heart_beat():
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    threading.Timer(1, heart_beat).start()


heart_beat()


import cv2 as cv

def video_demo():
    # 0是代表摄像头编号，只有一个的话默认为0
    capture = cv.VideoCapture(0)
    while (True):
        ref, frame = capture.read()

        cv.imshow("1", frame)
        # 等待30ms显示图像，若过程中按“Esc”退出
        c = cv.waitKey(30) & 0xff
        if c == 27:
            capture.release()
            break


#video_demo()
#cv.waitKey()
#cv.destroyAllWindows()

capture = cv.VideoCapture(0)
while (True):
    ref, frame = capture.read()
    cv.imshow("1", frame)