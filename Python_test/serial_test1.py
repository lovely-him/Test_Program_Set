
#!/usr/bin/env python
#-*- coding: utf-8 -*

"""
自编写模块，serial_test1.py
功能：内含类 Canon_Port ；可创建串口对象并调用对象返回串口数据。
返回：返回的串口数据已经过字符串转换，不符合字符串格式的数据会转换失败直接输出空字符。
运行：直接运行本文件可创建串口对象并循环读取，为了适应情况，这里不对读取到的数据做处理
"""
# 第一步：导入模块，若未安装则询问是否安装
import os       #如果这2个都没安装就没救了，不会吧，不会吧
import sys

try:
    # 注意，不用安装 serial ，不然程序会失效，虽然导入的模块名字是 serial。但是要安装的是 pyserial 。
    import serial   
    import serial.tools.list_ports
    # 导入画图的工具,使用 pyqtgraph 还需要安装 PyQt5
    import pyqtgraph as pg
    from pyqtgraph.Qt import QtCore, QtGui
    import numpy
except:
    print("——————————————————————————————————————")
    ch = input("【him】：程序检测到有模块没安装，请问是否需要安装；(y/n)\n")
    # 如果输入不符合要求，就退出程序
    if (ch != 'y') and (ch != 'Y'):
        sys.exit()  
    # 所有使用到的模块名称
    use_module_list=["pyserial","pyqtgraph","PyQt5","pyqtgraph","numpy"]
    # 使用终端命令安装所有模块，已安装的不会再安装
    for module in use_module_list:
        os.system(f"pip install {module}")


class Canon_Port():
    """
    功能：创建串口端口对象，可自主选择端口号
    参数：（目前只支持修改波特率和等待超时时间）
    使用：创建实例对象后，调用对象即可放回一行端口信息
    """
    def __init__(self,baudrate=115200,timeout=2):
        # 获取波特率、端口号、等待超时时间(s)
        self.port = self.Get_Port()
        self.baudrate = baudrate
        self.timeout = timeout
        try:
            # 创建端口对象实例
            self.com = serial.Serial(
                port = self.port,
                baudrate = self.baudrate,
                timeout = self.timeout)
        except:
            print("【him】：端口对象创建失败，请自检；")
            sys.exit()  #退出程序

    # 内置方法，获取需要的端口号
    def Get_Port(self):
        # 获取可用端口号
        plist = list(serial.tools.list_ports.comports())

        print("——————————————————————————————————————")
        if len(plist) == 0:
            print("【him】：无可用串口，请检查设备；")    
            sys.exit()  #退出程序
        else:
            print("【him】：检测到系统有以下可用串口端口；")
            for i in range(len(plist)):
                print(plist[i],end = f" - {i}\n") 

        print("——————————————————————————————————————")
        print("【him】：请输入你需要连接的串口:",end = '')
        while 1:
            try:
                # 读取输入字符，把输入字符转换为整形， input 函数不会自动换行
                portx = int(input())
                # 读取列表中的对象，转换成列表会是含几个字符串的列表，取第一个有的
                portx = list(plist[portx])[0]
            except:
                print("【him】：警告！你输入内容有误，请重新输入：",end = '')
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

if __name__ == '__main__':
    # 创建实例对象
    com = Canon_Port()
    # 打印内容
    try:
        while 1:
            if com():
                try:
                    data = com()
                    data = data.strip()
                    data = str(data,'utf-8')
                except:
                    data = 0
                print(data)

    except:
        print("——————————————————————————————————————")
        print("【him】：程序结束；")

