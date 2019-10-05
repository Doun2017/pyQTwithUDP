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


DATA_TYPE = "int16"
CHANNELS = 1

class UdpAudioLogic(mainWin.Ui_MainWindow):
    # 信号槽机制：设置一个信号，用于触发接收区写入动作
    signal_receive_test_data_msg = QtCore.pyqtSignal(str)

    def __init__(self):
        super(UdpAudioLogic, self).__init__()
        self.udp_receive_socket_audio = None
        self.audio_dest_address = None
        self.audio_sever_th = None
        self.audio_client_th = None
        self.audio_play_th = None
        self.lock_new_receive_num = threading.Lock()
        self.new_receive_buffer = bytearray()
        self.test_data_last_t = 0
        self.time_lag = 0.1

    def audio_udp_server_start(self, port):
        """
        开启UDP服务端 接收语音数据并即时播放
        :return:
        """
        if self.udp_receive_socket_audio == None:
            self.udp_receive_socket_audio = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            address = ('', port)
            self.run_receiveing = True
            self.udp_receive_socket_audio.bind(address)
        except Exception as ret:
            msg = 'audio 请检查端口号\n'
            print(msg)
            print(ret)
        else:
            self.audio_sever_th = threading.Thread(target=self.audio_udp_server_concurrency)
            self.audio_sever_th.start()
            msg = 'audio UDP服务端正在监听端口:{}\n'.format(port)
            print(msg)
            self.audio_play_th = threading.Thread(target=self.audio_play_concurrency)
            self.audio_play_th.start()
            msg = 'audio 已启动播放线程\n'
            print(msg)

        
    def audio_udp_client_start(self, destIP, destPort):
        """
        确认UDP客户端的目的ip和port，启动音频inputstream录音，将录制的数据不断发送
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

    def audio_udp_client_concurrency(self):
        """
        线程函数，开启录音流，异步发送
        :return:
        """
        print('recording buffer ...')
        asyncio.run(self.record_buffer())

    async def record_buffer(self, **kwargs):
        loop = asyncio.get_event_loop()
        event = asyncio.Event()
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        def callback(indata, frame_count, time_info, status):
            if status:
                print(status)
            if self.run_sending == False:
                loop.call_soon_threadsafe(event.set)
                raise sd.CallbackStop
            # print(len(indata))
            try:
                udp_socket.sendto(indata.tobytes(), self.audio_dest_address)
                # print(self.audio_dest_address)
            except Exception as ret:
                print(ret)
        stream = sd.InputStream(callback=callback, dtype=DATA_TYPE,
                                channels=CHANNELS, **kwargs)
        with stream:
            await event.wait()


    async def play_buffer(self, **kwargs):
        loop = asyncio.get_event_loop()
        event = asyncio.Event()

        def callback(outdata, frame_count, time_info, status):
            if status:
                print(status)
            if self.run_receiveing == False:
                loop.call_soon_threadsafe(event.set)
                raise sd.CallbackStop
            self.lock_new_receive_num.acquire()
            remainder = len(self.new_receive_buffer)
            # print(remainder)
            byte_count = frame_count*2
            valid_frames = frame_count if remainder >= byte_count else remainder/2
            if valid_frames == 0:
                outdata[:] = 0
                # print("填0")
            else:
                # arr = np.array(list(self.new_receive_buffer))
                arr = np.ndarray((valid_frames, 1), dtype=DATA_TYPE, buffer=self.new_receive_buffer)
                outdata[:valid_frames] = arr[:valid_frames]
                outdata[valid_frames:] = 0
                self.new_receive_buffer = self.new_receive_buffer[valid_frames*2:]
            self.lock_new_receive_num.release()
      
        stream = sd.OutputStream(callback=callback, dtype=DATA_TYPE,
                                channels=CHANNELS, **kwargs)
        with stream:
            await event.wait()

    def audio_udp_server_concurrency(self):
        """
        线程函数，持续监听UDP通信
        :return:
        """
        while True:
            try:
                recv_msg, recv_addr = self.udp_receive_socket_audio.recvfrom(10240)
            except Exception as ret:
                msg = 'udp_receive_socket_audio 接收失败\n'
                print(msg)
            self.lock_new_receive_num.acquire()
            self.new_receive_buffer += recv_msg
            self.lock_new_receive_num.release()

    def audio_play_concurrency(self):
        """
        线程函数，播放声音
        :return:
        """
        print('playing buffer ...')
        asyncio.run(self.play_buffer())

    def audio_udp_close_all(self):
        """
        功能函数，关闭网络连接的方法
        :return:
        """
        try:
            self.udp_receive_socket_audio.close()
        except Exception as ret:
            pass
        try:
            stopThreading.stop_thread(self.audio_sever_th)
        except Exception:
            pass
        self.audio_udp_client_stop()
        self.run_receiveing = False
        print("audio 已断开网络\n")

