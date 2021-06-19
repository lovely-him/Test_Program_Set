/* Timer group-hardware timer example

   This example code is in the Public Domain (or CC0 licensed, at your option.)

   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/
#include <stdio.h>
#include "esp_types.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "driver/periph_ctrl.h"
#include "driver/timer.h"

#define TIMER_DIVIDER         16  //  Hardware timer clock divider 硬件定时器时钟分频器 
#define TIMER_SCALE           (TIMER_BASE_CLK / TIMER_DIVIDER)  // convert counter value to seconds 将计数器值转换为秒
#define TIMER_INTERVAL0_SEC   (3.4179) // sample test interval for the first timer 为第一个定时器取样测试间隔
#define TIMER_INTERVAL1_SEC   (5.78)   // sample test interval for the second timer 为第二个定时器取样测试间隔
#define TEST_WITHOUT_RELOAD   0        // testing will be done without auto reload 测试将在不自动重新加载的情况下完成
#define TEST_WITH_RELOAD      1        // testing will be done with auto reload 测试将自动重新加载

/*
 * A sample structure to pass events 传递事件的示例结构
 * from the timer interrupt handler to the main program. 从计时器中断处理程序到主程序。
 */
typedef struct {
    int type;  // the type of timer's event 定时器事件的类型
    int timer_group;
    int timer_idx;
    uint64_t timer_counter_value;
} timer_event_t;

xQueueHandle timer_queue;

/*
 * A simple helper function to print the raw timer counter value 一个简单的辅助函数，打印原始计时器计数器的值
 * and the counter value converted to seconds 和计数器值转换为秒
 */
static void inline print_timer_counter(uint64_t counter_value)
{
    printf("Counter: 0x%08x%08x\n", (uint32_t) (counter_value >> 32),
           (uint32_t) (counter_value));
    printf("Time   : %.8f s\n", (double) counter_value / TIMER_SCALE);
}

/*
 * Timer group0 ISR handler 定时器group0 ISR处理程序
 * 
 * Note: 注释
 * We don't call the timer API here because they are not declared with IRAM_ATTR.
 * If we're okay with the timer irq not being serviced while SPI flash cache is disabled,
 * we can allocate this interrupt without the ESP_INTR_FLAG_IRAM flag and use the normal API.
 * 这里我们不调用计时器API，因为它们没有使用 IRAM_ATTR 声明。
 * 如果我们可以接受定时器irq不被服务，而SPI flash缓存被禁用，
 * 我们可以在没有ESP_INTR_FLAG_IRAM标志的情况下分配这个中断，并使用普通的API。
 */
void IRAM_ATTR timer_group0_isr(void *para)
{
    timer_spinlock_take(TIMER_GROUP_0);                                                         // 和结尾的 timer_spinlock_give 搭配使用
    int timer_idx = (int) para;

    /* Retrieve the interrupt status and the counter value 获取中断状态和计数器值
       from the timer that reported the interrupt 从报告中断的定时器 */
    uint32_t timer_intr = timer_group_get_intr_status_in_isr(TIMER_GROUP_0);                        // 获取中断状态，只在ISR中使用。
    uint64_t timer_counter_value = timer_group_get_counter_value_in_isr(TIMER_GROUP_0, timer_idx);  // 获取当前的计数器值，只是在ISR中使用。

    /* Prepare basic event data 准备基本事件数据
       that will be then sent back to the main program task 然后将其发送回主程序任务 */
    timer_event_t evt;
    evt.timer_group = 0;
    evt.timer_idx = timer_idx;
    evt.timer_counter_value = timer_counter_value;

    /* Clear the interrupt 清除中断
       and update the alarm time for the timer with without reload 并更新定时器的报警时间与不重载 */
    if (timer_intr & TIMER_INTR_T0) {                                                           // 获取标志位
        evt.type = TEST_WITHOUT_RELOAD;
        timer_group_clr_intr_status_in_isr(TIMER_GROUP_0, TIMER_0);                             // 清除定时器中断状态，仅在ISR中使用。
        timer_counter_value += (uint64_t) (TIMER_INTERVAL0_SEC * TIMER_SCALE);
        timer_group_set_alarm_value_in_isr(TIMER_GROUP_0, timer_idx, timer_counter_value);     // 设置定时器的告警阈值，仅在ISR中使用。
    } else if (timer_intr & TIMER_INTR_T1) {
        evt.type = TEST_WITH_RELOAD;
        timer_group_clr_intr_status_in_isr(TIMER_GROUP_0, TIMER_1);                             // 清除定时器中断状态，仅在ISR中使用。
    } else {
        evt.type = -1; // not supported even type 类型都不支持
    }

    /* After the alarm has been triggered 当告警被触发后
      we need enable it again, so it is triggered the next time 我们需要再次启用它，以便下次触发它 */
    timer_group_enable_alarm_in_isr(TIMER_GROUP_0, timer_idx);                                  // 启用警报中断，仅在ISR中使用。

    /*现在只需将事件数据发送回主程序任务*/
    /* Now just send the event data back to the main program task */
    xQueueSendFromISR(timer_queue, &evt, NULL);                                                 // 队列发送
    timer_spinlock_give(TIMER_GROUP_0);                                                         // 和开头的 timer_spinlock_take 搭配使用
}

/*
 * Initialize selected timer of the timer group 0 初始化定时器组0所选定时器
 * 
 * timer_idx - the timer number to initialize  -初始化的定时器号
 * auto_reload - should the timer auto reload on alarm? 计时器应该在警报时自动重新加载吗?
 * timer_interval_sec - the interval of alarm to set 要设置的报警间隔
 */
