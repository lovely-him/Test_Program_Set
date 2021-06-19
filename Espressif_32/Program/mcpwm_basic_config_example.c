/* MCPWM basic config example

   This example code is in the Public Domain (or CC0 licensed, at your option.)

   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/

/*
 * This example will show you how to use each submodule of MCPWM unit.
 * The example can't be used without modifying the code first.
 * Edit the macros at the top of mcpwm_example_basic_config.c to enable/disable the submodules which are used in the example.
 */

/* 总结，该历程展示了各个功能的初始化配置，和简单运用。 */

#include <stdio.h>
#include "string.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "esp_attr.h"
#include "soc/rtc.h"
#include "driver/mcpwm.h"
#include "soc/mcpwm_periph.h"

//使此1测试mcpwm载波子模块，设置高频载波参数
#define MCPWM_EN_CARRIER 0   //Make this 1 to test carrier submodule of mcpwm, set high frequency carrier parameters
//设为1，测试mcpwm的死时间子模块，设置死时间值和死时间模式
#define MCPWM_EN_DEADTIME 0  //Make this 1 to test deadtime submodule of mcpwm, set deadtime value and deadtime mode
//1 .测试mcpwm的故障子模块，在出现过流、过压等故障时对mcpwm信号设置动作
#define MCPWM_EN_FAULT 0     //Make this 1 to test fault submodule of mcpwm, set action on MCPWM signal on fault occurence like overcurrent, overvoltage, etc
//使此1 .测试mcpwm的同步子模块，同步定时器信号
#define MCPWM_EN_SYNC 0      //Make this 1 to test sync submodule of mcpwm, sync timer signals
//1 .测试mcpwm的捕获子模块，测量捕获信号上升/下降沿之间的时间
#define MCPWM_EN_CAPTURE 0   //Make this 1 to test capture submodule of mcpwm, measure time between rising/falling edge of captured signal
//选择使用哪个函数来初始化gpio信号
#define MCPWM_GPIO_INIT 0    //select which function to use to initialize gpio signals
//三个捕获信号
#define CAP_SIG_NUM 3   //Three capture signals

//捕获0中断位
#define CAP0_INT_EN BIT(27)  //Capture 0 interrupt bit
#define CAP1_INT_EN BIT(28)  //Capture 1 interrupt bit
#define CAP2_INT_EN BIT(29)  //Capture 2 interrupt bit

// GPIO 19设置为PWM0A
#define GPIO_PWM0A_OUT 19   //Set GPIO 19 as PWM0A
#define GPIO_PWM0B_OUT 18   //Set GPIO 18 as PWM0B
#define GPIO_PWM1A_OUT 17   //Set GPIO 17 as PWM1A
#define GPIO_PWM1B_OUT 16   //Set GPIO 16 as PWM1B
#define GPIO_PWM2A_OUT 15   //Set GPIO 15 as PWM2A
#define GPIO_PWM2B_OUT 14   //Set GPIO 14 as PWM2B
#define GPIO_CAP0_IN   23   //Set GPIO 23 as  CAP0
#define GPIO_CAP1_IN   25   //Set GPIO 25 as  CAP1
#define GPIO_CAP2_IN   26   //Set GPIO 26 as  CAP2
#define GPIO_SYNC0_IN   2   //Set GPIO 02 as SYNC0
#define GPIO_SYNC1_IN   4   //Set GPIO 04 as SYNC1
#define GPIO_SYNC2_IN   5   //Set GPIO 05 as SYNC2
#define GPIO_FAULT0_IN 32   //Set GPIO 32 as FAULT0
#define GPIO_FAULT1_IN 34   //Set GPIO 34 as FAULT1
#define GPIO_FAULT2_IN 34   //Set GPIO 34 as FAULT2

typedef struct {
    uint32_t capture_signal;
    mcpwm_capture_signal_t sel_cap_signal;
} capture;

