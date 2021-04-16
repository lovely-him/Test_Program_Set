


#!/usr/bin/env python
#-*- coding: utf-8 -*

"""
尝试编写读取串口图像数组
"""

import numpy as np
import serial_test1 as him


# 创建指定大小的数组，数组元素以 0 来填充：设置类型为整数
bmp_y = np.zeros((128), dtype = np.uint32) 
bmp = np.zeros((32,128), dtype = np.uint32) 
# print(bmp,bmp_y)

flay = 0
num = 0


# 创建实例对象
com = him.Canon_Port()
# 打印内容
try:
    while 1:
        if com():
            try:
                data = com()
                data = data.strip()
                data = str(data,'utf-8')
                
                print(data)

                "检测帧头帧尾"
                if data[2] is 'A':              # 检测帧头
                    flay = 1
                    bmp_y = np.zeros((128), dtype = np.uint32) 
                    #pc的图像中，第一维行，第二维才是列
                    bmp = np.zeros((128,32), dtype = np.uint32) 
                    print(data)
                    continue
                elif flay is 0:                 # 检测是否开始接收
                    continue
                elif data[5] is 'A':            # 检测帧尾
                    print(data)
                    break
                
                "提取数据"
                data = data.split(':')         # 分割字符串
                if len(data) is not 2:
                    continue

                x = int(data[0])                # 提取x坐标
                y_str = data[1]                 # 提取y坐标
                y_hex = 0
                for i in range(len(y_str)):
                    if y_str[i]:
                        y_hex |= int(y_str[i])<< ((len(y_str)-i-1)*4)


                "转换图片"
                bmp_y[x] = y_hex
                for y in range(32):
                    if (bmp_y[x] >> y) & 0x01:
                        bmp[x][31-y] = 255

                num = 0                 # 错误次数重置
            except:
                num = 1
                # print(f"【him】：串口数据错误累计次数：{num}")
except:
    print("——————————————————————————————————————")
    print("【him】：程序结束；")


print(bmp)
print(bmp_y)

import numpy as np
import pyqtgraph as pg

pg.image(bmp, title="Simplest possible image example")

pg.mkQApp().exec_()