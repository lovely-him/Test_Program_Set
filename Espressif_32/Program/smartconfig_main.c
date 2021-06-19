/* Esptouch example

   This example code is in the Public Domain (or CC0 licensed, at your option.)

   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/

#include <string.h>
#include <stdlib.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"
#include "esp_wifi.h"
#include "esp_wpa2.h"
#include "esp_event.h"
#include "esp_log.h"
#include "esp_system.h"
#include "nvs_flash.h"
#include "esp_netif.h"
#include "esp_smartconfig.h"

/* FreeRTOS事件组的信号，当我们连接和准备发出请求*/
/* FreeRTOS event group to signal when we are connected & ready to make a request */
static EventGroupHandle_t s_wifi_event_group;

/* The event group allows multiple bits for each event, 事件组允许多个位为每个事件，
   but we only care about one event - are we connected to the AP with an IP? 
   但我们只关心一个事件——我们是否用IP连接到AP ?*/
static const int CONNECTED_BIT = BIT0;          // connected bit 连接 标志位？
static const int ESPTOUCH_DONE_BIT = BIT1;      // esptouch done bit esptouch 完成 标志位？
static const char *TAG = "smartconfig_example"; // smartconfig example

static void smartconfig_example_task(void * parm);


// event handler 事件 处理程序
static void event_handler(void* arg, esp_event_base_t event_base, 
                                int32_t event_id, void* event_data)
{
    if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_START)                   // ESP32站启动
    {   /* 创建一个新任务，并将其添加到准备运行的任务列表中。 */
        xTaskCreate(smartconfig_example_task, "smartconfig_example_task", 4096, NULL, 3, NULL);
    } 
    else if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_DISCONNECTED)       // ESP32站与AP断连
    {   /* 将ESP32 WiFi站连接到AP。 */
        esp_wifi_connect();                                                             // 断连就尝试重新连接？
        /* 清除事件组中的位。？？？ 这个函数不能从中断调用。？？？ */
        xEventGroupClearBits(s_wifi_event_group, CONNECTED_BIT); 
    } 
    else if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP)                 // station 从连接的AP获得IP
    {   /* 在事件组中设置位。这个函数不能从中断调用。 */
        xEventGroupSetBits(s_wifi_event_group, CONNECTED_BIT);
    } 
    else if (event_base == SC_EVENT && event_id == SC_EVENT_SCAN_DONE)                  // ESP32站 smart config（智能配置） 已完成ap扫描
    {
        ESP_LOGI(TAG, "Scan done"); // 进行ct扫描
    } 
    else if (event_base == SC_EVENT && event_id == SC_EVENT_FOUND_CHANNEL)              // ESP32站 smartconfig 已经找到目标AP的通道
    {
        ESP_LOGI(TAG, "Found channel"); // 发现频道
    } 
    else if (event_base == SC_EVENT && event_id == SC_EVENT_GOT_SSID_PSWD)              // ESP32站 smartconfig 获得SSID和密码
    {
        ESP_LOGI(TAG, "Got SSID and password"); // 找到SSID和密码了

        smartconfig_event_got_ssid_pswd_t *evt = (smartconfig_event_got_ssid_pswd_t *)event_data;
        wifi_config_t wifi_config;                      // 下面开始 ESP32的STA配置。
        uint8_t ssid[33] = { 0 };
        uint8_t password[65] = { 0 };

        bzero(&wifi_config, sizeof(wifi_config_t));     // 清零
        memcpy(wifi_config.sta.ssid, evt->ssid, sizeof(wifi_config.sta.ssid));      // 拷贝
        memcpy(wifi_config.sta.password, evt->password, sizeof(wifi_config.sta.password));
        wifi_config.sta.bssid_set = evt->bssid_set; 
        /*
        参数 bssid_set ：是否设置目标AP的MAC地址。一般来说,station_config。Bssid_set需要为0;仅当用户需要查看AP的MAC地址时，取值为1。
        */
        if (wifi_config.sta.bssid_set == true) 
        {
            memcpy(wifi_config.sta.bssid, evt->bssid, sizeof(wifi_config.sta.bssid));
        }

        memcpy(ssid, evt->ssid, sizeof(evt->ssid));
        memcpy(password, evt->password, sizeof(evt->password));
        ESP_LOGI(TAG, "SSID:%s", ssid);
        ESP_LOGI(TAG, "PASSWORD:%s", password);

        ESP_ERROR_CHECK( esp_wifi_disconnect() );                                   // 将ESP32 WiFi站与AP断开连接。
        ESP_ERROR_CHECK( esp_wifi_set_config(ESP_IF_WIFI_STA, &wifi_config) );      // 配置ESP32 STA / AP的配置信息。
        ESP_ERROR_CHECK( esp_wifi_connect() );                                      // 将ESP32 WiFi站连接到AP。
    } 
    else if (event_base == SC_EVENT && event_id == SC_EVENT_SEND_ACK_DONE)          // ESP32站 smartconfig 已向手机发送ACK
    {   /* 在事件组中设置位。这个函数不能从中断调用。 */
        xEventGroupSetBits(s_wifi_event_group, ESPTOUCH_DONE_BIT);
    }
}

