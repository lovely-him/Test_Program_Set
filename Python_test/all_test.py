


import numpy as np
import matplotlib.pyplot as plt
import imageio

path = "./Python_test/out_jpg/6.jpg"
com_img = imageio.imread(path)                                      # 读取图片
com_img = list(com_img)

path = "./Python_test/out_jpg/him_data.txt"
with open(path,'rt') as f:
    text = f.read()
    text = text.split('\n')
    text = text[5]
    text = text.split('|')
    text = text[2]
    text = text.split(' ')
    text.pop(0)
    text.pop(-1)
    
    
    img = np.zeros((32,128), dtype = np.uint8) # 重置图像数组
    for x in range(128):            # 解压数据
        data = int(text[x],16)
        if data != 0:               # 列不为空
            for y in range(32):     
                gray = (data>>y) & 0x01
                if gray == 1:       # 行不为空
                    img[31-y][x] = 1     # 计算机中的图片原点为左上角


img = list(img)

    # 显示图片
# plt.imshow(com_img)
# plt.show()

# img = np.zeros((32,128), dtype = np.uint8) # 重置图像数组

num = [i for i in range(128)]
# print(num)

img.append(num)

np.savetxt("./Python_test/out_jpg/img.txt", img, fmt="%2.0f")
