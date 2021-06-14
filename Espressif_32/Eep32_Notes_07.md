ESP32 单片机学习笔记 - 07 - 例程学习

> 之前只用了 `Wifi` 和 `Ethernet` 的连接，例程一下载就能连接的，但是没有讲到通讯。所以我还是很不懂。这次教程接触到了TCP/IP协议了，在使用例程时，就明显感受到，起始wifi和以太网在其中扮演什么角色了。
> 
@[TOC]

# TCP连接

> 开源教程：[第十六章 ESP32的TCP连接](https://blog.csdn.net/qq_24550925/article/details/85855018)。
> 编程指南：[lwIP](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/lwip.html?highlight=socket)，lwip是嵌入式的简约版tcp/ip协议，开源且轻量级（个人理解）。

# 一、例程实践

> 官方例程：`examples/protocols/sockets/`目录下的`tcp_client/`，[github](https://github.com/espressif/esp-idf/tree/1d7068e4be430edd92bb63f2d922036dcf5c3cc1/examples/protocols/sockets/tcp_client)传送门链接。
> 官方例程②：`examples/protocols/asio/`目录下的`tcp_echo_server/`，[github](https://github.com/espressif/esp-idf/tree/1d7068e4be430edd92bb63f2d922036dcf5c3cc1/examples/protocols/asio/tcp_echo_server)传送门链接。


> 这次我选择直接上手例程，先看看实验现象再看分析步骤。因为我发现步骤代码里没什么东西……这esp32封装的也太彻底了。*灵异事件：我昨晚还能在 `VS Code` 的esp插件例程中看到上面2个例程的页面。今天早上我起来写笔记时却怎么也找不到了。最后无奈到系统目录搜索文件夹才知道原来是分别在两个目录下的。不知道一晚改了什么，插件居然不找子目录下的例程了。又浪费了几小时找问题，不知道到底是哪里出现问题导致例程目录不会找子目录了，这下完蛋了，之后找例程都要去本地目录里找了。*

## 1）建立TCP客户端 - tcp_client

- 先拷贝项目工程，然后看`README.md`的说明文档。得知例程的功能如下：

> 应用程序创建一个 TCP 接口并尝试使用预定义的 IP 地址和端口号连接到服务器。 
> 成功建立连接后，应用程序发送消息并等待应答。 服务器回复后，应用程序将收到的回复打印为 ASCII 文本，等待 2 秒并发送另一条消息。 

- 单片机esp32建立了预设的IP和端口的客户端，那么我们还需要一个服务器来与它对接。可以选择一个终端工具 `netcat` ，也可以选择一些上位机（网络调试助手）。

![网络调试助手](.\img_list\20210611110441.png)

> 小插曲 - Netcat 工具
> 1. 下载本体：[Netcat](https://eternallybored.org/misc/netcat/)，点击最新版本，即第二个。（我目前显示的是1.12）
> 2. 解压文件，将本体存好，路径最好不要有中文，且要短。然后在系统变量`PAth`里添加该本体文件路径。
> 2. 网传还有另一种方法，就是单纯将本体中的一个`nc.exe`文件放到系统目录内。个人不喜欢，且操作时也没成功。
> 3. 经历一二步就已经算安装完了，然后就可以开始用了，[看不懂的教程](https://blog.csdn.net/weixin_30783629/article/details/95327380)。
> 3. 测试，打开2个终端，一个输入`nc -l -p 99999`，一个输入`nc localhost 99999`，这样2个终端就链接起来了。任意一一个终端输入东西按回车都会发送另一个终端里。

- 例程中还提供了一个python脚本，可以运行该脚本来建立服务器与客户端连接。使用前需要先安装python软件包，和把`$IDF_PATH/tools/ci/python_packages` 添加到 `PYTHONPATH`中。

> 该脚本有2个新的软件包需要安装`netifaces`和`ttfw_idf`，前者倒是安装好了，但是后者怎么也找不到，我怀疑是不是idf内的脚本了。然后`PYTHONPATH`路径我也不知道在哪里添加……所以我没使用这个脚本。

- 在下载程序之前要先配置网络`idf.py menuconfig`，选择使用`WiFi`联网，还是`Ethernet`联网，后者和上一个笔记中的操作一样，选择协议、模块、引脚、选择时钟频率。前者，也是之前笔记记载过的，不过当时没太在意界面配置，而是直接修改代码。
- 除了在idf终端使用界面配置外，我发现原来`VS code`内也可以配置，按`F1`后，在输入`ESP-IDF:SDK Configuration editor`指令，就进入到了`SDK 配置编辑器`。然后发觉之前生成的配置文件名也确实是`sdkconfig`。无论在终端还是IDE，打开这个配置编辑器都要加载一会，对比之下，为了稳定快速。果然还是终端比较好用……

> 1. 在`Top - Example Connection Configuration`中可以配置使用WiFi还是Ethernet，这个wifi和ethernet都是让esp32连接上网络的。不要理解成ethernet转wifi。（另外，不可以2个模式都选择打开，不然esp32会一直报错，然后一直复位）
> 2. 如果设置了ethernet模式，别忘记了还需要到`Top - Component config - Ethernet - Support ESP32 internal EMAC controller`修改以太网的引脚、时钟频率。
> 3. 在`Top - Example Configuration`中配置esp32客户端要连接IP地址和端口。这里我设置我自己电脑的IP地址和端口，那就可以实现互连了。如下图。

![终端截图1](.\img_list\20210611110442.png)

- 如果你设置没有问题，然后连接也没问题，那监视器就会有以下输出：

![终端截图1](.\img_list\20210611150714.png)

- 然后上位机就会有以下输出。

![终端截图2](.\img_list\20210611150853.png)

- 注意，上位机要提前打开连接，这样方便esp32刚上电连接上网络后直接连接。
- 例程里有写着，如果超时没连接就会退出程序，不会持续等待连接。所以如果你发现监视器显示esp32只获取了IP地址后没有下一步了。就可以尝试复位单片机重新运行程序看看。
- 在监视器模式下单片机好像无法复位，所以我是选择在终端里退出监视器，然后再退出监视器。
- 而且程序里设定每次收到信息后打印会有2秒的延时，所以不要想着做压力测试（收发速度测试）。

## 2）总结

- 经过wifi和ethernet的连接例程，终于到了能通讯例程。我原本以为wifi和ethernet会像uart那样，连接上就是可以直接获取信息。现在看来，前者只是底层的接口通讯协议，然后往上一层，网络端也有另外一套通讯协议……
- 类比uart的使用，本身有通讯协议，然后不同使用者又会另外定制通讯协议，再次打包解包uart的数据。比如我现在使用的蓝牙调试器app，其通讯协议就规定了帧头帧尾和校验位。
- 而`tcp/ip`协议就不只是帧头帧尾校验位这种形式了，还有多次握手模式等定义。

> 第二个例程的实现功能类似，在第一个例程的互连基础上相互通讯，第一个例子只能单向通讯（服务端到客户端）。

# 二、TCP/IP协议 - 科普

## 1）科普了解

> **相关资料**
> 1. [互联网知识基础-TCP/IP协议簇](http://www.taichi-maker.com/homepage/esp8266-nodemcu-iot/internet-basics/tcp-ip-stack/)；
> 2. [互联网知识基础-传输层](http://www.taichi-maker.com/homepage/esp8266-nodemcu-iot/internet-basics/transportation-layer/)；
> 3. [TCP和UDP的区别和优缺点](https://blog.csdn.net/xiaobangkuaipao/article/details/76793702)；
> 4. [百科：TCP/IP协议](https://baike.baidu.com/item/TCP%2FIP%E5%8D%8F%E8%AE%AE)。

- 总结：
- `TCP/IP协议`不是专门指tcp或ip，而是一个模型，具有4层结构，包含多个协议。不过取其中具有代表性的tcp和ip来命名。
- 这个模型中，`wifi/ethernet`属于接口协议，`tcp/udp`属于网络通讯协议，`ip`属于地址协议，再往上还有准备学的`http`等协议。
- 其中传输层中的`tcp`和`udp`协议分别针对准确和快速两种特点，在不同场景使用。

## 2）三次握手/四次握手

> 我本来并不在意这个定义的，只是看介绍时没看懂。然后查小破站，发现原来这还是个面试常考题目？那就得了解一下了。
> 在小破站上找到一个讲解视频，不过视频我还没看，我发现评论区就有很好的比喻。然后我就把评论保存下来，视频直接不看了。*白嫖*

> **三次握手**： TCP/IP 协议是传输层的一个面向连接的安全可靠的一个传输协议，三次握手的机制是为了保证能建立一个安全可靠的连接，那么第一次握手是由客户端发起，客户端会向服务端发送一个报文，在报文里面：SYN标志位置为1，表示发起新的连接。当服务端收到这个报文之后就知道客户端要和我建立一个新的连接，于是服务端就向客户端发送一个确认消息包，在这个消息包里面：ack标志位置为1，表示确认客户端发起的第一次连接请求。以上两次握手之后，对于客户端而言：已经明确了我既能给服务端成功发消息，也能成功收到服务端的响应。但是对于服务端而言：两次握手是不够的，因为到目前为止，服务端只知道一件事，客户端发给我的消息我能收到，但是我响应给客户端的消息，客户端能不能收到我是不知道的。所以，还需要进行第三次握手，第三次握手就是当客户端收到服务端发送的确认响应报文之后，还要继续去给服务端进行回应，也是一个ack标志位置1的确认消息。通过以上三次连接，不管是客户端还是服务端，都知道我既能给对方发送消息，也能收到对方的响应。那么，这个连接就被安全的建了。

> **四次握手**：四次握手机制也是由客户端去发起，客户端会发送一个报文，在报文里面FIN位标志位置一，当服务端收到这个报文之后，我就知道了客户端想要和我断开连接，但是此时服务端不一定能做好准备，因为当客户端发起断开连接的这个消息的时候，对于服务端而言，他和还有可能有未发送完的消息，他还要继续发送，所以呢，此时对于服务端而言，我只能进行一个消息确认，就是我先告诉服务端，我知道你要给我断开连接了，但是我这里边还可能没有做好准备，你需要等我一下，等会儿我会告诉你，于是呢，发完这个消息确认包之后，可能稍过片刻它就会继续发送一个断开连接的一个报文啊，也是一个FIN位置1的报文也是由服务端发给客户端的啊，这个报文表示服务端已经做好了断开连接的准备，那么当这个报文发给客户端的时候，客户端同样要给服务端继续发送一个消息确认的报文一共有四次，那么，通过这四次的相互沟通和连接，我就知道了，不管是服务端还是客户端都已经做好了断开连接的准备，于是连接就可以被断开啊，这是我对三次握手和四次挥手的一个理解。

> **巧妙比喻**：
| 【三次握手】| 
| 男：我们在一起吧| 
| 女：好的啊| 
| 男：好的，从现在开始吧| 
| 【四次挥手】| 
| 男：我们分手吧| 
| 女：我想一下| 
| 女：我们分手吧| 
| 男：好的，现在就结束吧| 

- 个人理解：连接时，客户端和服务器都需要知道对方能收能发。所以三次握手，2个来回。断连时，服务器不一定能立刻断开，所以需要发一个中间等待的握手。所以断连时需要多一次握手。

# 三、编程指南

> 我发现原来个例程的内容是归属到了`API 指南 - lwIP TCP/IP 协议栈`，[传送门](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/lwip.html?highlight=lwip)，为了防止中文版比英文版缺失东西，我们还是直接看英文版吧。因为中文版也是全英文……

- ESP-IDF使用开源lwIP轻量级TCP/IP栈。ESP-IDF版本的lwIP (esp-lwip)与上游项目相比有一些修改和补充。
- 百科介绍：[lwIP](https://baike.baidu.com/item/LwIP/10694326)，lwip提供三种API：1)RAW API 2)lwip API 3)BSD API。esp32支持的就是第三种，`BSD API`。

## 1. BSD 接口 API - BSD Sockets API

> `BSD Sockets API`是一个通用的跨平台`TCP/IP Sockets API`，起源于`UNIX`的`Berkeley`标准发行版，但现在已在`POSIX`规范的一部分中标准化。`BSD Sockets`有时被称为`POSIX Sockets`或`Berkeley Sockets`。 示例：protocols/sockets/tcp_server 、 tcp_client 、 udp_server 、 udp_client 、 udp_multicast 、 http_request。

## 2. 常用函数

> ESP32的TCP接口介绍
新建socket函数：`socket()`;
连接函数：`connect()`;
关闭socket函数：`close()`;
获取socket错误代码：`getsocketopt()`;
接收数据函数：`recv()`;
发送数据函数：`send()`;
绑定函数：`bing()`;
监听函数：`listen()`;
获取连接函数：`accept()`;

> ESP32使用的是LwIP，LwIP是特别适用于嵌入式设备的小型开源TCP/IP协议栈，对内存资源占用很小。ESP-IDF即是移植了LwIP协议栈。学习了解LwIP，给大家推荐本书，《嵌入式网络那些事:LwIP协议深度剖析与实战演练》。

> 我们的这个例程是直接怼的是**标准socket接口（内部是LwIP封装的），没有用LwIP的**，关于LwIP的接口讲解在Websocket中讲解，用法都是一样，知道流程后，API调用即可，处理好异常。流程+接口，打遍无敌手。LwIP的教程可以参考安富莱、野火的文档。

> 在[src/include/lwip/socket.h](https://github.com/espressif/esp-lwip/blob/2195f74/src/include/lwip/sockets.h)文件中可以看到下面的宏定义，lwip的socket也提供标准的socket接口函数。

## 3. Socket 错误处理

- BSD Socket错误处理代码对于稳定的socket应用程序非常重要。socket错误处理通常涉及以下几个方面:①检测错误。②获取错误原因代码。③根据原因代码处理错误。
- 在lwIP中，我们有两种不同的场景来处理socket错误：一种是返回[错误代码](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/lwip.html?highlight=lwip#socket-api-errors)，socket API返回值，不含错误原因；一种是返回[错误信息](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/lwip.html?highlight=lwip#select-errors)，不能直接感觉错误代码来判断。
- 常用的Socket错误原因码：[传送门链接](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/lwip.html?highlight=lwip#socket-error-reason-code)。

## 4. Socket 配置

- 使用`getsockopt()`和`setsockopt()`函数获取/设置每个Socket选项。

## 5. Netconn API

## 6. lwIP FreeRTOS Task

## 7. 总结

- 后面越来越看不懂了……暂时跳过吧，先看看代码。

# 四、代码解析

1. 第一步开始熟悉的`nvs_flash_init()`初始化，`esp_netif_init()`初始化，还有默认事件循环。

```c#
ESP_ERROR_CHECK(nvs_flash_init());
ESP_ERROR_CHECK(esp_netif_init());
ESP_ERROR_CHECK(esp_event_loop_create_default());
```

2. 然后是一个很特别的打包函数`example_connect()`，在`examples/protocols/README.md`说明文档中对它有详细说明。
- 简单点说就是个专门为例程打包的初始化调用函数。其原型在`examples/common_components/protocol_examples/common/connect.c`中。是为了省略例程中非重点的初始化。配合`idf.py menuconfig`指令可实现快速修改配置。
- 简单的`example_connect()`函数不能处理超时，不能优雅地处理各种错误条件，只适合在示例中使用。真正开发时应该参考基础配置例程，要求完整稳定的初始化过程。

```c#
/* This helper function configures Wi-Fi or Ethernet, as selected in menuconfig.
    * Read "Establishing Wi-Fi or Ethernet Connection" section in
    * examples/protocols/README.md for more information about this function.
    */
ESP_ERROR_CHECK(example_connect());
```

3. 最后一步建立任务，简单粗暴死循环运行tcp部分，包含创建，接收，发送。貌似没有初始化。只需要配置参数创建就可以了。
- 这次的例程显得没那么专业（繁琐）打包，简单（方便）的排列几个函数，然后死循环调用。
- 创建socket、连接服务器、发送数据、接收数据、关闭socket。一气呵成。每一步后还跟有错误检查，处理异常。

```c#
xTaskCreate(tcp_client_task, "tcp_client", 4096, NULL, 5, NULL);

static void tcp_client_task(void *pvParameters)
{
    char rx_buffer[128];
    char host_ip[] = HOST_IP_ADDR;
    int addr_family = 0;
    int ip_protocol = 0;

    while (1) 
    {
        //配置连接服务器信息：端口+ip
        struct sockaddr_in dest_addr;
        dest_addr.sin_addr.s_addr = inet_addr(host_ip);
        dest_addr.sin_family = AF_INET;
        dest_addr.sin_port = htons(PORT);
        addr_family = AF_INET;
        ip_protocol = IPPROTO_IP;

        //新建socket
        int sock =  socket(addr_family, SOCK_STREAM, ip_protocol);
        if (sock < 0) 
        {
            //打印报错信息
            ESP_LOGE(TAG, "Unable to create socket: errno %d", errno);
            //新建失败后，直接退出，懒得关闭新建的socket，也不再准备下次新建
            break;
        }
        ESP_LOGI(TAG, "Socket created, connecting to %s:%d", host_ip, PORT);

        //连接服务器
        int err = connect(sock, (struct sockaddr *)&dest_addr, sizeof(struct sockaddr_in6));
        if (err != 0) 
        {
            //打印报错信息
            ESP_LOGE(TAG, "Socket unable to connect: errno %d", errno);
            //新建失败后，直接退出，懒得关闭新建的socket，也不再准备下次新建
            break;
        }
        ESP_LOGI(TAG, "Successfully connected");

        while (1) 
        {
            //发送数据函数
            int err = send(sock, payload, strlen(payload), 0);
            if (err < 0) 
            {
                ESP_LOGE(TAG, "Error occurred during sending: errno %d", errno);
                break;
            }

            //读取接收数据
            int len = recv(sock, rx_buffer, sizeof(rx_buffer) - 1, 0);
            // Error occurred during receiving 接收时出错
            if (len < 0) 
            {
                //打印错误信息
                ESP_LOGE(TAG, "recv failed: errno %d", errno);
                break;
            }
            // Data received 收到的数据
            else 
            {
                rx_buffer[len] = 0; // Null-terminate whatever we received and treat like a string 无论接收到什么，都以null结束，并将其视为字符串
                ESP_LOGI(TAG, "Received %d bytes from %s:", len, host_ip);
                ESP_LOGI(TAG, "%s", rx_buffer);
            }

            // 每次循环都有2秒的时间间隔
            vTaskDelay(2000 / portTICK_PERIOD_MS);
        }

        // 如果连接成功，又退出来，那么会执行到这里，会关闭，再重新进入循环，再次开启
        if (sock != -1) 
        {
            ESP_LOGE(TAG, "Shutting down socket and restarting...");
            shutdown(sock, 0);
            //关闭之前新建的socket，等待下次新建
            close(sock);
        }
    }
    // 可以通过传递 NULL 值以 vTaskDelete ()来删除自己，但是为了纯粹的演示，传递的是任务自己的句柄。
    vTaskDelete(NULL);           
}
```
- 最后一行的`vTaskPrioritySet()`API函数 ，[传送门](https://www.cnblogs.com/Liu-Jing/p/7106376.html)。

- 第二个例程的代码居然是c++写的，然后我临时2小时快速入门c++的类对象后，感觉差不多了。再看例程发现，自己还是太菜了。第二个例程暂时看不懂，以后再补上。

# 五、总结

- 那到这里也算简单的完成了网络连接和通讯了，那我简单的把电机控制写上，再写个上位机接收，那是不是就完了？