static void initialise_wifi(void)
{
    ESP_ERROR_CHECK(esp_netif_init());                                              // 1.1. 初始化底层TCP/IP堆栈。
    s_wifi_event_group = xEventGroupCreate();                                       // 创建一个新的事件组。
    ESP_ERROR_CHECK(esp_event_loop_create_default());                               // 1.2. 创建默认事件循环。
    esp_netif_t *sta_netif = esp_netif_create_default_wifi_sta();                   // 创建默认的WIFI STA。在任何初始化错误的情况下，这个API将中止。
    assert(sta_netif);

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();                            // 获取Wifi初始化配置默认
    ESP_ERROR_CHECK( esp_wifi_init(&cfg) );                                         // 为WiFi驱动分配资源，如WiFi控制结构、RX/TX缓冲区、

    /* 向系统事件循环(遗留)注册一个事件处理程序。 
    event_base : 要为其注册处理程序的事件的基本id;
    event_id : 要为其注册处理程序的事件的id;
    event_handler : 当事件被分派时被调用的处理函数;
    event_handler_arg : 除事件数据外，在调用处理程序时传递给该处理程序的数据;
    */
    ESP_ERROR_CHECK( esp_event_handler_register(WIFI_EVENT, ESP_EVENT_ANY_ID, &event_handler, NULL) );  
    ESP_ERROR_CHECK( esp_event_handler_register(IP_EVENT, IP_EVENT_STA_GOT_IP, &event_handler, NULL) );
    ESP_ERROR_CHECK( esp_event_handler_register(SC_EVENT, ESP_EVENT_ANY_ID, &event_handler, NULL) );

    ESP_ERROR_CHECK( esp_wifi_set_mode(WIFI_MODE_STA) );                            // 2.0. 设置WiFi工作模式。 STA模式
    ESP_ERROR_CHECK( esp_wifi_start() );                                            // 3.1. 根据当前配置启动WiFi
}

// 死循环任务，因为是RTOS系统，所以相当于多了一个不会关闭的线程。
static void smartconfig_example_task(void * parm)
{
    EventBits_t uxBits;
    ESP_ERROR_CHECK( esp_smartconfig_set_type(SC_TYPE_ESPTOUCH) );                  // 设置 Smart Config(智能配置) 协议类型 : 协议:ESPTouch
    smartconfig_start_config_t cfg = SMARTCONFIG_START_CONFIG_DEFAULT();            // 获取参数
    /*
    开启SmartConfig，配置ESP设备连接AP，需要通过手机APP广播信息。设备从空中嗅出包含目标AP的SSID和密码的特殊报文。
    */
    ESP_ERROR_CHECK( esp_smartconfig_start(&cfg) );                                 // 初始化 Smart Config(智能配置) 

    while (1) 
    {
        /* 块等待一个或多个位在先前创建的事件组中被设置。 */
        uxBits = xEventGroupWaitBits(s_wifi_event_group, CONNECTED_BIT | ESPTOUCH_DONE_BIT, true, false, portMAX_DELAY); 
        if(uxBits & CONNECTED_BIT) 
        {
            ESP_LOGI(TAG, "WiFi Connected to ap");
        }
        if(uxBits & ESPTOUCH_DONE_BIT) 
        {
            ESP_LOGI(TAG, "smartconfig over");
            esp_smartconfig_stop();                  // 停止SmartConfig，释放esp_smartconfig_start占用的缓冲区。
            vTaskDelete(NULL);
        }
    }
}

void app_main(void)
{
    ESP_ERROR_CHECK( nvs_flash_init() );            // 初始化默认NVS分区。
    initialise_wifi();                              // 调用函数
}

