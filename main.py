# -*- coding: utf-8 -*-
import sys, os
import configparser
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.QtWidgets import QApplication, QMainWindow
import udp_control, udp_test_data, udp_text


class MyMainWindow(QMainWindow, udp_control.UdpControLogic, 
udp_test_data.UdpTestDataLogic, udp_text.UdpTextLogic):
    def __init__(self, parent=None):    
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.readIniFile()
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
        # 启动UDP
        self.control_udp_client_start(self.configIP, self.configPort)
        self.testdata_udp_server_start(6001)
        self.text_udp_server_start(6002)

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

    def sendTextData(self):
        self.text_udp_client_send(self.getCheckedIP(), 6002)

    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        # 连接时根据用户选择的功能调用函数
        self.control_udp_close()
        self.testdata_udp_close_all()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())
