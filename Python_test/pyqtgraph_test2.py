
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph as pg
import pyqtgraph.ptime as ptime

"""
pyqtgraph 学习测试程序
测试一下连续图片的显示
"""

import serial_test1 as him1
import serial_test3 as him3
# 创建串口对象
com = him1.Canon_Port()
# 创建转换数据对象
get_data = him3.Open_win(com,print_on = 1)

#建立app
app = pg.mkQApp()

"设置 win 窗口属性"
##使用GraphicsView小部件创建窗口（和 GraphicsWindow 有什么不一样？）
win = pg.GraphicsLayoutWidget()     # 还没弹出窗口
##在自己的窗口中显示小部件
win.setWindowTitle('这一行是设置窗口名字')
win.resize(1280,640)                 #不指定也有默认大小

"设置 view 窗口属性"
#创建一个对象并返回，这时窗口里还是空空如也，如果是添加plot的话，已经有坐标轴了
view = win.addViewBox()
##设置初始视图边界
view.setRange(QtCore.QRectF(0, 0, 128, 32))
##锁定长宽比，
# view.setAspectLocked(True)          #我很需要
# view.setTitle("测试是不是也有这个函数")

win.show()                          #才弹出窗口
##创建图像项目
img = pg.ImageItem(border='w')
view.addItem(img)

##创建随机图像
# data = np.random.normal(size=(128, 32), loc=1024, scale=64).astype(np.uint16)

# 导入自己的图片
import cv2
data = np.zeros((128,32), dtype = np.uint8) 
data1 = cv2.imread('./Python_test/out_jpg/out.jpg', 0)
# 坑爹的库，为什么显示时倒着的，我要自己装置矩阵
for x in range(128):
    for y in range(32):
        data[x][y] = data1[31-y][x]


i = 0

fps = 0
updateTime = ptime.time()


"更新数据函数"
def updateData():
    global img, data, i, updateTime, fps

    # 读取一幅图像
    data1 = get_data()
    data = np.zeros((128,32), dtype = np.uint8) 
    
    for x in range(128):
        for y in range(32):
            data[x][y] = data1[31-y][x]

    img.setImage(data)

    timer.start(1)
    now = ptime.time()
    fps2 = 1.0 / (now-updateTime)
    updateTime = now
    fps = fps * 0.9 + fps2 * 0.1
    
    print (f"{fps} fps")

"定时器，用于更新数据"
timer = QtCore.QTimer()
#由于PyQt的持久性而不使用QTimer.singleShot()。see PR #1605
timer.setSingleShot(True)
timer.timeout.connect(updateData)
updateData()

app.exec_()
