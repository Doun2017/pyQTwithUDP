# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWin.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(860, 721)
        MainWindow.setAcceptDrops(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.verticalLayout_left = QtWidgets.QVBoxLayout()
        self.verticalLayout_left.setObjectName("verticalLayout_left")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.connecting_point_status_listView = QtWidgets.QListView(self.groupBox)
        self.connecting_point_status_listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.connecting_point_status_listView.setObjectName("connecting_point_status_listView")
        self.verticalLayout_4.addWidget(self.connecting_point_status_listView)
        self.verticalLayout_left.addWidget(self.groupBox)
        self.groupBox_control = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_control.setMinimumSize(QtCore.QSize(0, 330))
        self.groupBox_control.setObjectName("groupBox_control")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_control)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_3 = QtWidgets.QLabel(self.groupBox_control)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_7.addWidget(self.label_3)
        self.id_settint_comboBox = QtWidgets.QComboBox(self.groupBox_control)
        self.id_settint_comboBox.setObjectName("id_settint_comboBox")
        self.horizontalLayout_7.addWidget(self.id_settint_comboBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.id_settint_pushButton = QtWidgets.QPushButton(self.groupBox_control)
        self.id_settint_pushButton.setObjectName("id_settint_pushButton")
        self.horizontalLayout_7.addWidget(self.id_settint_pushButton)
        self.horizontalLayout_7.setStretch(0, 1)
        self.horizontalLayout_7.setStretch(1, 1)
        self.horizontalLayout_7.setStretch(2, 1)
        self.horizontalLayout_7.setStretch(3, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_11 = QtWidgets.QLabel(self.groupBox_control)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_10.addWidget(self.label_11)
        self.frequencyband_comboBox = QtWidgets.QComboBox(self.groupBox_control)
        self.frequencyband_comboBox.setObjectName("frequencyband_comboBox")
        self.horizontalLayout_10.addWidget(self.frequencyband_comboBox)
        self.frequencyband_pushButton = QtWidgets.QPushButton(self.groupBox_control)
        self.frequencyband_pushButton.setObjectName("frequencyband_pushButton")
        self.horizontalLayout_10.addWidget(self.frequencyband_pushButton)
        self.horizontalLayout_10.setStretch(0, 1)
        self.horizontalLayout_10.setStretch(1, 2)
        self.horizontalLayout_10.setStretch(2, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox_control)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.center_frequency_spinBox = QtWidgets.QSpinBox(self.groupBox_control)
        self.center_frequency_spinBox.setMinimum(1000)
        self.center_frequency_spinBox.setMaximum(2000)
        self.center_frequency_spinBox.setObjectName("center_frequency_spinBox")
        self.horizontalLayout_3.addWidget(self.center_frequency_spinBox)
        self.label_5 = QtWidgets.QLabel(self.groupBox_control)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.center_frequency_pushButton = QtWidgets.QPushButton(self.groupBox_control)
        self.center_frequency_pushButton.setObjectName("center_frequency_pushButton")
        self.horizontalLayout_3.addWidget(self.center_frequency_pushButton)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 1)
        self.horizontalLayout_3.setStretch(2, 1)
        self.horizontalLayout_3.setStretch(3, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.line_2 = QtWidgets.QFrame(self.groupBox_control)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label = QtWidgets.QLabel(self.groupBox_control)
        self.label.setObjectName("label")
        self.horizontalLayout_6.addWidget(self.label)
        self.frequency_comboBox = QtWidgets.QComboBox(self.groupBox_control)
        self.frequency_comboBox.setObjectName("frequency_comboBox")
        self.horizontalLayout_6.addWidget(self.frequency_comboBox)
        self.label_9 = QtWidgets.QLabel(self.groupBox_control)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_6.addWidget(self.label_9)
        self.frequency_pushButton = QtWidgets.QPushButton(self.groupBox_control)
        self.frequency_pushButton.setObjectName("frequency_pushButton")
        self.horizontalLayout_6.addWidget(self.frequency_pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_10 = QtWidgets.QLabel(self.groupBox_control)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_11.addWidget(self.label_10)
        self.use_band_comboBox = QtWidgets.QComboBox(self.groupBox_control)
        self.use_band_comboBox.setObjectName("use_band_comboBox")
        self.horizontalLayout_11.addWidget(self.use_band_comboBox)
        self.use_band_pushButton = QtWidgets.QPushButton(self.groupBox_control)
        self.use_band_pushButton.setObjectName("use_band_pushButton")
        self.horizontalLayout_11.addWidget(self.use_band_pushButton)
        self.horizontalLayout_11.setStretch(0, 1)
        self.horizontalLayout_11.setStretch(1, 2)
        self.horizontalLayout_11.setStretch(2, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_11)
        self.line = QtWidgets.QFrame(self.groupBox_control)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox_control)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.synchronization_inside_radioButton = QtWidgets.QRadioButton(self.groupBox_control)
        self.synchronization_inside_radioButton.setChecked(True)
        self.synchronization_inside_radioButton.setObjectName("synchronization_inside_radioButton")
        self.horizontalLayout_2.addWidget(self.synchronization_inside_radioButton)
        self.synchronization_outside_radioButton = QtWidgets.QRadioButton(self.groupBox_control)
        self.synchronization_outside_radioButton.setObjectName("synchronization_outside_radioButton")
        self.horizontalLayout_2.addWidget(self.synchronization_outside_radioButton)
        self.synchronization_pushButton = QtWidgets.QPushButton(self.groupBox_control)
        self.synchronization_pushButton.setObjectName("synchronization_pushButton")
        self.horizontalLayout_2.addWidget(self.synchronization_pushButton)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 1)
        self.horizontalLayout_2.setStretch(3, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.line_3 = QtWidgets.QFrame(self.groupBox_control)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_6 = QtWidgets.QLabel(self.groupBox_control)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.high_priority_spinBox = QtWidgets.QSpinBox(self.groupBox_control)
        self.high_priority_spinBox.setMinimum(5000)
        self.high_priority_spinBox.setMaximum(65535)
        self.high_priority_spinBox.setObjectName("high_priority_spinBox")
        self.horizontalLayout_4.addWidget(self.high_priority_spinBox)
        self.label_7 = QtWidgets.QLabel(self.groupBox_control)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_4.addWidget(self.label_7)
        self.middle_priority_spinBox = QtWidgets.QSpinBox(self.groupBox_control)
        self.middle_priority_spinBox.setMinimum(5000)
        self.middle_priority_spinBox.setMaximum(65535)
        self.middle_priority_spinBox.setObjectName("middle_priority_spinBox")
        self.horizontalLayout_4.addWidget(self.middle_priority_spinBox)
        self.priority_pushButton = QtWidgets.QPushButton(self.groupBox_control)
        self.priority_pushButton.setObjectName("priority_pushButton")
        self.horizontalLayout_4.addWidget(self.priority_pushButton)
        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(2, 1)
        self.horizontalLayout_4.setStretch(4, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout_left.addWidget(self.groupBox_control)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_5.addWidget(self.label_8)
        self.dst_ip_textEdit = QtWidgets.QTextEdit(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dst_ip_textEdit.sizePolicy().hasHeightForWidth())
        self.dst_ip_textEdit.setSizePolicy(sizePolicy)
        self.dst_ip_textEdit.setMinimumSize(QtCore.QSize(0, 15))
        self.dst_ip_textEdit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.dst_ip_textEdit.setObjectName("dst_ip_textEdit")
        self.horizontalLayout_5.addWidget(self.dst_ip_textEdit)
        self.audio_pushButton = QtWidgets.QPushButton(self.groupBox_2)
        self.audio_pushButton.setObjectName("audio_pushButton")
        self.horizontalLayout_5.addWidget(self.audio_pushButton)
        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 2)
        self.horizontalLayout_5.setStretch(2, 1)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.verticalLayout_left.addWidget(self.groupBox_2)
        self.horizontalLayout_9.addLayout(self.verticalLayout_left)
        self.verticalLayout_right = QtWidgets.QVBoxLayout()
        self.verticalLayout_right.setObjectName("verticalLayout_right")
        self.groupBox_netStatus = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_netStatus.setObjectName("groupBox_netStatus")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.groupBox_netStatus)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.netStatus_listView = QtWidgets.QListView(self.groupBox_netStatus)
        self.netStatus_listView.setObjectName("netStatus_listView")
        self.horizontalLayout_13.addWidget(self.netStatus_listView)
        self.horizontalLayout_13.setStretch(0, 1)
        self.verticalLayout_right.addWidget(self.groupBox_netStatus)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.device_list_listView = QtWidgets.QListView(self.centralwidget)
        self.device_list_listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.device_list_listView.setObjectName("device_list_listView")
        self.horizontalLayout_8.addWidget(self.device_list_listView)
        self.point_status_listView = QtWidgets.QListView(self.centralwidget)
        self.point_status_listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.point_status_listView.setObjectName("point_status_listView")
        self.horizontalLayout_8.addWidget(self.point_status_listView)
        self.verticalLayout_right.addLayout(self.horizontalLayout_8)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_right.addWidget(self.pushButton)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_open = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_open.setObjectName("pushButton_open")
        self.horizontalLayout.addWidget(self.pushButton_open)
        self.pushButton_close = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_close.setObjectName("pushButton_close")
        self.horizontalLayout.addWidget(self.pushButton_close)
        self.auto_start_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.auto_start_checkBox.setObjectName("auto_start_checkBox")
        self.horizontalLayout.addWidget(self.auto_start_checkBox)
        self.auto_start_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.auto_start_pushButton.setObjectName("auto_start_pushButton")
        self.horizontalLayout.addWidget(self.auto_start_pushButton)
        self.verticalLayout_right.addLayout(self.horizontalLayout)
        self.horizontalLayout_9.addLayout(self.verticalLayout_right)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "QBL测试程序"))
        self.groupBox.setTitle(_translate("MainWindow", "直连节点状态"))
        self.groupBox_control.setTitle(_translate("MainWindow", "控制"))
        self.label_3.setText(_translate("MainWindow", "工作模式:"))
        self.id_settint_pushButton.setText(_translate("MainWindow", "设置"))
        self.label_11.setText(_translate("MainWindow", "占用频段："))
        self.frequencyband_pushButton.setText(_translate("MainWindow", "设置"))
        self.label_4.setText(_translate("MainWindow", "中心频点:"))
        self.label_5.setText(_translate("MainWindow", "MHz"))
        self.center_frequency_pushButton.setText(_translate("MainWindow", "设置"))
        self.label.setText(_translate("MainWindow", "速率等级:"))
        self.label_9.setText(_translate("MainWindow", "Mbps"))
        self.frequency_pushButton.setText(_translate("MainWindow", "设置"))
        self.label_10.setText(_translate("MainWindow", "占用带宽："))
        self.use_band_pushButton.setText(_translate("MainWindow", "设置"))
        self.label_2.setText(_translate("MainWindow", "同步:"))
        self.synchronization_inside_radioButton.setText(_translate("MainWindow", "自同步"))
        self.synchronization_outside_radioButton.setText(_translate("MainWindow", "外同步"))
        self.synchronization_pushButton.setText(_translate("MainWindow", "设置"))
        self.label_6.setText(_translate("MainWindow", "优先级端口 高:"))
        self.label_7.setText(_translate("MainWindow", "中："))
        self.priority_pushButton.setText(_translate("MainWindow", "设置"))
        self.groupBox_2.setTitle(_translate("MainWindow", "音频设置"))
        self.label_8.setText(_translate("MainWindow", "目的地址:"))
        self.audio_pushButton.setText(_translate("MainWindow", "设置"))
        self.groupBox_netStatus.setTitle(_translate("MainWindow", "网络拓扑"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_open.setText(_translate("MainWindow", "开始"))
        self.pushButton_close.setText(_translate("MainWindow", "停止"))
        self.auto_start_checkBox.setText(_translate("MainWindow", "波形自启动"))
        self.auto_start_pushButton.setText(_translate("MainWindow", "设置"))
