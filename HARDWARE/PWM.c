#include "stm32f10x.h"                  // Device header
#include "PWM.h"

//void TIM_PWM_Init(TIM_TypeDef* TIMx, u16 arr, u16 psc, 
//                  GPIO_TypeDef* GPIOx, u16 GPIO_Pin)
//{  
//    GPIO_InitTypeDef GPIO_InitStructure;
//    TIM_TimeBaseInitTypeDef  TIM_TimeBaseStructure;
//    TIM_OCInitTypeDef  TIM_OCInitStructure;

//    // ���ݶ�ʱ��ѡ��ʹ�ܶ�Ӧ APB1 ��ʱ��ʱ��
//    if (TIMx == TIM2) {
//        RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2, ENABLE);
//    } else if (TIMx == TIM3) {
//        RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM3, ENABLE);
//    }

//    // ʹ�� GPIO ����� AFIO ���ù���ģ��ʱ��
//    if (GPIOx == GPIOA) {
//        RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA | RCC_APB2Periph_AFIO, ENABLE);
//    } else if (GPIOx == GPIOB) {
//        RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB | RCC_APB2Periph_AFIO, ENABLE);
//    }

//    // ��������Ϊ�����������
//    GPIO_InitStructure.GPIO_Pin = GPIO_Pin;
//    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;  
//    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
//    GPIO_Init(GPIOx, &GPIO_InitStructure);

//    // ��ʼ����ʱ��ʱ�� 
//    TIM_TimeBaseStructInit(&TIM_TimeBaseStructure);
//    TIM_TimeBaseStructure.TIM_Period = arr;             
//    TIM_TimeBaseStructure.TIM_Prescaler = psc;          
//    TIM_TimeBaseStructure.TIM_ClockDivision = 0;        
//    TIM_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_Up; 
//    TIM_TimeBaseInit(TIMx, &TIM_TimeBaseStructure);

//    // ��ʼ����ʱ�� PWM ģʽ��ͨ�����ã�����Ӧ�õ� CH3 �� CH4��
//    TIM_OCStructInit(&TIM_OCInitStructure);
//    TIM_OCInitStructure.TIM_OCMode = TIM_OCMode_PWM1;   
//    TIM_OCInitStructure.TIM_Pulse = 0;                  
//    TIM_OCInitStructure.TIM_OutputState = TIM_OutputState_Enable; 
//    TIM_OCInitStructure.TIM_OCPolarity = TIM_OCPolarity_High; 

//    // ��ʼ�� Channel3 PWM ģʽ��ʹ��Ԥװ��
//    TIM_OC3Init(TIMx, &TIM_OCInitStructure);            
//    TIM_OC3PreloadConfig(TIMx, TIM_OCPreload_Enable);

//    // ��ʼ�� Channel4 PWM ģʽ��ʹ��Ԥװ��
//    TIM_OC4Init(TIMx, &TIM_OCInitStructure);            
//    TIM_OC4PreloadConfig(TIMx, TIM_OCPreload_Enable);

//    // ʹ�� PWM ����Ͷ�ʱ��
//    TIM_CtrlPWMOutputs(TIMx, ENABLE);
//    TIM_ARRPreloadConfig(TIMx, ENABLE);
//    TIM_Cmd(TIMx, ENABLE);
//}

void STM32_PWM_Configuration(TIM_TypeDef* TIMx, uint16_t autoReload, uint16_t prescaler,
                            GPIO_TypeDef* GPIOx, uint16_t GPIO_Pin)
{
    // �����ʼ���ṹ��
    GPIO_InitTypeDef GPIO_InitPara;
    TIM_TimeBaseInitTypeDef TIM_TimeBasePara;
    TIM_OCInitTypeDef TIM_OCInitPara;

    // ʹ�ܶ�ʱ��ʱ��
    if (TIMx == TIM2)
    {
        RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2, ENABLE);
    }
    else if (TIMx == TIM3)
    {
        RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM3, ENABLE);
    }

    // ʹ��GPIO�͸��ù���ʱ��
    if (GPIOx == GPIOA)
    {
        RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA | RCC_APB2Periph_AFIO, ENABLE);
    }
    else if (GPIOx == GPIOB)
    {
        RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB | RCC_APB2Periph_AFIO, ENABLE);
    }

    // ����GPIOΪ�����������
    GPIO_InitPara.GPIO_Pin = GPIO_Pin;
    GPIO_InitPara.GPIO_Mode = GPIO_Mode_AF_PP;
    GPIO_InitPara.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOx, &GPIO_InitPara);

    // ���ö�ʱ��ʱ������
    TIM_TimeBasePara.TIM_Period = autoReload;
    TIM_TimeBasePara.TIM_Prescaler = prescaler;
    TIM_TimeBasePara.TIM_ClockDivision = TIM_CKD_DIV1;
    TIM_TimeBasePara.TIM_CounterMode = TIM_CounterMode_Up;
    TIM_TimeBaseInit(TIMx, &TIM_TimeBasePara);

    // ����PWMģʽ
    TIM_OCInitPara.TIM_OCMode = TIM_OCMode_PWM1;
    TIM_OCInitPara.TIM_OutputState = TIM_OutputState_Enable;
    TIM_OCInitPara.TIM_Pulse = 0;
    TIM_OCInitPara.TIM_OCPolarity = TIM_OCPolarity_High;

    // ��ʼ��ͨ��3��ʹ��Ԥװ��
    TIM_OC3Init(TIMx, &TIM_OCInitPara);
    TIM_OC3PreloadConfig(TIMx, TIM_OCPreload_Enable);

    // ��ʼ��ͨ��4��ʹ��Ԥװ��
    TIM_OC4Init(TIMx, &TIM_OCInitPara);
    TIM_OC4PreloadConfig(TIMx, TIM_OCPreload_Enable);

    // ʹ���Զ���װ��Ԥװ�غͶ�ʱ��
    TIM_ARRPreloadConfig(TIMx, ENABLE);
    //TIM_CtrlPWMOutputs(TIMx, ENABLE);
    TIM_Cmd(TIMx, ENABLE);
}
