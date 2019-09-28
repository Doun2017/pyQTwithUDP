# -*- coding: utf-8 -*-
import sys, os
import configparser
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.QtWidgets import QApplication, QMainWindow
import udp_control


class MyMainWindow(QMainWindow, udp_control.UdpControLogic):
    def __init__(self, parent=None):    
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.readIniFile()
        # 信号连接
        self.frequency_pushButton.clicked.connect(self.sendFrequency)
        self.synchronization_pushButton.clicked.connect(self.sendSynchronization)
        # 启动UDP
        self.control_udp_client_start(self.configIP, self.configPort)

    def connect(self, ):
        """
        控件信号-槽的设置
        :param : QDialog类创建的对象
        :return: None
        """
        # 如需传递参数可以修改为connect(lambda: self.click(参数))
        super(MainWindow, self).connect()

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

    def sendFrequency(self):
        print("sendFrequency")
        self.control_udp_send_frequency()

    def sendSynchronization(self):
        print("synchronization")
        self.control_udp_send_synchronization()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())
