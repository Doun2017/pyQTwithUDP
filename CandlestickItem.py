import pyqtgraph as pg
from PyQt5 import QtCore, QtGui
import CandlestickItem


class CandlestickItem(pg.GraphicsObject):  
    # 初始化时填入数据
    def __init__(self, data):  
        pg.GraphicsObject.__init__(self)  
        self.data = data ## data must have fields: x:MHz;y:能量dbm/40KHz     time, open, close, min, max  
        self.generatePicture()

    # 调用此函数 根据data生成QPicture
    def generatePicture(self):
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('w'))
        # w = (self.data[1][0] - self.data[0][0]) / 3.
        for (x,y) in self.data:
            p.drawPoint(QtCore.QPointF(x,y))
            # p.drawLine(QtCore.QPointF(t, min), QtCore.QPointF(t, max))
            # if open > close:
            #     p.setBrush(pg.mkBrush('g'))
            # else:
            #     p.setBrush(pg.mkBrush('r'))
            # p.drawRect(QtCore.QRectF(t-w, open, w*2, close-open))
        p.end()
        
    def updataData(self,data):
        self.data = data ## data must have fields: x:MHz;y:能量dbm/40KHz     time, open, close, min, max  
        self.generatePicture()

    # 每次重绘picture
    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())

# class MainWindow(object):  
#     def __init__(self):  
#         self.ui.verticalLayout_3.addWidget(chart())  
        
def chart():
    # hist_data = ts.get_hist_data('600519',start='2017-05-01',end='2017-11-24')
    data_list = []
    axis = []
    # for dates,row in hist_data.iterrows():
    for dates,row in {}:
        # 将时间转换为数字
        date_time = datetime.datetime.strptime(dates,'%Y-%m-%d')
        t = date2num(date_time)
        # t = dict(enumerate(datetime))
        open,high,close,low = row[:4]
        datas = (t,open,close,low,high)
        data_list.append(datas)
        axis.append(t)
    # print(axis)

    #test
    data_list.append((1,1))
    data_list.append((2,1))
    data_list.append((31.44,1))


    axis_dict = dict(enumerate(axis))
    item = CandlestickItem(data_list)
    plt = pg.PlotWidget()
    # print(plt.getAxis('bottom'))
    plt.addItem(item)
    plt.showGrid(x=True,y=True)
    plt.setYRange(min=-150,max=10)
    return (plt, item)