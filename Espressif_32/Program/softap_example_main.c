/*  WiFi softAP Example

   This example code is in the Public Domain (or CC0 licensed, at your option.)

   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_log.h"
#include "nvs_flash.h"

#include "lwip/err.h"
#include "lwip/sys.h"

/* The examples use WiFi configuration that you can set via project configuration menu.
    示例使用WiFi配置，您可以通过项目配置菜单设置。
   If you'd rather not, just change the below entries to strings with the config you want - ie 

   #define EXAMPLE_WIFI_SSID "mywifissid"
*/
#define EXAMPLE_ESP_WIFI_SSID      CONFIG_ESP_WIFI_SSID             // wifi名称
#define EXAMPLE_ESP_WIFI_PASS      CONFIG_ESP_WIFI_PASSWORD         // wifi密码
#define EXAMPLE_ESP_WIFI_CHANNEL   CONFIG_ESP_WIFI_CHANNEL          // 通道？
#define EXAMPLE_MAX_STA_CONN       CONFIG_ESP_MAX_STA_CONN          // 允许连接的最大站数，默认4，最大10

static const char *TAG = "wifi softAP";

// 1.4. 创建应用程序任务            // 中断服务函数 
static void wifi_event_handler(void* arg, esp_event_base_t event_base,
                                    int32_t event_id, void* event_data)
{   
    if (event_id == WIFI_EVENT_AP_STACONNECTED)                     // 一个工作站连接到ESP32软ap 
    {
        wifi_event_ap_staconnected_t* event = (wifi_event_ap_staconnected_t*) event_data;
        ESP_LOGI(TAG, "station "MACSTR" join, AID=%d",              // 连接 join
                 MAC2STR(event->mac), event->aid);
    } 
    else if (event_id == WIFI_EVENT_AP_STADISCONNECTED)             // 一个从ESP32软ap断开的工作站
    {
        wifi_event_ap_stadisconnected_t* event = (wifi_event_ap_stadisconnected_t*) event_data;
        ESP_LOGI(TAG, "station "MACSTR" leave, AID=%d",             // 剩下 leave
                 MAC2STR(event->mac), event->aid);
    }
}

void wifi_init_softap(void)
{
    ESP_ERROR_CHECK(esp_netif_init());                      // 1.1. 初始化底层TCP/IP堆栈。
    ESP_ERROR_CHECK(esp_event_loop_create_default());       // 1.2. 创建默认事件循环。
    esp_netif_create_default_wifi_ap();                     // 1.3. 创建默认的WIFI AP。在任何init错误的情况下，此API将中止。

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();    // wifi init config default 获取Wifi初始化配置默认
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));                   // Init WiFi为WiFi驱动分配资源，如WiFi控制结构、RX/TX缓冲区、WiFi NVS结构等，该WiFi也启动WiFi任务。

    //1.4. 向默认循环注册一个事件处理程序实例。
    ESP_ERROR_CHECK(esp_event_handler_instance_register(WIFI_EVENT,             // 要为其注册处理程序的事件的基本id 。
                                                        ESP_EVENT_ANY_ID,       // 要为其注册处理程序的事件的id。
                                                        &wifi_event_handler,    // 当事件被分派时被调用的处理函数。
                                                        NULL,                   // 除事件数据外，在调用处理程序时传递给该处理程序的数据。
                                                        NULL));                 // 与注册事件处理程序和数据相关的事件处理程序实例对象可以是NULL。

    wifi_config_t wifi_config = {
        .ap = {
            .ssid = EXAMPLE_ESP_WIFI_SSID,                  // wifi 名字
            .ssid_len = strlen(EXAMPLE_ESP_WIFI_SSID),      // wifi 名字 的长度
            .channel = EXAMPLE_ESP_WIFI_CHANNEL,            // 设置为1~13，表示从指定的通道开始扫描，然后再连接AP。如果AP的通道未知，则设置为0。
            .password = EXAMPLE_ESP_WIFI_PASS,              // wifi 密码
            .max_connection = EXAMPLE_MAX_STA_CONN,         // 允许连接的最大站数，默认4，最大10
            .authmode = WIFI_AUTH_WPA_WPA2_PSK              /**<认证模式:WPA_WPA2_PSK */ // ESP32软ap的认证模式。软ap模式下不支持AUTH_WEP
        },
    };
    if (strlen(EXAMPLE_ESP_WIFI_PASS) == 0) {               // 如果明明为空，那 “认证模式” 就设为 开放模式
        wifi_config.ap.authmode = WIFI_AUTH_OPEN;
    }

    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_AP));       // 2.0. 设置WiFi工作模式。
    ESP_ERROR_CHECK(esp_wifi_set_config(ESP_IF_WIFI_AP, &wifi_config));         // 2.0. 配置ESP32 STA / AP的配置信息。
    ESP_ERROR_CHECK(esp_wifi_start());                      // 3.1. 根据当前配置启动WiFi

    ESP_LOGI(TAG, "wifi_init_softap finished. SSID:%s password:%s channel:%d",
             EXAMPLE_ESP_WIFI_SSID, EXAMPLE_ESP_WIFI_PASS, EXAMPLE_ESP_WIFI_CHANNEL);
}

void app_main(void)
{
    //Initialize NVS 初始化默认NVS分区。
    esp_err_t ret = nvs_flash_init();       

    /* !< NVS分区不包含任何空页。如果NVS分区被截断，可能会发生这种情况。擦除整个分区并再次调用nvs_flash_init。*/
    /* !< NVS分区包含新格式的数据，不能被此代码版本识别*/
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) 
    {
        /*擦除默认NVS分区。擦除默认NVS分区(标签为“NVS”)的所有内容。*/
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();                 // 重新初始化
    }
    ESP_ERROR_CHECK(ret);                       // 如果还没成功就报错

    ESP_LOGI(TAG, "ESP_WIFI_MODE_AP");
    wifi_init_softap();                         // 调用初始化函数
}
