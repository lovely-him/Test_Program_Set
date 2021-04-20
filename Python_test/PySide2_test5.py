
from serial_test4 import Canon_com

import os
import time
import sys

try:
    # 注意，不用安装 serial ，不然程序会失效，虽然导入的模块名字是 serial。但是要安装的是 pyserial 。

    import PySide2
    dirname = os.path.dirname(PySide2.__file__)
    plugin_path = os.path.join(dirname, 'plugins', 'platforms')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtWidgets import QApplication
    import pyqtgraph as pg
    import numpy as np
    from threading import Thread
    import imageio
    
    from PySide2.QtWidgets import QFileDialog

except:
    print("——————————————————————————————————————")
    ch = input("【him】：程序检测到有模块没安装，请问是否需要安装；(y/n)\n")
    # 如果输入不符合要求，就退出程序
    if (ch != 'y') and (ch != 'Y'):
        sys.exit()
    # 所有使用到的模块名称
    # 导入画图的工具,使用 pyqtgraph 的话，还需要安装 PyQt5
    use_module_list=["pyserial","pyqtgraph","PyQt5","PySide2","numpy","imageio"]
    # 使用终端命令安装所有模块，已安装的不会再安装
    for module in use_module_list:
        os.system(f"pip install {module}")
    sys.exit()  # 退出程序，要重新打开程序，防止没安装成功


from PySide2.QtCore import Signal,QObject
class My_Signals(QObject):
    comboBox = Signal(int)
    textBrowser_3 = Signal(str)
    textBrowser_2 = Signal(str)


