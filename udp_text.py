from PyQt5 import QtCore, QtWidgets
import socket
import threading
import time
import sys

import mainWin
import stopThreading


class UdpTextLogic(mainWin.Ui_MainWindow):
    # 信号槽机制：设置一个信号，用于触发接收区写入动作
    signal_receive_text_msg = QtCore.pyqtSignal(str)

    def __init__(self):
        super(UdpTextLogic, self).__init__()
        self.udp_receive_socket_text = None
        self.sever_th = None

    def text_udp_server_start(self, port):
        """
        开启UDP服务端方法
        :return:
        """
        if self.udp_receive_socket_text == None:
            self.udp_receive_socket_text = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            address = ('', port)
            self.udp_receive_socket_text.bind(address)
        except Exception as ret:
            msg = 'text 请检查端口号\n'
            print(msg)
        else:
            self.sever_th = threading.Thread(target=self.text_udp_server_concurrency)
            self.sever_th.start()
            msg = 'text UDP服务端正在监听端口:{}\n'.format(port)
            print(msg)
            
    def text_udp_server_concurrency(self):
        """
        线程函数，持续监听UDP通信
        :return:
        """
        while True:
            try:
                recv_msg, recv_addr = self.udp_receive_socket_text.recvfrom(10240)
            except Exception as ret:
                msg = 'udp_receive_socket_text 接收失败\n'
                print(msg)
            msg = recv_msg.decode('utf-8')
            self.signal_receive_text_msg.emit(msg)

    def text_udp_client_send(self, destIP, destPort):
        """
        确认UDP客户端的目的ip和port，向其发送一条文本数据
        :return:
        """     
        dest_address = (destIP, destPort)
        try:
            send_msg = (str(self.textSend_plainTextEdit.toPlainText())).encode('utf-8')
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.sendto(send_msg, dest_address)
        except Exception as ret:
            msg = '发送失败\n'
            print(msg)
        else:
            msg = 'text UDP客户端端正在向:{}发送数据\n'.format(dest_address)
            print(msg)
            
    def text_udp_close_all(self):
        """
        功能函数，关闭网络连接的方法
        :return:
        """
        try:
            self.udp_receive_socket_text.close()
            time.sleep(0.1)
        except Exception as ret:
            pass
        try:
            stopThreading.stop_thread(self.sever_th)
        except Exception:
            pass