xQueueHandle cap_queue;
#if MCPWM_EN_CAPTURE  // 测试mcpwm的捕获子模块，测量捕获信号上升/下降沿之间的时间
static mcpwm_dev_t *MCPWM[2] = {&MCPWM0, &MCPWM1};
#endif
/*
1.一个MPWn单元，将用于驱动电机。在ESP32上有两个单位可用 mcpwm_unit_t 枚举
2.1.通过调用在选定单元内初始化两个gpio作为输出信号 mcpwm_gpio_init 函数；.这两个输出信号通常用于命令电机向右或向左旋转。所有可用的信号选项列在 mcpwm_io_signals_t 枚举；
2.2.如果要一次设置多个引脚，请使用功能  mcpwm_set_pin 函数 和 mcpwm_pin_config_t 结构体。
3.选择一个计时器。在单元内有三个可用计时器。计时器列在列表中 mcpwm_timer_t 枚举（0-2）；
4. mcpwm_config_t 结构体 中 设置 定时器频率 和 初始负荷。
5. 使用上述参数调用 mcpwm_init() 以使配置生效。
*/
static void mcpwm_example_gpio_initialize(void)
{
    printf("initializing mcpwm gpio...\n");
#if MCPWM_GPIO_INIT   // 选择使用哪个函数来初始化gpio信号
    mcpwm_gpio_init(MCPWM_UNIT_0, MCPWM0A, GPIO_PWM0A_OUT); // 该函数初始化MCPWM的每个gpio信号。
    mcpwm_gpio_init(MCPWM_UNIT_0, MCPWM0B, GPIO_PWM0B_OUT); // 这个函数每次初始化一个gpio。
    mcpwm_gpio_init(MCPWM_UNIT_0, MCPWM1A, GPIO_PWM1A_OUT); // mcpwm_num:设置MCPWM单元(0-1)
    mcpwm_gpio_init(MCPWM_UNIT_0, MCPWM1B, GPIO_PWM1B_OUT); // io_signal:设置MCPWM信号，每个MCPWM单元有6个输出(MCPWMXA, MCPWMXB)和9个输入(SYNC_X, FAULT_X, CAP_X)其中X是timer_num(0-2)
    mcpwm_gpio_init(MCPWM_UNIT_0, MCPWM2A, GPIO_PWM2A_OUT); // gpio_num:设置为MCPWM配置gpio，如果你想使用gpio16, gpio_num = 16
    mcpwm_gpio_init(MCPWM_UNIT_0, MCPWM2B, GPIO_PWM2B_OUT);
    mcpwm_gpio_init(MCPWM_UNIT_0, MCPWM_CAP_0, GPIO_CAP0_IN); // 总结： mcpwm_gpio_init 函数可用来初始化当个引脚的pwm，简易快速的指定 MCPWM单元(0/1) 和 输出模块(A/B)，还有引脚。
    mcpwm_gpio_init(MCPWM_UNIT_0, MCPWM_CAP_1, GPIO_CAP1_IN);
    mcpwm_gpio_init(MCPWM_UNIT_0, MCPWM_CAP_2, GPIO_CAP2_IN);
    mcpwm_gpio_init(MCPWM_UNIT_0, MCPWM_SYNC_0, GPIO_SYNC0_IN);
    mcpwm_gpio_init(MCPWM_UNIT_0, MCPWM_SYNC_1, GPIO_SYNC1_IN);
    mcpwm_gpio_init(MCPWM_UNIT_0, MCPWM_SYNC_2, GPIO_SYNC2_IN);
    mcpwm_gpio_init(MCPWM_UNIT_0, MCPWM_FAULT_0, GPIO_FAULT0_IN);
    mcpwm_gpio_init(MCPWM_UNIT_0, MCPWM_FAULT_1, GPIO_FAULT1_IN);
    mcpwm_gpio_init(MCPWM_UNIT_0, MCPWM_FAULT_2, GPIO_FAULT2_IN);
#else
    mcpwm_pin_config_t pin_config = {
        .mcpwm0a_out_num = GPIO_PWM0A_OUT,   // 使用结构体快速一次性指定多个引脚，然后使用初始化函数一次完成。
        .mcpwm0b_out_num = GPIO_PWM0B_OUT, 
        .mcpwm1a_out_num = GPIO_PWM1A_OUT,
        .mcpwm1b_out_num = GPIO_PWM1B_OUT,
        .mcpwm2a_out_num = GPIO_PWM2A_OUT,
        .mcpwm2b_out_num = GPIO_PWM2B_OUT,
        .mcpwm_sync0_in_num  = GPIO_SYNC0_IN,
        .mcpwm_sync1_in_num  = GPIO_SYNC1_IN,
        .mcpwm_sync2_in_num  = GPIO_SYNC2_IN,
        .mcpwm_fault0_in_num = GPIO_FAULT0_IN,
        .mcpwm_fault1_in_num = GPIO_FAULT1_IN,
        .mcpwm_fault2_in_num = GPIO_FAULT2_IN,
        .mcpwm_cap0_in_num   = GPIO_CAP0_IN,
        .mcpwm_cap1_in_num   = GPIO_CAP1_IN,
        .mcpwm_cap2_in_num   = GPIO_CAP2_IN
    };
    mcpwm_set_pin(MCPWM_UNIT_0, &pin_config); // 设置MCPWM单元(0 - 1) MCPWM销结构
#endif
	// 使能下拉CAP0信号
    gpio_pulldown_en(GPIO_CAP0_IN);    //Enable pull down on CAP0   signal
    gpio_pulldown_en(GPIO_CAP1_IN);    //Enable pull down on CAP1   signal
    gpio_pulldown_en(GPIO_CAP2_IN);    //Enable pull down on CAP2   signal
    gpio_pulldown_en(GPIO_SYNC0_IN);   //Enable pull down on SYNC0  signal
    gpio_pulldown_en(GPIO_SYNC1_IN);   //Enable pull down on SYNC1  signal
    gpio_pulldown_en(GPIO_SYNC2_IN);   //Enable pull down on SYNC2  signal
    gpio_pulldown_en(GPIO_FAULT0_IN);  //Enable pull down on FAULT0 signal
    gpio_pulldown_en(GPIO_FAULT1_IN);  //Enable pull down on FAULT1 signal
    gpio_pulldown_en(GPIO_FAULT2_IN);  //Enable pull down on FAULT2 signal
}

