# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_AddSteelType.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 239)
        self.Lne_steelName = QtWidgets.QLineEdit(Dialog)
        self.Lne_steelName.setGeometry(QtCore.QRect(220, 40, 132, 21))
        self.Lne_steelName.setObjectName("Lne_steelName")
        self.Lne_steelDensity = QtWidgets.QLineEdit(Dialog)
        self.Lne_steelDensity.setGeometry(QtCore.QRect(220, 90, 132, 21))
        self.Lne_steelDensity.setObjectName("Lne_steelDensity")
        self.Lab_showSteelType = QtWidgets.QLabel(Dialog)
        self.Lab_showSteelType.setGeometry(QtCore.QRect(60, 40, 72, 15))
        self.Lab_showSteelType.setObjectName("Lab_showSteelType")
        self.Lab_showSteelType_2 = QtWidgets.QLabel(Dialog)
        self.Lab_showSteelType_2.setGeometry(QtCore.QRect(40, 90, 151, 16))
        self.Lab_showSteelType_2.setObjectName("Lab_showSteelType_2")
        self.Btn_Yes = QtWidgets.QPushButton(Dialog)
        self.Btn_Yes.setGeometry(QtCore.QRect(60, 170, 93, 28))
        self.Btn_Yes.setObjectName("Btn_Yes")
        self.Btn_No = QtWidgets.QPushButton(Dialog)
        self.Btn_No.setGeometry(QtCore.QRect(240, 170, 93, 28))
        self.Btn_No.setObjectName("Btn_No")
        self.Lab_showSteelType.setBuddy(self.Lne_steelName)
        self.Lab_showSteelType_2.setBuddy(self.Lne_steelDensity)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Lab_showSteelType.setText(_translate("Dialog", "钢种名称:"))
        self.Lab_showSteelType_2.setText(_translate("Dialog", "钢种密度(吨/立方米):"))
        self.Btn_Yes.setText(_translate("Dialog", "确定"))
        self.Btn_No.setText(_translate("Dialog", "取消"))

