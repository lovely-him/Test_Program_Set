
#!/usr/bin/env python
#-*- coding: utf-8 -*

"""
第二版 - 图像接收上位机
"""

# 文件目录前缀（指定 UI 文件 和 图标文件） 和 保存图片的默认路径
file_catalog = "./Python_test/ui/"
file_catalog_1 = "E:/Program/Documents/GitHub/Program_test/Python_test/out_img/全向-30cm-0/"#./Python_test/out_img/

# 算法文件 也可以外部调用 这个也是一个路径
from him_math.him_math_all import math_all     

import os
import time
import sys
from pathlib import Path
from threading import Thread

try:
    import serial   
    import serial.tools.list_ports    
    import numpy as np
    import imageio

    import PySide2
    import os.path
    # dirname = os.path.dirname(PySide2.__file__)
    # plugin_path = os.path.join(dirname, 'plugins', 'platforms')
    # os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
    
    from PySide2.QtGui import  QIcon
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtWidgets import QApplication,QMessageBox,QFileDialog
    from PySide2.QtCore import Signal,QObject
    import pyqtgraph as pg                      # PySide2 的 要放在后面
    from pyqtgraph.Qt import QtCore
except:
    print("——————————————————————————————————————")
    ch = input("【him】：程序检测到有模块没安装，请问是否需要安装；(y/n)\n")
    if (ch != 'y') and (ch != 'Y'):     # 如果输入不符合要求，就退出程序
        sys.exit()
    use_module_list=["pyserial","pyqtgraph","PyQt5","PySide2","numpy","imageio"]
    for module in use_module_list:      # 使用终端命令安装所有模块，已安装的不会再安装
        os.system(f"pip install {module}")
    sys.exit()                          # 退出程序，要重新打开程序，防止没安装成功


class Canon_com():
    "创建串口对象"
    def __init__(self):
        "设置属性"
        self.read_u8_num = 0            # 定义接收字节数
        self.read_y_num = 0             # 定义接收列数
        self.read_img_time = 0          # 定义读取时间

    def Get_Port(self):
        "获取可用端口"
        plist = list(serial.tools.list_ports.comports())
        return plist

    def Cmd_Set_Port(self):
        "终端设置端口"
        plist = self.Get_Port()

        if len(plist) == 0:
            print("【him】：无可用端口；")
            while 1:
                pass
        else:
            print("【him】：可用端口；")
            for i in range(len(plist)):
                print(f"【him】：{i} - {plist[i]}") 

        print("【him】：输入选择:",end = '')
        while 1:                            # 循环等待成功
            try:
                num = int(input())          # 读取终端输入
                portx = list(plist[num])[0] # 获取对应端口号
            except:
                print("【him】：重新输入：",end = '')
            else:
                print("【him】：成功选择：" + portx + " ;")
                break

        self.port = portx                   # 保存选择

    def read(self,num):
        "嵌套读取，用与计算读取所消耗的时间"
        self.read_u8_num += num
        return self.com.read(num)

    def Read_img_y(self):
        """读取图像一列数据，固定格式为：0xA5、列数号、uint8[0-3]、校验、0x5A
        如果接收错误会返回一个字符串，内容是 'error' """
        while 1:                            # 直到成功读取
            data = 0
            
            error_num = 0                   # 重置，累加在死循环中的错误情况
            while data != 0xA5:             # 等待帧头
                ch = self.read(1)
                if ch:
                    data = ord(ch)          # 有内容才转换
                    error_num += 1          # 如果是有内容，但是是错的，就加一次
                    if data != 0xA5:
                        print("【him】：判断列数据的帧头有错！！！",data)
                else:
                    error_num += 20         # 如果是超时就认为是断线了，直接加20

                # print("【him】：Read_img_y - 接收列数据 - error")
                if error_num > 100:         # 读了100个数据还没？有问题
                    return 'error'

            data = list(self.read(1+4+1+1))
            if len(data) != (1+4+1+1):      # 在接收后续内容的时候超时了！！！这样会接收到一般直接卡主……
                print("【him】：判断列数据的长度有错！！！")
                continue

            if data[-1] != 0x5A:            # 判断帧尾
                print("【him】：判断列数据的帧尾有错！！！")
                continue

            if data[-2] != (data[0]&data[1]&data[2]&data[3]&data[4]):
                print("【him】：判断列数据的校验有错！！！")
                continue                    # 判断校验

            x_num = data.pop(0)             # 弹出列数号
            uint32 = data[0] | data[1]<<8 | data[2]<<16 | data[3]<<24

            return (x_num, uint32)          # 返回数据

    def Read_img(self):
        """读取整幅图像，固定长宽(32,128)，共返回一个元组包含2个数组，
        如果接收错误会返回一个字符串，内容是 'error' """
        self.img = np.zeros((32,128,3), dtype = np.uint8) # 重置图像数组
        self.bmp = np.zeros(128, dtype = np.uint32)     # 注意，这里为了避免错误用bmp先存起来
        self.read_u8_num = 0                # 重置接收字节数
        self.read_y_num = 0                 # 重置接收列数
        self.read_img_time = time.time()    # 记录时间
        
        data = [0,0]                    # 创建临时变量
        
        error_num = 0                   # 重置，累加在死循环中的错误情况
        while 1:                        # 等待帧头
            data = self.Read_img_y()

            if data == 'error':
                error_num += 1
                print("【him】：Read_img - 等待帧头 - error")
                if error_num >= 1:      # 读了200个数据还没？有问题
                    return 'error'
            
            if data[0] == 0xBB:         # 符合帧头，退出这次循环
                break
        error_num = 0                   # 重置，累加在死循环中的错误情况
        while 1:
            data = self.Read_img_y()

            if data == 'error':
                error_num += 1
                print("【him】：Read_img - 等待帧尾 - error")
                if error_num >= 1:      # 读了200个数据还没？有问题
                    return 'error'
                continue                # while 的判断条件用不到，如果是错误内容直接跳过这次循环

            if data[0] != 0xDD:         # 等待帧尾
                if data[0] >= 128:      # 收到的东西有误，直接等待下一个帧尾，虽然图像错位，但是好过卡主
                    print("【him】场帧尾接收失败，收到的值大于128", data[0])
                    continue        
                self.bmp[data[0]] = data[1]
            else:
                break

        # 已经矫正，可以屏蔽掉了。
        # for x in range(128):                                # 将压缩图的坐标回归左上角。如果之后硬件改了，这部分就可以屏蔽掉
        #     data = 0                                        # 重置
        #     for y in range(32):                             # 遍历一列的每一行    
        #         data |= (((self.bmp[x]>>y)&0x1)<<(31-y))    # 将整列反转
        #     self.bmp[x] = data                              # 覆盖这一列的数据

        for x in range(128):                                # 解压数据
            data = self.bmp[x]
            if data != 0:                                   # 列不为空
                self.read_y_num += 1                        # 累加列数
                for y in range(32):     
                    gray = (data>>y) & 0x1
                    if gray == 1:                           # 行不为空
                        self.img[y][x][0] = 255             # 计算机中的图片原点为左上角
                        self.img[y][x][1] = 255             # 扩展为三维的图像
                        self.img[y][x][2] = 255             
                        
        self.read_img_time -= time.time()   # 记录时间
        self.read_img_time = -self.read_img_time
        return (self.img, self.bmp)         # 返回图片

    def Read_midcourt(self):
        "读取中线，只包含中线和部分标志位的内容"
        num = 0                                                     # 接收数目
        self.BT_SET_NUM = 41                                        # 发送数目
        rx_array = np.zeros((self.BT_SET_NUM), dtype = np.uint8)    # 接收数组
        self.img = np.zeros((32,128,3), dtype = np.uint8)           # 重置图像数组
        self.bmp = np.zeros(128, dtype = np.uint32)                 # 注意，这里为了避免错误用bmp先存起来
        self.read_u8_num = 0                                        # 重置接收字节数
        self.read_img_time = time.time()                            # 记录时间

        while 1:
            ch = self.read(1)
            if ch:
                rx_array[num] = ord(ch)
            else:
                continue
            if num < 2 and rx_array[num] != 0xA5:               # 判断帧头
                num = 0
                continue
            else:                                               # 接收数据
                num += 1
                if num == self.BT_SET_NUM:                      # 接收完毕
                    
                    rx_check = 0
                    for i in range(2,self.BT_SET_NUM-2,1):      # 计算校验位
                        rx_check += rx_array[i]
                    #     print(f"{i}:{rx_array[i]};{rx_check};",end=" ")
                    
                    # print(rx_array[self.BT_SET_NUM-2],rx_check&0xF,rx_array[self.BT_SET_NUM-1])
                    if rx_array[self.BT_SET_NUM-2] == (rx_check&0xF):    # 对比校验位
                        break
                    else:
                        num = 0
                        continue
        
        self.Status_flag = rx_array[6]                          # 取出状态标志位

        for i in range(7,7+32,1):
            i_y = i-7
            ch = rx_array[i]

            if ch & 0x80:                                       # 判断正负
                i_x = ~ch+1
            else:
                i_x = ch

            i_x += 64
            if i_x>0 and i_x<126:                               # 判断范围
                self.img[i_y][i_x][0] = 255
                self.img[i_y][i_x][1] = 255
                self.img[i_y][i_x][2] = 255
                self.bmp[i_x] = 0x1<<i_y

        self.read_img_time -= time.time()   # 记录时间
        self.read_img_time = -self.read_img_time
        return (self.img, self.bmp)         # 返回图片
        
    def get_log_2(self, flag=1):
        "读取中线时专用"
        correct_data = self.BT_SET_NUM
        error_data = self.read_u8_num - correct_data 
        fps = 1/self.read_img_time if self.read_img_time else 0
        string = f"【him】：耗时→{self.read_img_time:1.4f} s；帧率→{fps:8.2f}；"
        string += f"标志位→{self.Status_flag:2}；正确数据→：{correct_data:5}；错误数据→{error_data:5}；"
        if flag == 1:           # 根据参数选择打印(玄学，为什么要8不能5)
            print(string)
            
        return (self.read_img_time, self.BT_SET_NUM, fps, correct_data, error_data, string)




    def get_log(self, flag=1):
        "返回上一次接收图片的时间、列数、和有效字节数、无效字节数"
        correct_data = (2+self.read_y_num) * (1+1+4+1+1)
        error_data = self.read_u8_num - correct_data        # 计算错误数据，如果我把空数据也发回来，那计算方法就不一样了。所以会显示一堆错误数据……找了好久的问题
        fps = 1/self.read_img_time if self.read_img_time else 0
        string = f"【him】：耗时→{self.read_img_time:1.4f} s；帧率→{fps:8.2f}；"
        string += f"列数→{self.read_y_num:3}；正确数据→：{correct_data:5}；错误数据→{error_data:5}；"
        if flag == 1:           # 根据参数选择打印(玄学，为什么要8不能5)
            print(string)
            
        return (self.read_img_time, self.read_y_num, fps, correct_data, error_data, string)

    def __call__(self, port='', baudrate=115200, timeout=2):
        "创建实例对象"
        if port != '':                  # 外部设置端口
            self.port = port
        self.baudrate = baudrate        # 设置波特率
        self.timeout = timeout          # 设置超时时间
        self.com = serial.Serial(
            port = self.port,           # 调用前应先获取
            baudrate = self.baudrate,
            timeout = self.timeout)
        
