# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_SetAlgorithm.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(649, 518)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(30, 140, 151, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(60, 190, 81, 21))
        self.label_5.setObjectName("label_5")
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(160, 190, 113, 21))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_4.setGeometry(QtCore.QRect(160, 230, 113, 21))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(60, 230, 81, 21))
        self.label_6.setObjectName("label_6")
        self.lineEdit_5 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_5.setGeometry(QtCore.QRect(160, 270, 113, 21))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(60, 270, 81, 21))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(320, 150, 151, 21))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(Dialog)
        self.label_9.setGeometry(QtCore.QRect(320, 180, 91, 21))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(Dialog)
        self.label_10.setGeometry(QtCore.QRect(320, 210, 321, 21))
        self.label_10.setObjectName("label_10")
        self.lineEdit_6 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_6.setGeometry(QtCore.QRect(370, 260, 113, 21))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.setGeometry(QtCore.QRect(110, 370, 141, 19))
        self.checkBox.setObjectName("checkBox")
        self.label_11 = QtWidgets.QLabel(Dialog)
        self.label_11.setGeometry(QtCore.QRect(60, 320, 111, 21))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(Dialog)
        self.label_12.setGeometry(QtCore.QRect(330, 370, 131, 21))
        self.label_12.setObjectName("label_12")
        self.lineEdit_7 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_7.setGeometry(QtCore.QRect(490, 370, 113, 21))
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.Btn_Yes = QtWidgets.QPushButton(Dialog)
        self.Btn_Yes.setGeometry(QtCore.QRect(60, 420, 93, 28))
        self.Btn_Yes.setObjectName("Btn_Yes")
        self.Btn_No = QtWidgets.QPushButton(Dialog)
        self.Btn_No.setGeometry(QtCore.QRect(490, 420, 93, 28))
        self.Btn_No.setObjectName("Btn_No")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(60, 40, 521, 63))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.Lab_SetCutLimt_f1 = QtWidgets.QLabel(self.widget)
        self.Lab_SetCutLimt_f1.setStyleSheet("\n"
"font: 75 10pt \"微软雅黑\";\n"
"\n"
"")
        self.Lab_SetCutLimt_f1.setObjectName("Lab_SetCutLimt_f1")
        self.verticalLayout.addWidget(self.Lab_SetCutLimt_f1)
        self.Lne_SetCutLimt_f1 = QtWidgets.QLineEdit(self.widget)
        self.Lne_SetCutLimt_f1.setStyleSheet("font: 75 10pt \"微软雅黑\";")
        self.Lne_SetCutLimt_f1.setObjectName("Lne_SetCutLimt_f1")
        self.verticalLayout.addWidget(self.Lne_SetCutLimt_f1)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 2, 1)
        self.Lab_SetCutLimt_f2 = QtWidgets.QLabel(self.widget)
        self.Lab_SetCutLimt_f2.setStyleSheet("\n"
"font: 75 10pt \"微软雅黑\";\n"
"\n"
"")
        self.Lab_SetCutLimt_f2.setObjectName("Lab_SetCutLimt_f2")
        self.gridLayout.addWidget(self.Lab_SetCutLimt_f2, 0, 1, 1, 1)
        self.Lab_SetCutLimt_f3 = QtWidgets.QLabel(self.widget)
        self.Lab_SetCutLimt_f3.setStyleSheet("\n"
"font: 75 10pt \"微软雅黑\";\n"
"\n"
"")
        self.Lab_SetCutLimt_f3.setObjectName("Lab_SetCutLimt_f3")
        self.gridLayout.addWidget(self.Lab_SetCutLimt_f3, 0, 2, 1, 1)
        self.Lab_SetCutLimt_f4 = QtWidgets.QLabel(self.widget)
        self.Lab_SetCutLimt_f4.setStyleSheet("\n"
"font: 75 10pt \"微软雅黑\";\n"
"\n"
"")
        self.Lab_SetCutLimt_f4.setObjectName("Lab_SetCutLimt_f4")
        self.gridLayout.addWidget(self.Lab_SetCutLimt_f4, 0, 3, 1, 1)
        self.Lne_SetCutLimt_f2 = QtWidgets.QLineEdit(self.widget)
        self.Lne_SetCutLimt_f2.setStyleSheet("font: 75 10pt \"微软雅黑\";")
        self.Lne_SetCutLimt_f2.setObjectName("Lne_SetCutLimt_f2")
        self.gridLayout.addWidget(self.Lne_SetCutLimt_f2, 1, 1, 1, 1)
        self.Lne_SetCutLimt_f3 = QtWidgets.QLineEdit(self.widget)
        self.Lne_SetCutLimt_f3.setStyleSheet("font: 75 10pt \"微软雅黑\";")
        self.Lne_SetCutLimt_f3.setObjectName("Lne_SetCutLimt_f3")
        self.gridLayout.addWidget(self.Lne_SetCutLimt_f3, 1, 2, 1, 1)
        self.Lne_SetCutLimt_f4 = QtWidgets.QLineEdit(self.widget)
        self.Lne_SetCutLimt_f4.setStyleSheet("font: 75 10pt \"微软雅黑\";")
        self.Lne_SetCutLimt_f4.setObjectName("Lne_SetCutLimt_f4")
        self.gridLayout.addWidget(self.Lne_SetCutLimt_f4, 1, 3, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "算法设置"))
        self.label_4.setText(_translate("Dialog", "延时设置（单位：秒)"))
        self.label_5.setText(_translate("Dialog", "预夹延时："))
        self.label_6.setText(_translate("Dialog", "切割延时："))
        self.label_7.setText(_translate("Dialog", "运行延时："))
        self.label_8.setText(_translate("Dialog", "当前屏幕跟踪起点设置"))
        self.label_9.setText(_translate("Dialog", "单位：毫米"))
        self.label_10.setText(_translate("Dialog", "注意：如默认从第一个标定点开始，则设置成-1"))
        self.checkBox.setText(_translate("Dialog", "使用自适应算法"))
        self.label_11.setText(_translate("Dialog", "自适应算法参数"))
        self.label_12.setText(_translate("Dialog", "基准阀差(20~100)"))
        self.Btn_Yes.setText(_translate("Dialog", "确定"))
        self.Btn_No.setText(_translate("Dialog", "取消"))
        self.Lab_SetCutLimt_f1.setText(_translate("Dialog", "1流切割设定值"))
        self.Lab_SetCutLimt_f2.setText(_translate("Dialog", "2流切割设定值"))
        self.Lab_SetCutLimt_f3.setText(_translate("Dialog", "3流切割设定值"))
        self.Lab_SetCutLimt_f4.setText(_translate("Dialog", "4流切割设定值"))

