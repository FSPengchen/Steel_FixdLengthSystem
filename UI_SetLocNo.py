# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_SetLocNo.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(511, 343)
        self.LabInput_LocNo = QtWidgets.QTextEdit(Dialog)
        self.LabInput_LocNo.setGeometry(QtCore.QRect(230, 110, 171, 41))
        self.LabInput_LocNo.setStyleSheet("font: 12pt \\\"微软雅黑\\\";")
        self.LabInput_LocNo.setObjectName("LabInput_LocNo")
        self.Btn_LocNoYes = QtWidgets.QPushButton(Dialog)
        self.Btn_LocNoYes.setGeometry(QtCore.QRect(130, 180, 101, 41))
        self.Btn_LocNoYes.setObjectName("Btn_LocNoYes")
        self.Btn_LocNoNo = QtWidgets.QPushButton(Dialog)
        self.Btn_LocNoNo.setGeometry(QtCore.QRect(280, 180, 101, 41))
        self.Btn_LocNoNo.setObjectName("Btn_LocNoNo")
        self.Labtxt_ClassNo = QtWidgets.QLabel(Dialog)
        self.Labtxt_ClassNo.setGeometry(QtCore.QRect(80, 110, 131, 41))
        self.Labtxt_ClassNo.setStyleSheet("font: 12pt \\\"微软雅黑\\\";")
        self.Labtxt_ClassNo.setObjectName("Labtxt_ClassNo")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "修改连铸机号"))
        self.Btn_LocNoYes.setText(_translate("Dialog", "确定"))
        self.Btn_LocNoNo.setText(_translate("Dialog", "取消"))
        self.Labtxt_ClassNo.setText(_translate("Dialog", "当前连铸机号:"))