
#!/usr/bin/env python
#-*- coding: utf-8 -*

# 第一步：导入模块，若未安装则询问是否安装
import os       #如果这几个都没安装就没救了，不会吧，不会吧
import sys
import time

"""
简易上位机【第一版】：接受串口数据（类型为字符串），转换为十六进制的uint32解压数据还原图片
还学会了使用以下命令可以打包成一个可执行文件（不要加F就不是一个单独的文件）
pyinstaller -F  ****.py
"""

try:
    # 注意，不用安装 serial ，不然程序会失效，虽然导入的模块名字是 serial。但是要安装的是 pyserial 。
    import serial
    import serial.tools.list_ports
    import pyqtgraph as pg
    import pyqtgraph.ptime as ptime
    from pyqtgraph.Qt import QtCore
    import numpy as np
except:
    print("——————————————————————————————————————")
    ch = input("【him】：程序检测到有模块没安装，请问是否需要安装；(y/n)\n")
    # 如果输入不符合要求，就退出程序
    if (ch != 'y') and (ch != 'Y'):
        sys.exit()
    # 所有使用到的模块名称
    # 导入画图的工具,使用 pyqtgraph 的话，还需要安装 PyQt5
    use_module_list=["pyserial","pyqtgraph","PyQt5","pyqtgraph","numpy"]
    # 使用终端命令安装所有模块，已安装的不会再安装
    for module in use_module_list:
        os.system(f"pip install {module}")
    sys.exit()  # 退出程序，要重新打开程序，防止没安装成功
    

class Canon_Port():
    """
    功能：创建串口端口对象，可自主选择端口号
    参数：（目前只支持修改波特率和等待超时时间）
    使用：创建实例对象后，调用方法call即可返回一行端口信息
    """
    def __init__(self, baudrate=115200, timeout=2):
        # 获取波特率、端口号、等待超时时间(s)
        self.port = self.Get_Port()
        self.baudrate = baudrate
        self.timeout = timeout
        try:
            # 创建端口对象实例
            self.com = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout)
        except:
            print("【him】：端口对象创建失败，请自检；")
            sys.exit()  # 退出程序

    # 内置方法，获取需要的端口号
    def Get_Port(self):
        # 获取可用端口号
        plist = list(serial.tools.list_ports.comports())

        print("——————————————————————————————————————")
        if len(plist) == 0:
            print("【him】：无可用串口，请检查设备；")
            sys.exit()  # 退出程序
        else:
            print("【him】：检测到系统有以下可用串口端口；")
            for i in range(len(plist)):
                print(plist[i], end=f" - {i}\n")

        print("——————————————————————————————————————")
        print("【him】：请输入你需要连接的串口:", end='')
        while 1:
            try:
                # 读取输入字符，把输入字符转换为整形， input 函数不会自动换行
                portx = int(input())
                # 读取列表中的对象，转换成列表会是含几个字符串的列表，取第一个有的
                portx = list(plist[portx])[0]
            except:
                print("【him】：警告！你输入内容有误，请重新输入：", end='')
            else:
                print("【him】：你选择的串口为 " + portx + " ;")
                break
        # 成功选择了端口，并返回
        return portx

    # 获取串口的一行信息（以回车结束）
    def __call__(self):
        try:
            # 获取串口信号，如果超时则返回空
            data = self.com.readline()
            # 返回字符串的标准化
            # data = data.strip()
            # 转换为标准字符
            # data = str(data,'utf-8')
            # 为了适应情况，这里不对数据做处理
        except:
            # 读取转换失败就返回空
            data = ''

        return data

