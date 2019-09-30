from PyQt5 import QtCore, QtWidgets
import socket
import threading
import time

import asyncio
import sys

import numpy as np
import sounddevice as sd

import mainWin
import stopThreading


class UdpAudioLogic(mainWin.Ui_MainWindow):
    # 信号槽机制：设置一个信号，用于触发接收区写入动作
    signal_receive_test_data_msg = QtCore.pyqtSignal(str)

    def __init__(self):
        super(UdpAudioLogic, self).__init__()
        self.udp_receive_socket_test_data = None
        self.audio_dest_address = None
        self.audio_sever_th = None
        self.count_th = None
        self.audio_client_th = None
        self.lock_new_receive_num = threading.Lock()
        self.new_receive_num = 0
        self.test_data_last_t = 0
        self.time_lag = 0.1

    def audio_udp_server_start(self, port):
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
            msg = 'audio 请检查端口号\n'
            print(msg)
        else:
            self.audio_sever_th = threading.Thread(target=self.audio_udp_server_concurrency)
            self.audio_sever_th.start()
            msg = 'audio UDP服务端正在监听端口:{}\n'.format(port)
            print(msg)
            self.audio_udp_report_receive_data_sum_on_time()

    def audio_udp_report_receive_data_sum_on_time(self):
        self.count_th = threading.Thread(target=self.audio_udp_report_concurrency)
        self.count_th.start()

    def audio_udp_client_start(self, destIP, destPort):
        """
        确认UDP客户端的目的ip和port，启动持续发送线程
        :return:
        """       
        try:
            self.audio_dest_address = (destIP, destPort)
            self.run_sending = True
            self.audio_client_th = threading.Thread(target=self.audio_udp_client_concurrency)
            self.audio_client_th.start()
        except Exception as ret:
            msg = 'audio 请检查目标IP，目标端口\n'
            print(msg)
        else:
            msg = 'audio UDP客户端端正在向:{}发送数据\n'.format(self.audio_dest_address)
            print(msg)
            
    def audio_udp_client_stop(self):
        self.run_sending = False

    def audio_udp_report_concurrency(self):
        while True:
            self.lock_new_receive_num.acquire()
            if self.new_receive_num > 0:
                current_sum = int(self.audioReceive_label.text()[:-5])
                current_sum += self.new_receive_num
                # self.audioReceive_label.setText(str(current_sum) + 'Bytes')
                self.signal_receive_test_data_msg.emit(str(current_sum) + 'Bytes')
                self.new_receive_num = 0
            self.lock_new_receive_num.release()
            time.sleep(1)

    def audio_udp_server_concurrency(self):
        """
        线程函数，持续监听UDP通信
        :return:
        """
        while True:
            try:
                recv_msg, recv_addr = self.udp_receive_socket_test_data.recvfrom(10240)
            except Exception as ret:
                msg = 'udp_receive_socket_test_data 接收失败\n'
                print(msg)
            recv_msg_len = len(recv_msg)
            self.lock_new_receive_num.acquire()
            self.new_receive_num += recv_msg_len
            self.lock_new_receive_num.release()

    def audio_udp_client_concurrency(self):
        """
        线程函数，持续进行UDP发送
        :return:
        """
        data_len = self.audioSend_len_spinBox.value()
        send_frequency = self.audioSend_frequency_spinBox.value()
        data = bytes(data_len)
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while self.run_sending:
            # 发送频率大于10，分10次发送，每次sleep 0.1秒
            if send_frequency > 10:
                t = time.time()
                if self.test_data_last_t != 0:
                    real_time_range = round(t*1000) - round(self.test_data_last_t*1000)
                    if not (real_time_range > 950 and real_time_range < 1050):
                        self.time_lag = (1000 - (real_time_range - 1000))/10000
                else:
                    self.time_lag = 0.1
                self.test_data_last_t = t
                print(int(round(t*1000)))
                print(self.time_lag)
                for iLoop in range(10):
                    for i in range(int(send_frequency/10)):
                        self.audio_udp_send(udp_socket, data)
                    if send_frequency % 10 != 0 and iLoop == 9:
                        for i in range(int(send_frequency % 10)):
                            self.audio_udp_send(udp_socket, data)
                    if self.time_lag > 0:
                        time.sleep(self.time_lag)
                    else:
                        time.sleep(0.01)

            # 发送频率小于10，直接发完sleep 1秒
            else:
                for i in range(send_frequency):
                    self.audio_udp_send(udp_socket, data)
                    time.sleep(1)
            # 1秒更新一次发送总数
            current_sum = int(self.audioSend_label.text()[:-5])
            current_sum += data_len*send_frequency
            self.audioSend_label.setText(str(current_sum) + 'Bytes')


    def audio_udp_send(self, udp_socket, data):
        """
        功能函数，用于UDP客户端发送一帧audio
        :return: None
        """
        try:
            udp_socket.sendto(data, self.audio_dest_address)
        except Exception as ret:
            msg = '发送失败\n'
            print(msg)

    def audio_udp_close_all(self):
        """
        功能函数，关闭网络连接的方法
        :return:
        """
        try:
            self.udp_receive_socket_test_data.close()
        except Exception as ret:
            pass
        try:
            stopThreading.stop_thread(self.audio_sever_th)
        except Exception:
            pass
        self.audio_udp_client_stop()

    async def record_buffer(buffer, **kwargs):
        loop = asyncio.get_event_loop()
        event = asyncio.Event()
        idx = 0

        def callback(indata, frame_count, time_info, status):
            nonlocal idx
            if status:
                print(status)
            remainder = len(buffer) - idx
            if remainder == 0:
                loop.call_soon_threadsafe(event.set)
                raise sd.CallbackStop
            indata = indata[:remainder]
            buffer[idx:idx + len(indata)] = indata
            idx += len(indata)
            print(idx)

        stream = sd.InputStream(callback=callback, dtype=buffer.dtype,
                                channels=buffer.shape[1], **kwargs)
        with stream:
            await event.wait()


    async def play_buffer(buffer, **kwargs):
        loop = asyncio.get_event_loop()
        event = asyncio.Event()
        idx = 0

        def callback(outdata, frame_count, time_info, status):
            nonlocal idx
            if status:
                print(status)
            remainder = len(buffer) - idx
            if remainder == 0:
                loop.call_soon_threadsafe(event.set)
                raise sd.CallbackStop
            valid_frames = frame_count if remainder >= frame_count else remainder
            outdata[:valid_frames] = buffer[idx:idx + valid_frames]
            outdata[valid_frames:] = 0
            idx += valid_frames

        stream = sd.OutputStream(callback=callback, dtype=buffer.dtype,
                                channels=buffer.shape[1], **kwargs)
        with stream:
            await event.wait()

