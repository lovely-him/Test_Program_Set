/* ESP HTTP Client Example

   This example code is in the Public Domain (or CC0 licensed, at your option.)

   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/


#include <stdio.h>
#include "esp_wifi.h"
#include "esp_system.h"
#include "nvs_flash.h"
#include "esp_event.h"
#include "protocol_examples_common.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"
#include "freertos/event_groups.h"

#include "esp_log.h"
#include "esp_websocket_client.h"
#include "esp_event.h"

#define NO_DATA_TIMEOUT_SEC 10

static const char *TAG = "lovely_him";

static TimerHandle_t shutdown_signal_timer;
static SemaphoreHandle_t shutdown_sema;

static void shutdown_signaler(TimerHandle_t xTimer)
{
    ESP_LOGI(TAG, "No data received for %d seconds, signaling shutdown", NO_DATA_TIMEOUT_SEC);
    // 宏定义 释放信号量
    xSemaphoreGive(shutdown_sema);
}

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

static void websocket_event_handler(void *handler_args, esp_event_base_t base, int32_t event_id, void *event_data)
{
    esp_websocket_event_data_t *data = (esp_websocket_event_data_t *)event_data;
    switch (event_id) {
    case WEBSOCKET_EVENT_CONNECTED:
        ESP_LOGI(TAG, "WEBSOCKET_EVENT_CONNECTED");
        break;
    case WEBSOCKET_EVENT_DISCONNECTED:
        ESP_LOGI(TAG, "WEBSOCKET_EVENT_DISCONNECTED");
        break;
    case WEBSOCKET_EVENT_DATA:
        ESP_LOGI(TAG, "WEBSOCKET_EVENT_DATA");
        ESP_LOGI(TAG, "Received opcode=%d", data->op_code);
        ESP_LOGW(TAG, "Received=%.*s", data->data_len, (char *)data->data_ptr);
        ESP_LOGW(TAG, "Total payload length=%d, data_len=%d, current payload offset=%d\r\n", data->payload_len, data->data_len, data->payload_offset);

        xTimerReset(shutdown_signal_timer, portMAX_DELAY);
        break;
    case WEBSOCKET_EVENT_ERROR:
        ESP_LOGI(TAG, "WEBSOCKET_EVENT_ERROR");
        break;
    }
}

static void websocket_app_start(void)
{
    esp_websocket_client_config_t websocket_cfg = {};

    // 创建一个新的软件计时器实例，并返回一个句柄，通过这个句柄可以引用创建的软件计时器。
    shutdown_signal_timer = xTimerCreate("Websocket shutdown timer",                        // 只是一个文本名称，不被内核使用。
                                         NO_DATA_TIMEOUT_SEC * 1000 / portTICK_PERIOD_MS,   // 计时器周期(单位是tick)。
                                         pdFALSE,                                           // 计时器将在到期时自动重新加载。（不会）
                                         NULL,                                              // 为每个计时器分配一个唯一的id等于它的数组索引。
                                         shutdown_signaler);                                // 每个计时器在到期时调用同一个回调。
    // 创建一个新的二进制信号量实例，并返回一个句柄，通过这个句柄可以引用新的信号量。
    shutdown_sema = xSemaphoreCreateBinary();

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

    ESP_LOGI(TAG, "Connecting to %s...", websocket_cfg.uri);

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
}

void app_main(void)
{
    ESP_LOGI(TAG, "[APP] Startup..");
    ESP_LOGI(TAG, "[APP] Free memory: %d bytes", esp_get_free_heap_size());
    ESP_LOGI(TAG, "[APP] IDF version: %s", esp_get_idf_version());
    esp_log_level_set("*", ESP_LOG_INFO);
    esp_log_level_set("WEBSOCKET_CLIENT", ESP_LOG_DEBUG);
    esp_log_level_set("TRANS_TCP", ESP_LOG_DEBUG);

    ESP_ERROR_CHECK(nvs_flash_init());
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());

    /* This helper function configures Wi-Fi or Ethernet, as selected in menuconfig.
     * Read "Establishing Wi-Fi or Ethernet Connection" section in
     * examples/protocols/README.md for more information about this function.
     */
    ESP_ERROR_CHECK(example_connect());

    websocket_app_start();
}
