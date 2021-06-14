ESP32 单片机学习笔记 - 08 - 例程学习

> 前言，终于要到网络模型的最后一层，第四层，应用层，http、websocket的实践了。

@[TOC]

# WebSocket客户端

# 一、应用层协议 科普概念

> 在看例程之前先补补概念，我现在还是一脸懵逼，不知道这个是什么的状态。明明上一层的tcp已经能够通讯了，怎么又加多了一层。
> 各个知识点讲解：[90分钟搞定Web基础：网络协议，HTTP，Web服务器](https://www.bilibili.com/video/BV1S7411R7kF)（只挑想看的）。
> WebSocket大概介绍：[WebSocket打造在线聊天室【完结】](https://www.bilibili.com/video/BV1r54y1D72U)（只看了第一个介绍视频）。
> 知乎白话文解释：[WebSocket 是什么原理？为什么可以实现持久连接？](https://www.zhihu.com/question/20215561)（文字）。
> 几分钟快速入门：[前后端交互之 HTTP 协议](https://www.bilibili.com/video/BV1KV411o7u5)（AE短视频？怀念）。
> WebSocket的使用教程：[WebSocket 教程](http://www.ruanyifeng.com/blog/2017/05/websocket.html)。

- 快速看完上面的资料后，对`Http`和`WebSocket`都有了初步的认知。总结以下几点：

1. `http`有1.0和1.1版本，现在基本1.1版本。http属于**无状态、无连接、单向**的应用层协议。即通讯请求只能有客户端发起，服务端只负责响应请求，不能主动发起。在应用中表现为 *通过频繁的请求实现长轮询* 。
2. `WebSocket`对比http，最大的特点就是可以主动向客户端发起请求。两者属于交集关系，有相同的地方，但不一样（所以应该是并列关系？）。

![特点](.\img_list\20210613085514.png)

1. 二者的握手协议也很相识，下图中，左图是`WebSocket`右图是`http`，可发现格式差不多。

![握手协议](.\img_list\20210613090252.png)

- 总结回顾之前三层内容：[Ethernet，TCP,IP协议简介](https://blog.csdn.net/qq_25072517/article/details/78478968)（链路层、网络层、传输层）。梳理一下之前学到的知识（按我个人的理解）：

> 1. **wifi和Ethernet协议**，本身有通讯协议。类比uart底层发送，定义电信号0/1的层面，有自身的校验位、起始位结束位等。属于**链路层**（也称网络接口层），主要是物理层面，保证了字节数据的正确性。
> 2. **IP协议**，本身有通讯协议，规定了数据要发送给网络中的哪个设备。类比片选等功能。属于**网络层**，主要是指定设备，保证传输对象的正确性。
> 3. **TCP/UDP协议**，也是有协议，用链路层得到的信息都是0/1的字节信息，打包了一些通讯数据，保证这些通讯数据的正确性。类比我用uart通讯时也写了一个帧头帧尾校验位的协议，如果一个数据包不符合设定要求，我就认为错误不可用。这时已经能初步得到想要的通讯数据了，不是八位的0/1或是单个字符，而是按我自己设定的16位、32位数据读取。属于**传输层**，主要是数据包的传输，保证设备间数据包传输的正确性。

![我感觉这张图就很清晰明了](.\img_list\20210613134718.png)

- 通过上图就能清晰明了的理解，数据是如何被层层打包的。再上一层，就是**应用层** —— **HTTP/WebSocket协议**，用传输层得到的数据包为基础，进一步规定两个设备的通讯（对话）方式。是一问一答还是多问多答，还是只答不问、只问不答……这样的规定是很重要的，因为网络通讯中要同时访问多个服务器/设备。应用层的协议有很多，适用不同的应用场景。

# 二、编程指南 翻译

> 编程指南：[ESP WebSocket Client](https://docs.espressif.com/projects/esp-idf/zh_CN/latest/esp32/api-reference/protocols/esp_websocket_client.html)。
> 系列教程：[第十八章 ESP32的WebSocket服务器](https://blog.csdn.net/qq_24550925/article/details/85855867)。
> 官方例程：[examples/protocols/websocket](https://github.com/espressif/esp-idf/tree/1d7068e/examples/protocols/websocket)。

## 1. 概述

- `ESP WebSocket`客户端是用于ESP32的[WebSocket](https://datatracker.ietf.org/doc/html/rfc6455)协议客户端实现。

## 2. 特点

- 支持基于`TCP`的`WebSocket`，带有`mbedtls`的`TLS`。
- 易于设置`URI`。
- 多个实例(一个应用程序中的多个客户机)。

## 3. 配置

### 1）URI

- 支持`ws`, `wss`方案。
- WebSocket样本:①`ws://echo.websocket.org`: `WebSocket`通过`TCP`，默认端口`80`，②`wss://echo.websocket.org`: `WebSocket`通过`SSL`，默认端口`443`。

```c#
// 最小的配置:
const esp_websocket_client_config_t ws_cfg = {
    .uri = "ws://echo.websocket.org",
};
// WebSocket客户端支持在URI中同时使用路径和查询。示例:
const esp_websocket_client_config_t ws_cfg = {
    .uri = "ws://echo.websocket.org/connectionhandler?id=104",
};
// 如果在 esp_websocket_client_config_t 中有任何与URI相关的选项，则URI定义的选项将被覆盖。示例:
const esp_websocket_client_config_t ws_cfg = {
    .uri = "ws://echo.websocket.org:123",
    .port = 4567,       //WebSocket客户端将使用端口4567连接到websocket.org
};
```

### 2）TLS

- 如果需要验证服务器端，需要提供`PEM`格式的证书，并在“`websocket_client_config_t`”中提供`cert_pem`。如果没有提供证书，那么`TLS`连接将默认不需要验证。

```c#
// 配置
const esp_websocket_client_config_t ws_cfg = {
    .uri = "wss://echo.websocket.org",
    .cert_pem = (const char *)websocket_org_pem_start,
};
```

### 3）子协议

- 客户端对服务器响应中的子协议字段无关，并且无论服务器响应什么都将接受连接。

```c#
// 配置结构中的子协议字段可用于请求子协议
const esp_websocket_client_config_t ws_cfg = {
    .uri = "ws://websocket.org",
    .subprotocol = "soap",
};
```

## 4. 事件

- `WEBSOCKET_EVENT_CONNECTED`:客户端与服务器成功建立连接。客户机现在可以发送和接收数据了。不包含事件数据。
- `WEBSOCKET_EVENT_DISCONNECTED`:由于传输层读取数据失败(例如服务器不可用)，客户端已经终止连接。不包含事件数据。
- `WEBSOCKET_EVENT_DATA`:客户端已经成功接收并解析了一个`WebSocket`帧。事件数据包含一个指向有效载荷数据的指针，有效载荷数据的长度以及接收帧的操作码。如果长度超过缓冲区大小，则消息可能被分割成多个事件。此事件也将被发布为非有效载荷帧，例如pong或连接关闭帧。
- `WEBSOCKET_EVENT_ERROR`:在客户端的当前实现中未使用。

```c#
// 如果客户端句柄需要在事件处理程序中，它可以通过传递给事件处理程序的指针访问:
esp_websocket_client_handle_t client = (esp_websocket_client_handle_t)handler_args;
```

## 5. 限制和已知问题

- 客户端可以在握手期间请求服务器使用子协议，但是不会对来自服务器的响应进行任何与子协议相关的检查。

## 6. 应用举例

- 一个简单的`WebSocket`示例，使用`esp_websocket_client`建立一个`WebSocket`连接，并通过[websocket.org](https://websocket.org/)服务器发送/接收数据，可以在这里找到:[protocols/ WebSocket](https://github.com/espressif/esp-idf/tree/1d7068e/examples/protocols/websocket)。

```c#
// WebSocket客户端支持以文本数据帧的形式发送数据，这告知应用层有效载荷数据是编码为UTF-8的文本数据。例子:
esp_websocket_client_send_text(client, data, len, portMAX_DELAY);
```

# 三、例程解析

1. 一堆打印和老三件初始化。

```c#
ESP_LOGI(TAG, "[APP] Startup..");
ESP_LOGI(TAG, "[APP] Free memory: %d bytes", esp_get_free_heap_size());
ESP_LOGI(TAG, "[APP] IDF version: %s", esp_get_idf_version());
esp_log_level_set("*", ESP_LOG_INFO);
esp_log_level_set("WEBSOCKET_CLIENT", ESP_LOG_DEBUG);
esp_log_level_set("TRANS_TCP", ESP_LOG_DEBUG);

ESP_ERROR_CHECK(nvs_flash_init());
ESP_ERROR_CHECK(esp_netif_init());
ESP_ERROR_CHECK(esp_event_loop_create_default());
```

2. 初始化联网，开启联网，记得打开项目配置菜单(`idf.py menuconfig`)修改配置。

```c#
/* This helper function configures Wi-Fi or Ethernet, as selected in menuconfig.
* Read "Establishing Wi-Fi or Ethernet Connection" section in
* examples/protocols/README.md for more information about this function.
*/
ESP_ERROR_CHECK(example_connect());
```

3. 例程创建了一个定时器和信号用于调试，如果定时器超时，就表示已经10s没有收到信息，同时释放信号量。如果有收到信息，会触发事件重置定时器。

```c#
// 定时器超时函数
static void shutdown_signaler(TimerHandle_t xTimer)
{
    ESP_LOGI(TAG, "No data received for %d seconds, signaling shutdown", NO_DATA_TIMEOUT_SEC);
    // 宏定义 释放信号量
    xSemaphoreGive(shutdown_sema);
}

// 创建一个新的软件计时器实例，并返回一个句柄，通过这个句柄可以引用创建的软件计时器。
shutdown_signal_timer = xTimerCreate("Websocket shutdown timer",                        // 只是一个文本名称，不被内核使用。
                                        NO_DATA_TIMEOUT_SEC * 1000 / portTICK_PERIOD_MS,   // 计时器周期(单位是tick)。
                                        pdFALSE,                                           // 计时器将在到期时自动重新加载。（不会）
                                        NULL,                                              // 为每个计时器分配一个唯一的id等于它的数组索引。
                                        shutdown_signaler);                                // 每个计时器在到期时调用同一个回调。
// 创建一个新的二进制信号量实例，并返回一个句柄，通过这个句柄可以引用新的信号量。
shutdown_sema = xSemaphoreCreateBinary();
```

4. 除了联网的内容需要配置，还有`WebSocket`客户端的`URI`需要配置，如果第一个选项设定了`From stdin`，例程就会开启`WEBSOCKET_URI_FROM_STDIN`宏定义。在联网成功后，连接服务器的`URI`需要手动输入（在监视器中）。如果设定为`From string`，会开启`CONFIG_WEBSOCKET_URI`宏定义，直接配置`URI`设置。

![URI配置](.\img_list\20210613145240.png)

```c#
    // 打包函数，用于获取uri字符串 
#if CONFIG_WEBSOCKET_URI_FROM_STDIN
static void get_string(char *line, size_t size)
{
    int count = 0;
    while (count < size) {
        int c = fgetc(stdin);
        if (c == '\n') {
            line[count] = '\0';
            break;
        } else if (c > 0 && c < 127) {
            line[count] = c;
            ++count;
        }
        vTaskDelay(10 / portTICK_PERIOD_MS);
    }
}
#endif /* CONFIG_WEBSOCKET_URI_FROM_STDIN */

    // 是否需要手动输入uri地址，若配置中不存在则需要
#if CONFIG_WEBSOCKET_URI_FROM_STDIN
    char line[128];

    ESP_LOGI(TAG, "Please enter uri of websocket endpoint");
    get_string(line, sizeof(line));

    websocket_cfg.uri = line;
    ESP_LOGI(TAG, "Endpoint uri: %s\n", line);

#else
    // 直接获取uri地址
    websocket_cfg.uri = CONFIG_WEBSOCKET_URI;

#endif /* CONFIG_WEBSOCKET_URI_FROM_STDIN */

    /*
    这个函数必须是第一个调用的函数，它返回一个 esp_websocket_client_handle_t ，
    你必须把它作为接口中其他函数的输入。
    当操作完成时，这个调用必须有一个对应的 esp_websocket_client_destroy 调用。
    */
    esp_websocket_client_handle_t client = esp_websocket_client_init(&websocket_cfg);
    // 注册Websocket事件。
    esp_websocket_register_events(client, WEBSOCKET_EVENT_ANY, websocket_event_handler, (void *)client);
    // 打开WebSocket连接。
    esp_websocket_client_start(client);
```

5. 在上一步中注册了`Websocket`事件。以下是处理事件的函数。

```c#
static void websocket_event_handler(void *handler_args, esp_event_base_t base, int32_t event_id, void *event_data)
{
    esp_websocket_event_data_t *data = (esp_websocket_event_data_t *)event_data;
    switch (event_id) {
        // 客户端与服务器成功建立连接。客户机现在可以发送和接收数据了。不包含事件数据。
    case WEBSOCKET_EVENT_CONNECTED:
        ESP_LOGI(TAG, "WEBSOCKET_EVENT_CONNECTED");
        break;
        // 由于传输层读取数据失败(例如服务器不可用)，客户端已经终止连接。不包含事件数据。
    case WEBSOCKET_EVENT_DISCONNECTED:
        ESP_LOGI(TAG, "WEBSOCKET_EVENT_DISCONNECTED");
        break;
        // 客户端已经成功接收并解析了一个`WebSocket`帧。
        // 事件数据包含一个指向有效载荷数据的指针，有效载荷数据的长度以及接收帧的操作码。
        // 如果长度超过缓冲区大小，则消息可能被分割成多个事件。
        // 此事件也将被发布为非有效载荷帧，例如pong或连接关闭帧。
    case WEBSOCKET_EVENT_DATA:
        ESP_LOGI(TAG, "WEBSOCKET_EVENT_DATA");
        ESP_LOGI(TAG, "Received opcode=%d", data->op_code);
        ESP_LOGW(TAG, "Received=%.*s", data->data_len, (char *)data->data_ptr);
        ESP_LOGW(TAG, "Total payload length=%d, data_len=%d, current payload offset=%d\r\n", data->payload_len, data->data_len, data->payload_offset);

        xTimerReset(shutdown_signal_timer, portMAX_DELAY);
        break;
        // 在客户端的当前实现中未使用。
    case WEBSOCKET_EVENT_ERROR:
        ESP_LOGI(TAG, "WEBSOCKET_EVENT_ERROR");
        break;
    }
}
```

6. 启动定时器，循环查询接收数据。

> - 表现结果：一直循环（1s间隔）查询连接状态，如果连接上，就连续发送10次数据，然后退出。
> - 不然就一直查询连接状态。如果没有发送满10次，也没有收到数据，定时器就会每10s打印一次报错，且释放一次信号量。
> - 如果一直没连接上，试验现象就是每隔10秒打印。

```c#
// 启动定时器
xTimerStart(shutdown_signal_timer, portMAX_DELAY);
char data[32];
int i = 0;
while (i < 10) 
{
    // 检查WebSocket客户端连接状态。
    if (esp_websocket_client_is_connected(client)) 
    {
        int len = sprintf(data, "hello %04d", i++);
        ESP_LOGI(TAG, "Sending %s", data);
        // 将文本数据写入WebSocket连接
        esp_websocket_client_send_text(client, data, len, portMAX_DELAY);
    }
    vTaskDelay(1000 / portTICK_RATE_MS);
}
```

7. 已经发送完数据，等待是否没有数据接收，然后关闭程序，退出。没有收到数据的判断依据是信号量。只要进入一次定时器超时就会满足。

```c#
// 宏获取信号量
xSemaphoreTake(shutdown_sema, portMAX_DELAY);
/*
停止WebSocket连接而没有WebSocket关闭握手。
此API停止ws客户端并直接关闭TCP连接，而不发送关闭帧。
使用 esp_websocket_client_close() 以一种干净的方式关闭连接是一个很好的实践。
*/
esp_websocket_client_stop(client);
ESP_LOGI(TAG, "Websocket Stopped");
/*
销毁 WebSocket 连接并释放所有资源。
这个函数必须是会话调用的最后一个函数。
它与 esp_websocket_client_init 函数相反，
调用时必须使用与 esp_websocket_client_init 调用返回的输入相同的句柄。
这可能会关闭该句柄使用过的所有连接。
*/
esp_websocket_client_destroy(client);
```

# 四、试验总结

## 1. 查看握手协议

- 我使用网络调试助手上位机，连接esp32。注意，该上位机没有`Websocket服务端`功能，我只是用来看esp32发送的tcp数据到底是什么。
- esp32配置中的URI设置为`ws://192.168.1.101:8080`，连接到我的上位机，然后上位机就接收到了`Websocket客户端`的握手数据。

![截图](.\img_list\20210613152438.png)

- 但是这个上位机不具有`Websocket服务端`的功能，所以不会回应握手数据。esp32也就连接不上，发送不了10次数据，也接收不到数据，就会每10s进入一次超时函数打印错误。从接收信息上看，客户端好像在重复发送握手，尝试链接。我在例程里没看到具体写出来的步骤，应该是打包在api中实现的功能。

![截图](.\img_list\20210613152510.png)

- 对比上一个笔记，tcp例程的实验。加深理解： *传输层就是发送应用层的数据* 。不同层之间的数据是层层打包的关系。

## 2. 连接 Websocket服务器

- 例程中自带的python脚本运行不了，搜索不到`Websocket服务器`的小工具，基本都是`Websocket客户端`的小工具。真的是奇了怪了。
- 在看Websocket概念时明白到可以用`node.js`写一个服务器，恰巧之前为了学上位机安装了`node.js`。可以用上了。

### 使用 node.js 编写简易 Websocket服务器

1. 第一步应该先安装nodejs，然后安装npm，设定npm软件包的安装目录：[Nodejs+npm详细安装](https://blog.csdn.net/qq_39308408/article/details/97754889)。

2. 第二步要注意是否导入了npm安装包的路径，以免在编写程序导入包时报错找不到：[nodejs require模块找不到的两种解决办法](https://blog.csdn.net/weixin_43988498/article/details/107943102)。

3. 在编写程序之前，先安装模块`npm install nodejs-websocket (-g)`。要注意安装模块的方法：[【nodejs】使用 npm安装模块方法](https://blog.csdn.net/qq_22182989/article/details/90053035)。本地安装就是指直接安装在读取目录的`node_modules`文件夹下，如果没有就会新建。直接到全局目录下使用本地安装，得到的效果和全局安装一样。

4. 编写参考教程，[nodejs-websocket创建websocket服务器](https://blog.csdn.net/qq_35779070/article/details/109531390)。注意教程中用的是本地安装，包不算大，所以本地安装也没关系。不过已经全局安装就不用再安装了。

5. 然后我直接拷贝了教程中的代码，仅把端口改成了`8080`。运行，成功（这个程序好像有点bug，无论如何都会打印“连接成功”）。好了，剩下的之后学`node.js`时再深究。

## 3. 实验现象

- 半完整的实验现象如下图，还有一半是打印接收内容。因为服务器没有写发送内容，所以就没有。

> 注意事项：连接前记得查看自己电脑的IP地址，然后输入正确的`URI`，不然连接不上。我刚刚重启了一下路由器，我的ip地址就变了……要重新修改。

![截图](.\img_list\20210613172417.png)

- 客户端在连续发送10次数据，且进入了一次定时器超时函数后，就关闭了`Websocket客户端`功能。
- 另外，不知道为什么看同步效果好差，怀疑是不是服务器小工具的问题。居然肉眼可见的不同步，达到1s以上（即客户端发送2次数据，服务器才打印一次）。暂时留下疑问，日后解答。

## 4. 总结的总结

> 以上没了。下一步继续按着教程系列学习。话说这节的教程系列的内容的`Websocket服务器`，而且用到的api好像都是再次宏定义后的接口，在官方api里找不到（我去没看源码证实猜想）。