static void example_tg0_timer_init(int timer_idx,
                                   bool auto_reload, double timer_interval_sec)
{
    /*初始化定时器的基本参数*/
    /* Select and initialize basic parameters of the timer */
    timer_config_t config = {
        .divider = TIMER_DIVIDER,           // 计数器时钟分频器。范围从2到65536。
        .counter_dir = TIMER_COUNT_UP,      // 计数方向
        .counter_en = TIMER_PAUSE,          // 使能定时器————————————————————————————开启这个后再初始化就会直接启动定时器
        .alarm_en = TIMER_ALARM_EN,         // 定时报警使
        .auto_reload = auto_reload,         // 定时器自动重载
        // .intr_type = TIMER_INTR_LEVEL,   // 参数只有一个枚举可以设置…………如果运行在告警模式下，请选择中断类型。
    }; // default clock source is APB 默认时钟源为APB，这个结构体有一个被屏蔽的参数，是用来设置时钟源的，应该是想保持默认
    timer_init(TIMER_GROUP_0, timer_idx, &config);      // ESP32 的定时器分为 2 组，每组 2 个。

    /* Timer's counter will initially start from value below. Timer的计数器将从下面的值开始。
       Also, if auto_reload is set, this value will be automatically reload on alarm 另外，如果设置了auto_reload，这个值将在告警时自动重新加载 */
    timer_set_counter_value(TIMER_GROUP_0, timer_idx, 0x00000000ULL);           // 指定定时器的首个计数值（同时这个值也是每次的重装载的值）

    /*设置告警值和中断告警。* /
    /* Configure the alarm value and the interrupt on alarm. */
    timer_set_alarm_value(TIMER_GROUP_0, timer_idx, timer_interval_sec * TIMER_SCALE);      // 但是还没使能，第三个参数是设置警告值。
                                                                                // 请勿搞混了，警告值和重装载值是不一样的。一个是结束值，一个是开始值。
    timer_enable_intr(TIMER_GROUP_0, timer_idx);                                // 允许定时中断，单独设置函数？
    /*
    寄存器定时器中断处理程序，这个处理程序是一个ISR。处理程序将被附加到运行此函数的同一CPU核心上。
    如果设置了 intr_alloc_flags 值 ESP_INTR_FLAG_IRAM ，则处理函数必须声明为 IRAM_ATTR 属性，并且只能调用 IRAM 或 ROM 中的函数。
    它不能调用其他计时器api。在这种情况下，使用直接注册访问从ISR内部配置计时器。

    如果使用此函数重新注册ISR，则需要编写完整的ISR。
    在中断处理程序中，您需要在处理之前调用timer_spinlock_take(..)，在处理之后调用timer_spinlock_give(…)。（在上面的中断函数中可以看到）
     */ 
    timer_isr_register(  
        TIMER_GROUP_0,              // 定时器组号
        timer_idx,                  // 定时器组的定时器索引
        timer_group0_isr,           // 中断处理程序函数
        (void *) timer_idx,         // 处理函数参数             // 注意，参数是无符合指针类型，所以先强制类型转换了，在中断函数再转回去。
        ESP_INTR_FLAG_IRAM,         // 用于分配中断的标志
        NULL);                      // 返回句柄的指针。

    timer_start(TIMER_GROUP_0, timer_idx);      // 使能定时器
}

/*
 * The main task of this example program 本示例程序的主要任务
 */
static void timer_example_evt_task(void *arg)
{
    while (1) {
        timer_event_t evt;
        xQueueReceive(timer_queue, &evt, portMAX_DELAY);            // 等待队列

        /*打印定时器报告的事件信息*/
        /* Print information that the timer reported an event */
        if (evt.type == TEST_WITHOUT_RELOAD) {
            printf("\n    Example timer without reload\n");
        } else if (evt.type == TEST_WITH_RELOAD) {
            printf("\n    Example timer with auto reload\n");
        } else {
            printf("\n    UNKNOWN EVENT TYPE\n");
        }
        printf("Group[%d], timer[%d] alarm event\n", evt.timer_group, evt.timer_idx);

        /*打印事件传递的定时器值*/
        /* Print the timer values passed by event */
        printf("------- EVENT TIME --------\n");
        print_timer_counter(evt.timer_counter_value);

        /*打印此任务可见的计时器值*/
        /* Print the timer values as visible by this task */
        printf("-------- TASK TIME --------\n");
        uint64_t task_counter_value;
        timer_get_counter_value(evt.timer_group, evt.timer_idx, &task_counter_value);   // 读取硬件定时器的计数器值。
        print_timer_counter(task_counter_value);
    }
}

/* 在这个例子中，我们将测试定时器group0的硬件timer0和timer1。
 * In this example, we will test hardware timer0 and timer1 of timer group0.
 */
void app_main(void)
{
    timer_queue = xQueueCreate(10, sizeof(timer_event_t));      // 创建队列
    example_tg0_timer_init(TIMER_0, TEST_WITHOUT_RELOAD, TIMER_INTERVAL0_SEC);      // 初始化 定时器组0 的 定时器0
    example_tg0_timer_init(TIMER_1, TEST_WITH_RELOAD,    TIMER_INTERVAL1_SEC);      // 初始化 定时器组0 的 定时器1
    xTaskCreate(timer_example_evt_task, "timer_evt_task", 2048, NULL, 5, NULL);     // 运行 主任务函数
}