class Win_UI():
    "说明：统合整个上位机的界面窗口"
    def __init__(self):
        # 添加第三方模块
        loader = QUiLoader()
        loader.registerCustomWidget(pg.GraphicsLayoutWidget)
        # 从文件中加载UI定义
        self.ui = QUiLoader().load('./Python_test/ui/untitled_4.ui')
        # 从自定义类中加载信号类型，用于多线程的通讯
        self.signals = My_Signals()
        
        self.groupBox_init()            # 基本界面初始化
        self.tabWidget_init()
        self.com = Canon_com()          # 创建串口对象
        self.textBrowser_3_init()       # 基本线程、回调初始化
        self.comboBox_init()     
        self.pushButton_init()
        self.comboBox_3_init()
        self.lineEdit_7_init()
        self.pushButton_7_init()
        self.pushButton_3_init()
        self.textBrowser_2_init()
        self.buttonGroup_init()
        self.pushButton_11_init()
        self.pushButton_10_init()
        self.pushButton_5_init()
    

    "界面初始化 部分"
    def groupBox_init(self):
        "界面初始化 串口设置 部分"
        # self.ui.label.setText("默认：串口")           # 设置标签 label
        # self.ui.label_2.setText("默认：波特率")
        # self.ui.label_3.setText("默认：超时时间")
        # self.ui.label_4.setText("默认：v0.0.1")
        self.com_port_e = ['']                          # 设置组合选择框 comboBox
        self.ui.comboBox.addItems(self.com_port_e)
        self.com_baudrate_e = ['115200','9600']
        self.ui.comboBox_2.addItems(self.com_baudrate_e)
        self.com_timeout = 2                            # 设置数字输入框 doubleSpinBox
        self.ui.doubleSpinBox.setValue(self.com_timeout)
        self.com_state = '连接'                         # 设置按钮 pushButton
        self.ui.pushButton.setText(self.com_state)
        
        "界面初始化 发送预览 部分"
        # self.ui.label_5.setText("默认：binary")       # 设置标签 label
        # self.ui.label_6.setText("默认：hex")
        # self.ui.label_9.setText("默认：utf-8")
        # self.ui.lineEdit.setPlaceholderText('默认：预览二进制')   # 设置单行文本框 lineEdit
        # self.ui.lineEdit_2.setPlaceholderText('默认：预览十六进制')
        # self.ui.lineEdit_3.setPlaceholderText('默认：预览字符串')
        self.ui.lineEdit.setReadOnly(True)                          # 禁止编辑
        self.ui.lineEdit_2.setReadOnly(True)
        self.ui.lineEdit_3.setReadOnly(True)
        # self.preview_binary = ''                                  # 创建存储预览输出的字符串
        # self.preview_hex = ''                                     # 好像不用变量存也可以
        # self.preview_utf8 = ''

        "界面初始化 发送设置 部分"
        self.com_out_type = ''                                      # 设置组合选择框 comboBox
        self.ui.comboBox_3.addItems(['hex','uint8','utf-8'])
        # self.ui.lineEdit_7.setPlaceholderText('默认：lovely_him') # 设置单行文本框 lineEdit
        # self.ui.pushButton_2.setText('默认：发送')                # 设置按钮 pushButton
        self.ui.pushButton_2.setEnabled(False)                      # 禁用按键

    def tabWidget_init(self):
        "界面初始化 串口接收 部分"
        self.com_inp_type = 'utf-8'                                 # 设置单选按钮 radioButton
        # self.ui.radioButton_4.setText("默认：binary")         
        # self.ui.radioButton_2.setText("默认：hex")
        # self.ui.radioButton.setText("默认：uint8")
        # self.ui.radioButton_3.setText("默认：utf-8")
        # self.ui.pushButton_3.setText('默认：清空')                # 设置按钮 pushButton
        # self.ui.pushButton_7.setText('开始接收')
        self.get_data_state = "开始接收"                            # 存储状态


        "界面初始化 可视化 部分"
        # 已将 widget 升级为 GraphicsLayoutWidget
        view = self.ui.widget.addViewBox()                          # 添加 ViewBox 模块
        self.com_inp_img = pg.ImageItem(border='w')                 # 创建 图像模块
        view.addItem(self.com_inp_img)                              # 添加 图像模块
        self.data_inp_img = np.zeros((128,32), dtype = np.uint8)    # 创建 图像数组
        self.com_inp_img.setImage(self.data_inp_img)                # 添加 图像数组

        self.save_img_state = '保存图片'                            # 设置按钮 pushButton
        self.get_img_state = '开始接收'
        self.ui.pushButton_10.setText(self.save_img_state)
        self.ui.pushButton_11.setText(self.get_img_state)
        # self.ui.pushButton_9.setText("默认：删除图片")
        # self.ui.pushButton_5.setText("默认：保存地址")
        # self.ui.lineEdit_8.setPlaceholderText("默认")             # 设置单行文本框 lineEdit

        "界面初始化 图像分析 部分"
        view = self.ui.widget_2.addViewBox()                        # 添加 ViewBox 模块
        self.com_out_img_A = pg.ImageItem(border='w')               # 创建 图像模块
        view.addItem(self.com_out_img_A)                            # 添加 图像模块
        self.data_inp_img_A = np.zeros((128,32), dtype = np.uint8)  # 创建 图像数组
        self.com_out_img_A.setImage(self.data_inp_img_A)            # 添加 图像数组
        
        view = self.ui.widget_3.addViewBox()                        # 添加 ViewBox 模块
        self.com_out_img_B = pg.ImageItem(border='w')               # 创建 图像模块
        view.addItem(self.com_out_img_B)                            # 添加 图像模块
        self.data_inp_img_B = np.zeros((128,32), dtype = np.uint8)  # 创建 图像数组
        self.com_out_img_B.setImage(self.data_inp_img_B)            # 添加 图像数组

        self.ui.progressBar.setRange(0,100)                         # 设置 进度条 progressBar
        self.ui.progressBar.setValue(0)                             # 设置 100份进度，当前为进度0
        # self.ui.pushButton_6.setText("默认：开始")                # 设置按钮 pushButton
        # self.ui.pushButton_8.setText("默认：待定")

        "界面初始化 帮助说明 部分"
        # self.ui.label_10.setText("默认：待定")                    # 设置标签 label
        # self.ui.label_11.setText("默认：待定")
        # self.ui.pushButton_4.setText("默认：待定")                # 设置按钮 pushButton

    "状态窗口打印 部分"
    def textBrowser_3_init(self):
        "部件 textBrowser_3 文本浏览框-调试信息打印 的初始化 链接信号回调函数"
        self.signals.textBrowser_3.connect(self.textBrowser_3_connect)  # 链接信号回调
        
    def textBrowser_3_connect(self,string):
        "部件 textBrowser_3 的回调 改变 用于输出运行信息"
        self.ui.textBrowser_3.append(string)                    # 在末尾添加文本
        self.ui.textBrowser_3.ensureCursorVisible()             # 确保光标可见

    def print(self,string):
        "内置打包方法 缩短函数名 用与向 textBrowser_3 发送信号"
        localtime = time.asctime( time.localtime(time.time()))  # 获取格式化的时间
        localtime = localtime.split(' ')[3]
        string = localtime + ' - ' + string                     # 字符串拼接
        self.signals.textBrowser_3.emit(string)                 # 输出到窗口

    "串口号检测 部分"
    def comboBox_init(self):
        "部件 comboBox 组合选择框-串口号ID 的初始化 链接信号回调函数、创建线程"
        self.signals.comboBox.connect(self.comboBox_connect)        # 每次串口号被改变就回调
        thread = Thread(                                            # 检测端口的线程
            target=self.comboBox_thread,                # 线程入口
            daemon=True)                                # 设置新线程为daemon线程
        thread.start()                                  # 启动线程

    def comboBox_thread(self):
        "部件 comboBox 的线程 持续读取串口号"
        while 1:
            flag = 0                                    # 变化的标志位
            plist = self.com.Get_Port()                 # 获取串口号列表
            for i in range(len(plist)): 
                plist[i] = str(plist[i])                # 提取串口号字符

            if len(plist) != len(self.com_port_e):
                flag = 1                                # 改变标志位
            else:
                for i in range(len(plist)):             # 比较串口号号有没有变化
                    if self.com_port_e[i] != plist[i]:
                        flag = 1                        # 改变标志位
            
            if flag == 1:                               # 串口号发送了改变
                self.com_port_e = plist                 # 保存串口号字符串
                self.signals.comboBox.emit(1)           # 发送信号

    def comboBox_connect(self, int):
        "部件 comboBox 的回调 改变 串口号内容"
        if int != 1:
            self.print("comboBox_connect 接收有问题")
            return
        self.ui.comboBox.clear()                       # 清空所有选项，再重新显示
        self.ui.comboBox.addItems(self.com_port_e)
        self.print('【him】：检测到端口已变化')         # 向窗口打印信息

    "串口连接按钮 部分"
    def pushButton_init(self):
        "部件 pushButton 按钮-连接 的初始化 链接信号回调函数"
        self.ui.pushButton.clicked.connect(self.pushButton_connect) # 每次按钮被按下就回调

    def pushButton_connect(self):
        "部件 pushButton 的回调 改变 按钮状态"
        if self.com_state == '连接':                        # 改变按键状态
            self.com_init()                                 # 打开串口 
            self.com_state = '关闭'
            self.ui.pushButton.setText(self.com_state)      # 改变按键文本
            self.print('【him】：串口已打开')
            self.ui.pushButton_2.setEnabled(True)           # 启用按键
            # self.ui.pushButton_11.setEnabled(True)          # 启用按键 这个已经写了防止措施了，就懒得禁用了
            # self.ui.pushButton_7.setEnabled(True)           # 启用按键
        else:

            if self.get_img_state == "停止接收":            # 要在 self.com_state 改变之前判断
                self.pushButton_11_connect()                # 回调一次按钮，把图片接收的开关关闭
                self.print("【him】：已自动关闭串口接收图片") 
            elif self.get_data_state == "停止接收":
                self.pushButton_7_connect()
                self.print("【him】：已自动关闭串口接收数据")

            self.com_state = '连接'                         # 改变按键状态
            self.com.com.close()                            # 关闭串口
            self.ui.pushButton.setText(self.com_state)
            self.print('【him】：串口已关闭')
            self.ui.pushButton_2.setEnabled(False)          # 禁用按键

    "创建串口 部分"
    def com_init(self):
        "获取设置 打开串口 被 按钮-连接 调用"
        # self.com = Canon_com()          # 创建串口对象，在创建对象时就创建了
        port = self.ui.comboBox.currentText()               # 获取文本端口号
        port = port.split(' ')[0]
        baudrate = self.ui.comboBox_2.currentText()         # 获取文本波特率
        baudrate = int(baudrate)
        timeout = self.ui.doubleSpinBox.value()             # 获取超时时间
        self.com(port, baudrate, timeout)                   # 打开串口

    def com_read(self):
        pass

    "串口预览 部分"
    def comboBox_3_init(self):
        "部件 comboBox_3 组合选择框-'hex/uint8/utf-8' 的初始化 链接信号回调函数"
        self.ui.comboBox_3.currentIndexChanged.connect(self.comboBox_3_connect) # 每次选项被修改就回调
        self.comboBox_3_connect()           # 先回调一次，给变量赋值

    def comboBox_3_connect(self):
        "部件 lineEdit_7 的回调 每次选项被修改就回调 储存被修改的值"
        self.com_out_type = self.ui.comboBox_3.currentText()    # ['hex','utf-8','uint8']
        self.lineEdit_7_connect()                               # 每次修改都会重新回调，修改预览
        self.print("【him】：输出类型被修改")

    def lineEdit_7_init(self):
        "部件 lineEdit_7 的初始化 链接信号回调函数"
        self.ui.lineEdit_7.textChanged.connect(self.lineEdit_7_connect) # 每次文本被修改就回调

    def lineEdit_7_connect(self):
        "部件 lineEdit_7 的回调 根据输入改变预览"
        binary = ''                                         # 创建些局部变量
        hex_data = ''
        utf_8 = ''
        data = self.ui.lineEdit_7.text()                    # 获取 输入框 的内容
        data = data.strip()                                 # 先标准化，再切分
        
        if self.com_out_type == 'utf-8':                    # 如果输入是字符串就再进行一个预处理
            data = list(data)                               # 将字符串拆分
            # data.remove(' ')                              # 删除列表中空的元素(如果没有空元素还会报错……)
            for i in data:                                  # 所以换个方法实现
                if i == '':
                    data.remove(i)
                elif i == ' ':
                    data.remove(i)
        else:
            data = data.split(' ')                          # 拆分之后就是列表了
        
        if data == ['']:                                      
            self.ui.lineEdit.clear()                        # 如果是空就清空预览
            self.ui.lineEdit_2.clear()
            self.ui.lineEdit_3.clear()
            return          
        
        for i in range(len(data)):                          # 转换 二进制 组合
            if self.com_out_type == 'hex':
                binary += str(f"{int(data[i],16):b}")+' '   # 使用 int+16 将字符串作为 hex读取
                hex_data += data[i]+' '                     # 如果输入为 hex 直接赋值
                utf_8 += chr(int(data[i],16))+' '
            if self.com_out_type == 'uint8':
                binary += str(f"{int(data[i]):b}")+' '      # 使用 int 将字符串作为 整数读取
                hex_data += str(f"{int(data[i]):x}")+' '
                utf_8 += chr(int(data[i]))+' '              # 使用 chr 将读取到的 hex取对应的ascii输出字符
            if self.com_out_type == 'utf-8':
                binary += str(f"{ord(data[i]):b}")+' '      # 使用 ord 返回字符串的 ascii
                hex_data += str(f"{ord(data[i]):x}")+' '    
                utf_8 += data[i]+' '                        # 如果输入为 utf-8 直接赋值

        self.ui.lineEdit.setText(binary)                # 设置文本框显示预览
        self.ui.lineEdit_2.setText(hex_data)
        self.ui.lineEdit_3.setText(utf_8)

    "串口接收按钮 部分"
    def pushButton_7_init(self):
        "部件 pushButton_7 按钮-开始接收 的初始化 链接信号回调函数"
        self.ui.pushButton_7.clicked.connect(self.pushButton_7_connect) # 每次按钮被按下就回调

    def pushButton_7_connect(self):
        "部件 lineEdit_7 的回调 切换接收和断开的状态"
        if self.com_state == '连接':
            self.print("【him】：请先打开串口")                 # 在接收前要打开串口
            return
            
        if self.get_img_state == "停止接收":
            self.pushButton_11_connect()                        # 回调一次按钮，把图片接收的开关关闭
            self.print("【him】：已自动关闭串口接收图片")        # 在接收前要打开串口

        if self.get_data_state == "开始接收":
            self.get_data_state = "停止接收"
            self.ui.pushButton_7.setText(self.get_data_state)   # 改变按键文本
            self.pushButton_7_thread_init()                     # 打开持续接收线程
            self.textBrowser_2_timer_init()                     # 打开周期打印输出的定时器
            self.print('【him】：串口已开始接收')
        else:
            self.get_data_state = "开始接收"
            self.ui.pushButton_7.setText(self.get_data_state)   # 改变按键文本
            self.textBrowser_2_timer.stop()                     # 关闭周期定时器
            self.print('【him】：串口已停止接收')

    def pushButton_7_thread_init(self):
        "部件 pushButton_7 按钮-开始接收 的初始化 线程，每次按下开始接收按键就会调用"
        thread = Thread(                                            # 检测端口的线程
            target=self.pushButton_7_thread,            # 线程入口
            daemon=True)                                # 设置新线程为daemon线程
        thread.start()                                  # 启动线程
        self.get_com_data = 0                           # 存储串口接收的内容

    def pushButton_7_thread(self):
        "线程 pushButton_7 按钮-开始接收 用于死循环读取串口"
        while self.get_data_state == "停止接收":
            data = self.com.com.read(1)                 # 程序读取一个字节
            self.get_com_data = data                    # 这里不判断是否空，在使用时再判断，相当于用作标志了

    "打印窗口 清空按钮 部分"
    def pushButton_3_init(self):
        "部件 pushButton_3 按钮-清空 的初始化 链接信号回调函数"
        self.ui.pushButton_3.clicked.connect(self.pushButton_3_connect) # 每次按钮被按下就回调

    def pushButton_3_connect(self):
        "部件 pushButton_3 的回调 用于清空 串口接收 窗口"
        self.ui.textBrowser_2.clear()                                   # 清空
        self.print('【him】：串口接收历史已清空')

    "串口接收窗口 打印 部分"
    def textBrowser_2_init(self):
        "部件 textBrowser_2 文本浏览框-串口接收信息打印 的初始化 链接信号回调函数"
        self.signals.textBrowser_2.connect(self.textBrowser_2_connect)      # 链接信号回调
        
    def textBrowser_2_connect(self,string):
        "部件 textBrowser_2 的回调 改变 用于输出 串口接收 窗口"
        self.ui.textBrowser_2.insertPlainText(string)       # 在光标处插入文本（这个光标可以鼠标改动的……）
        self.ui.textBrowser_2.ensureCursorVisible()       # 确保光标可见
        
    def textBrowser_2_timer_init(self):
        "初始化 textBrowser_2 定时器 用于循环定时循环显示，不加定时会卡死，打开后记得关闭"
        self.textBrowser_2_timer = pg.QtCore.QTimer()                           # 创建一个定时器
        self.textBrowser_2_timer.timeout.connect(self.textBrowser_2_timer_main) # 设定定时器的回调函数
        self.textBrowser_2_timer.start(10)                                      # 多少ms调用一次（不会自动停止）

    def textBrowser_2_timer_main(self):
        "定时器 textBrowser_2 的回调函数 用于输出 串口接收窗口"
        if self.get_com_data:       # 不可以使用（data != ''）如果不能转换为有效字符也是空字符

            if self.com_inp_type == "binary":                   # 二进制打印
                data = str(f"{ord(self.get_com_data):b}")+' '
            elif self.com_inp_type == "hex":                    # 十六进制打印
                data = str(f"{ord(self.get_com_data):x}")+' '
            elif self.com_inp_type == "uint8":                  # 十进制打印
                data = str(f"{ord(self.get_com_data)}")+' '
            elif self.com_inp_type == "utf-8":                  # 普通字符打印
                data = str(self.get_com_data)+' '

            self.signals.textBrowser_2.emit(data)               # 输出到窗口

    "串口接收窗口 打印类型选择 部分"
    def buttonGroup_init(self):
        "部件 buttonGroup 按钮组-打印类型选择 的初始化 链接信号回调函数"
        self.ui.buttonGroup.buttonClicked.connect(self.buttonGroup_connect)

    def buttonGroup_connect(self):
        "部件 buttonGroup 按钮组-打印类型选择 的回调函数 用于读取所选按钮"
        buttongroup = self.ui.buttonGroup.checkedButton()
        self.com_inp_type = buttongroup.text()

    "图像接收按钮 部分"
    def pushButton_11_init(self):
        "部件 pushButton_11 按钮-开始接收 的初始化 链接信号回调函数"
        self.ui.pushButton_11.clicked.connect(self.pushButton_11_connect) # 每次按钮被按下就回调

    def pushButton_11_connect(self):
        "部件 pushButton_11 的回调 切换接收和断开的状态"
        if self.com_state == '连接':
            self.print("【him】：请先打开串口")
            return

        if self.get_data_state == "停止接收":
            self.pushButton_7_connect()                         # 回调一次按钮，把串口接收的开关关闭
            self.print("【him】：已自动关闭串口接收数据")        # 在接收前要打开串口

        if self.get_img_state == "开始接收":
            self.get_img_state = "停止接收"
            self.ui.pushButton_11.setText(self.get_img_state)   # 改变按键文本
            self.pushButton_11_thread_init()                    # 打开持续接收线程
            self.widget_timer_init()                            # 打开周期打印输出的定时器
            self.print('【him】：串口已开始接收')
        else:
            self.get_img_state = "开始接收"
            self.ui.pushButton_11.setText(self.get_img_state)   # 改变按键文本
            self.widget_timer.stop()                            # 强行中断好像会引发线程的读取图片错误，应该不影响就算了
            self.print('【him】：串口已停止接收')

    def pushButton_11_thread_init(self):
        "部件 pushButton_11 按钮-开始接收 的初始化 线程，每次按下开始接收按键就会调用"
        self.get_img_data = np.zeros((32,128), dtype = np.uint8)    # 重置图像数组
        thread = Thread(                                # 检测端口的线程
            target=self.pushButton_11_thread,           # 线程入口
            daemon=True)                                # 设置新线程为daemon线程
        thread.start()                                  # 启动线程

    def pushButton_11_thread(self):
        "线程 pushButton_11 按钮-开始接收 用于死循环读取图像"
        while self.get_img_state == "停止接收":
            data = self.com.Read_img()                          # 调用类方法读取图片
            self.get_img_data = data[0]
            
            string = self.com.get_log(0)[-1]+"\n"               # 读取完图片就取出日志
            self.signals.textBrowser_2.emit(string)             # 输出到窗口

            if self.save_img_state == "停止保存":
                self.save_img_num += 1
                path = str(f'./Python_test/out_jpg/{self.save_img_num}.jpg')
                imageio.imsave(path, self.get_img_data)
                
    "图像显示 view 部分"
    def widget_timer_init(self):
        "初始化 widget 定时器 用于循环定时循环显示 更新数据"
        self.widget_timer = pg.QtCore.QTimer()                          # 创建一个定时器
        self.widget_timer.timeout.connect(self.widget_timer_main)       # 设定定时器的回调函数
        self.widget_timer.start(50)                                     # 多少ms调用一次（不会自动停止）

    def widget_timer_main(self):
        "定时器 textBrowser_2 的回调函数 用于输出 串口接收窗口"
        # 坑爹的库，为什么显示时倒着的，我要自己装置矩阵
        data_t = np.zeros((128,32), dtype = np.uint8) 
        for x in range(128):                                            # 反转图片
            for y in range(32):
                data_t[x][y] = self.get_img_data[31-y][x]

        self.data_inp_img = data_t                                      # 保持图片
        self.com_inp_img.setImage(self.data_inp_img)                    # 更新 图像数组

    "图像保存 view 部分"
    def pushButton_10_init(self):
        "部件 pushButton_10 按钮-保存图片 的初始化 链接信号回调函数"
        self.ui.pushButton_10.clicked.connect(self.pushButton_10_connect)
        self.save_img_num = 0                                           # 设置保存图片的序号

    def pushButton_10_connect(self):
        "部件 pushButton_10 的回调 切换是否保存图片的标志位"
        if self.save_img_state == "保存图片":
            self.save_img_state = "停止保存"
            self.ui.pushButton_10.setText(self.save_img_state)
            self.print("【him】：已打开图片保存")            
            self.ui.pushButton_2.setEnabled(False)                      # 禁用按键,还是禁用启用比较方便
            self.ui.pushButton_11.setEnabled(False)
            self.ui.pushButton.setEnabled(False)
            self.ui.pushButton_7.setEnabled(False)
        else:
            self.save_img_num = 0                                       # 重置变量
            self.save_img_state = "保存图片"
            self.ui.pushButton_10.setText(self.save_img_state)
            self.print("【him】：已关闭图片保存")
            self.ui.pushButton_2.setEnabled(True)                       # 启用按键,还是禁用启用比较方便
            self.ui.pushButton_11.setEnabled(True)
            self.ui.pushButton.setEnabled(True)
            self.ui.pushButton_7.setEnabled(True)

    "图像保存 路径 部分"
    def pushButton_5_init(self):
        "部件 pushButton_5 按钮-保存地址 的初始化 链接信号回调函数"
        self.ui.pushButton_5.clicked.connect(self.pushButton_5_connect)
    
    def pushButton_5_connect(self):
        "部件 pushButton_5 按钮-保存地址 的回调函数 用于读取路径"
        filePath = QFileDialog.getExistingDirectory(self.ui, "选择存储路径")
        self.ui.lineEdit_8.setText(filePath)    
        print(filePath)



if __name__ == '__main__':
    app = QApplication([])
    com_ui = Win_UI()
    com_ui.ui.show()
    app.exec_()