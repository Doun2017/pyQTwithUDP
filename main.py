# -*- coding: utf-8 -*-
import sys, os
import threading
import configparser
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

import udp_control, udp_test_data, udp_text, udp_audio
from Server.server import LFTPserver
from Client.client import LFTPClient
import stopThreading


class MyMainWindow(QMainWindow, udp_control.UdpControLogic, 
        udp_test_data.UdpTestDataLogic, udp_text.UdpTextLogic, udp_audio.UdpAudioLogic):
    signal_file_receive_msg = pyqtSignal(str)
    signal_file_sending_msg = pyqtSignal(str)

    def __init__(self, parent=None):    
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.readIniFile()
        self.file_server = None
        self.file_client = None
        self.cwd = os.getcwd() # 获取当前程序文件位置
        # 信号连接
        self.frequency_pushButton.clicked.connect(self.sendFrequency)
        self.synchronization_pushButton.clicked.connect(self.sendSynchronization)
        self.testDataSend_start_pushButton.clicked.connect(self.startSendTestData)
        self.testDataSend_stop_pushButton.clicked.connect(self.stopSendTestData)
        self.testDataSend_clear_pushButton.clicked.connect(self.clearSendTestData)
        self.testDataReceive_clear_pushButton.clicked.connect(self.clearReceiveTestData)
        self.signal_receive_test_data_msg.connect(self.update_test_data_receive_sum)
        self.signal_receive_text_msg.connect(self.update_text_receive_sum)
        self.textSend_pushButton.clicked.connect(self.sendTextData)
        self.audioSend_start_pushButton.clicked.connect(self.startAudioSending)
        self.audioSend_stop_pushButton.clicked.connect(self.stopAudioSending)
        self.signal_file_receive_msg.connect(self.handle_signal_file_receive_msg)
        self.signal_file_sending_msg.connect(self.handle_signal_file_sending_msg)
        self.fileSend_chooseFile_pushButton.clicked.connect(self.slot_btn_chooseFile)
        self.fileSend_pushButton.clicked.connect(self.sendFile)

        # 启动UDP
        self.control_udp_client_start(self.configIP, self.configPort)
        self.testdata_udp_server_start(6001)
        self.text_udp_server_start(6002)
        self.audio_udp_server_start(6666)
        self.file_trans_server_th = threading.Thread(target=self.file_trans_server_concurrency)
        self.file_trans_server_th.start()

        
    def file_trans_server_concurrency(self):
        try:
            self.file_server = LFTPserver(server_type='control', host='', port=12345, bufferSize=2048, myMainWindow=self)
            self.file_server.start()
        except Exception as ret:
            print(ret)

    def file_trans_client_concurrency(self):
        try:
            filepath = str(self.fileSend_fileName_plainTextEdit.toPlainText())
            if len(filepath) == 0:
                return
            if os.path.isfile(filepath) == False:
                print("这不是一个文件:", filepath)
                return
            self.file_client = LFTPClient(self.getCheckedIP(), 12345, 1024, myMainWindow=self)
            self.file_client.start("UPLOAD", filepath)
        except Exception as ret:
            print(ret)

    def emitReceiveMessage(self, msg):
        self.signal_file_receive_msg.emit(msg)

    def emitSendingMessage(self, msg):
        self.signal_file_sending_msg.emit(msg)

    def readIniFile(self):
        config = configparser.ConfigParser()    # 注意大小写
        config.read("config.ini")
        self.configIP = config.get('ControlConfig', 'ip')
        self.configPort = config.getint('ControlConfig', 'port')
        self.IP1 = config.get('IPConfig', 'ip1')
        self.IP2 = config.get('IPConfig', 'ip2')
        self.IP3 = config.get('IPConfig', 'ip3')
        self.IP4 = config.get('IPConfig', 'ip4')
        self.IP5 = config.get('IPConfig', 'ip5')
        self.IP6 = config.get('IPConfig', 'ip6')
        self.IP1_radioButton.setText(self.IP1)
        self.IP2_radioButton.setText(self.IP2)
        self.IP3_radioButton.setText(self.IP3)
        self.IP4_radioButton.setText(self.IP4)
        self.IP5_radioButton.setText(self.IP5)
        self.IP6_radioButton.setText(self.IP6)
        self.sourceIP_comboBox.addItem(self.IP1)
        self.sourceIP_comboBox.addItem(self.IP2)
        self.sourceIP_comboBox.addItem(self.IP3)
        self.sourceIP_comboBox.addItem(self.IP4)
        self.sourceIP_comboBox.addItem(self.IP5)
        self.sourceIP_comboBox.addItem(self.IP6)

    def getCheckedIP(self):
        if self.IP1_radioButton.isChecked():
            return self.IP1_radioButton.text()
        if self.IP2_radioButton.isChecked():
            return self.IP2_radioButton.text()
        if self.IP3_radioButton.isChecked():
            return self.IP3_radioButton.text()
        if self.IP4_radioButton.isChecked():
            return self.IP4_radioButton.text()
        if self.IP5_radioButton.isChecked():
            return self.IP5_radioButton.text()
        if self.IP6_radioButton.isChecked():
            return self.IP6_radioButton.text()
        if self.broadcast_radioButton.isChecked():
            return self.broadcast_radioButton.text()
        return ""

    def sendFrequency(self):
        print("sendFrequency")
        self.control_udp_send_frequency()

    def sendSynchronization(self):
        print("synchronization")
        self.control_udp_send_synchronization()
        
    def startSendTestData(self):
        print("startSendTestData")
        self.testdata_udp_client_start(self.getCheckedIP(), 6001)
        self.testDataSend_start_pushButton.setEnabled(False)

    def stopSendTestData(self):
        print("stopSendTestData")
        self.testdata_udp_client_stop()
        self.testDataSend_start_pushButton.setEnabled(True)

    def clearSendTestData(self):
        print("clearSendTestData")
        self.testDataSend_label.setText('0Bytes')

    def clearReceiveTestData(self):
        print("clearSendTestData")
        self.testDataReceive_label.setText('0Bytes')

    def update_test_data_receive_sum(self, msg):
        self.testDataReceive_label.setText(msg)

    def update_text_receive_sum(self, msg):
        self.textReceive_plainTextEdit.appendPlainText(msg)

    def handle_signal_file_receive_msg(self, msg):
        self.fileReceive_plainTextEdit.appendPlainText(msg)

    def handle_signal_file_sending_msg(self, msg):
        self.fileSend_sending_info_label.setText(msg)

    def sendTextData(self):
        self.text_udp_client_send(self.getCheckedIP(), 6002)

    def startAudioSending(self):
        self.audio_udp_client_start(self.getCheckedIP(), 6666)
        self.audioSend_start_pushButton.setEnabled(False)

    def stopAudioSending(self):
        self.audio_udp_client_stop()
        self.audioSend_start_pushButton.setEnabled(True)

    def sendFile(self):
        self.file_trans_client_th = threading.Thread(target=self.file_trans_client_concurrency)
        self.file_trans_client_th.start()
            
    def slot_btn_chooseFile(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName(self,  
                                    "选取文件",  
                                    self.cwd, # 起始路径 
                                    "All Files (*);;Text Files (*.txt)")   # 设置文件扩展名过滤,用双分号间隔
        if fileName_choose == "":
            print("\n取消选择")
            return
        print("\n你选择的文件为:")
        print(fileName_choose)
        print("文件筛选器类型: ",filetype)
        self.fileSend_fileName_plainTextEdit.setPlainText(fileName_choose)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self,event):
        if event.mimeData().hasUrls():
            u = event.mimeData().urls()[0]
            path = u.path()
            if path[0] == '/':
                path = path[1:]
            self.fileSend_fileName_plainTextEdit.setPlainText(path)

    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        # 连接时根据用户选择的功能调用函数
        self.control_udp_close()
        self.testdata_udp_close_all()
        self.text_udp_close_all()
        self.audio_udp_close_all()
        self.file_server.stop()
        try:
            stopThreading.stop_thread(self.file_trans_client_th)
        except Exception:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())
