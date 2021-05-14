# ESP32 单片机学习笔记 - 02 - 例程学习

> 前言，继续上一篇的内容。为了不堆积太多内容，所以切分编写。

## 一、ESP32读取陀螺仪（IIC）

> 官方例程：[github:esp-idf/examples/peripherals/i2c/i2c_self_test/](https://github.com/espressif/esp-idf/tree/master/examples/peripherals/i2c/i2c_self_test)，官方给的硬件iic例程，我之前用惯的都是软件iic。
> 官方指南：[I2C 驱动程序](https://docs.espressif.com/projects/esp-idf/zh_CN/latest/esp32/api-reference/peripherals/i2c.html)，开篇第一句“*I2C 是一种串行同步半双工通信协议，总线上可以同时挂载多个主机和从机。I2C 总线由串行数据线 (SDA) 和串行时钟线 (SCL) 线构成。这些线都需要上拉电阻。*”，我使用了软件上拉。（这一篇有中文版介绍）
> 教程笔记：[第十二章 ESP32读取SHT30的温湿度（IIC）](https://blog.csdn.net/qq_24550925/article/details/85852672)，第一篇例子我自己没怎么看，直接看官方指南了。其实官方指南如果有中文的话，看官方指南更好。
> 数据手册：[ESP32 技术参考手册](https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_cn.pdf)，在PDF的第十一章：*I2C 控制器 (I2C)*。

- 第一步，先上了我熟悉的软件iic。我直接使用逐飞科技的[RT1064库](https://gitee.com/seekfree/RT1064_Library/blob/master/Seekfree_RT1064_Opensource_Library/Libraries/seekfree_peripheral/SEEKFREE_IIC.c)中的软件iic给*扣*了出来。注意，我一开始顺手拿了CH32V103的库，但是发现库中不带改变输出输入方向的内容，所以就换了个RT1064的，是带有输入输出方向的改变的。虽然[esp32手册](https://docs.espressif.com/projects/esp-idf/zh_CN/latest/esp32/api-reference/peripherals/gpio.html#_CPPv411gpio_mode_t)上我看到有一个模式：`GPIO_MODE_INPUT_OUTPUT`，写着：“*GPIO模式:输入输出模式*”。但是暂时没用过，之后再研究其意思。目前先使用`GPIO_MODE_INPUT`仅输入模式和`GPIO_MODE_OUTPUT`仅输出模式，然后使用`gpio_set_direction`函数切换即可。（这些函数功能都是在手册查到的，多自己查查能发现新大陆）

- 拿到软件iic的模板后，只需要把`SDA`和`SCL`的相关宏定义都改了，再改初始化引脚函数就可以了。软件延时的长度都没改，先试试可不可以有。在`mpu6050.c`里有2个硬件延时的调用，改成esp32的FreeRTOS中的`vTaskDelay`延时即可。还有一步是数据类型名称不一样，要给`uint8`这类名词加上后缀变为`uint8_t`，不然会报错。*然后，其他的都不用改，逐飞已经封装好了，真不错。*

```C#
#define SEEKFREE_SCL    GPIO_NUM_18                           //定义SCL引脚  可任意更改为其他IO
#define SEEKFREE_SDA    GPIO_NUM_19                           //定义SDA引脚  可任意更改为其他IO

#define SDA             gpio_get_level (SEEKFREE_SDA)
#define SDA0()          gpio_set_level (SEEKFREE_SDA, 0)        //IO口输出低电平
#define SDA1()          gpio_set_level (SEEKFREE_SDA, 1)        //IO口输出高电平  
#define SCL0()          gpio_set_level (SEEKFREE_SCL, 0)        //IO口输出低电平
#define SCL1()          gpio_set_level (SEEKFREE_SCL, 1)        //IO口输出高电平
#define DIR_OUT()       gpio_set_direction (SEEKFREE_SDA, GPIO_MODE_OUTPUT)    //输出方向
#define DIR_IN()        gpio_set_direction (SEEKFREE_SDA, GPIO_MODE_INPUT)    //输入方向

void simiic_init(void)
{
    gpio_config_t io_conf;
    //disable interrupt
    io_conf.intr_type = GPIO_INTR_DISABLE;
    //set as output mode
    io_conf.mode = GPIO_MODE_OUTPUT;
    //bit mask of the pins that you want to set,e.g.SDA
    io_conf.pin_bit_mask = ((1ULL<<SEEKFREE_SCL) | (1ULL<<SEEKFREE_SDA));   // 重中之重！！！！！！！！！！！！！
    //disable pull-down mode
    io_conf.pull_down_en = 0;
    //disable pull-up mode
    io_conf.pull_up_en = 1;
    //configure GPIO with the given settings
    gpio_config(&io_conf);
}
```

> 一开始其实并不实例，初始化引脚是卡主了，在串口中**打印日志内容**（注意是带颜色的内容，所以可以判断是日志打印，不属于我人为手动打印）：`I (309) gpio: GPIO[0]| InputEn: 0| OutputEn: 1| OpenDrain: 0| Pullup: 1| Pul`。非常奇怪，因为我明明初始化的是`IO18`和`IO19`引脚，为什么这里显示是`IO0`引脚。而且每次都会直接卡在这里，不能继续下一步。然后查到一篇笔记：[esp8266~获取mpu6050六轴传感器数据 [可在此基础上做wifi平衡小车]](https://chalk.blog.csdn.net/article/details/84311457)。其中说，这种提示是报错的意思。但是它报错内容起码应该是对应有引脚号的，而且是2行。回来发现原来是我`gpio_config`引脚配置弄错了，其中的`pin_bit_mask`要放的是1的位移数，而不算纯数字。上一篇uart用函数初始化引脚，或是key也是用函数快捷初始化引脚，填的都是纯数字的io口号。但是用结构体初始化的话，应该要加个位移转换操作。然后就成功了。打印出如下内容：（因为程序的卡主了，而我又没弄在线调试功能，所以就在程序里设置打印步骤，提示我哪一步卡主了。另外，可以看到初始化引脚后好像就是会产生一个提示的？）

```
I (297) cpu_start: Starting scheduler on PRO CPU.
I (0) cpu_start: Starting scheduler on APP CPU.
app_main Start - 01
simiic_init Start - 02
I (309) gpio: GPIO[18]| InputEn: 0| OutputEn: 1| OpenDrain: 0| Pullup: 1| Pulldown: 0| Intr:0
I (319) gpio: GPIO[19]| InputEn: 0| OutputEn: 1| OpenDrain: 0| Pullup: 1| Pulldown: 0| Intr:0
simiic_init Start - 03
mpu6050_self1_check Start - 04
mpu6050卡在这里原因有以下几点
simiic_write_reg Start - 05
mpu_acc_x = 1
mpu_acc_x = 71
mpu_acc_x = 57
mpu_acc_x = 63
mpu_acc_x = 47
mpu_acc_x = 65
mpu_acc_x = 69
mpu_acc_x = 55
mpu_acc_x = 55
mpu_acc_x = 185
mpu_acc_x = -2
mpu_acc_x = -2050
mpu_acc_x = -1026
mpu_acc_x = 15
mpu_acc_x = 243
mpu_acc_x = 37
mpu_acc_x = 53
```

- 硬件iic就不移植了，我直接看硬件spi的移植。应该大同小异，也是为了加快进度。



## 二、ESP32驱动IPS彩屏显示（SPI）

> 官方例程：[github:esp-idf/examples/peripherals/spi_master/lcd/](https://github.com/espressif/esp-idf/tree/master/examples/peripherals/spi_master/lcd)，官方有一个关于的lcd的例程，我只看了其中基本的收发和初始化，其他数据处理都没看，因为我自己有对应的库，只需要关心底层配置就好了。
> 官方指南：[SPI Master Driver](https://docs.espressif.com/projects/esp-idf/zh_CN/latest/esp32/api-reference/peripherals/spi_master.html?highlight=spi_device_polling_transmit#overview-of-esp32-s-spi-peripherals)，又是全英文介绍，头大。因为我以前用也是调用api，没在意过其中的协议或是配置。只知道和iic差不多，也是拉高拉低cs，选择设备，发送发送地址、发送命令、发送数据之类的。
> 数据手册：[ESP32 技术参考手册](https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_cn.pdf)，在PDF的第七章：*SPI 控制器 (SPI)*。

> 我一开始想着拿着逐飞的库和eps官方例程的底层，移植在一起，就可以用了，结果折腾了好久，还是不成功。查了篇同样是硬件配置的笔记：[ESP32设备SPI主设备驱动](https://blog.csdn.net/zhejfl/article/details/85999816)，对照官方的一起尝试着改，还是没成功。折腾许久后，我想着试一下软件模拟spi吧，因为软件iic都成功了，那软件spi应该也很简单吧。然后也参考了一篇笔记：[(ESP32学习13)驱动TFTLCD（SPI接口）](https://blog.csdn.net/ailta/article/details/106611044)。呜呜，还是失败了。我怎么想都想不到还可能是问题了……下面笔记总结一下我发现的问题，但是即使如此目前还是没成功。之后成功了再回来补（2021.05.04）。
> 没想到那么快就回来了，第二天早上我询问逐飞的小M，他热心的接待我，说可以帮我看看。等我接好线下载好程序后准备问他时，发现居然成功可以用了！！！我应该什么都没改啊，只是重新接了一下线而已。（我记得昨晚在目前这个配置下也下载过的，但是没成功）

- 初始化时需要注意的（已发现）问题：
- 1. esp32没有spi，只有hspi和vspi，不过我还不清楚这三者的区别。目前是跟着例程选了`HSPI_HOST`；
- 1. 初始化流程，先初始化相关引脚，使用`spi_bus_initialize`，再配置各种参数`spi_bus_add_device`。其中 `clock_speed_hz` 频率参数，esp32最大是26，如果大于这个数会在运行初始化时报错；`pre_cb`指定了一个回调函数，一开始不知道怎么用的。后来结合写数据和写命令发现，会发送一个参数，每次会相应的调用该函数读取到参数，根据此改变`IPS114_DC_PIN`的电平。所以其实是起到一个改变电平的作用，在逐飞的库中，这个操作是在调用写数据或写命令函数前手动执行的。最后，`spi_bus_add_device`还有一个`spi_device_handle_t`类型参数，感觉是类似句柄一样，之后每次调用该spi操作时都会要传入这个句柄，原来指代是这个spi。

```C#
//-----------------引脚定义------------------------------
#define IPS114_SPIN_PIN         HSPI_HOST       //定义使用的SPI号(esp32 只有hspi或是vspi？！)
#define IPS114_SCL_PIN          19              //定义SPI_SCK引脚
#define IPS114_SDA_PIN          23              //定义SPI_MOSI引脚
#define IPS114_SDA_IN_PIN       25              //定义SPI_MISO引脚  IPS没有MISO引脚，但是这里任然需要定义，在spi的初始化时需要使用
#define IPS114_CS_PIN           22              //定义SPI_CS引脚
#define IPS114_DC_PIN 	        21	            //液晶命令位引脚定义

spi_device_handle_t ips114_spi;

//This function is called (in irq context!) just before a transmission starts. It will
//set the D/C line to the value indicated in the user field.
// 用来触发回调函数，然后在回调函数中拉高电平
void lcd_spi_pre_transfer_callback(spi_transaction_t *t)
{
    int dc=(int)t->user;
    gpio_set_level(IPS114_DC_PIN, dc);
    // printf("dc\n");
}

void spi_init(void)
{
    gpio_set_direction(IPS114_DC_PIN, GPIO_MODE_OUTPUT);
    gpio_set_level(IPS114_DC_PIN, 0);

    esp_err_t ret;
    spi_bus_config_t buscfg={
        .miso_io_num=IPS114_SDA_IN_PIN,
        .mosi_io_num=IPS114_SDA_PIN,
        .sclk_io_num=IPS114_SCL_PIN,
        .quadwp_io_num=-1,
        .quadhd_io_num=-1,
    };
    spi_device_interface_config_t devcfg={
        // .command_bits = 8,
        // .address_bits = 24,
        .clock_speed_hz=26*1000*1000,           //Clock out at 26 MHz (最大26)
        .mode=0,                                //SPI mode 0 SPI模式 0：CPOL=0 CPHA=0    1：CPOL=0 CPHA=1   2：CPOL=1 CPHA=0   3：CPOL=1 CPHA=1 //具体细节可自行百度
        .spics_io_num=IPS114_CS_PIN,            //CS pin
        .queue_size=7,                          //We want to be able to queue 7 transactions at a time
        .pre_cb=lcd_spi_pre_transfer_callback,  //Specify pre-transfer callback to handle D/C line
    };
    //Initialize the SPI bus 初始化SPI总线
    ret=spi_bus_initialize(IPS114_SPIN_PIN, &buscfg, 0);
    ESP_ERROR_CHECK(ret);
    //Attach the LCD to the SPI bus 将LCD连接到SPI总线
    ret=spi_bus_add_device(IPS114_SPIN_PIN, &devcfg, &ips114_spi);
    ESP_ERROR_CHECK(ret);
}
```

- 写数据/命令时需要注意的（已发现）问题：
- 1. 无论发送还是接收，用到的都是`spi_device_polling_transmit`函数来调用，其中是配置`spi_transaction_t`类型数据决定。
- 1. 参数`flags`的作用，是用来指定是用`tx_data`数组来放数据还是用`tx_buffer`指针来放数据。如果不配置的话，默认就是用指针。例程用的指针，然后我看别人写的笔记里是用数组，因为逐飞原本也是用数组来拆分16位数据的，所以我也用了数组。~~不过我2种都试过了，不知道为什么都不成功。~~
- 1. 参数`length`的作用，和特别的，是用位来计数，所以要用字节数乘于8计算得到。
- 1. 这个结构体除了data外，还有很多其他参数可以配置，比如`addr`和`cmd`，看注释好像分别指地址和命令。但是看例程统一都是用data来存。也就是把命令也当数据发出去。所以我推断应该是作用一样的，只是为了方便管理。

```C#
void lcd_cmd(const uint8_t cmd)
{
    esp_err_t ret;
    spi_transaction_t t;
    memset(&t, 0, sizeof(t));       //Zero out the transaction
    t.flags=SPI_TRANS_USE_TXDATA;   //
    t.length=8;                     //Command is 8 bits
    t.tx_data[0]=cmd;               //The data is the cmd itself
    t.user=(void*)0;                //D/C needs to be set to 0 用来触发回调函数，改变DC引脚的电平
    ret=spi_device_polling_transmit(ips114_spi, &t);  //Transmit!
    assert(ret==ESP_OK);            //Should have had no issues.
}

void lcd_data(const uint8_t data[2], int len)
{
    esp_err_t ret;
    spi_transaction_t t;
    if (len==0) return;             //no need to send anything
    memset(&t, 0, sizeof(t));       //Zero out the transaction
    t.user=(void*)1;                //D/C needs to be set to 1
    t.flags=SPI_TRANS_USE_TXDATA;
    if(len == 1)
    {
        t.length=8;
        t.tx_data[0]=data[0];        //Data
    }
    else if(len == 2)
    {
        t.length=2*8;
        t.tx_data[0]=data[0];
        t.tx_data[1]=data[1];
    }
    else
    {
        assert(1);
    }
    ret=spi_device_polling_transmit(ips114_spi, &t);  //Transmit!
    assert(ret==ESP_OK);            //Should have had no issues.
}
```

> 额外的有趣知识点，`ESP_ERROR_CHECK`和`assert`;在手册里有专门的一章讲述：[错误处理](https://docs.espressif.com/projects/esp-idf/zh_CN/latest/esp32/api-guides/error-handling.html?highlight=esp_error_check)。我发现这功能很好用，如果配置错误了会直接在终端里打印错误内容。打印的内容甚至具体到哪个文件那一行，比之前用过的（指单片机或库）好太多了。以往如果配置错了会直接掉硬件错误中断，或是没有现象。要找问题得半天，特别是不能在线调试的情况下就更加痛苦了。

> - 先记载那么多，如果之后发现发现到底是问题的话再补。（2021年5月4日 22:05:21）没有发现问题，但是问题已经消失了……（2021年5月5日 09:57:14）

- 2021.05.08 - 问题1： 我无意查了一下引脚定义，发现esp32-wroom-32的引脚名字中，对应有`HSPI`字符的引脚并不和例程的一样，而我使用的是例程的……也就是说我使用的并不是固定的硬件spi引脚？连硬件spi引脚也不是固定的吗？（目前已经学了`PCNT`和`MCPWM`，其引脚也都不是固定的）好了，测试完毕了，引脚都不是固定的，其中用不到的`SPI_MISO`引脚设定-1即可，背光引脚的初始化和定义屏蔽掉即可。


