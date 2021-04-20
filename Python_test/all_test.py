from pathlib import Path
path ="./Python_test/out_jpg/him_data.txt"                               # 文本保存路径
my_file = Path(path)
if my_file.is_file():
    print("文件存在")
    with open(path, "rt") as in_file:
        text = in_file.readlines()                                      # 返回一个列表，遗憾

        text.pop(0)         # 连续弹出3次，把开头的说明文件去掉
        text.pop(0)
        text.pop(0)

        read_text = []

        for i in range(len(text)):
            line = text[i]
            line = line.strip()            # 标准化
            data = line.split('|')
            if len(data) != 3:
                print("有问题")
                break

            file_name = data[0].strip()
            show_time = int(data[1].strip())
            img_data = data[2].strip().split(' ')
            for j in range(len(img_data)):
                img_data[j] = int(img_data[j],16)

            read_text.append([file_name,show_time,img_data])
    # print(read_text)
else:
    print("文件不存在")