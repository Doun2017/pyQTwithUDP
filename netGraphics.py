# -*- coding: utf-8 -*-
 

import sys 
import math 
from PyQt5.QtCore import pyqtSignal, QRectF, Qt, QPoint, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QLabel, \
	QGraphicsScene, QGraphicsRectItem, QGraphicsItem, QGraphicsEllipseItem, \
		QGraphicsLineItem

class NetNodeInfo:
	def __init__(self, id, strinfo):
		self.id = id
		self.info = strinfo
		

# 网络节点图形
class NetDeviceItem(QGraphicsEllipseItem):
	def __init__(self, parentView, infos):
		super(NetDeviceItem, self).__init__()
		self.pa = parentView
		self.infos = infos

	def mousePressEvent(self, event):
		self.pa.emitItemPressEvent([str(self.infos.id), self.infos.info])
		# item = QGraphicsLineItem(0,0, self.pos().x(), self.pos().y())
		# self.pa.myScene.addItem(item)
		self.pa.drawLines(self.infos.id)

# 整体图形
class WholeDeviceItem(QGraphicsRectItem):
	def __init__(self, rect, parentView, infos):
		super(WholeDeviceItem, self).__init__(rect)
		self.pa = parentView
		self.infos = infos

	def mousePressEvent(self, event):
		self.pa.emitItemPressEvent(self.infos)
		self.pa.drawAllLines()

# 整体网络状态示意图
class QMyGraphicsview(QGraphicsView):
	sigMouseMovePoint = pyqtSignal(QPoint)
	sigNetDeviceItemPress = pyqtSignal(list)
	paths = [[[0],[1,4,3,2],[1,4,3],[1,4],[0],[1,6]],
		[[2,1],[0],[2,4,3],[2,4],[0],[2,6]],
		[],
		[],
		[],
		[]]
	devices = []
	line_items = []

	def __init__(self, parent=None):
		super(QMyGraphicsview, self).__init__(parent)
		self.rect = QRectF(-200,-200,400,400)
		self.myScene = QGraphicsScene(self.rect)
		self.setScene(self.myScene)
		self.initPoints()
		self.initGraphicSystem()

	def initPoints(self):
		# 准备6个节点圆形
		for i in range(1, 7):
			item = NetDeviceItem(self, NetNodeInfo(i, "green"))
			x = 150*math.sin(math.radians(60*i))
			y = 150*math.cos(math.radians(60*i))
			item.setPos(x, y)
			item.setBrush(Qt.green)
			item.setRect(-15, -15, 30, 30)
			item.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable
					| QGraphicsItem.ItemIsFocusable)
			self.devices.append(item)

	def initGraphicSystem(self):
		# 清除所有item
		self.myScene.clear()
		# 显示scene边框
		item1 = WholeDeviceItem(self.rect, self, ["whole", "white"])
		item1.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
		self.myScene.addItem(item1)
		# 显示节点
		for item in self.devices:
			self.myScene.addItem(item)
			text_item = self.myScene.addSimpleText(str(item.infos.id))
			text_item.setPos(item.pos().x()+20, item.pos().y())
		self.myScene.clearSelection()

	def mouseMoveEvent(self, evt):
		self.sigMouseMovePoint.emit(evt.pos())

	def emitItemPressEvent(self, infos):
		self.sigNetDeviceItemPress.emit(infos)

	def removeAllLines(self):
		for item in self.line_items:
			self.myScene.removeItem(item)
		self.line_items.clear()

	def drawAllLines(self):
		self.removeAllLines()
		for path in self.paths:
			if len(path) == 6:
				for line in path:
					if len(line)>1:
						for i in range(len(line)-1):
							p1 = self.devices[line[i]-1]
							p2 = self.devices[line[i+1]-1]
							line_item = self.myScene.addLine(p1.pos().x(), p1.pos().y(), p2.pos().x(), p2.pos().y())
							self.line_items.append(line_item)

	def drawLines(self, id):
		self.removeAllLines()
		"""画出id节点的连接线"""
		for line in self.paths[id-1]:
			if len(line)>1:
				for i in range(len(line)-1):
					p1 = self.devices[line[i]-1]
					p2 = self.devices[line[i+1]-1]
					line_item = self.myScene.addLine(p1.pos().x(), p1.pos().y(), p2.pos().x(), p2.pos().y())
					self.line_items.append(line_item)
