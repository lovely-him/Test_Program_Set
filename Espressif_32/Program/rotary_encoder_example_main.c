/* PCNT example -- Rotary Encoder
   This example code is in the Public Domain (or CC0 licensed, at your option.)
   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"


#pragma once            //C语言的头文件宏定义。类似 ifndef 和 idefine 的功能

#ifdef __cplusplus
extern "C" {
#endif

#include "esp_err.h"

/* 类型的旋转底层设备处理 */
typedef void *rotary_encoder_dev_t;

/* 类型旋转编码器配置 */
typedef struct {
    rotary_encoder_dev_t dev; /*!< Underlying device handle */
    int phase_a_gpio_num;     /*!< Phase A GPIO number */
    int phase_b_gpio_num;     /*!< Phase B GPIO number */
    int flags;                /*!< Extra flags */
} rotary_encoder_config_t;

/* 默认的旋转编码器配置 */
#define ROTARY_ENCODER_DEFAULT_CONFIG(dev_hdl, gpio_a, gpio_b) \
    {                                                          \
        .dev = dev_hdl,                                        \
        .phase_a_gpio_num = gpio_a,                            \
        .phase_b_gpio_num = gpio_b,                            \
        .flags = 0,                                            \
    }

/* 类型的旋转编码器手柄 */
typedef struct rotary_encoder_t rotary_encoder_t;

/* 旋转编码器的接口 */
struct rotary_encoder_t {
    
    esp_err_t (*set_glitch_filter)(rotary_encoder_t *encoder, uint32_t max_glitch_us);
    
    esp_err_t (*start)(rotary_encoder_t *encoder);
    
    esp_err_t (*stop)(rotary_encoder_t *encoder);
    
    esp_err_t (*del)(rotary_encoder_t *encoder);
    
    int (*get_counter_value)(rotary_encoder_t *encoder);
};


esp_err_t rotary_encoder_new_ec11(const rotary_encoder_config_t *config, rotary_encoder_t **ret_encoder);

#ifdef __cplusplus
}
#endif

#include <stdlib.h>
#include <string.h>
#include <sys/cdefs.h>
#include "esp_compiler.h"
#include "esp_log.h"
#include "driver/pcnt.h"
#include "hal/pcnt_hal.h"

static const char *TAG = "rotary_encoder";

