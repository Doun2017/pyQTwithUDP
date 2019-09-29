from PyQt5 import QtCore, QtWidgets
import socket
import threading
import time
import sys

import mainWin
import stopThreading


class UdpTestDataLogic(mainWin.Ui_MainWindow):
    # 信号槽机制：设置一个信号，用于触发接收区写入动作
    signal_receive_test_data_msg = QtCore.pyqtSignal(str)

    def __init__(self):
        super(UdpTestDataLogic, self).__init__()
        self.udp_receive_socket_test_data = None
        self.dest_address = None
        self.sever_th = None
        self.client_th = None

    def testdata_udp_server_start(self, port):
        """
        开启UDP服务端方法
        :return:
        """
        if self.udp_receive_socket_test_data == None:
            self.udp_receive_socket_test_data = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            address = ('', port)
            self.udp_receive_socket_test_data.bind(address)
        except Exception as ret:
            msg = 'TestData 请检查端口号\n'
            print(msg)
        else:
            self.sever_th = threading.Thread(target=self.testdata_udp_server_concurrency)
            self.sever_th.start()
            msg = 'TestData UDP服务端正在监听端口:{}\n'.format(port)
            print(msg)

    def testdata_udp_client_start(self, destIP, destPort):
        """
        确认UDP客户端的目的ip和port，启动持续发送线程
        :return:
        """       
        try:
            self.dest_address = (destIP, destPort)
            self.run_sending = True
            self.client_th = threading.Thread(target=self.testdata_udp_client_concurrency)
            self.client_th.start()
        except Exception as ret:
            msg = 'TestData 请检查目标IP，目标端口\n'
            print(msg)
        else:
            msg = 'TestData UDP客户端端正在向:{}发送数据\n'.format(self.dest_address)
            print(msg)
            
    def testdata_udp_client_stop(self):
        self.run_sending = False

    def testdata_udp_server_concurrency(self):
        """
        线程函数，持续监听UDP通信
        :return:
        """
        while True:
            recv_msg, recv_addr = self.udp_receive_socket_test_data.recvfrom(1024)
            recv_msg_len = len(recv_msg)
            current_sum = int(self.testDataReceive_label.text()[:-5])
            current_sum += recv_msg_len
#            self.testDataReceive_label.setText(str(current_sum) + 'Bytes')
            self.signal_receive_test_data_msg.emit(str(current_sum) + 'Bytes')


    def testdata_udp_client_concurrency(self):
        """
        线程函数，持续进行UDP发送
        :return:
        """
        data_len = self.testDataSend_len_spinBox.value()
        send_frequency = self.testDataSend_frequency_spinBox.value()
        data = bytes(data_len)
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while self.run_sending:
            self.testdata_udp_send(udp_socket, data)
            current_sum = int(self.testDataSend_label.text()[:-5])
            current_sum += data_len
            self.testDataSend_label.setText(str(current_sum) + 'Bytes')
            try:
                time.sleep(1/send_frequency)
                t = time.time()
                print (int(round(t * 1000)))    #毫秒级时间戳
#                print (int(round(t * 1000000))) #微秒级时间戳
            except Exception as ret:
                print(ret)

#         while self.run_sending:
#             for i in range(send_frequency):
#                 self.testdata_udp_send(udp_socket, data)
#             current_sum = int(self.testDataSend_label.text()[:-5])
#             current_sum += data_len*send_frequency
#             self.testDataSend_label.setText(str(current_sum) + 'Bytes')
#             try:
#                 time.sleep(1)
#                 t = time.time()
#                 print (int(round(t * 1000)))    #毫秒级时间戳
# #                print (int(round(t * 1000000))) #微秒级时间戳
#             except Exception as ret:
#                 print(ret)




    def testdata_udp_send(self, udp_socket, data):
        """
        功能函数，用于UDP客户端发送一帧testdata
        :return: None
        """
        try:
            udp_socket.sendto(data, self.dest_address)
        except Exception as ret:
            msg = '发送失败\n'
            print(msg)

    def testdata_udp_close_all(self):
        """
        功能函数，关闭网络连接的方法
        :return:
        """
        try:
            self.udp_receive_socket_test_data.close()
        except Exception as ret:
            pass
        try:
            stopThreading.stop_thread(self.sever_th)
        except Exception:
            pass
        self.testdata_udp_client_stop()
