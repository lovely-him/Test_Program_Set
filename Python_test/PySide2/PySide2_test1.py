
import sys
import os
import PySide2
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QMessageBox

"""
在CSDN上找了半天的教程，都没找到合适的，最后在小破站上找到了大佬的详细教程，教的非常好，分享一下，
http://www.byhy.net/tut/py/gui/qt_02/
https://www.bilibili.com/video/BV1cJ411R7bP/?p=3&spm_id_from=pageDriver
之后的几份 PySide2 测试程序都是教程的例子
"""
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path



"""
QApplication 提供了整个图形界面程序的底层管理功能
概念：用来统一管理全部部件的，所以弄其他东西之前要先创建
和最后的 app.exec_() 搭配使用
"""
app = QApplication([])

"创建一个主窗口，用来存放所有部件，然后设置窗口的属性"
window = QMainWindow()
window.setWindowTitle('这里设置主窗口的文本')
window.resize(700, 400)     # 设置尺寸大小
window.move(300, 310)       # 设置起始位置

"创建一个文本输入框，是添加在主窗口下的，然后设置其属性"
textEdit = QPlainTextEdit(window)
textEdit.setPlaceholderText("这里设置提示的文本")
textEdit.resize(300,350)    # 如果不设置大小就没有了
textEdit.move(10,25)

"创建一个按键，也是添加在主窗口下的，然后设置其属性"
button = QPushButton('这里设置按键的文本', window)
button.resize(200,50)       # 默认大小都不会自动匹配，要自己输入
button.move(380,80)

"""
总结一：先创建app，然后主窗口，然后部件，层层嵌套
还有很多控件/部件的使用方法，在网站里有教程，感谢大佬的总结：www.byhy.net 
"""

"创建按键的回调函数"
def handleCalc():
    "获取文本框中的内容"
    str = textEdit.toPlainText()
    print(f"按钮被点击了")
    print(f"然后获取到了文本框里的内容：{str};内容的类型为：{type(str)}")
    
    "创建一个弹窗"
    QMessageBox.about(window,
    "这里是弹窗的第一个参数",
    "这里是弹窗的第二个参数")

"指定按键部件的回调函数"
button.clicked.connect(handleCalc)

"""
总结二：信号（signal）的概念
在 Qt 系统中， 当界面上一个控件被操作时，比如 被点击、被输入文本、被鼠标拖拽等， 就会发出 信号 ，英文叫 signal 。就是表明一个事件（比如被点击、被输入文本）发生了。
我们可以预先在代码中指定 处理这个 signal 的函数，这个处理 signal 的函数 叫做 slot 。
把 button 被 点击（clicked） 的信号（signal）， 连接（connect）到了 handleCalc 这样的一个 slot上
"""


"设置完所有属性后，显示窗口"
window.show()
"固定搭配"
app.exec_()

















