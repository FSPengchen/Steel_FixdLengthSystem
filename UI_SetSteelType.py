# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_SetSteelType.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(436, 413)
        self.Btn_Exit = QtWidgets.QPushButton(Dialog)
        self.Btn_Exit.setGeometry(QtCore.QRect(320, 320, 93, 28))
        self.Btn_Exit.setObjectName("Btn_Exit")
        self.Btn_changeSteelType = QtWidgets.QPushButton(Dialog)
        self.Btn_changeSteelType.setGeometry(QtCore.QRect(320, 170, 93, 28))
        self.Btn_changeSteelType.setObjectName("Btn_changeSteelType")
        self.Btn_changeSteelDensity = QtWidgets.QPushButton(Dialog)
        self.Btn_changeSteelDensity.setGeometry(QtCore.QRect(320, 130, 93, 28))
        self.Btn_changeSteelDensity.setObjectName("Btn_changeSteelDensity")
        self.LW_SteelType = QtWidgets.QListWidget(Dialog)
        self.LW_SteelType.setGeometry(QtCore.QRect(20, 50, 271, 341))
        self.LW_SteelType.setObjectName("LW_SteelType")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 20, 72, 15))
        self.label.setObjectName("label")
        self.Lab_showSteelType = QtWidgets.QLabel(Dialog)
        self.Lab_showSteelType.setGeometry(QtCore.QRect(130, 20, 72, 15))
        self.Lab_showSteelType.setObjectName("Lab_showSteelType")
        self.Btn_addSteelType = QtWidgets.QPushButton(Dialog)
        self.Btn_addSteelType.setGeometry(QtCore.QRect(320, 50, 93, 28))
        self.Btn_addSteelType.setObjectName("Btn_addSteelType")
        self.Btn_delSteelType = QtWidgets.QPushButton(Dialog)
        self.Btn_delSteelType.setGeometry(QtCore.QRect(320, 90, 93, 28))
        self.Btn_delSteelType.setObjectName("Btn_delSteelType")
        self.Btn_CheckSteelDensity = QtWidgets.QPushButton(Dialog)
        self.Btn_CheckSteelDensity.setGeometry(QtCore.QRect(320, 210, 93, 28))
        self.Btn_CheckSteelDensity.setObjectName("Btn_CheckSteelDensity")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "钢种管理"))
        self.Btn_Exit.setText(_translate("Dialog", "退出"))
        self.Btn_changeSteelType.setText(_translate("Dialog", "更换钢种"))
        self.Btn_changeSteelDensity.setText(_translate("Dialog", "更换密度"))
        self.label.setText(_translate("Dialog", "当前钢种:"))
        self.Lab_showSteelType.setText(_translate("Dialog", "通用钢种"))
        self.Btn_addSteelType.setText(_translate("Dialog", "新增钢种"))
        self.Btn_delSteelType.setText(_translate("Dialog", "删除钢种"))
        self.Btn_CheckSteelDensity.setText(_translate("Dialog", "查看密度"))

