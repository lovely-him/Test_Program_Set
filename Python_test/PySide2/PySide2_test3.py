

import PySide2
from PySide2 import QtWidgets
from PySide2.QtWidgets import QApplication, QMessageBox, QTextBrowser, QGraphicsScene
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Signal,QObject
import os
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
"""
坑爹的，找了那么久问题，才发现PySide2的graphicsView不可以加载ViewBox？？？？
"""

import numpy as np
import pyqtgraph as pg
import pyqtgraph.ptime as ptime
from pyqtgraph.Qt import QtGui, QtCore

# pg.setConfigOption('imageAxisOrder', 'row-major')

# from PyQt5 import uic
# from PyQt5.Qt import *
# from PyQt5.QtCore import Signal,QObject
# from PyQt5.QtWidgets import QApplication

from serial_test4 import Canon_com
from threading import Thread

# 自定义信号源对象类型，一定要继承自 QObject
class My_Signals(QObject):
    comboBox_port = Signal(str)         # 更新 下拉列表框——端口 的信号
    textBrowser_cominp = Signal(str)    # 更新 文本浏览框 的信号


class Com_Ui:
    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 用什么加载就会返回什么库中的对象
        # self.ui = uic.loadUi('./Python_test/ui/untitled_2.ui')
        self.ui = QUiLoader().load('./Python_test/ui/untitled_2.ui')
        # 从自定义类中加载信号类型，用于多线程的通讯
        self.signals = My_Signals()

    def Set_statusbar(self, string):
        "嵌套打包 状态栏设置 用于调试信息发布"
        self.ui.statusbar.showMessage(string)

    "端口设置 部分"
    def Com_init(self):
        "存放端口初始化的内容：线程、信号等"
        self.com = Canon_com()
        
        "设置 下拉列表框——端口 信号连接的函数，与线程运行的函数"
        self.plist = []                         # 存放端口字符串
        self.signals.comboBox_port.connect(self.connect_comboBox_port)
        thread = Thread(                        # 检测端口的线程
            target=self.Get_comboBox_port,      # 线程入口
            daemon=True)                        # 设置新线程为daemon线程
        thread.start()

        "设置 下拉列表框——波特率、超时时间 属性"
        self.ui.comboBox_baudrate.addItems(['115200','9600'])
        self.ui.doubleSpinBox_timeout.setValue(2)

        "设置 连接/断开-按键 属性"
        self.com_switch = 0                    # 开关状态标志位
        self.ui.pushButton_switch.setText("连接")
        self.ui.pushButton_switch.clicked.connect(self.connect_pushButton_switch)

        "初始化 工具A"
        self.Tool_A_init()                      # 初始化串口打印的部件

        "初始化 工具B"
        self.Tool_B_init()                      # 开启视频的部件
        
    def connect_pushButton_switch(self):
        "运行 端口开关的程序（由 按钮 引发 coonect 回调）"
        if self.com_switch == 0:                           # 切换状态
            self.com_switch = 1
            self.ui.pushButton_switch.setText("断开")
            "设置打开 端口"
            port = self.ui.comboBox_port.currentText()      # 获取文本
            port = port.split(' ')[0]                       # 提取端口号
            baudrate = self.ui.comboBox_baudrate.currentText()
            baudrate = int(baudrate)                        # 波特率
            timeout = self.ui.doubleSpinBox_timeout.value() # 超时时间
            self.com(port, baudrate, timeout)               # 打开端口
            read_portdata_thread = Thread(                  # 读取端口数据的线程
                target=self.Get_comboBox_port,              # 线程入口
                daemon=True)                                # 设置新线程为daemon线程
            read_portdata_thread.start()                    # 运行线程
            "设置打开 工具A"
            # self.Too_A_open()
            self.Too_B_open()
            self.Set_statusbar("【him】：端口已打开")
        else:
            self.com_switch = 0
            self.ui.pushButton_switch.setText("连接")
            self.com.com.close()                            # 关闭端口
            self.Set_statusbar("【him】：端口已关闭")
            
            self.timer.stop()       # 停止定时器

    def Get_comboBox_port(self):
        "获取 下拉列表框——端口 文本（多线程持续运行）"
        while 1:                                # 持续运行
            flag = 0                            # 变化的标志位
            plist = self.com.Get_Port()         # 获取端口列表
            for i in range(len(plist)): 
                plist[i] = str(plist[i])        # 提取端口字符
            
            if len(plist) != len(self.plist):   # 比较端口号有没有变化
                self.plist = plist
                flag = 1                        # 改变标志位
            else:
                for i in range(len(plist)):
                    if self.plist[i] != plist[i]:
                        self.plist[i] = plist[i]
                        flag = 1                # 改变标志位

            if flag == 1:                       # 发送信号
                self.signals.comboBox_port.emit("【him】：检测到端口已变化")

    def connect_comboBox_port(self,string):
        "设置 下拉列表框——端口 文本（由 Get_comboBox_port 引发 coonect 回调）"
        self.Set_statusbar(string)                  # 打印传入字符串
        self.ui.comboBox_port.clear()               # 清除端口列表
        self.ui.comboBox_port.addItems(self.plist)  # 输出端口列表
        # "端口变化时，带动的变化（不确定是不是正在连接的端口变化了）"
        # if self.com_switch == 1:
        #     self.com_switch = 0
        #     self.ui.pushButton_switch.setText("连接")
        #     self.com.com.close()                            # 关闭端口
        #     self.Set_statusbar("【him】：端口已关闭")

    "端口通讯 部分"
    def Tool_A_init(self):
        "工具A 初始化：端口通讯"
        self.ui.pushButton_comout.setText("发送")               # 设置按钮
        self.ui.comboBox_outtype.addItems(['utf8','hex'])       # 设置下拉列表框
        # self.ui.lineEdit_comout.setPlaceholderText('默认')    # 设置单文本框

        "设置 文本浏览框 的线程、回调"
        self.signals.textBrowser_cominp.connect(self.connect_textBrowser_cominp)

        "设置 按钮组 的回调"
        self.cominp_type = self.ui.radioButton_type0.text()     # 默认用十六进制显示
        self.ui.buttonGroup.buttonClicked.connect(self.connect_cominp_type)

    def Too_A_open(self):
        "打开 工具A 接受字符串线程 和 发送字符串线程"
        # 笔记：线程都在关闭端口时都因错误退出了，所以线程应该严格分类，需要重新打开的
        thread = Thread(                        # 读取端口字节的线程
            target=self.Get_com_data,           # 线程入口
            daemon=True)                        # 设置新线程为daemon线程
        thread.start()

    def connect_cominp_type(self):
        "获取 按钮组 设置端口输出格式（由 buttonGroup 引发 connect）"
        radioButton = self.ui.buttonGroup.checkedButton()
        self.cominp_type = radioButton.text()
        self.Set_statusbar(f"【him】：设置打印格式为{self.cominp_type}")    

    def connect_textBrowser_cominp(self, data):
        "设置 文本浏览框 的打印 （由 Get_com_data 引发 coonect 回调）"
        self.ui.textBrowser_cominp.insertPlainText(data)        # 在编辑框末尾添加文本内容
        #                                                       # （不会自动换行）
        # QtWidgets.QApplication.processEvents()  #一定加上这个功能，不然有卡顿
 
    def Get_com_data(self):
        "获取 串口字符 （多线程持续运行）"
        while 1:                                                # 持续读取
            try:
                data = self.com.com.read(1)                     # 调用类对象中的方法
            except:
                if self.com_switch == 1:                        # 如果当前仍在连接状态
                    self.connect_pushButton_switch()            # 手动调用切换按钮
                # self.Set_statusbar("【him】：端口读取失败")    # 没有用，会被检测的线程覆盖
                break

            # 不为空才发送,有时不能打印出来因为不不能转换为字符，并不是空
            # 可以打印查看，奇怪的是不能用(data != '')，会一直为True
            if data:
                if self.cominp_type == 'hex':                   # 十六进制输出
                    data = f"{ord(data):#x}"
                    # 实在找不到什么方法可以转换，手动滑稽写死
                    if len(data) == 3:                          # 统一输出格式
                        data = data[0]+data[1]+'0'+data[2]
                elif self.cominp_type == 'uint8':               # 十进制输出
                    data = f"{ord(data)}"
                elif self.cominp_type == 'utf8':                # 字符输出
                    pass                                        # 本身就是字符
                    
                # print(data)
                # 目前的bug，因为持续输出在ui中，直接卡死了程序
                # self.signals.textBrowser_cominp.emit(data)      # 发送信号

    "视频接收 部分"
    def Tool_B_init(self):

        # vb = pg.ViewBox()               # 这是PyQt5的操作方法？
        # self.ui.graphicsView_img.setCentralItem(vb) # PyQt5也没有这个方法……
        # vb.setAspectLocked()
        # img = pg.ImageItem()
        # vb.addItem(img)

        # vb = pg.ViewBox()               # 这是PyQt5的操作方法？
        # vb.setAspectLocked()
        # img = pg.ImageItem()
        # vb.addItem(img)
        # self.ui.graphicsView_img.setCentralItem(vb)

        self.imgv = pg.ImageItem()          # 这才是PySide2的使用方法？
        scene = QGraphicsScene()  # 创建场景
        # scene.addText('Hello, world')
        scene.addItem(self.imgv)
        self.ui.graphicsView_img.setScene(scene)
        
        # 导入自己的图片
        import cv2
        self.img = np.zeros((128,32), dtype = np.uint8) 
        data = cv2.imread('./Python_test/out_jpg/img.jpg', 0)
        # 坑爹的库，为什么显示时倒着的，我要自己装置矩阵
        for x in range(128):
            for y in range(32):
                self.img[x][y] = data[y][x]
        self.imgv.setImage(self.img)
        
        win = pg.GraphicsLayoutWidget()     # 还没弹出窗口
        view = win.addViewBox()
        self.img2 = pg.ImageItem(border='w')
        self.img2.setImage(self.img)
        view.addItem(self.img2)
        win.show() 
        self.ui.graphicsView_img.setScene(scene)
        
        self.timer = QtCore.QTimer()  # 返回定时器对象
        # 由于PyQt的持久性而不使用QTimer.singleShot()。see PR #1605
        # self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.__up_data)
        self.__up_data()

    def Too_B_open(self):
        # 笔记：线程都在关闭端口时都因错误退出了，所以线程应该严格分类，需要重新打开的
        thread = Thread(                        # 读取端口字节的线程
            target=self.Get_img_data,           # 线程入口
            daemon=True)                        # 设置新线程为daemon线程
        thread.start()
        self.timer.start(100)

        
    def Get_img_data(self):
        "获取图片数据"
        while 1:
            img = self.com.Read_img()
            data = img[0]
            for x in range(128):
                for y in range(32):
                    self.img[x][y] = data[y][x]
            self.com.get_log(1)

    def __up_data(self):
        "更新数据"
        self.imgv.setImage(self.img)
        self.timer.start(100)           # 每次都要重新设定……这个定时器怎么不会自己周期运行啊
        # print("__up_data")


if __name__ == '__main__':
    app = QApplication([])
    com_ui = Com_Ui()
    com_ui.Com_init()
    com_ui.ui.show()
    app.exec_()
