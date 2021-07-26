# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_SetSteelData.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(595, 536)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(200, 10, 111, 21))
        self.label.setObjectName("label")
        self.Btn_addLength = QtWidgets.QPushButton(Dialog)
        self.Btn_addLength.setGeometry(QtCore.QRect(460, 90, 111, 28))
        self.Btn_addLength.setObjectName("Btn_addLength")
        self.Btn_delLength = QtWidgets.QPushButton(Dialog)
        self.Btn_delLength.setGeometry(QtCore.QRect(460, 130, 111, 28))
        self.Btn_delLength.setObjectName("Btn_delLength")
        self.Btn_Exit = QtWidgets.QPushButton(Dialog)
        self.Btn_Exit.setGeometry(QtCore.QRect(470, 470, 111, 28))
        self.Btn_Exit.setObjectName("Btn_Exit")
        self.Btn_switchLength = QtWidgets.QPushButton(Dialog)
        self.Btn_switchLength.setGeometry(QtCore.QRect(460, 210, 111, 28))
        self.Btn_switchLength.setObjectName("Btn_switchLength")
        self.Btn_chgLength = QtWidgets.QPushButton(Dialog)
        self.Btn_chgLength.setGeometry(QtCore.QRect(460, 170, 111, 28))
        self.Btn_chgLength.setObjectName("Btn_chgLength")
        self.LW_lengthType = QtWidgets.QListWidget(Dialog)
        self.LW_lengthType.setGeometry(QtCore.QRect(30, 40, 411, 471))
        self.LW_lengthType.setObjectName("LW_lengthType")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "定尺选择（所有流）"))
        self.label.setText(_translate("Dialog", "定尺列表"))
        self.Btn_addLength.setText(_translate("Dialog", "添加新定尺"))
        self.Btn_delLength.setText(_translate("Dialog", "删除所选定尺"))
        self.Btn_Exit.setText(_translate("Dialog", "退出"))
        self.Btn_switchLength.setText(_translate("Dialog", "切换定尺"))
        self.Btn_chgLength.setText(_translate("Dialog", "修改所选定尺"))

