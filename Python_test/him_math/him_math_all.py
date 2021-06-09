
import numpy as np
import cv2

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
        self.Left_offset = np.zeros((32), dtype = np.int8)      # 左逆透视数组
        self.Right_offset = np.zeros((32), dtype = np.int8)
        self.Line_midcourt = np.zeros((32), dtype = np.int8)    # 中线数组
        self.Start_midcourt = 64                                # 扫线时中心扩展的起始点（就是上次中线的最后一行，第一次就是默认的64）
        self.Inverse_perspective_OK = "ON"                      # 是否算出逆矩阵数组
        self.or_border = 'Left'                                 # 当前所选取的中线参考边界
        self.or_border_num = 0


    def Step_01_y(self, inp_bmp):
        "第一步：从下到上列扫描"
        bmp = inp_bmp
        for x in range(128):                                # 全部列的编列
            data = bmp[x]
            if data != 0:                                   # 这一列有内容
                for y in range(31,-1,-1):                   # 在32位二进制中从右边找1
                    if (data) & (0x1<<y):
                        data = (0x01<<y)                    # 用找到的第一个点代替整列
                        bmp[x] = data
                        break                               # 退出这一列的循环

        return bmp

    def Step_02_y(self, inp_bmp):
        "第二步："
        bmp = inp_bmp
        left_01 = 0                                         # 临时变量
        left_02 = 0
        left_11 = 0
        left_12 = 0

        for x in range(127):                                # 从左边开始找
            if bmp[x] < bmp[x+1] or bmp[x]  == 0:           # 出现递增情况
                left_12 = x                                 # 记录这个拐点
                if (left_12-left_11)>(left_02-left_01):     # 比较最大长度
                    left_01 = left_11                       # 记录最大长度
                    left_02 = left_12
                left_11 = x                                 # 重新记录
        left_01 += 1                                        # 偏移一位
        left_02 += 1

        right_01 = 127                                      # 临时变量
        right_02 = 127
        right_11 = 127
        right_12 = 127
        for x in range(127,0,-1):                           # 从右边开始找
            if bmp[x] < bmp[x-1] or bmp[x]  == 0:           # 出现递增情况
                right_12 = x                                 
                if (right_11-right_12)>(right_01-right_02):
                    right_01 = right_11                 
                    right_02 = right_12
                right_11 = x                 
        right_01 -= 1                                       # 偏移一位
        right_02 -= 1

        left_bmp = np.zeros((128), dtype = np.uint32)       # 切记 是32位啊
        for x in range(left_01,left_02+1):
            if inp_bmp[x] != 0:
                left_bmp[x] = inp_bmp[x]
                
        right_bmp = np.zeros((128), dtype = np.uint32) 
        for x in range(right_02,right_01+1):
            if inp_bmp[x] != 0:
                right_bmp[x] = inp_bmp[x]

        # print(left_01,left_02,right_01,right_02)
        return (left_bmp,right_bmp)

    def Step_11_y(self, inp_bmp):
        "根据下面的16行全空来找中线"
        bmp = inp_bmp
        left_max = 0
        for x in range(63,-1,-1):       # 找左边的最大空白区域
            data = bmp[x]&0xFFFF0000
            if data != 0:
                left_max = x
                break
        right_max = 127
        for x in range(64,128,1):       # 找右边的最大空白区域
            data = bmp[x]&0xFFFF0000
            if data != 0:
                right_max = x
                break
            
        x_1 = ((left_max+right_max)/2)    # 计算一元线性方程
        y = [i for i in range(16,32)]

        if x_1 != 63:
            k = (31-16)/(63-x_1)    
            c = 31-k*63
            x = []
            for i in y:
                x.append(int((i-c)/k))
        else:                               # 生成竖直线
            x = [63 for i in range(16)]


        img = np.zeros((32,128), dtype = np.uint8)
        for i in range(len(y)):
            img[y[i]][x[i]] = 200
        
        return img

    def Inverse_perspective_count_0(self, inp_bmp):
        """
        说明：
            简易的逆透视偏移数组计算，每次刚开始就会计算一次，计算出结果后就不会再计算，而一直使用结果
        参数：
            inp_bmp 压缩图像
        返回：
            没有返回，计算的结果直接存在类的全局变量里了
        """
        if self.Inverse_perspective_OK != 'OK':

            bmp = inp_bmp                                           # 找左边偏差
            left_offset = np.zeros((32), dtype = np.uint8)
            for x in range(63,-1,-1):
                data = bmp[x]
                for y in range(31,-1,-1):
                    if (data>>y)&0x1:
                        left_offset[y] = x
                        break                                       # 退出这一列的循环
                if y >= 30:                                         # 退出这一行（全部）的循环(从中间往两边，扫到的是从低位到高位)
                    break
            
            bmp = inp_bmp                                           # 找右边偏差
            right_offset = np.zeros((32), dtype = np.int8)          # 有正负值
            for x in range(64,128,1):
                data = bmp[x]
                for y in range(31,-1,-1):
                    if (data>>y)&0x1:
                        right_offset[y] = x
                        break                                       # 退出这一列的循环
                if y >= 30:                                         # 退出这一行（全部）的循环
                    break
            
            line_offset = (right_offset[-2]-left_offset[-2])/2

            for y in range(31):        
                if left_offset[y] == 0:                             # 将零值填充
                    if left_offset[y-1] != 0:
                        left_offset[y] = left_offset[y+1]
                    else:
                        print("因为是先从高位到低位填值的，所以高位肯定有值的，如果没有就有问题了")
                if right_offset[y] == 0:
                    if right_offset[y-1] != 0:
                        right_offset[y] = right_offset[y+1]
                    else:
                        print("同理上面，不可以的情况")

                if left_offset[-2] != 0:                            # 计算边界的偏移量，有负有正
                    left_offset[y] -= left_offset[-2]
                else:
                    print("按道理来说第二个值肯定有的，没有就是车没放好，重新弄一下")
                if right_offset[-2] != 0:
                    right_offset[y] -= right_offset[-2]
                else:
                    print("同理上面，不可以的情况")

            add = 0
            for y in range(32):
                add += left_offset[y]+right_offset[y]
            add /= 32.0
            if add >= 2 or add <= -2:               # 检查对称性，不符合就退出
                return None
                
            self.Inverse_perspective_OK  = 'OK'
            self.Left_offset = left_offset
            self.Right_offset = right_offset
            self.Line_offset = line_offset

            print(add,left_offset,right_offset,line_offset)

    def Inverse_perspective(self, inp_bmp, or_LR):
        """
        说明：
            把输入的压缩图按照逆透视数组偏移
        参数：
            inp_bmp 压缩图像
            or_LR 对左右边界进行偏移
        返回：
            偏移过后的压缩图像
        """
        bmp = np.zeros((128), dtype = np.uint32)

        for x in range(0,128,1):                                    # 范围是整个图像
            for y in range(31,-1,-1):
                if inp_bmp[x] == 0:                                 # 如果是0就跳过
                    continue
                if (inp_bmp[x]>>y)&0x1 != 0:
                    if or_LR == 'Left':                             # 将左边的边界偏移
                        if x-self.Left_offset[y] >= 0:
                            bmp[x-self.Left_offset[y]] |= 0x1<<y
                    elif  or_LR == 'Right':                         # 将右边的边界偏移
                        if x-self.Right_offset[y] <= 127:
                            bmp[x-self.Right_offset[y]] |= 0x1<<y

        return bmp

    def line_composite(self, border_left, border_right):
        """合成中线
        """
        border_left_max = 0
        border_right_max = 0
        for y in range(32):                             # 找出左右边界的最大有效值
            if border_left[y] != 0:
                border_left_max = 31-y
                break
        for y in range(32):
            if border_right[y] != 0:
                border_right_max = 31-y
                break

        if self.or_border == 'Left' and border_right_max - border_left_max > 8:     # 根据最大有效边界求中线
            self.or_border_num += 1
            if border_right_max - border_left_max > 16:                             # 如果偏差太多就直接切换
                self.or_border_num += 10
            if self.or_border_num >= 5:                                             # 如果偏差不大就要累加一下，相当于滤波
                self.or_border = 'Right'
                self.or_border_num  = 0                                             # 然后将累加值重置
        elif self.or_border == 'Right' and border_left_max - border_right_max > 8:
            self.or_border_num -= 1
            if border_left_max - border_right_max > 16:
                self.or_border_num -= 10
            if self.or_border_num <= -5:                                            # 一个取正数，一个取负数，进一步滤波，同时方便比较
                self.or_border = 'Left'
                self.or_border_num = 0

        border_x = np.zeros((32), dtype = np.uint8)                                 # 创建空数组存储
        
        for y in range(0,32,1):
            if self.or_border == 'Left':                                            # 如果是左边界，操作如下
                if border_left[y]:
                    data = int(border_left[y]) - int(self.Left_offset[y]) + self.Line_offset
                    if data >= 127:
                        border_x[y] = 127
                    elif data <= 0:
                        border_x[y] = 0
                    else:
                        border_x[y] = data
            elif self.or_border == 'Right':                                         # 如果是右边界，同上
                if border_right[y]:
                    data = int(border_right[y]) - int(self.Right_offset[y]) - self.Line_offset
                    if data >= 127:
                        border_x[y] = 127
                    elif data <= 0:
                        border_x[y] = 0
                    else:
                        border_x[y] = data
            else:
                print("填错参数了")

                    
        img = np.zeros((32,128), dtype = np.uint8)
        for x in range(128):                                                        # 同时把点标在图上
            for y in range(32):
                if x == border_x[y] and border_x[y] != 0:
                    img[y][x] = 250

        return img
            
    def look_border_0(self, inp_bmp, or_LR, add_init=2, num_init=32, corner_init=1):
        """
        说明：
            找左右边界，流程为先在下部找个最低点，然后在最低点的四周找边界
        参数：
            inp_bmp 输入的压缩图像
            add_init 在拐角处扩大的搜索范围
            num_init 在拐角处退出搜索的依据 → 已找到的最大点数
            corner_init 允许拐角个数
            还有个终止搜索范围，这个参数就不引出来了
        返回：元组
            128长度的列数组，相当于压缩图
            32长度的行数组，存储每行的当个点
        """
        "笔记：事实证明 >> 优先级高于 &"
        border_x = np.zeros((32), dtype = np.uint8)             # 下标是行，存储列；存储的是行的一个点
        border_y = np.zeros((128), dtype = np.uint32)           # 下标是列，存储行；存储的是一整列的行信息
        bmp = inp_bmp
        
        data = self.start_point(bmp, or_LR)                     # 返回第一个点
        if data is None:
            return (border_y,border_x)
        x = data[2]                                             # 取出数据
        y = data[1]
        y_32 = data[0]
        border_x[y] = x                                         # 存储数据
        border_y[x] = y_32
        start_y = y                                             # 记录起始点

        # 我这里假定左边界就是从左到右，右边界就是从右到左，
        # 假设，一开始左转，左边界是从右到左，那就直接认为起始点有个拐点

        or_lr = -1 if or_LR == 'Right' else +1                  # 左右的找边
        or_UD = 'up'                                            # 从上往下还是从下往上
        corner = 0                                              # 拐角数累加
        add = 0                                                 # 扩大搜寻范围，在拐点处用到
        num = 0                                                 # 成功找到的点数，如果点数够多，就不再找拐点了
        add_RL = 0                                              # 指定在认为拐点前的进一步确认方向
        add_RL_num = 0                                          # 加了2个标志位，终于解决这个问题了
        while 1:
            data = self.block_for(bmp[x+or_lr+add_RL], y, 4+add, or_UD)
            if data is None and add_RL_num == 0:
                add_RL_num = 1
                if or_lr == -1:                                 # 在认为是拐点改变方向前，先跳一个格再找找看
                    add_RL = -1                                 # 
                if or_lr == +1:
                    add_RL = +1
                continue

            elif data is None and add_RL_num != 0:              # 跳了一列还是找不到，就认为是拐点，开始反向寻找
                add_RL = 0                                      # 如果这里重置，那么就无法扫描拐点了，会再次进来然后停止扫描退出函数
                                                                # 但是如果我在这里清除就会出现循环进入的情况，然后直接累加满拐点数
                if or_UD == 'up':                               # 如果现在的从下往上就改成从上往下
                    or_UD = 'down'
                    if or_LR == 'Right':
                        or_lr = +1                              # 从上往下就是往左边找
                        x -= 1                                  # 重新找上一个点
                    elif or_LR == 'Left':
                        or_lr = -1 
                        x += 1
                    else:
                        print("参数错误")
                        return None
                else:
                    or_UD = 'up'                                # 同理上
                    if or_LR == 'Right':
                        or_lr = -1
                        x += 1
                    elif or_LR == 'Left':
                        or_lr = +1
                        x -= 1
                    else:
                        print("参数错误")
                        return None
                add = add_init                                  # 在拐点处可能因为列的异或运算而丢边，增大搜索范围
                if y != start_y:                                # 避免把起始点也认为是拐点(其实用x列更加合理，但是发现这不好弄)
                    corner += 1                                 # 每次找不到点都认为这个点是拐角点
                    # print(or_LR, '有拐点',x+or_lr+add_RL,y)
                if corner > corner_init or num >= num_init:    # 超过3次拐点就直接退出
                    return (border_y,border_x)
                continue

            add_RL_num = 0
            add_RL = 0                                          # 重置，上面解释
            add = 0                                             # 清零
            num += 1                                            # 成功找到的点数
            x = x+or_lr                                         # 储存数据
            y = data[1]
            y_32 = data[0]
            border_x[y] = x
            border_y[x] |= y_32                                 # 注意这里是或运算，因为一列可能有多个点
            if num > num_init*1.5 or x>=126 or y<= 1 or x<=2:    # 退出循环的条件（y不能选下限，会误判）
                return (border_y,border_x)
            
    def start_point_0(self, inp_bmp, or_LR):
        """
        说明：
            寻找开始点，返回一次找边中最开始的起始点。返回空就代表找不到这一边的起始点。
        参数：
            inp_bmp 压缩图像
            or_LR 找左右起始点
        返回：元组
            列数据
            y坐标
            x坐标
        """
        bmp = inp_bmp

        if or_LR == 'Left':
            or_LR = range(63,-1,-1)                             # 根据参数选择生成器
        else: #if or_LR == 'Right':
            or_LR = range(64,128,1)                             # 这时候就体现了python语言的对象方法的妙用了，弱类型赛高
        # else:
        #     print("没有按要求输入参数")
        
        for y in (28,24):
            for x in or_LR:                                     # 在全部列中找这个点
                if bmp[x]:
                    data = self.block_for(bmp[x],y,2,'up')
                    if data:                                    # 要加判断，如果返回空代表没有点，要跳过
                        return (data[0],data[1],x)              # 找到后就返回这个点

        return None                                             # 返回空就代表找不到这一边的起始点。

    def block_for_0(self, data_32, start_y, size_y, or_UD):
        """
        说明：
            在指定的uint32内循环找点，根据参数的不同，可以修改往左还是往右，往上还是往下，循环范围。返回空就代表在这一个区域找不到点
        参数：
            data_32 列数据
            start_y 起始点
            size_y 起始点的上下范围
            or_UD 从上下开始找
        返回：元组
            列数据
            y坐标
        """
        # start_y_0 = start_y+size_y if start_y+size_y<=31 else 31        # 计算寻找范围，
        start_y_1 = start_y-size_y if start_y-size_y>=0 else 0          # 终止在y处，目的是为了找出的点一定要小于y

        if or_UD == "up":
            or_UD = range(start_y, start_y_1-1, -1)                     # 从大往小找（上）
        elif or_UD == "down":
            or_UD = range(start_y_1, start_y+1, 1)                      # 从小往大找（下）
        else:
            print("参数错误")                                           # 没有按规定填写参数
        
        for i in or_UD:
            if data_32>>i&0x1:
                return (0x1<<i, i)                                      # 找到后返回元组，包含列表示 和 具体位置
        
        return None                                                     # 找不到点就返回空（python会自己添加，为了严谨好看，自己手动加一下）

    '-------------------------上面的第一版，下面是第二版-------------------------'

    def show_gridding(self, show_img):
        "显示网格"
        
        for x in range(128):
            for y in range(32):
                if y == 16 and show_img[y][x][0]==0 and show_img[y][x][1]==0 and show_img[y][x][2]==0:
                    show_img[y][x][0] = 50
                    show_img[y][x][1] = 50
                    show_img[y][x][2] = 50
                if x == 64 and show_img[y][x][0]==0 and show_img[y][x][1]==0 and show_img[y][x][2]==0:
                    show_img[y][x][0] = 50
                    show_img[y][x][1] = 50
                    show_img[y][x][2] = 50

        return show_img

    def Inverse_perspective_count(self, inp_bmp):
        """
        说明：
            简易的逆透视偏移数组计算，每次刚开始就会计算一次，计算出结果后就不会再计算，而一直使用结果
        参数：
            inp_bmp 压缩图像
        返回：
            没有返回，计算的结果直接存在类的全局变量里了
        """
        bmp = inp_bmp                                           # 找左边边界
        left_offset = np.zeros((32), dtype = np.uint8)          # 改了这个就没了？？
        for x in range(63,-1,-1):                               # 从中间往两边扫
            for y in range(31,-1,-1):                           # 从下往上扫
                if bmp[x]>>y & 0x1:
                    left_offset[y] = x
                    break                                       # 退出这一列的循环
            if y >= 30:                                         # 如果右下找到值了就表示结束了
                break
        
        bmp = inp_bmp                                           # 找右边边界
        right_offset = np.zeros((32), dtype = np.int8)          # 有正负值
        for x in range(64,128,1):
            for y in range(31,-1,-1):
                if bmp[x]>>y & 0x1:
                    right_offset[y] = x                         # 这个还是边界，不是偏差（名字懒得变动了）
                    break                                       # 退出这一列的循环
            if y >= 30:                                         # 退出这一行（全部）的循环
                break

        if left_offset[30] == 0 or right_offset[30] == 0:      # 如果最下面的参考标准没有就退出
            print("左右，偏差失败")
            return None

        add = 0                                                 # 参考指标
        line_midcourt = np.zeros((32), dtype = np.uint8)        # 中线数组,无负值
        for y in range(31):                                     # 忽略最后31
            if left_offset[y] == 0:                             # 将零值填充
                if left_offset[y+1] != 0:
                    left_offset[y] = left_offset[y+1]
                else:
                    print("左，填零失败",left_offset[y] ,left_offset[y+1], y)
                    return
            if right_offset[y] == 0:
                if right_offset[y+1] != 0:
                    right_offset[y] = right_offset[y+1]
                else:
                    print("右，填零失败",right_offset[y] ,right_offset[y+1], y)
                    return

            line_midcourt[y] = (right_offset[y] + left_offset[y])/2     # 在计算偏差前先计算中值，保存
            if y==29:
                self.Standard = right_offset[y]

            left_offset[y] -= left_offset[-2]                           # 计算边界的偏移量，有负有正
            right_offset[y] -= right_offset[-2]

            add += left_offset[y]+right_offset[y]                       # 因为有正负，所以直接累加，

        add /= 32.0                                                     # 最后平均值小于指定标准
        if add >= 2 or add <= -2:                                       # 检查对称性，不符合就退出
            return None
            
        self.Inverse_perspective_OK = 'OK'                              # 运行到这里就表示通过检测了，保存
        self.Left_offset = left_offset                                  # 偏差数组
        self.Right_offset = right_offset                                # 
        self.Line_midcourt = line_midcourt                              # 第一次的中线数组
        self.Standard -= line_midcourt[29]                              # 计算中线偏差值

        print(add,left_offset,right_offset,line_midcourt, sep='\n')     # 打印结果看看

    def block_for(self, inp_bmp, start_y, start_x, or_LR, or_UD, size_y=4, or_him='Up', or_sp='OFF'):
        """
        说明：
            第二版区域内找点，现在默认是24的区域内找点，包含目标列和指定方向列，没有有反向找的功能。如果找到拐点就会返回拐点
        参数：
            inp_bmp 压缩图
            start_y 目标点y坐标
            start_x 目标点x坐标
            or_LR 指定寻找方向 - 左右（要找的方向，和要找的边界不一样）
            or_UD 指定寻找方向 - 上下
            size_y 指定寻找范围 - 上下（没有修改左右范围的参数，已经统一默认）
            or_him 测试参数
        返回：
            data 点的y坐标，点的x坐标，列数据，
        """
        if or_LR == 'Left':                                             # 判断初始寻找方向 - 左右
            or_lr = -1
        else: # if or_LR == 'Right':
            or_lr = 1

        if or_him == 'Up':                                              # 是正向扫描还是反向
            if start_y < size_y:                                        # 计算低位
                end_y = 0   
            else:
                end_y = start_y-size_y
        else:
            if start_y+size_y > 30:                                     # 计算高位
                end_y = 30   
            else:
                end_y = start_y+size_y
            i = start_y                                                 # 交换值，保持end是低位，
            start_y = end_y
            end_y = i

        if or_UD == 'Up':                                               # 根据寻找方向 - 上下，生成器
            or_ud = range(start_y+1, end_y-1, -1)                       # 有时候图像会有锯齿，那就不是刚好都是朝上的，把搜索范围往下扩充一格
        else: # if or_UD == 'Down':                                     # 从高位到低位，或是从低位到高位
            or_ud = range(end_y, start_y+2, 1)

        for i in or_ud:                                                 # 找指定列的点
            if inp_bmp[start_x+or_lr]>>i&0x1:
                return (i, start_x+or_lr, 0x1<<i)                       # 返回：点的y坐标，点的x坐标，列数据，

        if or_sp != 'OFF':                                              # 设立一个标志位，用来判断，是否要在原目标点的列数找拐点
            return

        if or_him == 'Up':
            j = 0   
            if end_y<4:                                                 # 扩大范围
                end_y = 0
            else:                                                       # 因为拐点处肯定是有2个点，那就应该能找到
                end_y -= 4
        else: # if or_UD == 'Down':
            j = 1
            if (start_y+4)>30:
                start_y = 30
            else:
                start_y += 4

        for i in range(end_y+j, start_y+j, 1):                          # 如果到这一步，就表示指定方向找不到点，就在原目标点的上方找点
            if inp_bmp[start_x]>>i&0x1:                                 # 排除原目标点(生成队列时就排除了)
                return (i, start_x, 0x1<<i)                             # 可以根据返回的x坐标，判断是不是拐点

        return None                                                     # 如果到这一步，就表示在指定目标范围内没有找到点

    def start_point(self, inp_bmp, or_LR, start_x=63, or_him='Up'):
        """
        说明：
            寻找起始点， 会连续寻找2个点，然后根据寻找方向来判断边界的走向，是向左还是向向右
        参数：
            inp_bmp 压缩图
            or_LR 要找的边界，内置换成要找的方向，别搞混了
            start_y 起始中点
        返回：
            data 起始点的坐标、列数据、还有方向
        """
        if or_LR == 'Left':                                             # 如果是找左边界，那认为起始是要往点的右边找
            or_LR_i = 'Right'
            or_lr = range(start_x,0,-1)                                 # 并不是到完全范围，为了省去一会判断取值范围
        else: #if or_LR == 'Right':                                     # 同理上
            or_LR_i = 'Left'
            or_lr = range(start_x+1,127,1)

        if or_him == 'Up':                                              # 判断是从下面开始找，还是从上面开始找
            or_ud = (31, 30)
        else: # if or_UD == 'Down':
            or_ud = (0, 1)

        for y_0 in or_ud:                                               # 指定找边界的下限
            for x_0 in or_lr:                                           # 在指定列范围中找这个点
                    data = self.block_for(inp_bmp, y_0, x_0, or_LR_i, 'Up', or_him=or_him, or_sp='ON')
                    if data:                                            # 要加判断，如果返回空代表没有点，要跳过
                        y_0 = data[0]                                   # 保存找到的第一个点
                        x_0 = data[1]
                        data_bmp = data[2]
                        break
            if data:                                                    # 如果有值就要退出了忘记退出，导致找到的值贼小
                break
        
        for i in range(2):                                              # 应对第一个点就是拐点的情况
            data = self.block_for(inp_bmp, y_0, x_0, or_LR_i, 'Up', or_him=or_him) 
            if data and x_0 != data[1]:
                y_1 = data[0]                                           # 以找到的第一个点再找个点，方向相同
                x_1 = data[1]                                           # 如果找到了，而且不是拐点，就认为是确定了整条边界线的方向
                data_bmp = data[2]
                return (y_1, x_1, data_bmp, or_LR_i)                    # 返回：起始点的坐标、列数据、还有方向
            elif data and x_0 == data[1]:
                y_0 = data[0]
                x_0 = data[1]
            else:                                                       # 没找到点就退出，换个方向找
                break
        
        data = self.block_for(inp_bmp, y_0, x_0, or_LR, 'Down', or_him=or_him)
        if data:
            y_1 = data[0]                                               # 如果顺着方向找不到，就反向找点。注意用的变量，复用了
            x_1 = data[1]
            data_bmp = data[2]
            if x_0 != x_1:  
                return (y_1, x_1, data_bmp, or_LR)                      # 同理上面
            else:
                print(f"这个时候就不应该还有拐点了吧:y={y_1}；x={x_1}；or_LR={or_LR}")

        return None                                                     # 返回空就代表找不到这一边的起始点。

    def start_point_test(self,inp_bmp):
        """
        说明：
            测试边界起始点检测的函数，将结果可视化出来
        参数：
            inp_bmp 压缩图
        返回：
            show_img 显示图
        """
        show_img = np.zeros((32,128), dtype = np.uint8)
        data_L = self.start_point(inp_bmp, 'Left')
        data_R = self.start_point(inp_bmp, 'Right')

        if ((data_L and data_R) and (data_L[3] == 'Right' and data_R[3] == 'Left')) or (data_L == None and data_R == None):
            for y_0 in range(32):
                for x_0 in range(128):
                    if x_0 == 64:
                        show_img[y_0][x_0] = 255
            return show_img
        else:
            if (data_L and data_L[3] == 'Left') or (data_R and data_R[3] == 'Left') :
                c = 32
                k = 2
                print(f"在向左转:{data_L},{data_R},")
            elif (data_L and data_L[3] == 'Right') or (data_R and data_R[3] == 'Right') :
                c = 96
                k = -2
                print(f"在向右转:{data_L},{data_R},")
            else:
                print(f"意料之外的情况发生了:{data_L},{data_R},")
                return show_img
            
            y = [i for i in range(16,32)] 
            x = [(i-16)*k+c for i in y]
            for y_0 in range(32):
                for x_0 in range(128):
                    for i in range(len(y)):
                        if x_0 == x[i] and y_0 == y[i]:
                            show_img[y_0][x_0] = 255

            return show_img

    def look_border(self, inp_bmp, or_LR, end_x_o=63, or_him='Up'):
        """
        说明：
            搜寻边界，先搜寻起始点，然后从起始点沿着起始点的方向扫描，终止于图像边界，或是拐点处
        参数：
            inp_bmp 压缩图像
            or_LR 要找的边界
            end_x_o 上一次中线的位置，可用来指定搜寻起始点时的扩展中心点
        返回：
            None 就算找不到边界也不会返回None
            (border_x, border_y) 行数组、列数组
            (start_direction, end_direction) 起始方向、终止方向
            (start_x, start_y) 起始点x、y
            (end_x, end_y) 终止点x、y
        """
        border_x = np.zeros((32), dtype = np.uint8)             # 下标是行，存储列；存储的是行的一个点
        border_y = np.zeros((128), dtype = np.uint32)           # 下标是列，存储行；存储的是一整列的行信息

        start_direction = None                                  # 创建初始值，可以用来返回
        end_direction = None
        if or_LR == 'Left':
            start_x = 0
            start_y = 31
            end_x = 0
            end_y = 31
        else:
            start_x = 127
            start_y = 31
            end_x = 127
            end_y = 31
            
        
        data = self.start_point(inp_bmp, or_LR, end_x_o, or_him=or_him)        # 寻找起始点，自带寻找2个点的功能，从而返回一个边界的衍生方向

        if data:
            start_y = data[0]                                   # 如果有数据就是找到点了 不然就是找不到边界
            start_x = data[1]
            start_direction = data[3]                           # 储存返回的数据
            border_x[start_y] = start_x
            border_y[start_x] = data[2]
            if start_direction == or_LR:                        # 如果返回的方向和要找的边界是相同的，那就表示边界是斜的，从低位到高位搜索
                or_UD = 'Down'
            else:
                or_UD = 'Up'                                    # 反之，同理

            x = start_x                                         # 设置起始点坐标
            y = start_y
            end_direction = start_direction                     # 设置起始方向
            # print(start_x,start_y)
            while 1:
                if (x>=126 and start_direction == 'Right'):     # 在计算之前判断，这样就可以把起始点也包括在判断里了
                    break
                elif (x<=2 and start_direction == 'Left'):
                    break
                elif (y<=2 and or_UD == 'Up'):
                    break
                
                data = self.block_for(inp_bmp, y, x, end_direction, or_UD, or_him=or_him)
                if data:
                    x_o = x                                     # 临时保存一下
                    y = data[0]
                    x = data[1]
                    if border_x[y] == 0:                      # 如果本身没有值就保存，如果有值就表示该行刚找过一次了，只保留最早的那次
                        border_x[y] = x                             # 好像是沿着方向找到，那每次找到的重复行的点都是更加靠中线的点，那应该保存

                    border_y[x] |= data[2]                      # 存储列数据，考虑到有拐点内容，所以用或运算
                    if x_o == x:
                        end_direction = 'corner'                # 如果2次都是在同一列就表示是拐点
                        break
                else:
                    break
            end_x = x                                           # 保存结束点坐标
            end_y = y

        return ((border_x, border_y), (start_direction, end_direction), (start_x, start_y), (end_x, end_y))

    def look_border_all(self, inp_bmp):

        border_DL = np.zeros((1,1,32), dtype = np.uint8)                                # 预设空数组
        border_DR = np.zeros((1,1,32), dtype = np.uint8)                

        border_UL = self.look_border(inp_bmp, 'Left', end_x_o=63, or_him='Up')          # 扫描边界，返回一系列信息
        border_UR = self.look_border(inp_bmp, 'Right', end_x_o=63, or_him='Up')

        x_0=0
        x_1=0
        x_2=0
        x_3=0
        if border_UL[3][1]>15 and border_UR[3][1]>15:                                   # 当从下扫描时得到的最高点小于定值时
            for x in range(128):                                                        # 扫描所有列，找出全空的列数区间，然后找中值，从中值开始从上向下扫描边界
                if x_1==0:
                    if x_0==0 and inp_bmp[x]==0:
                        x_0 = x
                    elif x_0!=0 and inp_bmp[x]!=0:
                        x_1 = x
                else:
                    if x_2==0 and inp_bmp[x]==0:
                        x_2 = x
                    elif x_2!=0 and inp_bmp[x]!=0:
                        x_3 = x
                        if x_3-x_2>x_1-x_0:
                            x_0 = x_2
                            x_1 = x_3
                            x_2 = 0
                            x_3 = 0
            if x_1-x_0>10:
                border_DL = self.look_border(inp_bmp, 'Left', end_x_o=int((x_1+x_0)/2), or_him='Down')
                border_DR = self.look_border(inp_bmp, 'Right', end_x_o=int((x_1+x_0)/2), or_him='Down')

                for y in range(border_DL[3][1]+1, border_DL[2][1], 1):                  # 补全零位
                    if border_DL[0][0][y] == 0 and border_DL[0][0][y+1] != 0:
                        border_DL[0][0][y] = border_DL[0][0][y-1]
                
                for y in range(border_DR[3][1]+1, border_DR[2][1], 1):
                    if border_DR[0][0][y] == 0 and border_DR[0][0][y+1] != 0:
                        border_DR[0][0][y] = border_DR[0][0][y-1]

                for y in range(32):
                    if border_DL[0][0][y] != 0 and border_UL[0][0][y] == 0:             # 叠加操作
                        border_UL[0][0][y] = border_DL[0][0][y]
                    if border_DR[0][0][y] != 0 and border_UR[0][0][y] == 0:
                        border_UR[0][0][y] = border_DR[0][0][y]


        for y in range(border_UL[3][1]+1, border_UL[2][1], 1):                          # 补全零位
            if border_UL[0][0][y] == 0 and border_UL[0][0][y+1] != 0:
                border_UL[0][0][y] = border_UL[0][0][y-1]
        
        for y in range(border_UR[3][1]+1, border_UR[2][1], 1):
            if border_UR[0][0][y] == 0 and border_UR[0][0][y+1] != 0:
                border_UR[0][0][y] = border_UR[0][0][y-1]

        for y in range(32):
            if border_UL[0][0][y] and border_UL[0][0][y] > self.Left_offset[y]:         # 偏移边界
                border_UL[0][0][y] -= self.Left_offset[y]
            else:
                border_UL[0][0][y] = 0

            if  border_UR[0][0][y] and border_UR[0][0][y] < self.Right_offset[y]+127:
                border_UR[0][0][y] -= self.Right_offset[y]
            else:
                border_UR[0][0][y] = 0

        line_midcourt = np.zeros((32), dtype = np.uint8)
        if border_UL[3][1]<border_UR[3][1]:                                             # 合成中线
            for y in range(32):
                if border_UL[0][0][y]!=0 and border_UL[0][0][y]+self.Standard>0 and border_UL[0][0][y]+self.Standard<127:
                    line_midcourt[y] = border_UL[0][0][y]+self.Standard
                else:
                    line_midcourt[y] = 0
        else:
            for y in range(32):
                if border_UR[0][0][y]!=0 and border_UR[0][0][y]-self.Standard>0 and border_UR[0][0][y]-self.Standard<127:
                    line_midcourt[y] = border_UR[0][0][y]-self.Standard
                else:
                    line_midcourt[y] = 0

        if x_1-x_0>10:                                                                  # 补全直线
            y_r = [i for i in (32,1)]
            pass

        

        return (border_UL[0][0], border_UR[0][0], line_midcourt, border_DL[0][0], border_DR[0][0])


    def read_file(self, bmp_data, read_mod):
        "如果是读文件，读到的图片是经过压缩保存的，所以要重新解压一次bmp再输出"

        show_img = np.zeros((32,128,3), dtype = np.uint8)           # 创建三维图片

        show_img = self.UnZip_img(show_img, bmp_data, 0x00CED1)     # 解压图片 - python 切片，秒啊。

        if read_mod == "模式一":                                    # 标注模式
            read_mod = 0
        elif read_mod == "模式二":
            read_mod = 1
        elif read_mod == "模式三":
            read_mod = 2
        elif read_mod == "模式四":
            read_mod = 3

        if read_mod >= 0:
            if self.Inverse_perspective_OK != 'OK':
                self.Inverse_perspective_count(bmp_data)
            else:
                data = self.look_border_all(bmp_data)               # 笔记：python 特定，这时 data_0 是数组，如果要对比数组，要使用 any 或是 all
                # show_img = self.UnZip_img(show_img, data[1][0], 0x4B0082)
                # show_img = self.UnZip_img(show_img, data[1][1], 0x6495ED)
                show_img = self.UnZip_img(show_img, data[3], 0x00CD66, mod='img')       # 显示 Down 左边界      叠加图片会覆盖，所以要考虑优先显示问题
                show_img = self.UnZip_img(show_img, data[4], 0x9ACD32, mod='img')       # 显示 Down 右边界
                show_img = self.UnZip_img(show_img, data[0], 0xDC143C, mod='img')       # 显示 UP 左边界
                show_img = self.UnZip_img(show_img, data[1], 0x8B008B, mod='img')       # 显示 UP 右边界
                show_img = self.UnZip_img(show_img, data[2], 0xF0E68C, mod='img')       # 显示中线
                # print(data)

        if read_mod >= 1:
            if self.Inverse_perspective_OK == 'OK':
                img = self.start_point_test(bmp_data)                   # 对边界起始点的测试程序
                show_img[:,:,1] += img 

        img_txt = list(show_img[:,:,2])
        img_txt.append([i for i in range(128)])
        # np.savetxt("./Python_test/out_img/img2.txt", img_txt, fmt="%3.0f")    # 保存文件，保存地址要自己改

        show_img = self.show_gridding(show_img)                     # 显示网格
        return show_img                                             # 图片输出

    def read_com(self, img_data, read_mod):
        "如果是读串口，那读到的图片数据就是解压bmp的数据，所以不做处理"

        return img_data

    def UnZip_img(self, show_img, bmp, color, mod='bmp'):
        """解压图片,传入压缩图片，输出一维的二值化图片，可以指定灰度/颜色大小
        """
        img = np.zeros((32,128,3), dtype = np.uint8) 

        if mod == 'bmp':
            for x in range(128):                                    # 解压数据
                data = bmp[x]
                if data != 0:                                       # 列不为空
                    for y in range(32):     
                        gray = (data>>y) & 0x01
                        if gray == 1:                               # 行不为空
                            img[y][x][0] = color>>16&0xFF
                            img[y][x][1] = color>>8&0xFF
                            img[y][x][2] = color>>0&0xFF
        else:
            for y in range(32):
                if bmp[y] != 0:
                    img[y][bmp[y]][0] = color>>16&0xFF
                    img[y][bmp[y]][1] = color>>8&0xFF
                    img[y][bmp[y]][2] = color>>0&0xFF
                
        
        for x in range(128):
            for y in range(32):
                if img[y][x][0] or img[y][x][1] or img[y][x][2]:
                    show_img[y][x][0] = img[y][x][0]
                    show_img[y][x][1] = img[y][x][1]
                    show_img[y][x][2] = img[y][x][2]

        return show_img

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