/** rief设置gpio 12作为连续产生高低波形的测试信号，将gpio连接到捕获引脚。
 * @brief Set gpio 12 as our test signal that generates high-low waveform continuously, connect this gpio to capture pin.
 */
static void gpio_test_signal(void *arg)
{
    printf("intializing test signal...\n");
    gpio_config_t gp;					// 初始化普通引脚
    gp.intr_type = GPIO_INTR_DISABLE;
    gp.mode = GPIO_MODE_OUTPUT;
    gp.pin_bit_mask = GPIO_SEL_12;
    gpio_config(&gp);
    while (1) {
        //here the period of test signal is 20ms 这里测试信号的周期是20ms 
        gpio_set_level(GPIO_NUM_12, 1); //Set high
        vTaskDelay(10);             //delay of 10ms
        gpio_set_level(GPIO_NUM_12, 0); //Set low
        vTaskDelay(10);         //delay of 10ms
		// 总结，手动软件延时然后拉高拉低
    }
}

/** 当中断发生时，我们收到计数器的值，并显示两个上升边之间的时间
 * @brief When interrupt occurs, we receive the counter value and display the time between two rising edge
 */
static void disp_captured_signal(void *arg)
{
    uint32_t *current_cap_value = (uint32_t *)malloc(CAP_SIG_NUM*sizeof(uint32_t));
    uint32_t *previous_cap_value = (uint32_t *)malloc(CAP_SIG_NUM*sizeof(uint32_t));
    capture evt; // 创建一个结构体变量（实例）来接受队列中的数据
    while (1) {
        xQueueReceive(cap_queue, &evt, portMAX_DELAY); // x队列接收
        if (evt.sel_cap_signal == MCPWM_SELECT_CAP0) {
            current_cap_value[0] = evt.capture_signal - previous_cap_value[0];
            previous_cap_value[0] = evt.capture_signal;
            current_cap_value[0] = (current_cap_value[0] / 10000) * (10000000000 / rtc_clk_apb_freq_get());
            printf("CAP0 : %d us\n", current_cap_value[0]); // 打印出来
        }
        if (evt.sel_cap_signal == MCPWM_SELECT_CAP1) {
            current_cap_value[1] = evt.capture_signal - previous_cap_value[1];
            previous_cap_value[1] = evt.capture_signal;
            current_cap_value[1] = (current_cap_value[1] / 10000) * (10000000000 / rtc_clk_apb_freq_get());
            printf("CAP1 : %d us\n", current_cap_value[1]);
        }
        if (evt.sel_cap_signal == MCPWM_SELECT_CAP2) {
            current_cap_value[2] = evt.capture_signal -  previous_cap_value[2];
            previous_cap_value[2] = evt.capture_signal;
            current_cap_value[2] = (current_cap_value[2] / 10000) * (10000000000 / rtc_clk_apb_freq_get());
            printf("CAP2 : %d us\n", current_cap_value[2]);
        }
    }
}

