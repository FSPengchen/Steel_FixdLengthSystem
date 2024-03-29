# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_ProductionData.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1279, 758)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.TaW_ProductionData = QtWidgets.QTableWidget(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TaW_ProductionData.sizePolicy().hasHeightForWidth())
        self.TaW_ProductionData.setSizePolicy(sizePolicy)
        self.TaW_ProductionData.setObjectName("TaW_ProductionData")
        self.TaW_ProductionData.setColumnCount(0)
        self.TaW_ProductionData.setRowCount(0)
        self.horizontalLayout.addWidget(self.TaW_ProductionData)
        self.frame = QtWidgets.QFrame(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.line_3 = QtWidgets.QFrame(self.frame)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout_5.addWidget(self.line_3, 3, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_18 = QtWidgets.QLabel(self.frame)
        self.label_18.setObjectName("label_18")
        self.gridLayout_2.addWidget(self.label_18, 4, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 3, 1, 1, 1)
        self.Lne_LengRangeTo = QtWidgets.QLineEdit(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Lne_LengRangeTo.sizePolicy().hasHeightForWidth())
        self.Lne_LengRangeTo.setSizePolicy(sizePolicy)
        self.Lne_LengRangeTo.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Lne_LengRangeTo.setObjectName("Lne_LengRangeTo")
        self.gridLayout_2.addWidget(self.Lne_LengRangeTo, 4, 0, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setMinimumSize(QtCore.QSize(30, 1))
        self.label_13.setObjectName("label_13")
        self.gridLayout_2.addWidget(self.label_13, 1, 0, 1, 1)
        self.Lne_LengRangeFrom = QtWidgets.QLineEdit(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Lne_LengRangeFrom.sizePolicy().hasHeightForWidth())
        self.Lne_LengRangeFrom.setSizePolicy(sizePolicy)
        self.Lne_LengRangeFrom.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Lne_LengRangeFrom.setObjectName("Lne_LengRangeFrom")
        self.gridLayout_2.addWidget(self.Lne_LengRangeFrom, 3, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 0, 0, 1, 2)
        self.gridLayout_5.addLayout(self.gridLayout_2, 1, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_16 = QtWidgets.QLabel(self.frame)
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 0, 0, 1, 1)
        self.Det_DateRangeFrom = QtWidgets.QDateEdit(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Det_DateRangeFrom.sizePolicy().hasHeightForWidth())
        self.Det_DateRangeFrom.setSizePolicy(sizePolicy)
        self.Det_DateRangeFrom.setMinimumSize(QtCore.QSize(100, 30))
        self.Det_DateRangeFrom.setObjectName("Det_DateRangeFrom")
        self.gridLayout.addWidget(self.Det_DateRangeFrom, 0, 1, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.frame)
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName("label_17")
        self.gridLayout.addWidget(self.label_17, 1, 0, 1, 1)
        self.Tet_TimeRangeTo = QtWidgets.QTimeEdit(self.frame)
        self.Tet_TimeRangeTo.setObjectName("Tet_TimeRangeTo")
        self.gridLayout.addWidget(self.Tet_TimeRangeTo, 1, 2, 1, 1)
        self.Det_DateRangeTo = QtWidgets.QDateEdit(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Det_DateRangeTo.sizePolicy().hasHeightForWidth())
        self.Det_DateRangeTo.setSizePolicy(sizePolicy)
        self.Det_DateRangeTo.setMinimumSize(QtCore.QSize(80, 30))
        self.Det_DateRangeTo.setObjectName("Det_DateRangeTo")
        self.gridLayout.addWidget(self.Det_DateRangeTo, 1, 1, 1, 1)
        self.Tet_TimeRangeFrom = QtWidgets.QTimeEdit(self.frame)
        self.Tet_TimeRangeFrom.setObjectName("Tet_TimeRangeFrom")
        self.gridLayout.addWidget(self.Tet_TimeRangeFrom, 0, 2, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.line_2 = QtWidgets.QFrame(self.frame)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_4.addWidget(self.line_2, 0, 0, 1, 2)
        self.label_19 = QtWidgets.QLabel(self.frame)
        self.label_19.setObjectName("label_19")
        self.gridLayout_4.addWidget(self.label_19, 3, 1, 1, 1)
        self.Lne_SetWeightFrom = QtWidgets.QLineEdit(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Lne_SetWeightFrom.sizePolicy().hasHeightForWidth())
        self.Lne_SetWeightFrom.setSizePolicy(sizePolicy)
        self.Lne_SetWeightFrom.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Lne_SetWeightFrom.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Lne_SetWeightFrom.setObjectName("Lne_SetWeightFrom")
        self.gridLayout_4.addWidget(self.Lne_SetWeightFrom, 3, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 4, 1, 1, 1)
        self.Lne_SetWeightTo = QtWidgets.QLineEdit(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Lne_SetWeightTo.sizePolicy().hasHeightForWidth())
        self.Lne_SetWeightTo.setSizePolicy(sizePolicy)
        self.Lne_SetWeightTo.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Lne_SetWeightTo.setObjectName("Lne_SetWeightTo")
        self.gridLayout_4.addWidget(self.Lne_SetWeightTo, 4, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setObjectName("label_10")
        self.gridLayout_4.addWidget(self.label_10, 2, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_4, 2, 0, 1, 1)
        self.Btn_excelExport = QtWidgets.QPushButton(self.frame)
        self.Btn_excelExport.setObjectName("Btn_excelExport")
        self.gridLayout_5.addWidget(self.Btn_excelExport, 7, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)
        self.cb_selectTeam = QtWidgets.QComboBox(self.frame)
        self.cb_selectTeam.setObjectName("cb_selectTeam")
        self.cb_selectTeam.addItem("")
        self.cb_selectTeam.addItem("")
        self.cb_selectTeam.addItem("")
        self.cb_selectTeam.addItem("")
        self.cb_selectTeam.addItem("")
        self.gridLayout_3.addWidget(self.cb_selectTeam, 0, 1, 1, 1)
        self.cb_selectFlow = QtWidgets.QComboBox(self.frame)
        self.cb_selectFlow.setObjectName("cb_selectFlow")
        self.cb_selectFlow.addItem("")
        self.cb_selectFlow.addItem("")
        self.cb_selectFlow.addItem("")
        self.cb_selectFlow.addItem("")
        self.cb_selectFlow.addItem("")
        self.gridLayout_3.addWidget(self.cb_selectFlow, 1, 1, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.frame)
        self.label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.label_20.setObjectName("label_20")
        self.gridLayout_3.addWidget(self.label_20, 1, 0, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.frame)
        self.label_21.setAlignment(QtCore.Qt.AlignCenter)
        self.label_21.setObjectName("label_21")
        self.gridLayout_3.addWidget(self.label_21, 2, 0, 1, 1)
        self.cb_selectSteelType = QtWidgets.QComboBox(self.frame)
        self.cb_selectSteelType.setObjectName("cb_selectSteelType")
        self.gridLayout_3.addWidget(self.cb_selectSteelType, 2, 1, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_3, 4, 0, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.frame)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout_5.addWidget(self.pushButton_4, 9, 0, 1, 1)
        self.Btn_Query = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Btn_Query.sizePolicy().hasHeightForWidth())
        self.Btn_Query.setSizePolicy(sizePolicy)
        self.Btn_Query.setObjectName("Btn_Query")
        self.gridLayout_5.addWidget(self.Btn_Query, 6, 0, 1, 1)
        self.Btn_PrintSupport = QtWidgets.QPushButton(self.frame)
        self.Btn_PrintSupport.setObjectName("Btn_PrintSupport")
        self.gridLayout_5.addWidget(self.Btn_PrintSupport, 8, 0, 1, 1)
        self.horizontalLayout.addWidget(self.frame)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.label_13.setBuddy(self.Lne_LengRangeFrom)
        self.label_10.setBuddy(self.Lne_SetWeightFrom)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.Tet_TimeRangeFrom, self.TaW_ProductionData)
        Dialog.setTabOrder(self.TaW_ProductionData, self.Lne_SetWeightFrom)
        Dialog.setTabOrder(self.Lne_SetWeightFrom, self.Lne_LengRangeFrom)
        Dialog.setTabOrder(self.Lne_LengRangeFrom, self.Lne_LengRangeTo)
        Dialog.setTabOrder(self.Lne_LengRangeTo, self.Det_DateRangeFrom)
        Dialog.setTabOrder(self.Det_DateRangeFrom, self.Det_DateRangeTo)
        Dialog.setTabOrder(self.Det_DateRangeTo, self.Tet_TimeRangeTo)
        Dialog.setTabOrder(self.Tet_TimeRangeTo, self.Btn_excelExport)
        Dialog.setTabOrder(self.Btn_excelExport, self.Btn_PrintSupport)
        Dialog.setTabOrder(self.Btn_PrintSupport, self.pushButton_4)
        Dialog.setTabOrder(self.pushButton_4, self.cb_selectTeam)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "生产数据管理对话框"))
        self.label_18.setText(_translate("Dialog", "至"))
        self.label.setText(_translate("Dialog", "毫米"))
        self.Lne_LengRangeTo.setText(_translate("Dialog", "13000"))
        self.label_13.setText(_translate("Dialog", "定尺范围"))
        self.Lne_LengRangeFrom.setText(_translate("Dialog", "11000"))
        self.label_16.setText(_translate("Dialog", "起始时间"))
        self.label_17.setText(_translate("Dialog", "结束时间"))
        self.label_19.setText(_translate("Dialog", "公斤"))
        self.Lne_SetWeightFrom.setText(_translate("Dialog", "0"))
        self.label_4.setText(_translate("Dialog", "至"))
        self.Lne_SetWeightTo.setText(_translate("Dialog", "3000"))
        self.label_10.setText(_translate("Dialog", "设定重量"))
        self.Btn_excelExport.setText(_translate("Dialog", "导出Excel表"))
        self.label_7.setText(_translate("Dialog", "班次"))
        self.cb_selectTeam.setItemText(0, _translate("Dialog", "全部"))
        self.cb_selectTeam.setItemText(1, _translate("Dialog", "甲班"))
        self.cb_selectTeam.setItemText(2, _translate("Dialog", "乙班"))
        self.cb_selectTeam.setItemText(3, _translate("Dialog", "丙班"))
        self.cb_selectTeam.setItemText(4, _translate("Dialog", "丁班"))
        self.cb_selectFlow.setItemText(0, _translate("Dialog", "全部"))
        self.cb_selectFlow.setItemText(1, _translate("Dialog", "1"))
        self.cb_selectFlow.setItemText(2, _translate("Dialog", "2"))
        self.cb_selectFlow.setItemText(3, _translate("Dialog", "3"))
        self.cb_selectFlow.setItemText(4, _translate("Dialog", "4"))
        self.label_20.setText(_translate("Dialog", "流"))
        self.label_21.setText(_translate("Dialog", "钢种"))
        self.pushButton_4.setText(_translate("Dialog", "退出"))
        self.Btn_Query.setText(_translate("Dialog", "查询"))
        self.Btn_PrintSupport.setText(_translate("Dialog", "打印"))