class My_Signals(QObject):
    "创建自定义信号类"
    comboBox = Signal(list)         # 接收字符串列表，用于接收串口列表
    textBrowser_3 = Signal(str)     # 用于打印系统信息窗口
    textBrowser_2 = Signal(str)     # 用于打印接收信息窗口
    pushButton_10 = Signal(int)     # 用于改变保存图片的按钮文本
    horizontalSlider = Signal(int)  # 用于改变进度条的值

class Win_UI():
    "统合整个上位机的界面窗口"
    def __init__(self):
        # 添加第三方模块
        loader = QUiLoader()
        loader.registerCustomWidget(pg.GraphicsLayoutWidget)
        # 从文件中加载UI定义
        self.ui = QUiLoader().load(file_catalog+'untitled_6.ui')
        # 从自定义类中加载信号类型，用于多线程的通讯
        self.signals = My_Signals()
        # 创建串口对象，用于串口操作
        self.com = Canon_com()
        # 个人算法集合
        self.him = math_all()

        # self.ui.setWindowTitle("him_com")     # 设置软件框名字，默认
        self.ui.setWindowIcon(QIcon(file_catalog+'logo.png'))   # 设置图标文件，分辨率不可以太大

        self.textBrowser_3_init()       # 调试信息打印窗口
        self.comboBox_2_init()          # 设置波特率显示
        self.doubleSpinBox_init()       # 设置超时时间显示
        self.comboBox_init()            # 设置串口选项
        self.lineEdit_023_init()        # 设置预览框
        self.lineEdit_7_init()          # 设置输入框
        self.comboBox_3_init()          # 设置发送类型选项
        self.pushButton_2_init()        # 设置发送按钮
        self.textBrowser_2_init()       # 接收信息打印窗口
        self.pushButton_7_init()        # 设置接收按钮
        self.pushButton_3_init()        # 设置清空输出按钮
        self.pushButton_6_init()        # 设置清空输入按钮
        self.comboBox_4_init()          # 设置接收类型选项
        self.pushButton_11_init()       # 设置接收图像按钮
        self.pushButton_10_init()       # 设置保存图像的按钮
        self.pushButton_init()          # 设置播放图像的按钮
        self.pushButton_5_init()        # 设置保存地址的按钮
        self.lineEdit_8_init()          # 设置地址框的内容
        self.horizontalSlider_init()    # 设置进度条
        self.widget_init()              # 设置图像显示窗口
        self.pushButton_4_init()        # 设置帮助按钮
        self.comboBox_5_init()          # 设置播放类型选项

    "系统信息打印窗口 textBrowser_3"
    def textBrowser_3_init(self):
        """所有部件中第一个初始化，设置回调函数，自定义信号量
        用于发布软件在运行时产生的变动"""
        self.signals.textBrowser_3.connect(self.textBrowser_3_connect)  # 链接信号回调
        
    def textBrowser_3_connect(self,string):
        """窗口的回调函数，用于在窗口末端打印，用时移动光标
        软件界面操控都在回调函数"""
        self.ui.textBrowser_3.append(string)                    # 在末尾添加文本（换行）
        self.ui.textBrowser_3.ensureCursorVisible()             # 确保光标可见

    def print(self,string, flag=1):
        """打包函数，方便调用，有第二个参数，如果设置为零，就不输出到状态栏，
        默认会同时设置状态栏的提示信息"""
        localtime = time.asctime( time.localtime(time.time()))  # 获取格式化的时间
        localtime = localtime.split(' ')[3]
        string = localtime + ' - ' + string                     # 字符串拼接
        self.signals.textBrowser_3.emit(string)                 # 输出到窗口
        if flag == 1:
            self.ui.statusbar.showMessage(string)

    "波特率选项 comboBox_2"
    def comboBox_2_init(self):
        """设置波特率显示 纯显示 
        不回调，在创建串口对象时读取"""
        # self.ui.label_2.setText("默认：波特率")               # 设置标签 label
        self.ui.comboBox_2.addItems(['115200','9600'])          # 设置组合选择框 comboBox
    
    "超时时间设置 doubleSpinBox"
    def doubleSpinBox_init(self):
        """设置超时时间显示 纯显示
        不回调，在创建串口对象时读取"""
        # self.ui.label_3.setText("默认：超时时间")             # 设置标签 label
        self.ui.doubleSpinBox.setValue(0.5)                    # 设置数字输入框 doubleSpinBox

    "串口选项 comboBox"
    def comboBox_init(self):
        """并非手动设置，初始化线程，持续读取串口用于显示
        不回调，在创建串口对象时读取"""
        # self.ui.label.setText("默认：串口")                   # 设置标签 label
        self.com_port_e = ['']                                  # 设置组合选择框 comboBox
        self.ui.comboBox.clear()
        self.signals.comboBox.connect(self.comboBox_connect)    # 每次串口号被改变就回调        
        self.comboBox_Thread_init()                             # 初始化读取串口数的线程

    def comboBox_connect(self,data):
        """回调函数，自定义信号量
        用于改变选项内容，同时发布变化信息"""
        self.ui.comboBox.clear()                                # 先清空
        self.ui.comboBox.addItems(data)                         # 再添加
        self.print("【him】：检测到串口设备发生变动")

    def comboBox_Thread_init(self):
        """线程初始化，只在一开始初始化一次，
        在部件初始化时候一起初始化"""
        thread = Thread(                                        # 检测端口的线程
            target=self.comboBox_thread,                        # 线程入口
            daemon=True)                                        # 设置新线程为daemon线程
        thread.start()                                          # 启动线程

    def comboBox_thread(self):
        """串口选项列表的线程的执行函数，属于死循环，不设置退出条件
        如果串口列表发生改变，就产生信号，执行回调函数"""
        while 1:
            flag = self.get_list_ports()                        # 获取串口列表

            if flag == 1:                                       # 串口号发送了改变
                self.signals.comboBox.emit(self.com_port_e)     # 发送信号

    "发送预览 lineEdit"
    def lineEdit_023_init(self):
        """设置预览模块的标签和提示信息，这些都是在设置ui时就设置好了，所以全部屏蔽
        启动禁止编辑输入框，单纯用作显示用"""
        # self.ui.label_5.setText("默认：binary")                   # 设置标签 label
        # self.ui.label_6.setText("默认：hex")
        # self.ui.label_9.setText("默认：utf-8")
        # self.ui.lineEdit.setPlaceholderText('默认：预览二进制')   # 设置单行文本框 lineEdit
        # self.ui.lineEdit_2.setPlaceholderText('默认：预览十六进制')
        # self.ui.lineEdit_3.setPlaceholderText('默认：预览字符串')
        self.ui.lineEdit.setReadOnly(True)                          # 禁止编辑
        self.ui.lineEdit_2.setReadOnly(True)
        self.ui.lineEdit_3.setReadOnly(True)

    "发送输入 lineEdit_7"
    def lineEdit_7_init(self):
        """设置回调函数，因为每次输入都要读取内容，用于改变预览部分的内容
        """
        # self.ui.lineEdit_7.setPlaceholderText('默认：lovely_him') # 设置单行文本框 lineEdit
        self.ui.lineEdit_7.textChanged.connect(self.lineEdit_7_connect) # 每次文本被修改就回调

    def lineEdit_7_connect(self):
        """输入框的回调函数，用于提取分割输入的内容，再在预览部分显示
        这里没有给预览部分另设一个于显示回调函数用"""

        data = self.com_write_see()                     # 获取需要显示的字符串

        if data == (''):       
            self.ui.lineEdit.clear()                        # 如果是空就清空预览
            self.ui.lineEdit_2.clear()
            self.ui.lineEdit_3.clear()
            return

        binary = data[0]                                # 取出对应的字符串
        hex_data = data[1]
        utf_8 = data[2]

        self.ui.lineEdit.setText(binary)                # 设置文本框显示预览
        self.ui.lineEdit_2.setText(hex_data)
        self.ui.lineEdit_3.setText(utf_8)

    "发送类型 comboBox_3"
    def comboBox_3_init(self):
        """设置发送类型有哪些，然后设置回调函数，
        同时先执行一次回调函数，用于给初始化变量赋值"""
        self.ui.comboBox_3.addItems(['hex','uint8','utf-8','binary'])               # 设置组合选择框 comboBox
        self.ui.comboBox_3.currentIndexChanged.connect(self.comboBox_3_connect)     # 每次选项被修改就回调
        self.comboBox_3_connect()           # 先回调一次，给变量赋值

    def comboBox_3_connect(self):
        """用于读取发送类型的选项，
        同时每次调用都会再调用一次输入框的回调函数，用于改变预览的内容"""
        self.com_out_type = self.ui.comboBox_3.currentText()    # ['hex','utf-8','uint8']
        self.lineEdit_7_connect()                               # 每次修改都会重新回调，修改预览
        self.print(f"【him】：输出类型已修改为 {self.com_out_type}")

    "发送按钮 pushButton_2"
    def pushButton_2_init(self):
        """一开始禁用发送按钮，只有在开始连接后才会启用
        发送内容，设置发送按钮的回调函数"""
        # self.ui.pushButton_2.setText('默认：发送')                # 设置按钮 pushButton
        self.ui.pushButton_2.setEnabled(False)                      # 禁用按键
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_connect)

    def pushButton_2_connect(self):
        """发送按钮的回调函数，每次点击发送按钮就发送
        暂时还没写串口发送的内容"""
        self.print("【him】：串口发送功能暂不可用！")
        # self.com_write()                                # 向串口发送一组信息（可能有多个）
        # self.print("【him】：向串口发送一次数据")

    "接收信息打印窗口 textBrowser_2"
    def textBrowser_2_init(self):
        """设置回调函数，自定义信号，
        同时无聊就清除了一下内容"""
        self.signals.textBrowser_2.connect(self.textBrowser_2_connect)      # 链接信号回调
        self.ui.textBrowser_2.clear()                                       # 清空内容
        
    def textBrowser_2_connect(self,string):
        """往窗口的文本末尾添加内容，而不换行，同时保持光标可见
        """
        self.ui.textBrowser_2.insertPlainText(string)       # 在光标处插入文本（这个光标可以鼠标改动的……）
        self.ui.textBrowser_2.ensureCursorVisible()         # 确保光标可见

    def com_print(self,string):
        """又打包了一层回调函数的调用，
        为了方便修改配置和缩短函数名"""
        self.signals.textBrowser_2.emit(string)             # 输出到窗口

    "开始接收数据按钮 pushButton_7"
    def pushButton_7_init(self):
        """设置按钮的文本，不用变量储存，因为可以读取按钮的文本
        """
        self.ui.pushButton_7.setText("开始接收")                        # 设置按键文本
        self.ui.pushButton_7.setEnabled(True)                           # 启用按键
        self.ui.pushButton_7.clicked.connect(self.pushButton_7_connect) # 每次按钮被按下就回调
    
    def pushButton_7_connect(self):
        """接收按钮的回调函数，直接读取按钮文本，不再另设变量存储了
        """
        if self.ui.pushButton_7.text() == "开始接收":
            self.ui.pushButton_7.setText("停止接收")                    # 改变按键文本
            self.pushButton_7_ON()                                      # 调用打包函数，运行按下开关时所需的内容
            self.print('【him】：已开始接收数据')
        else:
            self.ui.pushButton_7.setText("开始接收")                    # 改变按键文本
            self.pushButton_7_OFF()
            self.print('【him】：已停止接收数据')

    def pushButton_7_OFF(self):
        """停止 接收数据时 调用
        """
        self.ui.pushButton_2.setEnabled(False)              # 禁用 发送按钮
    
    def pushButton_7_ON(self):
        """开始 接收数据时 调用
        """
        self.Com_ON()                                       # 打开串口连接
        self.com_read_Thread_init()                         # 打开串口读取线程
        self.ui.pushButton_2.setEnabled(True)               # 启用 发送按钮

    "清空输出按钮 pushButton_3"
    def pushButton_3_init(self):
        """设置 清空输出按钮 回调函数，每次按下清空按钮就调用
        """
        # self.ui.pushButton_3.setText("清空")                          # 改变按键文本
        # self.ui.pushButton_3.setEnabled(False)                        # 不禁用按键，无论什么状态都可以清除
        self.ui.pushButton_3.clicked.connect(self.pushButton_3_connect) # 每次按钮被按下就回调

    def pushButton_3_connect(self):
        """每次调用就清空接收窗口的内容，无其他操作
        """
        self.ui.textBrowser_2.clear()                                   # 清空内容
        self.print('【him】：接收历史已清空')

    "清空输入按钮 pushButton_6"
    def pushButton_6_init(self):
        """设置 清空输入按钮 回调函数，每次按下清空按钮就调用
        """
        # self.ui.pushButton_6.setText("清空")                          # 改变按键文本
        # self.ui.pushButton_6.setEnabled(False)                        # 不禁用按键，无论什么状态都可以清除
        self.ui.pushButton_6.clicked.connect(self.pushButton_6_connect) # 每次按钮被按下就回调

    def pushButton_6_connect(self):
        """每次调用就清空输入框的内容，无其他操作
        """
        self.ui.lineEdit_7.clear()                                      # 清空内容
        self.print('【him】：发送内容已清空')

    "接收类型选择 comboBox_4"
    def comboBox_4_init(self):
        """设置接收类型的选项栏内人，链接回调函数，同时先调用一次回调函数
        """
        self.ui.comboBox_4.addItems(['hex','uint8','utf-8','binary'])               # 设置组合选择框 comboBox
        self.ui.comboBox_4.currentIndexChanged.connect(self.comboBox_4_connect)     # 每次选项被修改就回调
        self.comboBox_4_connect()           # 先回调一次，给变量赋值

    def comboBox_4_connect(self):
        """接收类型框的回调函数，用于获取选项框内容
        用作串口将接收的内容作为什么类型输出"""
        self.com_get_type = self.ui.comboBox_4.currentText()                        # 读取新选项
        self.print(f"【him】：接收类型已修改为 {self.com_get_type}")

    "图像接收按钮 pushButton_11"
    def pushButton_11_init(self):
        """设置图像接收按钮的文本，不另设变量储存这个文本，启用该按钮
        同时设置链接回调函数，每次按下都会回调"""
        self.ui.pushButton_11.setText('开始接收')
        self.ui.pushButton_11.setEnabled(True)                              # 启用按键
        self.ui.pushButton_11.clicked.connect(self.pushButton_11_connect)   # 每次按钮被按下就回调

    def pushButton_11_connect(self):
        """每次点击图像接收按钮就会切换文本信息，同时调用各自的打包方法
        """
        if self.ui.pushButton_11.text() == "开始接收":
            self.ui.pushButton_11.setText("停止接收")           # 改变按键文本
            self.pushButton_11_ON()
            self.print('【him】：已开始接收图片')
        else:
            self.ui.pushButton_11.setText("开始接收")           # 改变按键文本
            self.pushButton_11_OFF()
            self.print('【him】：已停止接收图片')

    def pushButton_11_OFF(self):
        """停止 接收数据时:启用普通数据接收按钮 和 图片播放。
        禁用图片保存按钮"""
        if self.ui.pushButton_10.text() != "保存图片":
            self.pushButton_10_connect()                        # 禁用图片保存前先检查是否要关闭
        self.ui.pushButton_10.setEnabled(False)                 # 禁用 图片保存
        self.ui.pushButton_7.setEnabled(True)                   # 启用 数据接收
        self.ui.pushButton.setEnabled(True)                     # 启用 图片播放

    def pushButton_11_ON(self):
        """开始 接收数据时:禁用普通数据接收按钮 和 图片播放。
        启用图片保存按钮"""
        self.ui.pushButton_10.setEnabled(True)                  # 启用 图片保存
        self.ui.pushButton_7.setEnabled(False)                  # 禁用 数据接收
        self.ui.pushButton.setEnabled(False)                    # 禁用 图片播放
        self.Com_ON()                                           # 打开串口连接
        self.com_img_Thread_init()                              # 打开读取图片的线程

    "图像保存按钮 pushButton_10"
    def pushButton_10_init(self):
        """设置图片保存按钮 的文本，同时设置回调函数。
        一开始还需要禁用按钮，当开始接收图片时会再启用"""
        self.ui.pushButton_10.setText('保存图片')
        self.ui.pushButton_10.setEnabled(False)                             # 禁用按键
        self.ui.pushButton_10.clicked.connect(self.pushButton_10_connect)   # 每次按钮被按下就回调
        self.pushButton_10_num_init()                                       # 初始化回调函数

    def pushButton_10_connect(self):
        """图像保存的按钮，每次按下都会改变文本。
        和 不用图片数量代表标志位了，直接用按钮文本"""
        if self.ui.pushButton_10.text() == "保存图片":
            self.pushButton_10_ON()
            self.print('【him】：开始保存接收的图片')
        else:
            self.ui.pushButton_10.setText('保存图片')
            self.pushButton_10_OFF()
            self.print('【him】：停止保存接收的图片')

    def pushButton_10_OFF(self):
        """关闭保存图片的时候调用，恢复文本内容
        """
        self.save_img_num = 0                                           # 退出图片保存时记得清除图片数目
        self.ui.pushButton_5.setEnabled(True)                           # 启用 图片地址按钮
        self.ui.lineEdit_8.setReadOnly(False)                           # 启用 图片地址编辑

    def pushButton_10_ON(self): 
        """开启保存图片的时候调用，改变按钮文本内容，
        这里不需要禁用其他按钮，因为开始接收图像的总开关已控制"""
        self.ui.pushButton_5.setEnabled(False)                          # 禁用 图片地址按钮
        self.ui.lineEdit_8.setReadOnly(True)                            # 禁止 图片地址编辑
        self.pushButton_10_num_connect(self.save_img_num)               # 改变按钮文本，显示目前已保存图片数目

    def pushButton_10_num_init(self):
        """这是一个回调函数的初始化，该回调函数是只有在处于正在保存图片时才调用
        用于改变按钮的文本，来提示目前保存了多少张图片"""
        self.save_img_num = 0                                               # 设置初始化值，在其他按钮中有用到
        self.signals.pushButton_10.connect(self.pushButton_10_num_connect)  # 链接信号回调

    def pushButton_10_num_connect(self,int_data):
        """保存图片按钮的回调函数，自定义信号，
        会传入整数参数，代表目前已经保存了几张图片"""
        self.ui.pushButton_10.setText(f'图片：{int_data}')                  # 设置显示已保存数目

    "图像播放按钮 pushButton"
    def pushButton_init(self):
        """设置图片播放按钮文本，链接回调函数
        """
        self.ui.pushButton.setText('播放图片')                          # 按钮文本
        self.ui.pushButton.clicked.connect(self.pushButton_connect)     # 每次按钮被按下就回调

    def pushButton_connect(self):
        """根据按钮的文本改变文本，同时调用相应的打包函数
        """
        if  self.ui.pushButton.text() == '播放图片':

            flag = self.read_file()                                     # 先读取文件，如果返回正确再进行其他操作
            if flag == 1:
                self.print("【him】：目录文本不存在！请检查。")
                return
            elif flag == 2: 
                self.print("【him】：目录格式不正确！请检查。")
                return
            elif flag == 3:
                self.print("【him】：目录内容对不上！请检查。")
                return
            elif flag == 0:
                self.print("【him】：目录文本正确读取。")
            else:
                self.print("【him】：读取目录文本时，程序运行错误！请不要按要求使用软件！！")
                
            self.ui.pushButton.setText('停止播放')
            self.pushButton_ON()
            self.print('【him】：开始播放图片')
        else:
            self.ui.pushButton.setText("播放图片")
            self.pushButton_OFF()
            self.print('【him】：停止播放图片')

    def pushButton_OFF(self): 
        """停止播放时，再启用地址修改框和图片地址按钮
        """
        self.ui.pushButton_5.setEnabled(True)                           # 启用 图片地址按钮
        self.ui.lineEdit_8.setReadOnly(False)                           # 启用 图片地址编辑
        self.ui.pushButton_11.setEnabled(True)                          # 启用 开始接收按钮
        # self.ui.horizontalSlider.setValue(0)                          # 停止播放就不操作进度条了

    def pushButton_ON(self):     
        """开始播放时，禁用修改图片地址按钮，防止错误
        """
        self.ui.pushButton_5.setEnabled(False)                          # 禁用 图片地址按钮
        self.ui.lineEdit_8.setReadOnly(True)                            # 禁止 图片地址编辑
        self.ui.pushButton_11.setEnabled(False)                         # 禁止 开始接收按钮
        self.read_img_timer_init()                                      # 初始化定时器，用于读取图片
        # self.ui.horizontalSlider.setValue(0)                          # 开始播放时也不操作进度条

    "图片地址按钮 pushButton_5"
    def pushButton_5_init(self):
        """设置 图片地址按钮 的回调函数，文本不设置，使用默认
        """
        # self.ui.pushButton.setText('默认')                          # 使用默认文本，在ui编辑器里修改
        self.ui.pushButton_5.clicked.connect(self.pushButton_5_connect)

    def pushButton_5_connect(self):
        """图片地址按钮 的回调函数，每次按下按钮就会调用，
        调用后会弹出窗口选择文本"""
        filePath = QFileDialog.getExistingDirectory(self.ui, "选择存储路径")
        self.ui.lineEdit_8.setText(filePath)        # 这个返回来的值是没有最后的'/'的，需要我自己加上

    "地址框 lineEdit_8"
    def lineEdit_8_init(self):
        """设置地址框的回调函数，为了分明功能，决定将检测路径写在对应的回调函数中
        另外，提示信息使用默认，需要的在ui设计中修改"""
        self.ui.lineEdit_8.textChanged.connect(self.lineEdit_8_connect)
        self.filePath_default = file_catalog_1                                  # 设置默认路径
        self.filePath = self.filePath_default                                   # 设置现在的路径

    def lineEdit_8_connect(self):
        """地址框的回调函数，每次修改地址后都会调用，不再是预想的按一次按钮才调用检测
        """
        filePath = self.ui.lineEdit_8.text()                                    # 获取路径文本

        if Path(filePath).is_dir() == False:
            self.filePath = self.filePath_default                               # 设置默认值
            self.print(f"【him】:所选路径无效，保留默认 - {self.filePath}")
        else:
            if filePath == '':
                self.filePath = self.filePath_default                           # 加上斜杆
            else:
                self.filePath = filePath + "/"                                  # 设置新的值，斜杆加多无所谓，少了就错了
            self.print(f"【him】:所选路径有效，成功修改 - {self.filePath}")

    "进度条 horizontalSlider"
    def horizontalSlider_init(self):
        """设置进度条的初始化，获取值和设置值函数如下，
        设置回调函数，本来不想设置的"""
        self.ui.horizontalSlider.setValue(0)                                    # 设置初始值
        self.signals.horizontalSlider.connect(self.horizontalSlider_connect)    # 链接信号回调
        # self.ui.horizontalSlider.value()                                      # 获取值

    def horizontalSlider_connect(self, Value):
        """设置进度条的值，这个只有在播放图片的时候会用到。
        """
        self.ui.horizontalSlider.setValue(Value)                                # 初始值

    "图片显示窗口 widget"
    def widget_init(self):
        """设置图像显示窗口的内容，已将 widget 升级为 GraphicsLayoutWidget
        """
        view = self.ui.widget.addViewBox()                              # 添加 ViewBox 模块
        view.setRange(QtCore.QRectF(0, 0, 128, 32))                     # 设置初始尺寸
        view.setAspectLocked(True)                                      # 锁定长宽比，我很需要

        self.com_inp_img = pg.ImageItem(border='w')                     # 创建 图像模块
        view.addItem(self.com_inp_img)                                  # 添加 图像模块
        self.data_inp_img = np.zeros((32,128,3), dtype = np.uint8)      # 创建 图像数组（正常图片尺寸）
        # self.com_inp_img.setImage(self.data_inp_img)                  # 添加 图像数组（在定时器里再输入，有反转处理）
        self.widget_timer_init()                                        # 启用定时器

    def widget_timer_init(self):
        """创建一个定时器，用于持续更新窗口内容的图像内容，
        只有一开始初始化一次，之后这个定时器不会停止"""
        self.widget_timer = pg.QtCore.QTimer()                          # 创建一个定时器
        self.widget_timer.timeout.connect(self.widget_timer_connect)    # 设定定时器的回调函数
        self.widget_timer.start(30)                                     # 多少ms调用一次（不会自动停止）
    
    def widget_timer_connect(self):
        """显示图像窗口的回调函数，用于显示图像，持续周期调用，不关闭。
        """            
        com_img = self.data_inp_img
        show_img = np.zeros((128,32,3), dtype = np.uint8)               # 都是 PySide2 的问题，所以在这里处理
        for x in range(128):                                            # 反转图片
            for y in range(32):
                show_img[x][y][0] = com_img[31-y][x][0]                 # 三通道叠加，显示就是白色
                show_img[x][y][1] = com_img[31-y][x][1]
                show_img[x][y][2] = com_img[31-y][x][2]
                
        self.com_inp_img.setImage(show_img)                             # 更新 图像数组

    "帮助按钮 pushButton_4"
    def pushButton_4_init(self):
        """设置帮助按钮的文本和回调函数，还有些标签的文本，全都默认
        """
        # self.ui.pushButton.setText('默认')                            # 按钮文本
        self.ui.pushButton_4.clicked.connect(self.pushButton_4_connect)     # 每次按钮被按下就回调

    def pushButton_4_connect(self):
        """帮助按钮的回调函数，弹出提示框，表示感谢
        """
        self.print("【him】:显示帮助弹窗")
        QMessageBox.information(
            self.ui,                                      # 设置弹窗的主窗口
            'him：谢谢支持',                               # 设置弹窗的标题
            '本上位机免费开源\n若有问题请联系我')           # 设置弹窗的内容

    def comboBox_5_init(self):
        """播放模式的选择，用于显示不同算法，根据情况不断增加
        """
        self.ui.comboBox_5.addItems(['模式一', '模式二','模式三', '模式四'])          # 设置组合选择框 comboBox
        self.ui.comboBox_5.currentIndexChanged.connect(self.comboBox_5_connect)     # 每次选项被修改就回调
        self.comboBox_5_connect()                                                   # 先回调一次，给变量赋值

    def comboBox_5_connect(self):
        """
        """
        self.read_img_mod = self.ui.comboBox_5.currentText()                        # 读取新选项
        self.print(f"【him】：播放图片模式已修改为 {self.read_img_mod}")


    "上面全是ui设计，下面全是串口内容 —————————————————————————————————————————————————————————————————————— "

    "检测系统的串口号"
    def get_list_ports(self):
        """串口读取的调用函数，
        检查串口列表是否改变，如果是就返回1，否者返回0"""
        flag = 0                                            # 变化的标志位
        plist = list(serial.tools.list_ports.comports())    # 获取串口号列表
        for i in range(len(plist)): 
            plist[i] = str(plist[i])                        # 提取串口号字符

        if len(plist) != len(self.com_port_e):
            flag = 1                                        # 改变标志位
        else:
            for i in range(len(plist)):                     # 比较串口号号有没有变化
                if self.com_port_e[i] != plist[i]:
                    flag = 1                                # 改变标志位
        
        if flag == 1:                                       # 串口号发送了改变
            self.com_port_e = plist                         # 保存串口号字符串

        return flag

    "串口连接 的 打开与关闭（普通数据连接和图片数据连接共用）"
    def Com_ON(self):
        """打开串口，我调用了自定义的类，在该类中，每次打开串口其实都会重新创建一个对象
        串口对象一开始就创建了，之后每次都是打开串口和关闭串口的操作,
        同时还会创建一个线程，用于死循环读取串口"""
        port = self.ui.comboBox.currentText()               # 获取文本端口号
        port = port.split(' ')[0]
        baudrate = self.ui.comboBox_2.currentText()         # 获取文本波特率
        baudrate = int(baudrate)
        timeout = self.ui.doubleSpinBox.value()             # 获取超时时间
        try:
            self.com(port, baudrate, timeout)               # 打开串口
        except:
            self.print("【him】：串口打开失败！！！请重新连接")

    def Com_OFF(self):
        """关闭串口连接，并不是立刻调用关闭，而是在读取串口中退出循环时再关闭
        """
        self.com.com.close()

    "串口数据读取 部分"
    def com_read_Thread_init(self):
        """串口读取时，所用到的线程，属于死循环读取的线程
        """
        thread = Thread(                                # 检测端口的线程
            target=self.com_read_Thread_connect,        # 线程入口
            daemon=True)                                # 设置新线程为daemon线程
        thread.start()                                  # 启动线程

    def com_read_Thread_connect(self):
        """串口读取线程的运行函数，死循环读取，根据标志位退出。
        已知问题：串口读取会有5ms的延时间隔"""
        while 1:
            if self.ui.pushButton_7.text() == "开始接收":   # 这个不像接收图片，不会一直等待帧头帧尾，所以可以读完最后一次在退出
                self.Com_OFF()
                return                                      # 如果按钮处于关闭状态就关闭串口并退出

            data = self.com.com.read(1)
            time.sleep(0.005)                               # 延时5ms，放在过快的输入把程序击崩
            
            if data:                                        # 如果有数据就为True

                if self.com_get_type == "binary":           # 二进制打印
                    data = str(f"{ord(data):b}")+' '
                elif self.com_get_type == "hex":            # 十六进制打印
                    data = str(f"{ord(data):x}")+' '
                elif self.com_get_type == "uint8":          # 十进制打印
                    data = str(f"{ord(data)}")+' '
                elif self.com_get_type == "utf-8":          # 普通字符打印
                    data = str(data)+' '                

                self.com_print(data)
                # print(data,end=" ")                         # 在运行时 都把原本的打印函数给卡没了

    "串口图片 接收 部分"
    def com_img_Thread_init(self):
        """串口读取时，所用到的线程，属于死循环读取的线程
        """
        self.com_img_Thread = Thread(                   # 检测端口的线程
            target=self.com_img_Thread_connect,         # 线程入口
            daemon=True)                                # 设置新线程为daemon线程
        self.com_img_Thread.start()                     # 启动线程

    def com_img_Thread_connect(self):
        """串口读取线程的运行函数，死循环的等待读取，
        如果是根据标志位退出,因为是死循环等待读取，如果超时了还是会引发错误。特别是选错串口的时候。但是Thread模块居然没有手动终结线程的方法……
        读取完毕后还会把日志打印到调试信息窗口"""
        while 1:
            if self.ui.pushButton_11.text() == "开始接收":    # 现在改为在按下按键时直接终结线程
                self.Com_OFF()
                return                                        # 如果按钮处于关闭状态就关闭串口并退出

            # data = self.com.Read_img()                      # 一直读取图片，读不到不会退出
            data = self.com.Read_midcourt()

            if data == 'error':                             # 接收错误了，退出
                self.pushButton_11_connect()                # 关闭图像接收按钮
                self.Com_OFF()
                self.print("【him】：图片接收错误了！！检查串口有没有按要求发送格式数据。")
                return                                      # 如果按钮处于关闭状态就关闭串口并退出

            com_img = data[0]                               # 提取出解压后的图片（三维的黑白图）
            com_bmp = data[1]                               # 坐标点都已经回归左上角
            
            show_img = self.him(com_img, com_bmp, "read_com", self.read_img_mod, self.print)    # 图片处理算法

            self.data_inp_img = show_img                    # 保存数据

            log = self.com.get_log_2(0)                       # 获取刚刚读取图片时的日志
            
            self.print(log[-1], 0)                          # 日志信息中的最后一个是全部信息的总和

            if self.ui.pushButton_10.text() != "保存图片":
                self.save_img(com_img, com_bmp, log[0])     # 保存图片文件（保存的和显示的是不一样的）

    "串口图片保存 部分"
    def save_img(self, img, bmp, time):
        """传入图片数据，把数据保存到相应的目录下，
        同时生成把信息记录到一个文本中，图片序号、读取时间、解包前的数据"""
        self.save_img_num += 1
        path = self.filePath +'/'+ str(f'{self.save_img_num}.png')      # 生成保存图片文件的路径，加一个斜杠防止错误
        imageio.imsave(path, img)                                       # 调用函数，保存图片

        self.pushButton_10_num_connect(self.save_img_num)               # 改变按钮文本，显示目前已保存图片数目
        self.print(f"【him】：已保存图片 - {path}",0)                    # 将信息打印到窗口查看

        num_data = str(f"{self.save_img_num:>4}.png")                   # 记录文件名，使用对其格式png 和 jpg，有什么不同？

        time_data = str(f"{int(time*1000):>4}")                         # 记录播放的持续时间，单位是ms

        bmp_data = ''
        for i in range(len(bmp)):
            bmp_data += str(f"{bmp[i]:#x} ")                            # 记录图像数据

        path = self.filePath + "him_data.txt"                           # 文本保存路径
        if self.save_img_num == 1:                                      # 如果是新一次的保存，就重新写入
            text_data = """【him】如此说道：该文本记录着该文件夹下的图片信息，用于读取图片显示时使用。\n\n 文件名  |   显示时间(ms)    |   纵向压缩的图像数据\n"""                                                                    
            # 需要存放的开头文本
            with open(path, 'wt') as out_file:                          # 写点标题、接收之类的
                out_file.write(text_data)

        save_data = num_data +" | "+ time_data +" | "+ bmp_data + "\n"  # 组合所有数据
        with open(path, 'a+') as out_file:                              # 如果是后续保存，就追加写入
            out_file.write(save_data)
 
    "串口图像 播放 部分"
    def read_file(self):
        """这是个一个打包函数，用来读取文件目录的，在点击播放图片时调用，如果读取失败就会终止播放
        很容易读取失败，如果文本被认为改过的话。为了避免问题，可能有必要判断错误。"""
        path = self.filePath +'/'+ "him_data.txt"                           # 文本保存路径
        if Path(path).is_file():
            pass
        else:
            return 1                                                        # 如果文件不存在就退出返回1

        with open(path, "rt") as in_file:
            text = in_file.readlines()                                      # 返回一个列表，遗憾

            text.pop(0)                                                     # 连续弹出3次，把开头的说明文件去掉
            text.pop(0)
            text.pop(0)

            self.read_text = []                                             # 用来存储文本内的所有内容，不做生成器啦！！！ 
            for i in range(len(text)):
                data = text[i].strip().split('|')                           # 标准化、切分
                if len(data) != 3:
                    return 2                                                # 如果文件内容不符合就退出

                file_name = data[0].strip()
                show_time = int(data[1].strip())
                img_data = data[2].strip().split(' ')
                for j in range(len(img_data)):  
                    img_data[j] = int(img_data[j],16)                       # 已进行字符串转换

                if len(img_data) != 128:
                    print("【him】：为什么长度不是128？？改了了什么东西吗？")

                self.read_text.append((file_name, show_time, img_data))     # 把数据全都保存在一个文件中

            examine_num = int(self.read_text[-1][0].split('.')[0])          # 读取最后一行记录的数目
            if examine_num != len(self.read_text):                          # 最后再检查一下文件内容符不符合。如果数目不对就是错的
                print(self.read_text[-1][0],len(self.read_text))
                self.read_text = []                                         # 清除内容
                return 3

        return 0                                                            # 返回正确值

    def read_img_timer_init(self):
        """读取图片文件，因为按钮都被禁用了，所以不太需要考虑太多，
        初始化一个定时器，定时时间为读取到的显示时间，
        注意调用位置，是按下按键时才调用。
        还包含了初始化"""
        self.read_img_num = 0                                               # 虽然也可以复用保存图片的变量，但是避免头脑风暴吧
        self.read_img_time = 50                                             # 定时器的时间，一开始这个值随便，之后每次都是读取文本中的值
        self.read_img_timer = pg.QtCore.QTimer()                            # 创建一个定时器
        self.read_img_timer.timeout.connect(self.read_img_timer_connect)    # 设定定时器的回调函数
        self.read_img_timer.start(self.read_img_time)                       # 多少ms调用一次（不会自动停止）

    def read_img_timer_connect(self):
        """读取图片的回调函数，一直读取图片，直到按暂停。
        内置获取和读取进度条的功能。不另设一个进度条的回调函数"""
        if self.ui.pushButton.text() == '播放图片':                         # 已经停止了播放图片
            # 理清思路：显示图片也是定时器，但是不会停止；接收图片是线程，会退出，保存图片在接收图片中；播放图片是定时器。会停止
            self.read_img_timer.stop()                                      # 退出并关闭定时器 
            self.read_img_num = 0                                           # 重置变量
            return

        self.read_img_horizontalSlider()                                    # 设置进度条进度

        path = self.filePath +'/'+ self.read_text[self.read_img_num][0]     # 读取图片的路径
        com_img = imageio.imread(path)                                      # 读取图片
        com_bmp = self.read_text[self.read_img_num][2]                      # 读取压缩图片的数组
        
        # 图片处理算法， 是要直接显示图片，还是还原压缩数据，都在这里改动
        show_img = self.him(com_img, com_bmp, "read_file", self.read_img_mod, self.print)

        self.data_inp_img = show_img                                        # 保存图片

        self.read_img_time = self.read_text[self.read_img_num][1]           # 在累加前读取显示图片的时间
        self.read_img_num += 1                                              # 累加

        if self.read_img_num >= len(self.read_text):                        # 已经显示完全部图片了
            self.read_img_timer.stop()                                      # 退出并关闭定时器 
            self.pushButton_connect()                                       # 调用一次按钮回调函数，关闭播放模式
            self.read_img_num = 0                                           # 重置变量
            self.signals.horizontalSlider.emit(0)                           # 重置进度条进度
        else:
            self.read_img_timer.start(self.read_img_time)                   # 修改显示的时间

    def read_img_horizontalSlider(self):
        """读取图片时的进度条的进度，每次显示内容前都判断一下，根据当前进度条进度来显示。
        不绞尽脑汁想那么多特殊情况了，如果除了bug再说"""
        progress_bar = int((self.read_img_num)*100/len(self.read_text))         # 计算进度条的进度
        old_progress_bar = self.ui.horizontalSlider.value()                     # 获取值

        if old_progress_bar != progress_bar: 
            self.read_img_num = int(old_progress_bar*len(self.read_text)/100)   #如果不一样就更新值
        
        progress_bar = int((self.read_img_num+1)*100/len(self.read_text))       # 重新计算
    
        self.signals.horizontalSlider.emit(progress_bar)                        # 设置进度条进度

    "串口普通数据 发送预览"
    def com_write_see(self):
        """发送数据的预览，在修改输入框的回调函数中调用
        最后返回3个字符串给回调函数出用,(binary, hex_data, utf_8)列表防止修改
        如果没有东西就会返回空字符串的元组，注意判断"""
        binary = ''                                         # 创建些局部变量
        hex_data = ''
        utf_8 = ''
        data = self.ui.lineEdit_7.text()                    # 获取 输入框 的内容
        data = data.strip()                                 # 先标准化，再切分
        
        # 其他情况就不预处理了，输入的东西千奇百怪，因为就算转换失败也不会卡死
        if self.com_out_type == 'utf-8':                    # 如果输入是字符串就再进行一个预处理
            data = list(data)                               # 将字符串拆分
            # data.remove(' ')                              # 删除列表中空的元素(如果没有空元素还会报错……)
            for i in data:                                  # 所以换个方法实现
                if i == '':                                 # 输出空元素
                    data.remove(i)
        else:
            data = data.split(' ')                          # 拆分之后就是列表了
        
        if data == ['']:                                      
            # self.ui.lineEdit.clear()                      # 如果是空就清空预览
            # self.ui.lineEdit_2.clear()
            # self.ui.lineEdit_3.clear()
            return ('')
        
        for i in range(len(data)):                          # 转换 二进制 组合
            if self.com_out_type == 'hex':
                binary += str(f"{int(data[i],16):b}")+' '   # 使用 int+16 将字符串作为 hex读取
                hex_data += data[i]+' '                     # 如果输入为 hex 直接赋值（不管大不大写了）
                utf_8 += chr(int(data[i],16))+' '
            if self.com_out_type == 'binary':
                binary += data[i]+' '                       # 如果输入为 二进制 直接赋值
                hex_data += str(f"{int(data[i],2):X}")+' '  # 使用 int+2 将字符串作为 二进制读取
                utf_8 += chr(int(data[i]))+' '
            if self.com_out_type == 'uint8':
                binary += str(f"{int(data[i]):b}")+' '      # 使用 int 将字符串作为 整数读取
                hex_data += str(f"{int(data[i]):X}")+' '    # 大写输出，
                utf_8 += chr(int(data[i]))+' '              # 使用 chr 将读取到的 hex取对应的ascii输出字符
            if self.com_out_type == 'utf-8':
                binary += str(f"{ord(data[i]):b}")+' '      # 使用 ord 返回字符串的 ascii
                hex_data += str(f"{ord(data[i]):X}")+' '    
                utf_8 += data[i]+' '                        # 如果输入为 utf-8 直接赋值

        return (binary, hex_data, utf_8)
        
    "串口普通数据 发送"
    def com_write(self):
        """串口发送内容，根据所选类型的不同，而发送不同类型的数据。
        在发送按钮中调用。有bug，好像发送不正常。暂时不管了"""
        list_data = self.com_write_see()                # 调用预览函数，直接返回要发送的内容
    
        if list_data == (""):                           # 如果为空就直接退出
            return      

        data = list_data[1]                             # 取出其中的十六进制数
        data = data.split(' ')                          # 切分列表
        data.remove('')                                 # 输出空元素

        for i in data:
            i = int(i,16)
            self.com.com.write(i)                       # 然后直接发送

if __name__ == '__main__':
    "UI + 串口 的主函数"
    app = QApplication([])
    # 加载 icon
    com_ui = Win_UI()
    com_ui.ui.show()
    app.exec_()

    if 0:
        "纯串口的主函数"
        com = Canon_com()       # 创建对象
        com.Cmd_Set_Port()      # 获取端口
        com()                   # 创建端口
        while 1:
            data = com.Read_img()   # 读取图像
            com.get_log()           # 打印日志

        # 保存文本
        np.savetxt("./Python_test/out_jpg/img.txt", data[1], fmt="%0.0f", newline=' | ')
        # 保存图片
        import imageio
        imageio.imsave('./Python_test/out_jpg/img.png', data[0])
        # 打开图片
        from PIL import Image
        img = Image.open('./Python_test/out_jpg/img.png')
        img = np.array(img)
        # 显示图片
        import matplotlib.pyplot as plt
        plt.imshow(img)
        plt.show()    

