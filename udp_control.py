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
    choose = 0

    def __init__(self):
        super(UdpControLogic, self).__init__()
        self.udp_socket = None
        self.dest_address = None
        self.__FRAME_STYPE_CTRL_MESH_MODE   =0x01
        self.__FRAME_STYPE_CTRL_ID          =0x02
        self.__FRAME_STYPE_CTRL_SYNC_MODE   =0x11
        self.__FRAME_STYPE_CTRL_RATEL       =0x12
        self.__FRAME_STYPE_CTRL_FERQ        =0x13
        self.__FRAME_STYPE_CTRL_DST_IP      =0x14
        self.__FRAME_STYPE_CTRL_AUTOSTART   =0x21
        self.__FRAME_STYPE_CTRL_START       =0xE1
        self.__FRAME_STYPE_CTRL_SAVE_PARAM  =0xF1


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
            self.control_sever_th = threading.Thread(target=self.control_udp_server_concurrency)
            self.control_sever_th.start()
            msg = '控制UDP客户端已启动\n'
            print(msg)
            self.link = True
            # 启动定时发送空控制帧
            self.send_ontime_th = threading.Thread(target=self.control_udp_sendontime_concurrency)
            self.send_ontime_th.start()

    def control_udp_sendontime_concurrency(self):
        while True:
            self.control_udp_send(self.control_frame0(0))
            try:
                time.sleep(5)
            except Exception as ret:
                print(ret)


    def control_udp_server_concurrency(self):
        """
        线程函数，UDP数据接收
        :return:
        """
        while True:
            try:
                recv_msg, recv_addr = self.udp_socket.recvfrom(10240)
                if recv_msg:
                    print('control_udp_server receive:' + recv_msg.hex())
                    if recv_msg[4] == 1 and recv_msg.__len__() == 8+4*7:
                        # FRAME_TYPE_STATUS
                        self.parse_status_frame(recv_msg)

                    # 发布状态信息 test
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

    def parse_status_frame(self, datas):
        int_values = []
        show_values = []
        head_len=8
        for i in range(7):
            b = datas[head_len+4*i:head_len+4*(i+1)]
            int_values.append(int.from_bytes(b,byteorder='little',signed=True))
        # 组网模式：
        # if int_values[0] == 0:
        #     show_values.append('组网模式：'+'两台设备的1跳网络')
        # elif int_values[0] == 1:
        #     show_values.append('组网模式：'+'多台设备的1跳网络')
        # else:
        #     show_values.append('组网模式：'+'多台设备的多跳网络')
        # 基带ID：
        show_values.append('基带ID：'+ str(hex(int_values[1])))
        # 同步模式：
        if int_values[2] == 0:
            show_values.append('同步模式：'+'内同步')
        else:
            show_values.append('同步模式：'+'外同步')
        # 组网模式：
        show_values.append('mode：'+str(int_values[0]))
        # 速率等级：
        show_values.append('速率等级：'+ str(int_values[3]) + 'Mbps')
        # 中心频率：
        show_values.append('中心频率：'+ str(int_values[4]/1000000) + 'MHz')
        # 语音目的IP：
        i=5
        bip = datas[head_len+4*i:head_len+4*(i+1)]
        show_values.append('语音目的IP：'+str(bip[0])+'.'+str(bip[1])+'.'+str(bip[2])+'.'+str(bip[3]))
        # 自动开始：
        if int_values[6] == 0:
            show_values.append('自动开始：'+'已禁止')
        else:
            show_values.append('自动开始：'+'已启动')

        self.signal_conecting_point_status_msg.emit(show_values)

            
    def control_frame(self, ctype, nvalue):
        """
        生成控制帧，ctype是具体的控制帧类型；nvalue是控制数据int
        """
        ba = bytearray([0xc1,0xd2])
        # 控制帧数据长度：4
        len = 4
        ba = ba.__add__(len.to_bytes(length=2,byteorder='little',signed=True))
        # 帧类型 0x2
        ba = ba.__add__(bytes([2]))
        # 控制类型
        ba = ba.__add__(bytes([ctype]))
        # CRC
        ba = ba.__add__(bytes([0,0]))
        # 控制数据
        ba = ba.__add__(nvalue.to_bytes(length=4,byteorder='little',signed=True))
        return bytes(ba)

    def control_frame1(self, ctype, nvalue):
        """
        生成控制帧，ctype是具体的控制帧类型；nvalue是控制数据bytes
        """
        ba = bytearray([0xc1,0xd2])
        # 控制帧数据长度：4
        len = 4
        ba = ba.__add__(len.to_bytes(length=2,byteorder='little',signed=True))
        # 帧类型 0x2
        ba = ba.__add__(bytes([2]))
        # 控制类型
        ba = ba.__add__(bytes([ctype]))
        # 控制数据
        ba = ba.__add__(nvalue)
        # CRC
        ba = ba.__add__(bytes([0,0]))
        return bytes(ba)

    def control_frame0(self, ctype):
        """
        生成空控制帧，ctype是具体的控制帧类型；
        """
        ba = bytearray([0xc1,0xd2])
        # 控制帧数据长度：4
        len = 0
        ba = ba.__add__(len.to_bytes(length=2,byteorder='little',signed=True))
        # 帧类型 0x2
        ba = ba.__add__(bytes([2]))
        # 控制类型
        ba = ba.__add__(bytes([ctype]))
        # CRC
        ba = ba.__add__(bytes([0,0]))
        return bytes(ba)
    def control_udp_send_ID(self):
        """
        发送控制信息，id配置
        """
        value = self.id_settint_comboBox.currentText()
        nvalue = int(value)
        send_msg = ("id=" + value)
        self.control_udp_send(self.control_frame(self.__FRAME_STYPE_CTRL_ID, nvalue))
        return send_msg

    def control_udp_send_frequency(self):
        """
        发送控制信息，速率等级
        """
        if self.fixed_frequency_radioButton.isChecked():
            value = self.frequency_comboBox.currentText()
            nvalue = int(value)
            send_msg = ("frequency=" + value)
        else:
            nvalue = 256
            send_msg = "unfixed_frequency"
        self.control_udp_send(self.control_frame(self.__FRAME_STYPE_CTRL_RATEL, nvalue))
        return send_msg

    def control_udp_send_synchronization(self):
        """
        发送控制信息，同步方式
        """
        way = ""
        if self.synchronization_inside_radioButton.isChecked():
            way = "in"
            nvalue = 0
        if self.synchronization_outside_radioButton.isChecked():
            way = "out"
            nvalue = 1
        send_msg = ("synchronization_way=" + way)
        self.control_udp_send(self.control_frame(self.__FRAME_STYPE_CTRL_SYNC_MODE, nvalue))
        return send_msg

    def control_udp_send_center_frequency(self):
        """
        发送控制信息，中心频点
        """
        value = self.center_frequency_spinBox.text()
        nvalue = int(value) * 1000000
        send_msg = ("center_frequency=" + value + 'MHz')
        self.control_udp_send(self.control_frame(self.__FRAME_STYPE_CTRL_FERQ, nvalue))
        return send_msg

    def control_udp_send_open(self, choose):
        """
        发送控制信息，开启、关闭波形
        """
        nvalue = int(choose)
        send_msg = ("open=" + str(nvalue))
        self.control_udp_send(self.control_frame(self.__FRAME_STYPE_CTRL_START, nvalue))
        return send_msg

    def control_udp_send_auto(self):
        """
        发送控制信息，开启、关闭波形自启动
        """
        if self.auto_start_checkBox.isChecked():
            nvalue = 1
        else:
            nvalue = 0
        send_msg = ("auto_start=" + str(nvalue))
        self.control_udp_send(self.control_frame(self.__FRAME_STYPE_CTRL_START, nvalue))
        return send_msg

    def control_udp_send_use_bandwidth(self):
        """
        发送控制信息，使用带宽
        """
        # value = self.use_bandwidth_doubleSpinBox.text()
        # send_msg = ("use_bandwidth=" + value)
        # self.control_udp_send(send_msg.encode('utf-8'))
        # return send_msg

        # for test
        b = bytearray([0xc1, 0xd2, 0, 3, 1,0,0,0,
        1,2,3,4,
        1,2,3,4,
        1,2,3,4,
        1,2,3,4,
        1,2,3,4,
        1,2,3,4,
        1,2,3,4])
        self.control_udp_send(b)
        return "test"

    def control_udp_send_audio_destID(self):
        """
        发送控制信息，语音目的节点
        """
        adr = self.dst_ip_textEdit.toPlainText()
        if adr.count('.') != 3:
            return "IP error"
        # if value == "广播":
        #     nvalue = 0xff
        # else:
        #     nvalue = int(value)
        # adr = self.dest_address[0]
        send_msg = ("destID=" + adr)
        try:
            l = adr.split('.')
            print(bytes([int(l[3]), int(l[2]), int(l[1]), int(l[0])]))
            b = bytes([int(l[3]), int(l[2]), int(l[1]), int(l[0])])
        except Exception as ret:
            print(ret)
            send_msg = str(ret)
        else:
            self.control_udp_send(self.control_frame1(self.__FRAME_STYPE_CTRL_DST_IP, b))
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
            stopThreading.stop_thread(self.send_ontime_th)
            stopThreading.stop_thread(self.control_sever_th)
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
