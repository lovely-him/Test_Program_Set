

import PySide2
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader

import os
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

from serial_test4 import Canon_com
import matplotlib.pyplot as plt

from threading import Thread
from time import sleep

class Him_ui:

    def __init__(self):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('./Python_test/ui/untitled_1.ui')
        self.ui.him_Button.clicked.connect(self.him_Button_connect)
        self.him_Button_text = 1

    def him_Button_connect(self):
        if self.him_Button_text == 1:
            self.him_Button_text = 0
            self.ui.him_Button.setText("按键被按下了")
            # self.ui.him_Button.setEnabled(False)
            string = self.ui.him_lineEdit.text()
            print(string,type(string))
        else:
            self.him_Button_text = 1
            self.ui.him_Button.setText("按键被按起了")
        # plt.imshow(self.img[0])
        # plt.show()
        print(self.log[-1])
        self.ui.him_textBrowser.append(self.log[-1])
        self.ui.him_textBrowser.ensureCursorVisible()
        self.ui.statusbar.showMessage(self.log[-1])

    def init_com(self):
        self.com = Canon_com()       # 创建对象
        self.com.Auto_Get_Port()     # 获取端口
        self.com()                   # 创建端口
        get_img_thread = Thread(
            target=self.get_img,    # 线程入口
            daemon=True)            # 设置新线程为daemon线程
        get_img_thread.start()

    def get_img(self):
        "多线程入口"
        while 1:
            self.img = self.com.Read_img()     # 读取图像
            self.log = self.com.get_log(0)     # 输出日志
            



app = QApplication([])
him_ui = Him_ui()
him_ui.init_com()
him_ui.ui.show()
app.exec_()