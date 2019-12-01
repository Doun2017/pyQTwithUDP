# -*- coding: utf-8 -*-
import sys, os
import threading
import configparser
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QRectF, Qt, QStringListModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QGraphicsScene, QGraphicsRectItem, QGraphicsItem, QGraphicsEllipseItem

import udp_control
import stopThreading
from netGraphics import QMyGraphicsview
from configparser import NoOptionError

class MyMainWindow(QMainWindow, udp_control.UdpControLogic):
    Alt_pressed=False

    def __init__(self, parent=None):    
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        # 在状态栏添加数据展示
        self.labItemMsg = QLabel(u' ')
        self.labItemMsg.setMinimumWidth(150)
        self.statusbar.addWidget(self.labItemMsg)
        self.labServerAdr = QLabel(u' ')
        self.labServerAdr.setMinimumWidth(150)
        self.statusbar.addWidget(self.labServerAdr)

        self.loadIniFile()
        self.file_server = None
        self.file_client = None
        self.cwd = os.getcwd() # 获取当前程序文件位置
        # 信号连接
        self.frequency_pushButton.clicked.connect(self.sendFrequency)
        self.id_settint_pushButton.clicked.connect(self.sendID)
        self.synchronization_pushButton.clicked.connect(self.sendSynchronization)
        self.center_frequency_pushButton.clicked.connect(self.sendCenterFrequency)
        self.priority_pushButton.clicked.connect(self.sendPrioritywidth)
        self.audio_pushButton.clicked.connect(self.sendAudioDestID)
        # self.unfixed_frequency_radioButton.clicked.connect(self.slot_btn_unfix_frequency)
        # self.fixed_frequency_radioButton.clicked.connect(self.slot_btn_fix_frequency)
        self.pushButton_open.clicked.connect(self.slot_btn_open)
        self.pushButton_close.clicked.connect(self.slot_btn_close)
        self.auto_start_pushButton.clicked.connect(self.slot_btn_auto)

        self.signal_conecting_point_status_msg.connect(self.slot_receive_connecting_point_status)
        self.signal_net_point_status_msg.connect(self.slot_receive_net_point_status)

        self.netStatus_listView.setVisible(False)
        # 启动UDP
        self.control_udp_client_start(self.configIP, self.configPort)
        # 初始化绘图
        self.initGraphicsUI()
        # 初始化各个list
        self.initInfoLists()

    def initInfoLists(self):
        # 初始化网络节点信息列表
        # 实例化列表模型，添加数据
        self.point_status_slm = QStringListModel()
        # 设置列表视图的模型
        self.point_status_listView.setModel(self.point_status_slm)
        # 初始化入网节点列表
        self.device_list_slm = QStringListModel()
        self.device_list_listView.setModel(self.device_list_slm)
        self.refreshPointsInNet()
        # 初始化直连节点状态列表
        self.connecting_point_status_slm = QStringListModel()
        self.connecting_point_status_listView.setModel(self.connecting_point_status_slm)

    def refreshPointsInNet(self):
        """
        刷新入网节点列表
        """
        note_list = ['入网节点列表：']
        for v in self.myView.devices.values():
            if v.route_info:
                note_list.append('ID：'+str(v.id))
        self.device_list_slm.setStringList(note_list)

    def initGraphicsUI(self):
        """
        初始化Graphics界面，建立相关的信号处理链接
        """
        self.myView = QMyGraphicsview()
        # self.myView.setCursor(Qt.CrossCursor)
        self.myView.setMouseTracking(True)
        self.myView.setMinimumSize(QtCore.QSize(410, 410))
        self.horizontalLayout_13.addWidget(self.myView, 3)
        # 绘图信号链接
        self.myView.sigMouseMovePoint.connect(self.slotMouseMovePoint)
        self.myView.sigNetDeviceItemPress.connect(self.slotDeviceItemPress)

    def slotMouseMovePoint(self, pt):
        """
        处理鼠标在Graphics上移动的消息
        """
        # self.labViewCorrd.setText('View 坐标：{}， {}'.format(pt.x(), pt.y()))
        # ptScene = self.myView.mapToScene(pt)
        # self.labScenecorrd.setText('Scene 坐标：{:.0f}, {:.0f}'.format(ptScene.x(), ptScene.y()))
        pass
        
    def slotDeviceItemPress(self, infos):
        """
        处理鼠标在Graphics上点击的消息
        """
        self.labItemMsg.setText(infos[0])
        self.point_status_slm.setStringList(infos)

    def loadIniFile(self):
        """
        加载ini配置文件
        """
        config = configparser.ConfigParser()    # 注意大小写
        config.read("config.ini")
        # 网络节点上接收命令的IP和port
        self.configIP = config.get('ControlConfig', 'ip')
        self.configPort = config.getint('ControlConfig', 'port')
        self.labServerAdr.setText(self.configIP + ':' + str(self.configPort))

        # 添加速率等级选项
        ilevel=0
        strlevel = config.get('level', 'level' + str(ilevel))
        while strlevel:
            self.frequency_comboBox.addItem(strlevel)
            ilevel += 1
            try:
                strlevel = config.get('level', 'level' + str(ilevel))
            except NoOptionError as ret:
                print(ret)
                break
        # 添加ID选项
        ilevel=0
        strid = config.get('id', 'id' + str(ilevel))
        while strid:
            self.id_settint_comboBox.addItem(strid)
            ilevel += 1
            try:
                strid = config.get('id', 'id' + str(ilevel))
            except NoOptionError as ret:
                print(ret)
                break

    def sendFrequency(self):
        msg = self.control_udp_send_frequency()
        print(msg)
        self.labItemMsg.setText('控制命令已发送：' + msg)

    def sendID(self):
        # msg = self.control_udp_send_ID()
        # print(msg)
        # self.labItemMsg.setText('控制命令已发送：' + msg)
        pass

    def sendSynchronization(self):
        msg = self.control_udp_send_synchronization()
        print(msg)
        self.labItemMsg.setText('控制命令已发送：' + msg)

    def sendCenterFrequency(self):
        msg = self.control_udp_send_center_frequency()
        print(msg)
        self.labItemMsg.setText('控制命令已发送：' + msg)
        
    def sendPrioritywidth(self):
        msg = self.control_udp_send_use_bandwidth()
        print(msg)
        self.labItemMsg.setText('控制命令已发送：' + msg)
        
    def sendAudioDestID(self):
        msg = self.control_udp_send_audio_destID()
        print(msg)
        self.labItemMsg.setText('控制命令已发送：' + msg)

    def slot_btn_open(self):
        msg = self.control_udp_send_open(True)
        print(msg)
        self.labItemMsg.setText('控制命令已发送：' + msg)
    def slot_btn_close(self):
        msg = self.control_udp_send_open(False)
        print(msg)
        self.labItemMsg.setText('控制命令已发送：' + msg)
    def slot_btn_auto(self):
        msg = self.control_udp_send_auto()
        print(msg)
        self.labItemMsg.setText('控制命令已发送：' + msg)

    # def slot_btn_fix_frequency(self):
    #     self.frequency_comboBox.setDisabled(False)
    # def slot_btn_unfix_frequency(self):
    #     self.frequency_comboBox.setDisabled(True)

    def slot_receive_connecting_point_status(self, status):
        """
        收到直连的网络节点状态信息
        """
        self.connecting_point_status_slm.setStringList(status)
        pass

    def slot_receive_net_point_status(self, id, status):
        """
        收到网络节点信息
        """
        self.myView.updateDevice(id, status)
        # self.refreshAudioDestIDList()
        self.refreshPointsInNet()
        
    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        # 连接时根据用户选择的功能调用函数
        self.control_udp_close()

    # 检测键盘回车按键，函数名字不要改，这是重写键盘事件
    def keyPressEvent(self, event):
        #这里event.key（）显示的是按键的编码
        print("按下：" + str(event.key()))
        # 举例，这里Qt.Key_A注意虽然字母大写，但按键事件对大小写不敏感
        # if (event.key() == Qt.Key_Shift):
        #     print('测试：Key_Shift')
        # if (event.key() == Qt.Key_Control):
        #     print('测试：Key_Control')
        if (event.key() == Qt.Key_Alt):
            print('测试：Key_Alt')
            self.Alt_pressed = True
            
    def keyReleaseEvent(self, event):
        #这里event.key（）显示的是按键的编码
        print("keyReleaseEvent：" + str(event.key()))
        # if (event.key() == Qt.Key_Shift):
        #     print('测试：Key_Shift')
        # if (event.key() == Qt.Key_Control):
        #     print('测试：Key_Control')
        if (event.key() == Qt.Key_Alt):
            print('测试：Key_Alt')
            self.Alt_pressed = False

    def mouseDoubleClickEvent(self, event):
        #这里event.key（）显示的是按键的编码
        print("mouseDoubleClickEvent" + str(event))
        if self.Alt_pressed:
            slist = self.connecting_point_status_slm.stringList()
            if ' ' in slist:
                print(self.control_udp_send_BEACON_DEV(0))
            else:
                print(self.control_udp_send_BEACON_DEV(1))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())
