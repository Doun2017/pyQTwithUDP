# -*- coding: utf-8 -*-
 

import sys 
import math 
from PyQt5.QtCore import pyqtSignal, QRectF, Qt, QPoint, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QLabel, QGraphicsScene, QGraphicsRectItem, QGraphicsItem, QGraphicsEllipseItem


class NetDeviceItem(QGraphicsEllipseItem):
	def __init__(self, parentView, infos):
		super(NetDeviceItem, self).__init__()
		self.pa = parentView
		self.infos = infos

	def mousePressEvent(self, event):
		self.pa.emitItemPressEvent(self.infos)


class QMyGraphicsview(QGraphicsView):
	sigMouseMovePoint = pyqtSignal(QPoint)
	sigNetDeviceItemPress = pyqtSignal(list)
	def __init__(self, parent=None):
		super(QMyGraphicsview, self).__init__(parent)
		self.devices = []
		self.initGraphicSystem()

	def mouseMoveEvent(self, evt):
		self.sigMouseMovePoint.emit(evt.pos())

	def initGraphicSystem(self):
		# 定义scene 显示其边框
		rect = QRectF(-200,-200,400,400)
		self.myScene = QGraphicsScene(rect)
		self.setScene(self.myScene)
		item1 = QGraphicsRectItem(rect)
		item1.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
		self.myScene.addItem(item1)

		for i in range(6):
			item = NetDeviceItem(self, [str(i), "green"])
			x = 150*math.sin(math.radians(60*i))
			y = 150*math.cos(math.radians(60*i))
			item.setPos(x, y)
			item.setBrush(Qt.green)
			item.setRect(-15, -15, 30, 30)
			item.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable
					| QGraphicsItem.ItemIsFocusable)
			self.devices.append(item)
			self.myScene.addItem(item)
		self.myScene.clearSelection()

	def emitItemPressEvent(self, infos):
		self.sigNetDeviceItemPress.emit(infos)
