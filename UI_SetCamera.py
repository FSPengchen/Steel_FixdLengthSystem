# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_SetCamera.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(873, 353)
        self.horizontalSlider_Contrast = QtWidgets.QSlider(Dialog)
        self.horizontalSlider_Contrast.setGeometry(QtCore.QRect(70, 120, 511, 22))
        self.horizontalSlider_Contrast.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_Contrast.setObjectName("horizontalSlider_Contrast")
        self.horizontalSlider_Light = QtWidgets.QSlider(Dialog)
        self.horizontalSlider_Light.setGeometry(QtCore.QRect(230, 40, 511, 22))
        self.horizontalSlider_Light.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_Light.setObjectName("horizontalSlider_Light")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(760, 40, 81, 16))
        self.label_2.setStyleSheet("background-color :red")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(620, 130, 91, 20))
        self.label_3.setStyleSheet("background-color :red")
        self.label_3.setObjectName("label_3")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(740, 130, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.Btn_Exit = QtWidgets.QPushButton(Dialog)
        self.Btn_Exit.setGeometry(QtCore.QRect(740, 260, 93, 28))
        self.Btn_Exit.setObjectName("Btn_Exit")
        self.Btn_SaveData = QtWidgets.QPushButton(Dialog)
        self.Btn_SaveData.setGeometry(QtCore.QRect(740, 190, 93, 28))
        self.Btn_SaveData.setObjectName("Btn_SaveData")
        self.Lab_LightValue = QtWidgets.QLabel(Dialog)
        self.Lab_LightValue.setGeometry(QtCore.QRect(810, 40, 31, 16))
        self.Lab_LightValue.setStyleSheet("background-color :red")
        self.Lab_LightValue.setObjectName("Lab_LightValue")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(60, 260, 619, 35))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_41 = QtWidgets.QLabel(self.layoutWidget)
        self.label_41.setStyleSheet("\n"
"font: 75 12pt \"微软雅黑\";\n"
"\n"
"")
        self.label_41.setAlignment(QtCore.Qt.AlignCenter)
        self.label_41.setObjectName("label_41")
        self.horizontalLayout.addWidget(self.label_41)
        self.Lne_SetCameraFlip = QtWidgets.QLineEdit(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Lne_SetCameraFlip.sizePolicy().hasHeightForWidth())
        self.Lne_SetCameraFlip.setSizePolicy(sizePolicy)
        self.Lne_SetCameraFlip.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Lne_SetCameraFlip.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Lne_SetCameraFlip.setStyleSheet("\n"
"font: 75 12pt \"微软雅黑\";\n"
"\n"
"")
        self.Lne_SetCameraFlip.setObjectName("Lne_SetCameraFlip")
        self.horizontalLayout.addWidget(self.Lne_SetCameraFlip)
        self.layoutWidget1 = QtWidgets.QWidget(Dialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(120, 170, 505, 71))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_37 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_37.setStyleSheet("\n"
"font: 75 12pt \"微软雅黑\";\n"
"\n"
"")
        self.label_37.setAlignment(QtCore.Qt.AlignCenter)
        self.label_37.setObjectName("label_37")
        self.verticalLayout.addWidget(self.label_37)
        self.Lne_Threshold_f1 = QtWidgets.QLineEdit(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Lne_Threshold_f1.sizePolicy().hasHeightForWidth())
        self.Lne_Threshold_f1.setSizePolicy(sizePolicy)
        self.Lne_Threshold_f1.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Lne_Threshold_f1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Lne_Threshold_f1.setStyleSheet("\n"
"font: 75 12pt \"微软雅黑\";\n"
"\n"
"")
        self.Lne_Threshold_f1.setObjectName("Lne_Threshold_f1")
        self.verticalLayout.addWidget(self.Lne_Threshold_f1)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 2, 1)
        self.label_38 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_38.setStyleSheet("\n"
"font: 75 12pt \"微软雅黑\";\n"
"\n"
"")
        self.label_38.setAlignment(QtCore.Qt.AlignCenter)
        self.label_38.setObjectName("label_38")
        self.gridLayout.addWidget(self.label_38, 0, 1, 1, 1)
        self.label_39 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_39.setStyleSheet("\n"
"font: 75 12pt \"微软雅黑\";\n"
"\n"
"")
        self.label_39.setAlignment(QtCore.Qt.AlignCenter)
        self.label_39.setObjectName("label_39")
        self.gridLayout.addWidget(self.label_39, 0, 2, 1, 1)
        self.label_40 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_40.setStyleSheet("\n"
"font: 75 12pt \"微软雅黑\";\n"
"\n"
"")
        self.label_40.setAlignment(QtCore.Qt.AlignCenter)
        self.label_40.setObjectName("label_40")
        self.gridLayout.addWidget(self.label_40, 0, 3, 1, 1)
        self.Lne_Threshold_f2 = QtWidgets.QLineEdit(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Lne_Threshold_f2.sizePolicy().hasHeightForWidth())
        self.Lne_Threshold_f2.setSizePolicy(sizePolicy)
        self.Lne_Threshold_f2.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Lne_Threshold_f2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Lne_Threshold_f2.setStyleSheet("\n"
"font: 75 12pt \"微软雅黑\";\n"
"\n"
"")
        self.Lne_Threshold_f2.setObjectName("Lne_Threshold_f2")
        self.gridLayout.addWidget(self.Lne_Threshold_f2, 1, 1, 1, 1)
        self.Lne_Threshold_f3 = QtWidgets.QLineEdit(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Lne_Threshold_f3.sizePolicy().hasHeightForWidth())
        self.Lne_Threshold_f3.setSizePolicy(sizePolicy)
        self.Lne_Threshold_f3.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Lne_Threshold_f3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Lne_Threshold_f3.setStyleSheet("\n"
"font: 75 12pt \"微软雅黑\";\n"
"\n"
"")
        self.Lne_Threshold_f3.setObjectName("Lne_Threshold_f3")
        self.gridLayout.addWidget(self.Lne_Threshold_f3, 1, 2, 1, 1)
        self.Lne_Threshold_f4 = QtWidgets.QLineEdit(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Lne_Threshold_f4.sizePolicy().hasHeightForWidth())
        self.Lne_Threshold_f4.setSizePolicy(sizePolicy)
        self.Lne_Threshold_f4.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Lne_Threshold_f4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Lne_Threshold_f4.setStyleSheet("\n"
"font: 75 12pt \"微软雅黑\";\n"
"\n"
"")
        self.Lne_Threshold_f4.setObjectName("Lne_Threshold_f4")
        self.gridLayout.addWidget(self.Lne_Threshold_f4, 1, 3, 1, 1)
        self.Btn_CameraSetAeState_auto = QtWidgets.QPushButton(Dialog)
        self.Btn_CameraSetAeState_auto.setGeometry(QtCore.QRect(20, 40, 93, 28))
        self.Btn_CameraSetAeState_auto.setObjectName("Btn_CameraSetAeState_auto")
        self.Btn_CameraSetAeState_man = QtWidgets.QPushButton(Dialog)
        self.Btn_CameraSetAeState_man.setGeometry(QtCore.QRect(120, 40, 93, 28))
        self.Btn_CameraSetAeState_man.setObjectName("Btn_CameraSetAeState_man")
        self.Lab_CameraSetAeState = QtWidgets.QLabel(Dialog)
        self.Lab_CameraSetAeState.setGeometry(QtCore.QRect(80, 20, 72, 15))
        self.Lab_CameraSetAeState.setObjectName("Lab_CameraSetAeState")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "视频参数调整"))
        self.label_2.setText(_translate("Dialog", "亮度："))
        self.label_3.setText(_translate("Dialog", "对比度：0"))
        self.pushButton_2.setText(_translate("Dialog", "使用默认值"))
        self.Btn_Exit.setText(_translate("Dialog", "退出"))
        self.Btn_SaveData.setText(_translate("Dialog", "保存"))
        self.Lab_LightValue.setText(_translate("Dialog", "0"))
        self.label_41.setText(_translate("Dialog", " 0:水平翻转  1:垂直翻转  -1:全翻转  2:不翻转"))
        self.Lne_SetCameraFlip.setText(_translate("Dialog", "0"))
        self.label_37.setText(_translate("Dialog", "1流阈值:"))
        self.Lne_Threshold_f1.setText(_translate("Dialog", "0"))
        self.label_38.setText(_translate("Dialog", "2流阈值:"))
        self.label_39.setText(_translate("Dialog", "3流阈值:"))
        self.label_40.setText(_translate("Dialog", "4流阈值:"))
        self.Lne_Threshold_f2.setText(_translate("Dialog", "0"))
        self.Lne_Threshold_f3.setText(_translate("Dialog", "0"))
        self.Lne_Threshold_f4.setText(_translate("Dialog", "0"))
        self.Btn_CameraSetAeState_auto.setText(_translate("Dialog", "自动调整"))
        self.Btn_CameraSetAeState_man.setText(_translate("Dialog", "手动调整"))
        self.Lab_CameraSetAeState.setText(_translate("Dialog", "调整模式"))