#if MCPWM_EN_CAPTURE // 测试mcpwm的捕获子模块，测量捕获信号上升/下降沿之间的时间
/** 这是ISR处理函数，在这里我们检查中断触发了上升沿的CAP0信号，并根据采取行动
 * @brief this is ISR handler function, here we check for interrupt that triggers rising edge on CAP0 signal and according take action
 */
static void IRAM_ATTR isr_handler(void)
{
    uint32_t mcpwm_intr_status;
    capture evt;
    mcpwm_intr_status = MCPWM[MCPWM_UNIT_0]->int_st.val; //Read interrupt status 读中断状态
    if (mcpwm_intr_status & CAP0_INT_EN) { //Check for interrupt on rising edge on CAP0 signal 检查CAP0信号上升沿是否中断
		// 获取捕获信号计数器值
        evt.capture_signal = mcpwm_capture_signal_get_value(MCPWM_UNIT_0, MCPWM_SELECT_CAP0); //get capture signal counter value 
        evt.sel_cap_signal = MCPWM_SELECT_CAP0;	
        xQueueSendFromISR(cap_queue, &evt, NULL);
    }
    if (mcpwm_intr_status & CAP1_INT_EN) { //Check for interrupt on rising edge on CAP0 signal
        evt.capture_signal = mcpwm_capture_signal_get_value(MCPWM_UNIT_0, MCPWM_SELECT_CAP1); //get capture signal counter value
        evt.sel_cap_signal = MCPWM_SELECT_CAP1;
        xQueueSendFromISR(cap_queue, &evt, NULL);
    }
    if (mcpwm_intr_status & CAP2_INT_EN) { //Check for interrupt on rising edge on CAP0 signal
        evt.capture_signal = mcpwm_capture_signal_get_value(MCPWM_UNIT_0, MCPWM_SELECT_CAP2); //get capture signal counter value
        evt.sel_cap_signal = MCPWM_SELECT_CAP2;
        xQueueSendFromISR(cap_queue, &evt, NULL);
    }
    MCPWM[MCPWM_UNIT_0]->int_clr.val = mcpwm_intr_status;
	// 捕获功能可用于其他类型的电机或任务。该功能通过两个步骤启用:
	// 1. 通过调用mcpwm_gpio_init()或mcpwm_set_pin()函数，配置gpio作为捕获信号输入，这在配置一节中进行了描述。
	// 2. 通过调用mcpwm_capture_enable()启用功能本身，
	// 2.1. 两个枚举中: 从 mcpwm_capture_signal_t 选择所需的信号输入，使用 mcpwm_capture_on_edge_t 设置信号边缘和信号计数预分频器。
	// 3. 对于每个捕获事件，捕获计时器的值存储在时间戳寄存器中，
	// 3.1 .然后可以通过调用 mcpwm_capture_signal_get_value() 检查该寄存器。
	// 3.2 最后一个信号的边缘可以用 mcpwm_capture_signal_get_edge() 检查。

	// 总结：先初始化引脚，然后开启对应功能，再编写读取函数，调用函数再函数内读取就可以了。
}
#endif

