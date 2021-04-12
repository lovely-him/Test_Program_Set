
#!/usr/bin/env python
#-*- coding: utf-8 -*
import sys
import serial
import serial.tools.list_ports
# 注意，不用安装 serial ，不然程序会失效，
# 虽然导入的模块名字是 serial。但是要安装的是 pyserial。

# 读取电脑中可用的串口，返回的是对象，用转换列表的方式，可以返回装有数个对象的列表
plist = list(serial.tools.list_ports.comports())


print("——————————————————————————————————————")
if len(plist) == 0:
    print("【him】：无可用串口，请检查设备；")
    sys.exit()  #退出程序
else:
    print("【him】：有以下可用串口；")
    for plist_n in range(len(plist)):   
        print(plist[plist_n],end = f" - {plist_n}\n") 
        # 这个列表里的所有对象 都可以使用转换字符串的方式，返回串口名字。
        # 如果是查看类型确实是对象，该对象应该存在：尝试对对象进行字符串操作是返回一段字符串。
        # 百度一查类的隐藏方法，就有了。果然如此。python训练营果然还是有作用的。

print("——————————————————————————————————————")
print("【him】：请输入你需要连接的串口:",end = '')

while 1:
    try:
        portx = int(input())            #读取输入字符，把输入字符转换为整形
        portx = list(plist[portx])[0]   #说明： 
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