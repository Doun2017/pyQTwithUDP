import socket

import mainWin


class UdpControLogic(mainWin.Ui_MainWindow):
    def __init__(self):
        super(UdpControLogic, self).__init__()
        self.udp_socket = None
        self.address = None

    def control_udp_client_start(self, controlIP, controlPort):
        """
        确认UDP客户端的ip及地址
        :return:
        """
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.address = (controlIP, controlPort)
        except Exception:
            msg = '请检查控制IP\n'
            print(msg)
#            self.signal_write_msg.emit(msg)
        else:
            msg = '控制UDP客户端已启动\n'
            print(msg)
            self.link = True

#            self.signal_write_msg.emit(msg)

    def control_udp_send_frequency(self):
        value = self.frequency_spinBox.value()
        send_msg = ("frequency=" + str(value)).encode('utf-8')
        self.control_udp_send(send_msg)

    def control_udp_send_synchronization(self):
        way = ""
        if self.synchronization_inside_radioButton.isChecked():
            way = "in"
        if self.synchronization_outside_radioButton.isChecked():
            way = "out"
        send_msg = ("synchronization_way=" + way).encode('utf-8')
        self.control_udp_send(send_msg)

    def control_udp_send(self, datas):
        """
        功能函数，用于UDP客户端发送消息
        :return: None
        """
        if self.link is False:
            msg = '控制UDP尚未连接\n'
            print(msg)
        else:
            try:
                self.udp_socket.sendto(datas, self.address)
                msg = 'UDP客户端已发送\n'
                print(msg)
            except Exception as ret:
                msg = '发送失败\n'
                print(msg)

    def control_udp_close(self):
        """
        功能函数，关闭网络连接的方法
        :return:
        """
        try:
            self.udp_socket.close()
            self.link = True
            if self.link is True:
                msg = 'control 已断开网络\n'
                print(msg)
        except Exception:
            pass

#
#if __name__ == '__main__':
#    app = QtWidgets.QApplication(sys.argv)
#    ui = UdpControLogic()
#    ui.show()
#    sys.exit(app.exec_())