class Com_Data():
    """
    功能：读取串口的字符串，将读取的字符串集成一幅图像
    参数：必须传入串口端口的对象，用于获取数据，还可设置是否打印调试
    使用：创建实例对象后使用对象call方法，可持续读取串口数据，直到完整的图片读取完毕
    """

    def __init__(self, com, print_on=0):
        "初始化变量"
        self.com = com  # 串口端口对象
        # 创建图像数组，坑爹的pyqtgraph会横转显示图像
        self.img = np.zeros((32, 128), dtype=np.uint8)
        # 重置串口数据数组，设为类属性是为了能被外界读取
        self.bmp = np.zeros(128, dtype=np.uint32)
        # 是否打印调试信息
        self.print_on = print_on

    def __call__(self):
        "创建空数组存东西"
        self.img = np.zeros((32, 128), dtype=np.uint8)  # 重置图像数组
        self.bmp = np.zeros(128, dtype=np.uint32)  # 重置串口数据数组
        keys = 0  # 开始结束的标志位
        x_num = 0  # 记录这一次收到了多个数据
        start_time = time.time()  # 记录程序开始运行时间

        while 1:  # 持续读，直到读完一幅图像
            "刚开始调试时就不用加 try 了，找半天不知道哪里错了"
            try:
                "读取数据"
                data = self.com()  # 读取串口数据
                data = data.strip()  # 字符串标准化
                data = str(data, 'utf-8')  # 字符串格式转换
                data = data.split(':')  # 切分字符串
            except:
                # 打印数据
                print(f"【him】：这一次的读取失败: {data}，开始重新读取")

            if len(data) is not 2:  # 数据格式不符合要求，退出
                continue

            "检测帧头帧尾 （三个判断顺序不能乱）"
            if (keys is 0) and (data[0][0] is 'A'):
                keys = 1  # 检测帧头
                continue
            elif (keys is 0):
                continue  # 没检测到帧头就看到帧尾或其他东西
            elif (keys is 1) and (data[0][0] is 'Z'):
                break  # 检测帧尾

            "提取数据"
            x = int(data[0])  # 提取列号
            y_str = data[1]  # 提取整列内容
            y_hex = int(y_str, 16)  # wc,原来那么简单就可以转16进制的字符串了

            "保存数据"
            self.bmp[x] = y_hex
            x_num += 1  # 成功接受，保存数据

        "读取完毕，开始转换图片"
        for x in range(128):
            for y in range(32):
                if (self.bmp[x] >> y) & 0x01:
                    self.img[31 - y][x] = 255

        "打印调试信息"
        end_time = time.time()  # 记录程序结束运行时间
        if self.print_on == 1:
            print(f"【him】：这次共接收到{x_num}个数据，共耗时{end_time - start_time}")

        return self.img

class Open_Win():
    """
    功能：创建显示图片的窗口，并打开，如果传入读取图片的对象，还可以实时显示
    参数：可以传入起始的第一张图片，如果不实时显示动态图就变成了普通的显示一张图片
    使用：创建对象实例后，调用set_com_data方法设置读取数据的对象，然后调用call开启窗口
    """

    def __init__(self,
                 data=[],
                 Title="默认名字",
                 win_w=1280,
                 win_h=640,
                 view_w=128,
                 view_h=32,
                 view_Locked=0,
                 print_on=0):
        "创建对象"
        self.app = pg.mkQApp()  # 建立app
        self.win = pg.GraphicsLayoutWidget()  # 创建窗口
        self.img = pg.ImageItem(border='w')  # 创建图像项目
        self.view = self.win.addViewBox()  # 添加插件
        self.view.addItem(self.img)  # 记载图片插件

        "设置属性"
        self.win.resize(win_w, win_h)  # 设定窗口大小
        self.win.setWindowTitle(Title)  # 设定窗口标题
        self.view.setRange(QtCore.QRectF(0, 0, view_w, view_h))  # 设置初始视图边界
        if view_Locked == 1:
            self.view.setAspectLocked(True)  # 锁定窗口长宽比

        if data != []:  # 非空就赋值
            if data.shape != (32, 128):  # 检查数组维度
                print("【him】：data 数组形状错误，请检查")
                sys.exit()  # 退出程序
            self.data = data  # 初始图片数据
        else:  # 创建存图片的空数组
            self.data = np.zeros((32, 128), dtype=np.uint8)

        "设置默认参数"
        self.com_on = 0  # 起始默认为0，还未给数据添加对象
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
            self.data = self.com_data()  # 获取图片数据

        # 坑爹的库，为什么显示时倒着的，我要自己装置矩阵
        data_t = np.zeros((128, 32), dtype=np.uint8)
        for x in range(128):
            for y in range(32):
                data_t[x][y] = self.data[31 - y][x]

        self.img.setImage(data_t)

        "还不知道为什么一定要有这个计算时间的程序才能连环显示"
        self.timer.start(1)
        self.now = ptime.time()
        fps2 = 1.0 / (self.now - self.updateTime)
        self.updateTime = self.now
        self.fps = self.fps * 0.9 + fps2 * 0.1

        "是否打印调试信息"
        if self.print_on == 1:
            print(f"{self.fps} fps")

    def __call__(self):
        "开始运行"
        self.win.show()  # 打开窗口，看来最后再打开也可以
        self.timer = QtCore.QTimer()  # 返回定时器对象
        # 由于PyQt的持久性而不使用QTimer.singleShot()。see PR #1605
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.__up_data)
        self.__up_data()
        self.app.exec_()

if __name__ == "__main__":  # 居然不可以用 is代替 ==
    # 创建串口对象
    com = Canon_Port()
    # 创建读取并转换数据的对象
    data = Com_Data(com, print_on = 1)
    # 创建显示窗口
    win = Open_Win(print_on = 1)
    # 设置读取数据的对象
    win.set_com_data(data)
    # 启动窗口显示
    win()