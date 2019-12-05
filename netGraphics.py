# -*- coding: utf-8 -*-
 

import sys 
import threading
import time
import math 
from PyQt5.QtCore import pyqtSignal, QRectF, Qt, QPoint, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QLabel, \
	QGraphicsScene, QGraphicsRectItem, QGraphicsItem, QGraphicsEllipseItem, \
		QGraphicsLineItem, QGraphicsSimpleTextItem

import stopThreading 

		

# 网络节点图形 route_info==None时不可见，route_info=[]时为灰色，route_info有内容时为绿色
class NetDeviceItem(QGraphicsEllipseItem):
	route_info = None
	text_tag = None
	last_time = 0
	def __init__(self, parentView, id, route_info=None):
		super(NetDeviceItem, self).__init__()
		self.pa = parentView
		self.id = id
		self.setBrush(Qt.gray)
		self.setRouteInfo(route_info)
		self.setRect(-15, -15, 30, 30)
		self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable
				| QGraphicsItem.ItemIsFocusable)
		self.last_time = 0

	def setRouteInfo(self, route_info):
		"""
		设置网络路由信息
		return 信息确实更新了返回True，没有更新返回False
		"""
		self.last_time = time.time()
		if route_info is not None:
			self.setVisible(True)
			if len(route_info)>0:
				self.setBrush(Qt.green)
			else:
				self.setBrush(Qt.gray)
		else:
			self.setVisible(False)
		self.synTextTag()
		if self.route_info == route_info:
			return False
		else:
			self.route_info = route_info
			return True

	def checkOutTime(self):
		if self.route_info:
			return time.time() - self.last_time > 5.1
		else:
			return False

	def getTextTag(self):
		if not self.text_tag:
			self.text_tag = QGraphicsSimpleTextItem()
		self.text_tag.setPos(self.pos())
		self.text_tag.setVisible(self.isVisible())
		return self.text_tag

	def setTextTag(self, item):
		self.text_tag = item
		self.synTextTag()

	def synTextTag(self):
		if self.text_tag:
			self.text_tag.setVisible(self.isVisible())
			self.text_tag.setPos(self.pos().x()+20,self.pos().y())

	def mousePressEvent(self, event):
		infos = ['id='+str(self.id)]
		if self.route_info:
			for item in self.route_info:
				if len(item)>1:
					infos.append(str(item[0])+' to '+str(item[-1]) + ' : ' +str(item))
		self.pa.onItemPressed(infos, self.id)

# 整体图形
class WholeDeviceItem(QGraphicsRectItem):
	def __init__(self, rect, parentView, infos):
		super(WholeDeviceItem, self).__init__(rect)
		self.pa = parentView
		self.infos = infos

	def mousePressEvent(self, event):
		self.pa.onWholePressed(self.infos)
		self.hasFocus()

# 整体网络状态示意图
class QMyGraphicsview(QGraphicsView):
	wholeDeviceItem = None
	running = True
	# 信号量
	signal_offline_msg = pyqtSignal(int)
	sigMouseMovePoint = pyqtSignal(QPoint)
	sigNetDeviceItemPress = pyqtSignal(list)
	# 设备信息数据，key为设备id
	devices = {}
	# 当前选中状态：-1：无选中；0：整体选中：>1:选中节点的ID
	pressedID = -1
	# 信号线
	line_items = []

	def __init__(self, parent=None):
		super(QMyGraphicsview, self).__init__(parent)
		self.rect = QRectF(-200,-200,400,400)
		self.myScene = QGraphicsScene(self.rect)
		self.setScene(self.myScene)
		self.refrashGraphicSystem()
		# 启动定时检测是否更新了路由信息
		self.check_ontime_th = threading.Thread(target=self.check_online_ontime_func)
		self.check_ontime_th.start()
		self.signal_offline_msg.connect(self.deviceOffline)

	def __del__(self):
		# stopThreading.stop_thread(self.check_ontime_th)
		self.running = False

	def check_online_ontime_func(self):
		'''
		线程函数，检测节点是否在线
		'''
		try:
			while(self.running):
				for key, item in self.devices.items():
					if item.checkOutTime():
						self.signal_offline_msg.emit(key)
						# item.setRouteInfo([])
						# self.updateLines(key, [])
						# self.devices[key] = NetDeviceItem(self, key, [])
						# self.devices[key].setPos(item.pos())
						# self.myScene.addItem(self.devices[key])
						# self.myScene.removeItem(item)
				time.sleep(1)
		except Exception as ret:
			print(ret)

	def deviceOffline(self, id):
		self.updateLines(id, [])

	def updateLines(self, id, route_info):
		"""
		更新某节点的信息，信息确实改变了的话，更新Graphicsview显示
		"""
		if self.devices.__contains__(id):
			if self.devices[id].setRouteInfo(route_info):
				# self.refrashGraphicSystem()
				if self.pressedID == 0:
					self.drawAllLines()
				elif self.pressedID > 0:
					self.removeAllLines()
					self.drawLines(self.pressedID)

	def refrashGraphicSystem(self):
		"""
		重新定义整个拓扑图
		"""
		# 显示scene边框
		self.wholeDeviceItem = WholeDeviceItem(self.rect, self, ["   ",])
		self.wholeDeviceItem.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
		self.myScene.addItem(self.wholeDeviceItem)
		# 显示节点，标签
		self.devices[1] = NetDeviceItem(self, 1, None)
		self.devices[2] = NetDeviceItem(self, 2, None)
		self.devices[3] = NetDeviceItem(self, 3, None)
		self.devices[4] = NetDeviceItem(self, 4, None)
		self.devices[5] = NetDeviceItem(self, 5, None)
		self.devices[6] = NetDeviceItem(self, 6, None)
		for key, value in self.devices.items():
			x = 150*math.sin(math.radians(60*key))
			y = 150*math.cos(math.radians(60*key))
			value.setPos(x, y)
			self.myScene.addItem(value)
			value.setTextTag(self.myScene.addSimpleText(str(value.id)))
		self.myScene.clearSelection()
		self.pressedID = -1

	def mouseMoveEvent(self, evt):
		self.sigMouseMovePoint.emit(evt.pos())

	def onItemPressed(self, infos, id):
		self.sigNetDeviceItemPress.emit(infos)
		self.removeAllLines()
		self.drawLines(id)
		self.pressedID = id

	def onWholePressed(self, infos):
		self.sigNetDeviceItemPress.emit(infos)
		self.drawAllLines()
		self.pressedID = 0

	def removeAllLines(self):
		for item in self.line_items:
			self.myScene.removeItem(item)
		self.line_items.clear()

	def removeAll(self):
		self.myScene.clear()
		self.line_items.clear()
		self.devices.clear()
		self.wholeDeviceItem = None

	def drawAllLines(self):
		"""
		画出所有节点的路由信号线
		"""
		self.removeAllLines()
		for k in self.devices.keys():
			self.drawLines(k)

	def drawLines(self, id):
		"""
		画出id节点的路由信号线
		"""
		lines = self.devices[id].route_info
		if lines:
			for line in lines:
				if line and len(line)>1:
					for i in range(len(line)-1):
						p1 = self.devices[line[i]]
						p2 = self.devices[line[i+1]]
						line_item = self.myScene.addLine(p1.pos().x(), p1.pos().y(), p2.pos().x(), p2.pos().y())
						self.line_items.append(line_item)
