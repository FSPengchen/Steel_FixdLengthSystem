# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_SetFixLeng.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(790, 612)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 40, 161, 41))
        self.label.setStyleSheet("font: 12pt \"微软雅黑\";")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(40, 130, 161, 41))
        self.label_2.setStyleSheet("font: 12pt \"微软雅黑\";")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(450, 120, 161, 41))
        self.label_3.setStyleSheet("font: 12pt \"微软雅黑\";")
        self.label_3.setObjectName("label_3")
        self.Lne_PreClampOffset = QtWidgets.QTextEdit(Dialog)
        self.Lne_PreClampOffset.setGeometry(QtCore.QRect(440, 170, 161, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.Lne_PreClampOffset.setFont(font)
        self.Lne_PreClampOffset.setStyleSheet("background-color:black;\n"
"font: 10pt \"微软雅黑\";\n"
"color:red;")
        self.Lne_PreClampOffset.setObjectName("Lne_PreClampOffset")
        self.Btn__PreClampOffset = QtWidgets.QPushButton(Dialog)
        self.Btn__PreClampOffset.setGeometry(QtCore.QRect(630, 170, 141, 41))
        self.Btn__PreClampOffset.setObjectName("Btn__PreClampOffset")
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(50, 180, 101, 31))
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(50, 380, 181, 41))
        self.label_7.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(250, 380, 31, 41))
        self.label_8.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(Dialog)
        self.label_9.setGeometry(QtCore.QRect(380, 380, 61, 41))
        self.label_9.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(Dialog)
        self.label_10.setGeometry(QtCore.QRect(470, 380, 31, 41))
        self.label_10.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(Dialog)
        self.label_11.setGeometry(QtCore.QRect(50, 450, 261, 41))
        self.label_11.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(Dialog)
        self.label_12.setGeometry(QtCore.QRect(450, 450, 181, 41))
        self.label_12.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.label_12.setObjectName("label_12")
        self.Btn_FixLengYes = QtWidgets.QPushButton(Dialog)
        self.Btn_FixLengYes.setGeometry(QtCore.QRect(40, 560, 141, 41))
        self.Btn_FixLengYes.setObjectName("Btn_FixLengYes")
        self.Btn_FixLengNo = QtWidgets.QPushButton(Dialog)
        self.Btn_FixLengNo.setGeometry(QtCore.QRect(620, 560, 141, 41))
        self.Btn_FixLengNo.setObjectName("Btn_FixLengNo")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(50, 216, 159, 45))
        self.label_4.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.label_4.setObjectName("label_4")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(50, 268, 159, 45))
        self.label_6.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.label_6.setObjectName("label_6")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(50, 320, 159, 45))
        self.label_5.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.label_5.setObjectName("label_5")
        self.Ceb_AllowEdit = QtWidgets.QCheckBox(Dialog)
        self.Ceb_AllowEdit.setGeometry(QtCore.QRect(40, 110, 91, 19))
        self.Ceb_AllowEdit.setObjectName("Ceb_AllowEdit")
        self.Lne_FixWeiht = QtWidgets.QLineEdit(Dialog)
        self.Lne_FixWeiht.setGeometry(QtCore.QRect(240, 220, 151, 41))
        self.Lne_FixWeiht.setObjectName("Lne_FixWeiht")
        self.Lne_TheoryWeiht = QtWidgets.QLineEdit(Dialog)
        self.Lne_TheoryWeiht.setGeometry(QtCore.QRect(240, 270, 151, 41))
        self.Lne_TheoryWeiht.setObjectName("Lne_TheoryWeiht")
        self.Lne_Density = QtWidgets.QLineEdit(Dialog)
        self.Lne_Density.setGeometry(QtCore.QRect(240, 320, 151, 41))
        self.Lne_Density.setObjectName("Lne_Density")
        self.Lne_FixLength = QtWidgets.QLineEdit(Dialog)
        self.Lne_FixLength.setGeometry(QtCore.QRect(210, 40, 151, 41))
        self.Lne_FixLength.setObjectName("Lne_FixLength")
        self.Lne_ErrRangeMinus = QtWidgets.QLineEdit(Dialog)
        self.Lne_ErrRangeMinus.setGeometry(QtCore.QRect(270, 380, 81, 41))
        self.Lne_ErrRangeMinus.setObjectName("Lne_ErrRangeMinus")
        self.Lne_LengthRangeMax = QtWidgets.QLineEdit(Dialog)
        self.Lne_LengthRangeMax.setGeometry(QtCore.QRect(340, 450, 81, 41))
        self.Lne_LengthRangeMax.setObjectName("Lne_LengthRangeMax")
        self.Lne_ErrRangePlus = QtWidgets.QLineEdit(Dialog)
        self.Lne_ErrRangePlus.setGeometry(QtCore.QRect(500, 380, 81, 41))
        self.Lne_ErrRangePlus.setObjectName("Lne_ErrRangePlus")
        self.Lne_WeightMax = QtWidgets.QLineEdit(Dialog)
        self.Lne_WeightMax.setGeometry(QtCore.QRect(620, 450, 81, 41))
        self.Lne_WeightMax.setObjectName("Lne_WeightMax")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "输入定尺(计量单位：毫米)"))
        self.label.setText(_translate("Dialog", "定尺长度（毫米):"))
        self.label_2.setText(_translate("Dialog", "断面规格(宽*高):"))
        self.label_3.setText(_translate("Dialog", "预夹紧偏移："))
        self.Lne_PreClampOffset.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'微软雅黑\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">500</span></p></body></html>"))
        self.Btn__PreClampOffset.setText(_translate("Dialog", "修改预夹偏移"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("Dialog", "120*120"))
        item = self.listWidget.item(1)
        item.setText(_translate("Dialog", "111"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.label_7.setText(_translate("Dialog", "合格误差范围（公斤）:"))
        self.label_8.setText(_translate("Dialog", "-"))
        self.label_9.setText(_translate("Dialog", "------"))
        self.label_10.setText(_translate("Dialog", "+"))
        self.label_11.setText(_translate("Dialog", "容许最大调节长度范围（毫米）:"))
        self.label_12.setText(_translate("Dialog", "对应重量（公斤）:"))
        self.Btn_FixLengYes.setText(_translate("Dialog", "确定"))
        self.Btn_FixLengNo.setText(_translate("Dialog", "取消"))
        self.label_4.setText(_translate("Dialog", "定重（公斤）："))
        self.label_6.setText(_translate("Dialog", "理论重量（公斤）:"))
        self.label_5.setText(_translate("Dialog", "热态密度(吨/立方米):"))
        self.Ceb_AllowEdit.setText(_translate("Dialog", "允许编辑"))
