import socket
import threading
import time
from PyQt5.QtCore import pyqtSignal

import mainWin
import stopThreading


class UdpControLogic(mainWin.Ui_MainWindow):
    # 直连节点发来的状态信息
    signal_conecting_point_status_msg = pyqtSignal(list)
    # 网络节点发来的状态信息
    signal_net_point_status_msg = pyqtSignal(int, list)

    def __init__(self):
        super(UdpControLogic, self).__init__()
        self.udp_socket = None
        self.dest_address = None

    def control_udp_client_start(self, controlIP, controlPort):
        """
        初始化UDP通信的socket，开启UDP接收线程
        :return:
        """
        if self.udp_socket == None:
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.dest_address = (controlIP, controlPort)
            address = ('', controlPort)
            self.udp_socket.bind(address)
        except Exception as ret:
            msg = '请检查控制IP\n'
            print(msg)
            print(ret)
        else:
            self.text_sever_th = threading.Thread(target=self.control_udp_server_concurrency)
            self.text_sever_th.start()
            msg = '控制UDP客户端已启动\n'
            print(msg)
            self.link = True


    choose = 0
    def control_udp_server_concurrency(self):
        """
        线程函数，UDP数据接收
        :return:
        """
        while True:
            try:
                recv_msg, recv_addr = self.udp_socket.recvfrom(10240)
                if recv_msg:
                    msg = recv_msg.decode('utf-8')
                    show_msg = str(recv_addr) + ":\n" + msg
                    print('control_udp_server receive:' + show_msg)
                    # 发布状态信息
                    if recv_msg.__len__()%2 == 0:
                        if self.choose == 0:
                            self.signal_net_point_status_msg.emit(1, [[0],[1,4,3,2],[1,4,3],[1,4],[0],[1,6]])
                            self.choose = 1
                        else:
                            self.signal_net_point_status_msg.emit(1, [[0],[1,4,3,2],[1,4,3],[1,4],[0],[0]])
                            self.choose = 0
                    else:
                        self.signal_net_point_status_msg.emit(2, [[2,1],[0],[2,4,3],[2,4],[0],[2,6]])

                        #self.signal_conecting_point_status_msg.emit(recv_msg)
                    # self.signal_net_point_status_msg.emit(recv_msg)
            except Exception as ret:
                msg = 'udp_socket 接收失败\n'
                time.sleep(0.1)
                print(msg)
                print(ret)
                break

    def control_udp_send_ID(self):
        """
        发送控制信息，id配置
        """
        value = self.id_settint_comboBox.currentIndex() + 1
        if self.id_settint_checkBox.isChecked():
            value += 1000
        send_msg = ("id=" + str(value))
        self.control_udp_send(send_msg.encode('utf-8'))
        return send_msg

    def control_udp_send_frequency(self):
        """
        发送控制信息，速率等级
        """
        if self.fixed_frequency_radioButton.isChecked():
            value = self.frequency_comboBox.currentText()
            send_msg = ("frequency=" + value)
        else:
            send_msg = "unfixed_frequency"
        self.control_udp_send(send_msg.encode('utf-8'))
        return send_msg

    def control_udp_send_synchronization(self):
        """
        发送控制信息，同步方式
        """
        way = ""
        if self.synchronization_inside_radioButton.isChecked():
            way = "in"
        if self.synchronization_outside_radioButton.isChecked():
            way = "out"
        send_msg = ("synchronization_way=" + way)
        self.control_udp_send(send_msg.encode('utf-8'))
        return send_msg

    def control_udp_send_center_frequency(self):
        """
        发送控制信息，中心频点
        """
        value = self.center_frequency_spinBox.text()
        send_msg = ("center_frequency=" + value)
        self.control_udp_send(send_msg.encode('utf-8'))
        return send_msg

    def control_udp_send_use_bandwidth(self):
        """
        发送控制信息，使用带宽
        """
        value = self.use_bandwidth_doubleSpinBox.text()
        send_msg = ("use_bandwidth=" + value)
        self.control_udp_send(send_msg.encode('utf-8'))
        return send_msg

    def control_udp_send_audio_destID(self):
        """
        发送控制信息，语音目的节点
        """
        value = self.audio_comboBox.currentText()
        send_msg = ("destID=" + value)
        self.control_udp_send(send_msg.encode('utf-8'))
        return send_msg
        
    def control_udp_send(self, datas):
        """
        UDP发送数据
        """
        if self.link is False:
            msg = '控制UDP尚未连接\n'
            print(msg)
        else:
            try:
                self.udp_socket.sendto(datas, self.dest_address)
                msg = 'UDP客户端已发送\n'
                print(msg)
            except Exception as ret:
                msg = '发送失败\n'
                print(msg)
                print(ret)

    def control_udp_close(self):
        """
        功能函数，关闭网络连接的方法
        :return:
        """
        try:
            self.udp_socket.close()
            time.sleep(0.2)
            stopThreading.stop_thread(self.text_sever_th)
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
