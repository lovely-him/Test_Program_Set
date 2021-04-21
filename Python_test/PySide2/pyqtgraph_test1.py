

import pyqtgraph as pg
import numpy as np
import array

"""
pyqtgraph 学习测试程序
使用：python -m pyqtgraph.examples 命令可以直接打开示例窗口
另一种方法：
import pyqtgraph.examples
pyqtgraph.examples.run()

"""


app = pg.mkQApp()           #建立app

"设置 win 窗口属性"
win = pg.GraphicsWindow()           #建立一个窗口 和 plot不一样
win.setWindowTitle(u'新窗口的名字') #默认名字是 python
win.resize(800,500)                 #不指定也有默认大小
p = win.addPlot()                   #在窗口中加入一个 plot？那为什么不直接打开一个plot啊，2333
# p1 = win.addPlot()                #原来是因为一个窗口可以插入多个图

"设置 Plot 窗口属性"
p.showGrid(x=True,y=True)           #显示参考线
p.setRange(xRange=[-100,100], yRange=[-1.2, 1.2])   #设置显示范围
p.setLabel(axis='left', text='这里是左边text')       # Label 标签
p.setLabel(axis='bottom', text='这里是底部text')     #参数 axis 代表显示的位置
p.setTitle('这里显示标题')                           # Title 标题

"设置 要显示的 数据内容"
curve = p.plot()            #创建一个要显示的曲线？
curve1 = p.plot()            #创建一个要显示的曲线？

i = 0
idx = 0
data = array.array('d') #可动态改变数组的大小,double型数组
data1 = array.array('d') #可动态改变数组的大小,double型数组

"更新数据函数"
def plotData():
    global idx#内部作用域想改变外部域变量
    global i
    idx += 1

    if i < 1000:
        tmp = np.sin(np.pi / 50 * idx)
        data.append(tmp)
        curve.setData(data)
        
        tmp = np.cos(np.pi / 50 * idx)
        data1.append(tmp)
        curve1.setData(data1)
        i = i+1
    else:
        data[:-1] = data[1:]
        data[i-1] = tmp
        
        data1[:-1] = data1[1:]
        data1[i-1] = tmp

"定时器，用于更新数据"
timer = pg.QtCore.QTimer()          #创建一个定时器
timer.timeout.connect(plotData)     #定时调用plotData函数
timer.start(50)                     #多少ms调用一次

"还可能需要用到多线程，和队列信息"

#上下固定搭配？如果中间没东西终端会一直空运行……看来这个代码类似让程序一直运行？如果没有的话程序运行完毕直接结束
app.exec_()