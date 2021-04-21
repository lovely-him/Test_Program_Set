
import numpy as np
import pyqtgraph as pg
import pyqtgraph.ptime as ptime
from pyqtgraph.Qt import QtCore, QtGui
import sys

"""
pyqtgraph 学习测试程序
测试一下连续图片的显示 ②
"""

class Open_win():
    """
    创建窗口
    """
    def __init__(self,
            data = [],
            Title = "默认名字",
            win_w = 1280,
            win_h = 640,
            view_w = 128,
            view_h = 32,
            view_Locked = 0,
            print_on = 0):
        "创建对象"
        self.app = pg.mkQApp()                  # 建立app
        self.win = pg.GraphicsLayoutWidget()    # 创建窗口
        self.img = pg.ImageItem(border='w')     # 创建图像项目
        self.view = self.win.addViewBox()       # 添加插件
        self.view.addItem(self.img)             # 记载图片插件
        
        "设置属性"
        self.win.resize(win_w, win_h)           # 设定窗口大小
        self.win.setWindowTitle(Title)          # 设定窗口标题
        self.view.setRange(QtCore.QRectF(0, 0, view_w, view_h)) # 设置初始视图边界
        if view_Locked == 1:
            self.view.setAspectLocked(True)     # 锁定窗口长宽比
        
        if data != []:                          # 非空就赋值
            if data.shape != (32,128):          # 检查数组维度
                print("【him】：data 数组形状错误，请检查")
                sys.exit()  #退出程序
            self.data = data                    # 初始图片数据
        else:                                   # 创建存图片的空数组
            self.data = np.zeros((32,128), dtype = np.uint8)

        "设置默认参数"
        self.com_on = 0     # 起始默认为0，还未给数据添加对象
        self.updateTime = 0
        self.fps = 0
        self.print_on = print_on

    def set_com_data(self, com_data):
        "设置获取图像的对象"
        self.com_on = 1
        self.com_data = com_data

    def __up_data(self):
        "更新数据"
        if self.com_on == 1:
            self.data = self.com_data()     # 获取图片数据

        # 坑爹的库，为什么显示时倒着的，我要自己装置矩阵
        data_t = np.zeros((128,32), dtype = np.uint8) 
        for x in range(128):
            for y in range(32):
                data_t[x][y] = self.data[31-y][x]

        self.img.setImage(data_t)

        "还不知道为什么一定要有这个计算时间的程序才能连环显示"
        self.timer.start(1)
        self.now = ptime.time()
        fps2 = 1.0 / (self.now-self.updateTime)
        self.updateTime = self.now
        self.fps = self.fps * 0.9 + fps2 * 0.1
        
        "是否打印调试信息"
        if self.print_on == 1:
            print (f"{self.fps} fps")

    def __call__(self):
        "开始运行"
        self.win.show()                         # 打开窗口，看来最后再打开也可以
        self.timer = QtCore.QTimer()                 # 返回定时器对象
        #由于PyQt的持久性而不使用QTimer.singleShot()。see PR #1605
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.__up_data)
        self.__up_data()
        self.app.exec_()


if __name__ == "__main__":  # 居然不可以用 is代替 ==
    # import cv2
    # data1 = cv2.imread('./Python_test/out_jpg/out.jpg', 0)
    import serial_test1 as him1
    import serial_test3 as him3
    # 创建串口对象
    com = him1.Canon_Port()
    # 创建转换数据对象
    get_data = him3.com_data(com, print_on = 0)
    # 创建窗口对象
    win = Open_win(print_on = 1)
    # 赋予获取数据对象
    win.set_com_data(get_data)
    # 运行窗口
    win()

