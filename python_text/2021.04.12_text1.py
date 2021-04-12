
#!/usr/bin/env python
#-*- coding: utf-8 -*
import sys
import serial
import serial.tools.list_ports
# 注意，不用安装 serial ，不然程序会失效，
# 虽然导入的模块名字是 serial。但是要安装的是 pyserial。

plist = list(serial.tools.list_ports.comports())


print("——————————————————————————————————————")
if len(plist) == 0:
    print("【him】：无可用串口，请检查设备；")
    sys.exit()  #退出程序
else:
    print("【him】：有以下可用串口；")
    for plist_n in range(len(plist)):
        print(plist[plist_n],end = f" - {plist_n}\n")

print("——————————————————————————————————————")
print("【him】：请输入你需要连接的串口:",end = '')

while 1:
    try:
        portx = int(input())
        portx = list(plist[portx])[0]
    except:
        print("【him】：警告！你输入内容有误，请重新输入；",end = '')
    else:
        print("【him】：你选择的串口为 " + portx + " ;")
        break

print("——————————————————————————————————————")
com = serial.Serial(port = portx,   #端口号
            baudrate = 115200,      #波特率
            timeout=5)              #超时时间

print(com.name)

try:
    while 1:
        data = com.readline()
        print(data.strip())
except:
    print("——————————————————————————————————————")
    print("【him】：串口读取失败")

"""
初步编写完毕，简单的读取一行串口内容然后打印，
交互上只能选中串口端。不能修改波特率等设置。
还学会了使用以下命令可以打包成一个可执行文件
pyinstaller -F  2021.04.12_text1.py
"""