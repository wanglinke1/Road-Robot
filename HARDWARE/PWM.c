#include "stm32f10x.h"                  // Device header
#include "PWM.h"

//void TIM_PWM_Init(TIM_TypeDef* TIMx, u16 arr, u16 psc, 
//                  GPIO_TypeDef* GPIOx, u16 GPIO_Pin)
//{  
//    GPIO_InitTypeDef GPIO_InitStructure;
//    TIM_TimeBaseInitTypeDef  TIM_TimeBaseStructure;
//    TIM_OCInitTypeDef  TIM_OCInitStructure;

//    // 根据定时器选择使能对应 APB1 定时器时钟
//    if (TIMx == TIM2) {
//        RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2, ENABLE);
//    } else if (TIMx == TIM3) {
//        RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM3, ENABLE);
//    }

//    // 使能 GPIO 外设和 AFIO 复用功能模块时钟
//    if (GPIOx == GPIOA) {
//        RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA | RCC_APB2Periph_AFIO, ENABLE);
//    } else if (GPIOx == GPIOB) {
//        RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB | RCC_APB2Periph_AFIO, ENABLE);
//    }

//    // 设置引脚为复用推挽输出
//    GPIO_InitStructure.GPIO_Pin = GPIO_Pin;
//    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;  
//    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
//    GPIO_Init(GPIOx, &GPIO_InitStructure);

//    // 初始化定时器时基 
//    TIM_TimeBaseStructInit(&TIM_TimeBaseStructure);
//    TIM_TimeBaseStructure.TIM_Period = arr;             
//    TIM_TimeBaseStructure.TIM_Prescaler = psc;          
//    TIM_TimeBaseStructure.TIM_ClockDivision = 0;        
//    TIM_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_Up; 
//    TIM_TimeBaseInit(TIMx, &TIM_TimeBaseStructure);

//    // 初始化定时器 PWM 模式（通用配置，后续应用到 CH3 和 CH4）
//    TIM_OCStructInit(&TIM_OCInitStructure);
//    TIM_OCInitStructure.TIM_OCMode = TIM_OCMode_PWM1;   
//    TIM_OCInitStructure.TIM_Pulse = 0;                  
//    TIM_OCInitStructure.TIM_OutputState = TIM_OutputState_Enable; 
//    TIM_OCInitStructure.TIM_OCPolarity = TIM_OCPolarity_High; 

//    // 初始化 Channel3 PWM 模式并使能预装载
//    TIM_OC3Init(TIMx, &TIM_OCInitStructure);            
//    TIM_OC3PreloadConfig(TIMx, TIM_OCPreload_Enable);

//    // 初始化 Channel4 PWM 模式并使能预装载
//    TIM_OC4Init(TIMx, &TIM_OCInitStructure);            
//    TIM_OC4PreloadConfig(TIMx, TIM_OCPreload_Enable);

//    // 使能 PWM 输出和定时器
//    TIM_CtrlPWMOutputs(TIMx, ENABLE);
//    TIM_ARRPreloadConfig(TIMx, ENABLE);
//    TIM_Cmd(TIMx, ENABLE);
//}

void STM32_PWM_Configuration(TIM_TypeDef* TIMx, uint16_t autoReload, uint16_t prescaler,
                            GPIO_TypeDef* GPIOx, uint16_t GPIO_Pin)
{
    // 定义初始化结构体
    GPIO_InitTypeDef GPIO_InitPara;
    TIM_TimeBaseInitTypeDef TIM_TimeBasePara;
    TIM_OCInitTypeDef TIM_OCInitPara;

    // 使能定时器时钟
    if (TIMx == TIM2)
    {
        RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2, ENABLE);
    }
    else if (TIMx == TIM3)
    {
        RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM3, ENABLE);
    }

    // 使能GPIO和复用功能时钟
    if (GPIOx == GPIOA)
    {
        RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA | RCC_APB2Periph_AFIO, ENABLE);
    }
    else if (GPIOx == GPIOB)
    {
        RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB | RCC_APB2Periph_AFIO, ENABLE);
    }

    // 配置GPIO为复用推挽输出
    GPIO_InitPara.GPIO_Pin = GPIO_Pin;
    GPIO_InitPara.GPIO_Mode = GPIO_Mode_AF_PP;
    GPIO_InitPara.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOx, &GPIO_InitPara);

    // 配置定时器时基参数
    TIM_TimeBasePara.TIM_Period = autoReload;
    TIM_TimeBasePara.TIM_Prescaler = prescaler;
    TIM_TimeBasePara.TIM_ClockDivision = TIM_CKD_DIV1;
    TIM_TimeBasePara.TIM_CounterMode = TIM_CounterMode_Up;
    TIM_TimeBaseInit(TIMx, &TIM_TimeBasePara);

    // 配置PWM模式
    TIM_OCInitPara.TIM_OCMode = TIM_OCMode_PWM1;
    TIM_OCInitPara.TIM_OutputState = TIM_OutputState_Enable;
    TIM_OCInitPara.TIM_Pulse = 0;
    TIM_OCInitPara.TIM_OCPolarity = TIM_OCPolarity_High;

    // 初始化通道3并使能预装载
    TIM_OC3Init(TIMx, &TIM_OCInitPara);
    TIM_OC3PreloadConfig(TIMx, TIM_OCPreload_Enable);

    // 初始化通道4并使能预装载
    TIM_OC4Init(TIMx, &TIM_OCInitPara);
    TIM_OC4PreloadConfig(TIMx, TIM_OCPreload_Enable);

    // 使能自动重装载预装载和定时器
    TIM_ARRPreloadConfig(TIMx, ENABLE);
    //TIM_CtrlPWMOutputs(TIMx, ENABLE);
    TIM_Cmd(TIMx, ENABLE);
}
