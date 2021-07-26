# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_ChangeSteelTypeDensity.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(385, 219)
        self.Btn_No = QtWidgets.QPushButton(Dialog)
        self.Btn_No.setGeometry(QtCore.QRect(240, 140, 93, 28))
        self.Btn_No.setObjectName("Btn_No")
        self.Lne_steelDensity = QtWidgets.QLineEdit(Dialog)
        self.Lne_steelDensity.setGeometry(QtCore.QRect(220, 80, 132, 21))
        self.Lne_steelDensity.setObjectName("Lne_steelDensity")
        self.Lab_showSteelTypeDensity = QtWidgets.QLabel(Dialog)
        self.Lab_showSteelTypeDensity.setGeometry(QtCore.QRect(30, 80, 151, 16))
        self.Lab_showSteelTypeDensity.setObjectName("Lab_showSteelTypeDensity")
        self.Btn_Yes = QtWidgets.QPushButton(Dialog)
        self.Btn_Yes.setGeometry(QtCore.QRect(60, 140, 93, 28))
        self.Btn_Yes.setObjectName("Btn_Yes")
        self.Lab_showSteelType = QtWidgets.QLabel(Dialog)
        self.Lab_showSteelType.setGeometry(QtCore.QRect(60, 30, 72, 15))
        self.Lab_showSteelType.setObjectName("Lab_showSteelType")
        self.Lab_showSteelTypename = QtWidgets.QLabel(Dialog)
        self.Lab_showSteelTypename.setGeometry(QtCore.QRect(250, 30, 72, 15))
        self.Lab_showSteelTypename.setObjectName("Lab_showSteelTypename")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Btn_No.setText(_translate("Dialog", "取消"))
        self.Lab_showSteelTypeDensity.setText(_translate("Dialog", "钢种密度(吨/立方米):"))
        self.Btn_Yes.setText(_translate("Dialog", "确定"))
        self.Lab_showSteelType.setText(_translate("Dialog", "钢种名称:"))
        self.Lab_showSteelTypename.setText(_translate("Dialog", "通用钢种"))

