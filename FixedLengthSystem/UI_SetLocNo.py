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
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(70, 40, 341, 123))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Labtxt_ClassNo = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.Labtxt_ClassNo.setStyleSheet("font: 12pt \\\"微软雅黑\\\";")
        self.Labtxt_ClassNo.setObjectName("Labtxt_ClassNo")
        self.verticalLayout.addWidget(self.Labtxt_ClassNo)
        self.LabInput_LocNo = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.LabInput_LocNo.setStyleSheet("font: 12pt \\\"微软雅黑\\\";")
        self.LabInput_LocNo.setObjectName("LabInput_LocNo")
        self.verticalLayout.addWidget(self.LabInput_LocNo)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(80, 210, 321, 71))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.Btn_LocNoNo = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Btn_LocNoNo.setObjectName("Btn_LocNoNo")
        self.gridLayout_2.addWidget(self.Btn_LocNoNo, 0, 1, 1, 1)
        self.Btn_LocNoYes = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Btn_LocNoYes.setObjectName("Btn_LocNoYes")
        self.gridLayout_2.addWidget(self.Btn_LocNoYes, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "修改连铸机号"))
        self.Labtxt_ClassNo.setText(_translate("Dialog", "当前连铸机号:"))
        self.Btn_LocNoNo.setText(_translate("Dialog", "取消"))
        self.Btn_LocNoYes.setText(_translate("Dialog", "确定"))