#define ROTARY_CHECK(a, msg, tag, ret, ...)                                       \
    do {                                                                          \
        if (unlikely(!(a))) {                                                     \
            ESP_LOGE(TAG, "%s(%d): " msg, __FUNCTION__, __LINE__, ##__VA_ARGS__); \
            ret_code = ret;                                                       \
            goto tag;                                                             \
        }                                                                         \
    } while (0)

#define EC11_PCNT_DEFAULT_HIGH_LIMIT (100)
#define EC11_PCNT_DEFAULT_LOW_LIMIT  (-100)

typedef struct {
    int accumu_count;
    rotary_encoder_t parent;
    pcnt_unit_t pcnt_unit;
} ec11_t;

static esp_err_t ec11_set_glitch_filter(rotary_encoder_t *encoder, uint32_t max_glitch_us)
{
    esp_err_t ret_code = ESP_OK;
    ec11_t *ec11 = __containerof(encoder, ec11_t, parent);

    /* Configure and enable the input filter */ /*配置和启用输入过滤器*/
    ROTARY_CHECK(pcnt_set_filter_value(ec11->pcnt_unit, max_glitch_us * 80) == ESP_OK, "set glitch filter failed", err, ESP_FAIL);

    if (max_glitch_us) {
        pcnt_filter_enable(ec11->pcnt_unit);
    } else {
        pcnt_filter_disable(ec11->pcnt_unit);
    }

    return ESP_OK;
err:
    return ret_code;
}

static esp_err_t ec11_start(rotary_encoder_t *encoder)
{
    ec11_t *ec11 = __containerof(encoder, ec11_t, parent);      // 这个函数的功能好像是检查结构体是否正确。
    pcnt_counter_resume(ec11->pcnt_unit);                       // 开始计数
    return ESP_OK;
}

static esp_err_t ec11_stop(rotary_encoder_t *encoder)
{
    ec11_t *ec11 = __containerof(encoder, ec11_t, parent);
    pcnt_counter_pause(ec11->pcnt_unit);                        // 停止计数
    return ESP_OK;
}

static int ec11_get_counter_value(rotary_encoder_t *encoder)
{
    ec11_t *ec11 = __containerof(encoder, ec11_t, parent);
    int16_t val = 0;
    pcnt_get_counter_value(ec11->pcnt_unit, &val);              // 获取计数
    return val + ec11->accumu_count;
}

static esp_err_t ec11_del(rotary_encoder_t *encoder)
{
    ec11_t *ec11 = __containerof(encoder, ec11_t, parent);
    free(ec11);                                                 // 释放指针空间
    return ESP_OK;
}

static void ec11_pcnt_overflow_handler(void *arg)
{
    ec11_t *ec11 = (ec11_t *)arg;
    uint32_t status = 0;
    pcnt_get_event_status(ec11->pcnt_unit, &status);    // 读取事件寄存器

    if (status & PCNT_EVT_H_LIM) {                      // 进行与位取值，判断标志位有没有变
        ec11->accumu_count += EC11_PCNT_DEFAULT_HIGH_LIMIT;     // 如果累计满了，硬件会清零，为了能累加更多的数，设置一个变量来存累加数。
    } else if (status & PCNT_EVT_L_LIM) {
        ec11->accumu_count += EC11_PCNT_DEFAULT_LOW_LIMIT;
    }
}

esp_err_t rotary_encoder_new_ec11(const rotary_encoder_config_t *config, rotary_encoder_t **ret_encoder)
{
    esp_err_t ret_code = ESP_OK;
    ec11_t *ec11 = NULL;

    ROTARY_CHECK(config, "configuration can't be null", err, ESP_ERR_INVALID_ARG);
    ROTARY_CHECK(ret_encoder, "can't assign context to null", err, ESP_ERR_INVALID_ARG);

    ec11 = calloc(1, sizeof(ec11_t));
    ROTARY_CHECK(ec11, "allocate context memory failed", err, ESP_ERR_NO_MEM);

    ec11->pcnt_unit = (pcnt_unit_t)(config->dev);

    // 配置通道0
    // Configure channel 0
    pcnt_config_t dev_config = {
        .pulse_gpio_num = config->phase_a_gpio_num,     // 脉冲引脚设置为A相
        .ctrl_gpio_num = config->phase_b_gpio_num,      // 方向引脚设置为B相
        .channel = PCNT_CHANNEL_0,                      // 通道0
        .unit = ec11->pcnt_unit,
        .pos_mode = PCNT_COUNT_DEC,                     // PCNT正边计数模式 - 计数器模式:减少计数器值
        .neg_mode = PCNT_COUNT_INC,                     // PCNT负边缘计数模式 - 对抗模式:增加对抗值
        .lctrl_mode = PCNT_MODE_REVERSE,
        .hctrl_mode = PCNT_MODE_KEEP,
        .counter_h_lim = EC11_PCNT_DEFAULT_HIGH_LIMIT,
        .counter_l_lim = EC11_PCNT_DEFAULT_LOW_LIMIT,
    };
    ROTARY_CHECK(pcnt_unit_config(&dev_config) == ESP_OK, "config pcnt channel 0 failed", err, ESP_FAIL);

    // 配置通道1
    // Configure channel 1
    dev_config.pulse_gpio_num = config->phase_b_gpio_num;     // 脉冲引脚设置为B相
    dev_config.ctrl_gpio_num = config->phase_a_gpio_num;      // 方向引脚设置为A相
    dev_config.channel = PCNT_CHANNEL_1;                      // 通道1
    dev_config.pos_mode = PCNT_COUNT_INC;                     // PCNT正边计数模式 - 对抗模式:增加对抗值
    dev_config.neg_mode = PCNT_COUNT_DEC;                     // PCNT负边缘计数模式 - 计数器模式:减少计数器值
    ROTARY_CHECK(pcnt_unit_config(&dev_config) == ESP_OK, "config pcnt channel 1 failed", err, ESP_FAIL);

    // PCNT暂停和复位值
    // PCNT pause and reset value
    pcnt_counter_pause(ec11->pcnt_unit);
    pcnt_counter_clear(ec11->pcnt_unit);

    // 寄存器中断处理程序
    // register interrupt handler
    ROTARY_CHECK(pcnt_isr_service_install(0) == ESP_OK, "install isr service failed", err, ESP_FAIL);
    pcnt_isr_handler_add(ec11->pcnt_unit, ec11_pcnt_overflow_handler, ec11);

    /*在最大和最小限值上启用事件*/
    pcnt_event_enable(ec11->pcnt_unit, PCNT_EVT_H_LIM);
    pcnt_event_enable(ec11->pcnt_unit, PCNT_EVT_L_LIM);

    ec11->parent.del = ec11_del;                                // 设置函数指针？？？
    ec11->parent.start = ec11_start;
    ec11->parent.stop = ec11_stop;
    ec11->parent.set_glitch_filter = ec11_set_glitch_filter;
    ec11->parent.get_counter_value = ec11_get_counter_value;

    *ret_encoder = &(ec11->parent);                             // 再将结构体的地址给参数？局部变量的地址给了外部参数的话，那局部变量地址里的内容会保留？？
    return ESP_OK;
err:
    if (ec11) {
        free(ec11);
    }
    return ret_code;
}

static const char *TAG = "example";

void app_main(void)
{
    // 在本例中，旋转编码器底层设备由PCNT单元表示
    // Rotary encoder underlying device is represented by a PCNT unit in this example
    uint32_t pcnt_unit = 0;

    // 创建旋转编码器实例  , 有趣的结构体赋值方法，用宏定义。
    // Create rotary encoder instance
    rotary_encoder_config_t config = ROTARY_ENCODER_DEFAULT_CONFIG((rotary_encoder_dev_t)pcnt_unit, 14, 15);

    // 初始化外设，同时把函数地址也给到指针。
    rotary_encoder_t *encoder = NULL;
    ESP_ERROR_CHECK(rotary_encoder_new_ec11(&config, &encoder));        

    //过滤出故障(1us)
    // Filter out glitch (1us)
    ESP_ERROR_CHECK(encoder->set_glitch_filter(encoder, 1));

    // 开始编码器
    // Start encoder
    ESP_ERROR_CHECK(encoder->start(encoder));

    // Report counter value
    while (1) {
        ESP_LOGI(TAG, "Encoder value: %d", encoder->get_counter_value(encoder));    // 读值
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}