/** 摘要 配置整个MCPWM模块
 * @brief Configure whole MCPWM module
 */
static void mcpwm_example_config(void *arg)
{
	// 1。mcpwm gpio初始化
    //1. mcpwm gpio initialization  
    mcpwm_example_gpio_initialize();

	// 2。初始化mcpwm配置
    //2. initialize mcpwm configuration
    printf("Configuring Initial Parameters of mcpwm...\n");

	// mcpwm_config_t结构中定时器频率和初始负荷的设置。
    mcpwm_config_t pwm_config;
    pwm_config.frequency = 1000;    //frequency = 1000Hz 1000赫兹频率
    pwm_config.cmpr_a = 60.0;       //duty cycle of PWMxA = 60.0% PWMxA占空比= 60.0%
    pwm_config.cmpr_b = 50.0;       //duty cycle of PWMxb = 50.0%
    pwm_config.counter_mode = MCPWM_UP_COUNTER; // 设置MCPWM计数器类型，
									//对于不对称MCPWM 或 
									//对于对称式MCPWM，频率为MCPWM设置频率的一半
    pwm_config.duty_mode = MCPWM_DUTY_MODE_0;  // 设定占空比类型 
									// 有源高占空比，即占空比与非对称MCPWM的高时间成正比 或 
									// 有源低占空比，即占空比与非对称MCPWM的低时间成正比，反相(倒)MCPWM
    mcpwm_init(MCPWM_UNIT_0, MCPWM_TIMER_0, &pwm_config);   //Configure PWM0A & PWM0B with above settings
									// 使用以上设置配置PWM0A和PWM0B

    pwm_config.frequency = 500;     //frequency = 500Hz
    pwm_config.cmpr_a = 45.9;       //duty cycle of PWMxA = 45.9%
    pwm_config.cmpr_b = 7.0;    //duty cycle of PWMxb = 07.0%
    pwm_config.counter_mode = MCPWM_UP_COUNTER;
    pwm_config.duty_mode = MCPWM_DUTY_MODE_0;
    mcpwm_init(MCPWM_UNIT_0, MCPWM_TIMER_1, &pwm_config);   //Configure PWM1A & PWM1B with above settings

    pwm_config.frequency = 400;     //frequency = 400Hz
    pwm_config.cmpr_a = 23.2;       //duty cycle of PWMxA = 23.2%
    pwm_config.cmpr_b = 97.0;       //duty cycle of PWMxb = 97.0%
    pwm_config.counter_mode = MCPWM_UP_DOWN_COUNTER; //frequency is half when up down count mode is set i.e. SYMMETRIC PWM
    pwm_config.duty_mode = MCPWM_DUTY_MODE_1;
    mcpwm_init(MCPWM_UNIT_0, MCPWM_TIMER_2, &pwm_config);   //Configure PWM2A & PWM2B with above settings
	// 总结： 先配置 mcpwm_config_t 结构体，再用 枚举 选择 设置MCPWM单元(0-1) 和 设置MCPWM定时器数(0-2)。最后初始化

#if MCPWM_EN_CARRIER  // 测试mcpwm载波子模块，设置高频载波参数
    //3. carrier configuration 载频配置
    //comment if you don't want to use carrier mode 如果你不想使用载波模式
    //in carrier mode very high frequency carrier signal is generated at mcpwm high level signal
	// 在载波模式下，MCPWM高电平信号产生非常高频的载波信号 （还不了解载波是什么，粗略看看，直接跳过）
    mcpwm_carrier_config_t chop_config;
    chop_config.carrier_period = 6;         //carrier period = (6 + 1)*800ns 载波周期 
    chop_config.carrier_duty = 3;           //carrier duty = (3)*12.5% 重负荷载体 
    chop_config.carrier_os_mode = MCPWM_ONESHOT_MODE_EN; //If one shot mode is enabled then set pulse width, if disabled no need to set pulse width
											// 如果开启了一次拍摄模式，请设置脉冲宽度，如果关闭了，则无需设置脉冲宽度    
	chop_config.pulse_width_in_os = 3;      //first pulse width = (3 + 1)*carrier_period
											// 第一脉冲宽度=(3 + 1)*载波周期
    chop_config.carrier_ivt_mode = MCPWM_CARRIER_OUT_IVT_EN; //output signal inversion enable 输出信号反转
    mcpwm_carrier_init(MCPWM_UNIT_0, MCPWM_TIMER_2, &chop_config);  //Enable carrier on PWM2A and PWM2B with above settings
											// 在PWM2A和PWM2B上使用上述设置使能运营商
    //use mcpwm_carrier_disable function to disable carrier on mcpwm timer on which it was enabled.
	// 使用McPwm_carrier_disable功能去使能MCPWM定时器的载波

	// 结构体 + 初始化，没有过多的操作
#endif

#if MCPWM_EN_DEADTIME // 测试mcpwm的死时间子模块，设置死时间值和死时间模式
    //4. deadtime configuration 死区时间配置
    //comment if you don't want to use deadtime submodule 如果你不想使用deadtime子模块，请注释
    //add rising edge delay or falling edge delay. There are 8 different types, each explained in mcpwm_deadtime_type_t in mcpwm.h
	// 增加上升沿延迟或下降沿延迟。有8种不同的类型，每种类型在mcpwm.h中的mcpwm_deadtime_type_t中解释

	// 在PWM2A和PWM2B上启用死时间，红色= (1000)*100ns
    mcpwm_deadtime_enable(MCPWM_UNIT_0, MCPWM_TIMER_2, MCPWM_BYPASS_FED, 1000, 1000);   //Enable deadtime on PWM2A and PWM2B with red = (1000)*100ns on PWM2A
	// 在PWM1B上使用fed = (2000)*100ns使死时间
    mcpwm_deadtime_enable(MCPWM_UNIT_0, MCPWM_TIMER_1, MCPWM_BYPASS_RED, 300, 2000);        //Enable deadtime on PWM1A and PWM1B with fed = (2000)*100ns on PWM1B
	// 启用死时间PWM0A和PWM0B与红色= (656)*100ns &馈电= (67)*100ns对PWM0A和PWM0B从PWM0A产生
    mcpwm_deadtime_enable(MCPWM_UNIT_0, MCPWM_TIMER_0, MCPWM_ACTIVE_RED_FED_FROM_PWMXA, 656, 67);  //Enable deadtime on PWM0A and PWM0B with red = (656)*100ns & fed = (67)*100ns on PWM0A and PWM0B generated from PWM0A
    //use mcpwm_deadtime_disable function to disable deadtime on mcpwm timer on which it was enabled
	//使用 McPwm_deadtime_disable 功能关闭MCPWM定时器的死时间

	// 死区也用的比较少，暂时跳过
#endif

#if MCPWM_EN_FAULT // 测试mcpwm的故障子模块，在出现过流、过压等故障时对mcpwm信号设置动作
    //5. enable fault condition 使能故障条件
	// 如果你不想使用fault子模块，你也可以注释fault gpio信号
    //comment if you don't want to use fault submodule, also u can comment the fault gpio signals
	// 当故障发生时，你可以配置MCPWM信号强制低电平，强制高电平或切换。
    //whenever fault occurs you can configure mcpwm signal to either force low, force high or toggle.
	// 在循环模式下，一旦故障状态结束，MCPWM信号就会恢复，而在一次性模式下，你需要重置。
    //in cycmode, as soon as fault condition is over, the mcpwm signal is resumed, whereas in oneshot mode you need to reset.
	// 当FAULT0信号出现高电平时，使能FAULT
    mcpwm_fault_init(MCPWM_UNIT_0, MCPWM_HIGH_LEVEL_TGR, MCPWM_SELECT_F0); //Enable FAULT, when high level occurs on FAULT0 signal
    mcpwm_fault_init(MCPWM_UNIT_0, MCPWM_HIGH_LEVEL_TGR, MCPWM_SELECT_F1); //Enable FAULT, when high level occurs on FAULT1 signal
    mcpwm_fault_init(MCPWM_UNIT_0, MCPWM_HIGH_LEVEL_TGR, MCPWM_SELECT_F2); //Enable FAULT, when high level occurs on FAULT2 signal
    // 发生FAULT0故障时，PWM1A和PWM1B的处理方法
    mcpwm_fault_set_oneshot_mode(MCPWM_UNIT_0, MCPWM_TIMER_1, MCPWM_SELECT_F0, MCPWM_FORCE_MCPWMXA_HIGH, MCPWM_FORCE_MCPWMXB_LOW); //Action taken on PWM1A and PWM1B, when FAULT0 occurs
    mcpwm_fault_set_oneshot_mode(MCPWM_UNIT_0, MCPWM_TIMER_1, MCPWM_SELECT_F1, MCPWM_FORCE_MCPWMXA_LOW, MCPWM_FORCE_MCPWMXB_HIGH); //Action taken on PWM1A and PWM1B, when FAULT1 occurs
    mcpwm_fault_set_oneshot_mode(MCPWM_UNIT_0, MCPWM_TIMER_0, MCPWM_SELECT_F2, MCPWM_FORCE_MCPWMXA_HIGH, MCPWM_FORCE_MCPWMXB_LOW); //Action taken on PWM0A and PWM0B, when FAULT2 occurs
    mcpwm_fault_set_oneshot_mode(MCPWM_UNIT_0, MCPWM_TIMER_0, MCPWM_SELECT_F1, MCPWM_FORCE_MCPWMXA_LOW, MCPWM_FORCE_MCPWMXB_HIGH); //Action taken on PWM0A and PWM0B, when FAULT1 occurs

	// 个人理解，感觉像是硬件实现了外部中断使能pwm，起到保护作用。以往这一步是人为再软件层面判断实现的。

	// 1. mcpwm_fault_input_level_t 枚举 配置gpio作为故障信号输入。
	// 1.1. 这是通过类似的方式来完成的，就像上面一节中描述的捕获信号。它包括设置触发中定义的故障的信号电平
	// 2. 通过调用任意一个来初始化错误处理程序 mcpwm_fault_set_oneshot_mode() 或 mcpwm_fault_set_cyc_mode()
	// 2.1. MCPWM单元的状态将被锁定直到重置 - mcpwm_fault_set_oneshot_mode()。（一次性直接卡死）
	// 2.2. 一旦故障信号变为非活动状态，MCPWM将恢复操作- mcpwm_fault_set_cyc_mode()。（还有退出的机会）

#endif

#if MCPWM_EN_SYNC // 测试mcpwm的同步子模块，同步定时器信号
    //6. Syncronization configuration 同步法配置
	// 注释如果你不想使用sync子模块，你也可以注释sync gpio信号
    //comment if you don't want to use sync submodule, also u can comment the sync gpio signals
	// 在PWM1A和PWM1B上同步
    //here synchronization occurs on PWM1A and PWM1B
	// 当同步0发生时，mcpwm定时器1的周期计数器的20%的负载计数器值
    mcpwm_sync_enable(MCPWM_UNIT_0, MCPWM_TIMER_1, MCPWM_SELECT_SYNC0, 200);    //Load counter value with 20% of period counter of mcpwm timer 1 when sync 0 occurs

	// 手册没有专门来讲述怎么配置。是嵌套在讨论怎么控制电机里讨论（还是注解的部分）

	// 同步运算子模块的输出，例如使PWM0A/B和PWM1A/B的上升边同时启动，或将它们彼此移动一个给定的相位。
	// 同步是由上面MCPWM框图中所示的SYNC SIGNALS触发的，并在mcpwm_sync_signal_t中定义。
	// 将信号附加到GPIO调用mcpwm_gpio_init()。然后可以使用mcpwm_sync_enable()函数启用同步。
	// 作为MCPWM单元的输入参数，定时器进行同步，同步信号和延时定时器的相位。

	// 总结：先初始化引脚，然后开启功能即可。也没有多余配置，也没有额外的服务函数要编写。(还不是很懂功能的运用)

#endif

#if MCPWM_EN_CAPTURE // 测试mcpwm的捕获子模块，测量捕获信号上升/下降沿之间的时间
    //7. Capture configuration  捕获 配置
	// 注释如果你不想使用capture子模块，你也可以注释捕获gpio信号
    //comment if you don't want to use capture submodule, also u can comment the capture gpio signals
	// 配置CAP0, CAP1和CAP2信号启动上升沿捕获计数器
    //configure CAP0, CAP1 and CAP2 signal to start capture counter on rising edge
    // 我们在GPIO 12上生成一个20ms的gpio_test_signal，并将其连接到捕获信号之一，disp_captured_function显示上升边缘之间的时间
	//we generate a gpio_test_signal of 20ms on GPIO 12 and connect it to one of the capture signal, the disp_captured_function displays the time between rising edge
	// 一般情况下，您可以将Capture连接到外部信号，测量上升沿或下降沿之间的时间，并采取相应的行动
    //In general practice you can connect Capture  to external signal, measure time between rising edge or falling edge and take action accordingly
	// 捕获信号上升边缘，前标度= 0即800000000计数等于1秒
    mcpwm_capture_enable(MCPWM_UNIT_0, MCPWM_SELECT_CAP0, MCPWM_POS_EDGE, 0);  //capture signal on rising edge, prescale = 0 i.e. 800,000,000 counts is equal to one second
    mcpwm_capture_enable(MCPWM_UNIT_0, MCPWM_SELECT_CAP2, MCPWM_POS_EDGE, 0);  //capture signal on rising edge, prescale = 0 i.e. 800,000,000 counts is equal to one second
    mcpwm_capture_enable(MCPWM_UNIT_0, MCPWM_SELECT_CAP1, MCPWM_POS_EDGE, 0);  //capture signal on rising edge, prescale = 0 i.e. 800,000,000 counts is equal to one second
    // 启用中断，这样每一个上升边发生中断就会被触发
	//enable interrupt, so each this a rising edge occurs interrupt is triggered
	// 对CAP0、CAP1和CAP2信号使能中断
    MCPWM[MCPWM_UNIT_0]->int_ena.val = CAP0_INT_EN | CAP1_INT_EN | CAP2_INT_EN;  //Enable interrupt on  CAP0, CAP1 and CAP2 signal
    mcpwm_isr_register(MCPWM_UNIT_0, isr_handler, NULL, ESP_INTR_FLAG_IRAM, NULL);  //Set ISR Handler 设置ISR处理程序

	// 总结： 前面已经对引脚初始化了，现在开启功能，再开启中断，设定中断函数，然后处理回调函数。
#endif
    vTaskDelete(NULL);
}

void app_main(void)
{
    printf("Testing MCPWM...\n");
	// 如果不想使用capture模块，请注释
    cap_queue = xQueueCreate(1, sizeof(capture)); //comment if you don't want to use capture module 
	// 如果不想使用capture模块，请注释  这是创建一个服务函数，里面接受队列消息，用来打印捕获到的内容。
    xTaskCreate(disp_captured_signal, "mcpwm_config", 4096, NULL, 5, NULL);  //comment if you don't want to use capture module
    // （这是创建一个服务函数，用来生成脉冲信号给捕获功能测试用）
	xTaskCreate(gpio_test_signal, "gpio_test_signal", 4096, NULL, 5, NULL); //comment if you don't want to use capture module
    
	// 初始化所有引脚（为什么不直接调用函数，还要弄个服务去执行？？？）
	xTaskCreate(mcpwm_example_config, "mcpwm_example_config", 4096, NULL, 5, NULL);
}

