/* LEDC (LED Controller) fade example

   This example code is in the Public Domain (or CC0 licensed, at your option.)

   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/
#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/ledc.h"
#include "esp_err.h"

void app_main(void)
{
    int ch;

    /*
     * Prepare and set configuration of timers 准备和设置定时器的配置
     * that will be used by LED Controller 将被LED控制器使用
     */
    ledc_timer_config_t ledc_timer = {
        .duty_resolution = LEDC_TIMER_13_BIT,       // resolution of PWM duty PWM占空比分辨力
        .freq_hz = 5000,                            // frequency of PWM signal PWM信号频率
        .speed_mode = LEDC_HIGH_SPEED_MODE,         // timer mode 计时模式
        .timer_num = LEDC_TIMER_0,                  // timer index 计时器索引
        .clk_cfg = LEDC_AUTO_CLK,                   // Auto select the source clock 自动选择源时钟
    };
    // Set configuration of timer0 for high speed channels 设置高速通道的timer0配置
    ledc_timer_config(&ledc_timer);
    
    
    /*
     * Prepare individual configuration 准备个人配置
     * for each channel of LED Controller 用于LED控制器的每个通道
     * by selecting:
     * - controller's channel number 控制器的通道号
     * - output duty cycle, set initially to 0 输出占空比，初始设置为0
     * - GPIO number where LED is connected to LED所连接的GPIO编号
     * - speed mode, either high or low 速度模式，高或低
     * - timer servicing selected channel 定时器服务选定信道
     *   Note: if different channels use one timer, 注意:如果不同的通道使用一个定时器，
     *         then frequency and bit_num of these channels will be the same 那么这些通道的频率和bit_num将是相同的
     */
    ledc_channel_config_t ledc_channel[2] = {
        {
            .channel    = LEDC_CHANNEL_0,
            .duty       = 0,
            .gpio_num   = 5,
            .speed_mode = LEDC_HIGH_SPEED_MODE,
            .hpoint     = 0,
            .timer_sel  = LEDC_TIMER_0
        },
        {
            .channel    = LEDC_CHANNEL_1,
            .duty       = 0,
            .gpio_num   = 18,
            .speed_mode = LEDC_HIGH_SPEED_MODE,
            .hpoint     = 0,
            .timer_sel  = LEDC_TIMER_0
        }
    };

    // Set LED Controller with previously prepared configuration 设置LED控制器与事先准备的配置
    for (ch = 0; ch < 2; ch++) {
        ledc_channel_config(&ledc_channel[ch]);
    }

    // Initialize fade service. 初始化服务消退。
    ledc_fade_func_install(0);

    while (1) {
        printf("1. LEDC fade up to duty = %d\n", 4000);
        ledc_set_fade_with_time(
            ledc_channel[0].speed_mode,                 // 使用硬件改变 PWM 占空比
            ledc_channel[0].channel, 
            4000, 
            3000);
        ledc_fade_start(
            ledc_channel[0].speed_mode,
            ledc_channel[0].channel, 
            LEDC_FADE_NO_WAIT);
        vTaskDelay(3000 / portTICK_PERIOD_MS);

        printf("3. LEDC set duty = %d without fade\n", 4000);
        ledc_set_duty(  
            ledc_channel[1].speed_mode,                //使用软件改变 PWM 占空比
            ledc_channel[1].channel, 
            4000);
        ledc_update_duty(   
            ledc_channel[1].speed_mode, 
            ledc_channel[1].channel);
        vTaskDelay(1000 / portTICK_PERIOD_MS);

        printf("2. LEDC fade down to duty = 0\n");
        ledc_set_fade_with_time(
            ledc_channel[0].speed_mode,
            ledc_channel[0].channel,
            0, 
            3000);
        ledc_fade_start(
            ledc_channel[0].speed_mode,
            ledc_channel[0].channel, 
            LEDC_FADE_NO_WAIT);
        vTaskDelay(3000 / portTICK_PERIOD_MS);

        printf("4. LEDC set duty = 0 without fade\n");
        ledc_set_duty(
            ledc_channel[1].speed_mode, 
            ledc_channel[1].channel, 
            0);
        ledc_update_duty(
            ledc_channel[1].speed_mode, 
            ledc_channel[1].channel);
        vTaskDelay(1000 / portTICK_PERIOD_MS);
    }
}