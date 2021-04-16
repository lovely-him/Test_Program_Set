

#!/usr/bin/env python
#-*- coding: utf-8 -*

"""
尝试编写读取串口图像数组
这次写规范点
"""

import numpy as np
import time

class com_data():
    """
    读取串口的字符串，将读取的字符串集成一幅图像
    """
    def __init__(self,com, print_on = 0):
        "初始化变量"
        self.com = com                  # 串口端口对象
        # 创建图像数组，坑爹的pyqtgraph会横转显示图像
        self.img = np.zeros((32,128), dtype = np.uint8) 
        # 重置串口数据数组，设为类属性是为了能被外界读取
        self.bmp = np.zeros(128, dtype = np.uint32)
        # 是否打印调试信息
        self.print_on = print_on
        
    def __call__(self):
        "创建空数组存东西"
        self.img = np.zeros((32,128), dtype = np.uint8)     # 重置图像数组
        self.bmp = np.zeros(128, dtype = np.uint32)         # 重置串口数据数组
        keys = 0                            # 开始结束的标志位
        x_num = 0                           # 记录这一次收到了多个数据
        start_time = time.time()            # 记录程序开始运行时间

        while 1:    #持续读，直到读完一幅图像
            "刚开始调试时就不用加 try 了，找半天不知道哪里错了"
            try:
                "读取数据"
                data = self.com()           # 读取串口数据
                data = data.strip()         # 字符串标准化
                data = str(data,'utf-8')    # 字符串格式转换
                data = data.split(':')      # 切分字符串
            except:
                # 打印数据
                print(f"【him】：这一次的读取失败: {data}，开始重新读取")    

            if len(data) is not 2:      # 数据格式不符合要求，退出
                continue

            "检测帧头帧尾 （三个判断顺序不能乱）"
            if (keys is 0) and (data[0][0] is 'A'):
                keys = 1           # 检测帧头
                continue
            elif (keys is 0):
                continue                # 没检测到帧头就看到帧尾或其他东西
            elif (keys is 1) and (data[0][0] is 'Z'):  
                break                   # 检测帧尾
            
            "提取数据"
            x = int(data[0])            # 提取列号
            y_str = data[1]             # 提取整列内容
            y_hex = int(y_str,16)       # wc,原来那么简单就可以转16进制的字符串了
            
            "保存数据"
            self.bmp[x] = y_hex
            x_num += 1                  # 成功接受，保存数据
        
        "读取完毕，开始转换图片"
        for x in range(128):
            for y in range(32):
                if (self.bmp[x] >> y) & 0x01:
                    self.img[31-y][x] = 255 

        "打印调试信息"
        end_time = time.time()  # 记录程序结束运行时间
        if self.print_on == 1:
            print(f"【him】：这次共接收到{x_num}个数据，共耗时{end_time - start_time}")

        return self.img


if __name__ == "__main__":
    import serial_test1 as him
    # 创建串口对象
    com = him.Canon_Port()
    # 创建转换数据对象
    data = com_data(com)
    # 读取一幅图像
    img = data()
    # 保存数组
    np.savetxt("./Python_test/out_jpg/img.txt", data.bmp, fmt="%.0f")

    # 方法一：保存图片
    import imageio
    imageio.imsave('./Python_test/out_jpg/out.jpg', img)

    # 方法二：保存图片
    # import cv2    # 导入这个库有报错，但是能运行，强迫症
    # cv2.imwrite("./Python_test/out_jpg/out.jpg", img)

    # import pyqtgraph as pg
    # # 在线显示图像，不过这个函数显示的话是竖着显示的
    # pg.image(img, title="Simplest possible image example")
    # # 持续显示图片窗口
    # pg.mkQApp().exec_()







