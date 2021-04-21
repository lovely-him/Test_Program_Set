
import numpy as np

"""
理一理思路：
①当初受学长的思路影响，先入为主的决定把图像的坐标定在了下方，然后学长们还是定在右下方。导致左边点是大，右边点是小
②我也先采用了坐标在下方，但是我选择改了一下左右的顺序，把左边点放在左边，右边放在右边，所以坐标是定在左下角
③后来了解到计算机的图像格式中，坐标本来就是左上角的。我……，现在返回去想象，其实定在哪里问题都不大。但是为了统一思维，我决定还是采用计算机的传统坐标
④但是现在硬件已经反转了，然后我程序又反了一次，那我暂时就不该硬件程序了。在电脑端统一格式。
⑤串口接收到压缩图数据是原模原样的，没变。然后我决定变一下。改回坐标是在左上角的问题。现在收到的压缩图就是坐标点在左上角了。
⑥同时把串口接收的二值化图也直接扩展为三维.
⑦一顿操作后，现在应该修改完毕了。现在串口接收返回的压缩图和全图都是左上角坐标，然后因为显示问题的反转在显示的定时回调函数里操作。其他地方还是正常的（32，128，3）

"""

class math_all():
    """图像处理函数，在播放图片或接收图片时嵌套调用，用来显示实时处理结果
    """
    def __init__(self):
        pass


    def Progressive_Scan_y(self, bmp):

        for x in range(128):                                # 全部列的编列
            data = bmp[x]
            if data != 0:                                   # 这一列有内容
                for y in range(31,-1,-1):                   # 在32位二进制中从右边找1
                    if (data) & (0x1<<y):
                        data = (0x01<<y)                    # 用找到的第一个点代替整列
                        bmp[x] = data
                        break                               # 退出这一列的循环
    
        img = self.UnZip_img(bmp)                           # 解压图片

        # img_txt = list(img)                                 # 要使用 append 方法就要转换一下
        # img_txt.append([i for i in range(128)])             # 生成一个坐标，方便查看
        # np.savetxt("./Python_test/out_img/img1.txt", img_txt, fmt="%3.0f")

        return img

    def read_file(self, bmp_data, read_mod):
        "如果是读文件，读到的图片是经过压缩保存的，所以要重新解压一次bmp再输出"

        show_img = np.zeros((32,128,3), dtype = np.uint8)           # 创建三维图片

        show_img[:,:,0] = self.UnZip_img(bmp_data)                  # 解压图片 - python 切片，秒啊。

        if read_mod == "模式一":
            show_img[:,:,1] = self.Progressive_Scan_y(bmp_data)     # 图片叠加

            img_txt = list(show_img[:,:,0])                         # 要使用 append 方法就要转换一下
            img_txt.append([i for i in range(128)])                 # 生成一个坐标，方便查看
            np.savetxt("./Python_test/out_img/img2.txt", img_txt, fmt="%3.0f")

        return show_img                                             # 图片输出

    def read_com(self, img_data, read_mod):
        "如果是读串口，那读到的图片数据就是解压bmp的数据，所以不做处理"

        return img_data

    def UnZip_img(self, bmp):
        """解压图片,传入压缩图片，输出一维的二值化图片
        """
        img = np.zeros((32,128), dtype = np.uint8) 

        for x in range(128):                            # 解压数据
            data = bmp[x]
            if data != 0:                               # 列不为空
                for y in range(32):     
                    gray = (data>>y) & 0x01
                    if gray == 1:                       # 行不为空
                        img[y][x] = 255                 # 计算机中的图片原点为左上角

        return img

    def __call__(self,img_data, bmp_data, show_mod, read_mod, app_print):
        """外部调用的综合算法，集合了类中的精华~~ ，
        其中把类方法传回来了，可以在这里调用 app_print 往窗口打印东西"""

        if show_mod == "read_file":
            img_data = self.read_file(bmp_data, read_mod)
        elif show_mod == "read_com":
            img_data = self.read_com(img_data, read_mod)

        return img_data

if __name__ == "__main__":
    print("搞错了，这个文件是算法内容，单独执行没有意义。")      