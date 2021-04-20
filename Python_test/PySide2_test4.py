from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader
import pyqtgraph as pg
import numpy as np

import os
import PySide2
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

"""
白忙活那么就，怪不得找来找去找不到相关资料，原来压根就不是这样实现的。
Qt Designer 本身不含 GraphicsLayoutWidget 我要实现就要自己外加。
啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊
"""


class Stock:

    def __init__(self):

        loader = QUiLoader()

        # pyside2 一定要 使用registerCustomWidget 
        # 来注册 ui文件中的第三方控件，这样加载的时候
        # loader才知道第三方控件对应的类，才能实例化对象
        loader.registerCustomWidget(pg.PlotWidget)
        loader.registerCustomWidget(pg.GraphicsLayoutWidget)
        self.ui = loader.load("./Python_test/ui/untitled_3.ui")

        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]

        # 通过控件名称 historyPlot，找到Qt designer设计的 控件
        self.ui.widget.plot(hour,temperature)

        view = self.ui.widget_2.addViewBox()
        ##设置初始视图边界
        # view.setRange(QtCore.QRectF(0, 0, 128, 32))
        img = pg.ImageItem(border='w')
        view.addItem(img)

        # data = np.zeros((128,32), dtype = np.uint8) 
        data = np.random.normal(size=(15, 600, 600), loc=1024, scale=64).astype(np.uint16)
        # 坑爹的库，为什么显示时倒着的，我要自己装置矩阵
        # for x in range(128):
        #     for y in range(32):
        #         data[x][y] = data1[31-y][x]

        img.setImage(data[0])


app = QApplication([])
stock = Stock()
stock.ui.show()
app.exec_()