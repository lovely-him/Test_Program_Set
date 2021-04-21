
#!/usr/bin/env python
#-*- coding: utf-8 -*

import serial   
import serial.tools.list_ports    
import numpy as np
import time

"""
重新编写串口类，包含读取与发送功能。
看得更加顺眼一点，也更加规范，如果之后要添加功能可以直接在类里添加方法。就不再从写了
"""

class Canon_com():

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
                else:
                    error_num += 20         # 如果是超时就认为是断线了，直接加20

                # print("【him】：Read_img_y - 接收列数据 - error")
                if error_num > 100:         # 读了100个数据还没？有问题
                    return 'error'

            data = list(self.read(1+4+1+1))

            if data[-1] != 0x5A:            # 判断帧尾
                continue

            if data[-2] != (data[0]&data[1]&data[2]&data[3]&data[4]):
                continue                    # 判断校验

            x_num = data.pop(0)             # 弹出列数号
            uint32 = data[0] | data[1]<<8 | data[2]<<16 | data[3]<<24

            return (x_num, uint32)          # 返回数据

    def Read_img(self):
        """读取整幅图像，固定长宽(32,128)，共返回一个元组包含2个数组，
        如果接收错误会返回一个字符串，内容是 'error' """
        self.img = np.zeros((32,128), dtype = np.uint8) # 重置图像数组
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
                self.bmp[data[0]] = data[1]
            else:
                break

        for x in range(128):            # 解压数据
            data = self.bmp[x]
            if data != 0:               # 列不为空
                self.read_y_num += 1    # 累加列数
                for y in range(32):     
                    gray = (data>>y) & 0x01
                    if gray == 1:       # 行不为空
                        self.img[31-y][x] = 255     # 计算机中的图片原点为左上角

        self.read_img_time -= time.time()   # 记录时间
        self.read_img_time = -self.read_img_time
        return (self.img, self.bmp)         # 返回图片

    def get_log(self, flag=1):
        "返回上一次接收图片的时间、列数、和有效字节数、无效字节数"
        correct_data = (2+self.read_y_num) * (1+1+4+1+1)
        error_data = self.read_u8_num - correct_data
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
            



if __name__ == '__main__':
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






