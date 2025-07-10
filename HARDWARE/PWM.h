#ifndef __PWM_H
#define __PWM_H
#include "stm32f10x.h"                  // Device header
                 // Device header


void STM32_PWM_Configuration(TIM_TypeDef* TIMx, uint16_t autoReload, uint16_t prescaler,
                            GPIO_TypeDef* GPIOx, uint16_t GPIO_Pin);
#endif
