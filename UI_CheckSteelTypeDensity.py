# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_CheckSteelTypeDensity.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(434, 778)
        self.Btn_Exit = QtWidgets.QPushButton(Dialog)
        self.Btn_Exit.setGeometry(QtCore.QRect(250, 730, 93, 28))
        self.Btn_Exit.setObjectName("Btn_Exit")
        self.TaW_CheckSteelDensity = QtWidgets.QTableWidget(Dialog)
        self.TaW_CheckSteelDensity.setGeometry(QtCore.QRect(40, 30, 351, 681))
        self.TaW_CheckSteelDensity.setObjectName("TaW_CheckSteelDensity")
        self.TaW_CheckSteelDensity.setColumnCount(0)
        self.TaW_CheckSteelDensity.setRowCount(0)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Btn_Exit.setText(_translate("Dialog", "退出"))

