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
        #是否主节点设置
        self.__FRAME_STYPE_CTRL_BEACON_DEV  =0x02
        self.__FRAME_STYPE_CTRL_SYNC_MODE   =0x11
        self.__FRAME_STYPE_CTRL_RATEL       =0x12
        self.__FRAME_STYPE_CTRL_FERQ        =0x13
        self.__FRAME_STYPE_CTRL_DST_IP      =0x14
        self.__FRAME_STYPE_CTRL_PRI_PORT    =0x15
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
            self.control_udp_send(self.control_frame_empty(0))
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
                    # FRAME_TYPE_STATUS状态帧
                    if recv_msg[4] == 1:
                        # FRAME_STYPE_STATUS_DEV直连节点状态
                        if recv_msg[5] == 1:
                            self.parse_status_frame(recv_msg)
                        else:
                            # FRAME_STYPE_STATUS_MESH节点组网表
                            self.parse_net_status_frame(recv_msg)

                    # test发布状态信息
                    # if recv_msg.__len__()%2 == 0:
                    #     if self.choose == 0:
                    #         self.signal_net_point_status_msg.emit(1, [[0],[1,4,3,2],[1,4,3],[1,4],[0],[1,6]])
                    #         self.choose = 1
                    #     else:
                    #         self.signal_net_point_status_msg.emit(1, [[0],[1,4,3,2],[1,4,3],[1,4],[0],[0]])
                    #         self.choose = 0
                    # else:
                    #     self.signal_net_point_status_msg.emit(2, [[2,1],[0],[2,4,3],[2,4],[0],[2,6]])

            except Exception as ret:
                msg = 'udp_socket 接收失败\n'
                time.sleep(0.1)
                print(msg)
                print(ret)
                break

    def parse_net_status_frame(self, datas):
        '''
        FRAME_STYPE_STATUS_MESH节点组网表
        '''
        # 组网表分组
        head_len=8
        group_list = []
        datalen = int.from_bytes(datas[2:4],'little')
        grouplen = datalen//3
        for gindex in range(grouplen):
            beg = head_len+3*gindex
            group_list.append(datas[beg:beg+3])

        # 分析此帧组网表的源id
        device_id=0
        for g in group_list:
            if g[0]==0:
                continue
            if g[0]==g[1] and g[2]==0:
                device_id = g[0]
        if device_id==0:
            return
            
        # 分析路由
        new_group_list = []
        for g in group_list:
            # 跳数在合法范围，则增加一条一跳的路由信息
            if g[2]>0 and g[2]<6:
                new_group_list.append([device_id, g[1]])
                
        self.signal_net_point_status_msg.emit(device_id, new_group_list)

    def parse_status_frame(self, datas):
        '''
        FRAME_STYPE_STATUS_DEV直连节点状态
        '''
        int_values = []
        show_values = []
        datalen = int.from_bytes(datas[2:4],'little')
        grouplen = datalen//4
        head_len=8
        for i in range(grouplen):
            b = datas[head_len+4*i:head_len+4*(i+1)]
            int_values.append(int.from_bytes(b,byteorder='little',signed=True))
        # 设备编号ID
        int_index = 0
        show_values.append('设备编号ID：'+ str(hex(int_values[int_index])))

        # 设备IP：
        int_index+=1
        bip = datas[head_len+4*int_index:head_len+4*(int_index+1)]
        show_values.append('设备IP：'+str(bip[0])+'.'+str(bip[1])+'.'+str(bip[2])+'.'+str(bip[3]))

        # 组网模式：(不显示)
        int_index+=1
        # show_values.append('mode：'+str(int_values[int_index]))

        # 0为普通节点，1为信标节点即主节点。
        int_index+=1
        if int_values[int_index]==1:
            # 1个空格表示是主节点
            show_values.append(' ')

        # 同步模式：
        int_index+=1
        if int_values[int_index] == 0:
            show_values.append('同步模式：'+'内同步')
        else:
            show_values.append('同步模式：'+'外同步')

        # 速率等级：
        int_index+=1
        s = self.frequency_comboBox.itemText(int_values[int_index])
        show_values.append('速率等级：'+ s)

        # 中心频率：
        int_index+=1
        show_values.append('中心频率：'+ str(int_values[int_index]/1000000) + 'MHz')

        # 语音目的IP：
        int_index+=1
        bip = datas[head_len+4*int_index:head_len+4*(int_index+1)]
        show_values.append('语音目的IP：'+str(bip[0])+'.'+str(bip[1])+'.'+str(bip[2])+'.'+str(bip[3]))

        # 优先级端口
        int_index+=1
        b1 = datas[head_len+4*int_index:head_len+4*int_index+2]
        i1 = int.from_bytes(b1,byteorder='little',signed=False)
        b2 = datas[head_len+4*int_index+2:head_len+4*int_index+4]
        i2 = int.from_bytes(b2,byteorder='little',signed=False)
        show_values.append('高优先级端口：'+ str(i1) + '中优先级端口：'+ str(i2) )

        # 自动开始：
        int_index+=1
        if int_index>grouplen-1:
            return
        if int_values[int_index] == 0:
            show_values.append('自动开始：'+'已禁止')
        else:
            show_values.append('自动开始：'+'已启动')

        # 波形启动状态
        int_index+=1
        if int_index>grouplen-1:
            return
        if self.pushButton_open:
            if int_values[int_index] == 0:
                self.pushButton_open.setEnabled(True)
                show_values.append('波形已关闭')
            else:
                self.pushButton_open.setEnabled(False)
                show_values.append('波形已开启')


        self.signal_conecting_point_status_msg.emit(show_values)

            
    def control_frame_from_int(self, ctype, nvalue):
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

    def control_frame_from_bytes(self, ctype, nvalue):
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

    def control_frame_empty(self, ctype):
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

    def control_udp_send_BEACON_DEV(self, value):
        """
        发送控制信息，是否主节点
        """
        # value = self.id_settint_comboBox.currentText()
        # nvalue = int(value)
        # send_msg = ("id=" + value)
        # self.control_udp_send(self.control_frame_from_int(self.__FRAME_STYPE_CTRL_ID, nvalue))
        # return send_msg
        
        self.control_udp_send(self.control_frame_from_int(self.__FRAME_STYPE_CTRL_BEACON_DEV, value))
        
        return "value" + str(value)

    def control_udp_send_frequency(self):
        """
        发送控制信息，速率等级
        """
        # if self.fixed_frequency_radioButton.isChecked():
        #     value = self.frequency_comboBox.currentText()
        #     nvalue = int(value)
        #     send_msg = ("frequency=" + value)
        # else:
        #     nvalue = 256
        #     send_msg = "unfixed_frequency"

        nvalue = self.frequency_comboBox.currentIndex()
        send_msg = ("frequency=" + self.frequency_comboBox.currentText())

        self.control_udp_send(self.control_frame_from_int(self.__FRAME_STYPE_CTRL_RATEL, nvalue))
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
        self.control_udp_send(self.control_frame_from_int(self.__FRAME_STYPE_CTRL_SYNC_MODE, nvalue))
        return send_msg

    def control_udp_send_center_frequency(self):
        """
        发送控制信息，中心频点
        """
        value = self.center_frequency_spinBox.text()
        nvalue = int(value) * 1000000
        send_msg = ("center_frequency=" + value + 'MHz')
        self.control_udp_send(self.control_frame_from_int(self.__FRAME_STYPE_CTRL_FERQ, nvalue))
        return send_msg

    def control_udp_send_open(self, choose):
        """
        发送控制信息，开启、关闭波形
        """
        nvalue = int(choose)
        send_msg = ("open=" + str(nvalue))
        self.control_udp_send(self.control_frame_from_int(self.__FRAME_STYPE_CTRL_START, nvalue))
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
        self.control_udp_send(self.control_frame_from_int(self.__FRAME_STYPE_CTRL_START, nvalue))
        return send_msg

    def control_udp_send_use_bandwidth(self):
        """
        发送控制信息，优先级端口
        """
        # value = self.use_bandwidth_doubleSpinBox.text()
        # send_msg = ("use_bandwidth=" + value)
        # self.control_udp_send(send_msg.encode('utf-8'))
        # return send_msg
        highport = int(self.high_priority_spinBox.text())
        middleport = int(self.middle_priority_spinBox.text())
        bh = highport.to_bytes(2,'little',signed=False)
        bm = middleport.to_bytes(2,'little',signed=False)
        b = bh+bm
        self.control_udp_send(self.control_frame_from_bytes(self.__FRAME_STYPE_CTRL_PRI_PORT, b))
        return 'high=' + str(highport) +'middle=' + str(middleport)

        # for test
        # b = bytearray([0xc1, 0xd2, 0, 3, 1,0,0,0,
        # 1,2,3,4,
        # 1,2,3,4,
        # 1,2,3,4,
        # 1,2,3,4,
        # 1,2,3,4,
        # 1,2,3,4,
        # 1,2,3,4,
        # 1,2,3,4,
        # 1,2,3,4,
        # 1,2,3,4])
        # self.control_udp_send(b)
        # return "test"

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
            self.control_udp_send(self.control_frame_from_bytes(self.__FRAME_STYPE_CTRL_DST_IP, b))
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
