#include "stm32f10x.h"                  // Device header
#include "TB6612.h"
void TB6612_GPIO_Init(void)
{
    GPIO_InitTypeDef  GPIO_InitStructure;
 	
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOC|RCC_APB2Periph_GPIOA|RCC_APB2Periph_GPIOF, ENABLE);	 //使能PB,PE端口时钟
	
     GPIO_InitStructure.GPIO_Pin = GPIO_Pin_4|GPIO_Pin_5;				 //LED0-->PB.5 端口配置
     GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP; 		 //推挽输出
     GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;		 //IO口速度为50MHz
     GPIO_Init(GPIOA, &GPIO_InitStructure);					 //根据设定参数ADC1
    GPIO_SetBits(GPIOA,GPIO_Pin_4|GPIO_Pin_5);
    
     GPIO_InitStructure.GPIO_Pin = GPIO_Pin_4|GPIO_Pin_2;	    		 //LED1-->PE.5 端口配置, 推挽输出
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP; 		 //推挽输出
     GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;		 //IO口速度为50MHz
     GPIO_Init(GPIOC, &GPIO_InitStructure);	  				 //推挽输出 ，IO口速度为50MHz	
     GPIO_SetBits(GPIOC,GPIO_Pin_4|GPIO_Pin_2);
    
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_9|GPIO_Pin_11|GPIO_Pin_13|GPIO_Pin_15;	    		 //LED1-->PE.5 端口配置, 推挽输出
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP; 		 //推挽输出
     GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;		 //IO口速度为50MHz
     GPIO_Init(GPIOF, &GPIO_InitStructure);	  				 //推挽输出 ，IO口速度为50MHz
    GPIO_SetBits(GPIOF,GPIO_Pin_9|GPIO_Pin_11|GPIO_Pin_13|GPIO_Pin_15);
}

void Turn_F(void)
{
    Motor1_IN1=1;
    Motor1_IN2=0;
    Motor2_IN1=1;
    Motor2_IN2=0;
    Motor3_IN1=1;
    Motor3_IN2=0;
    Motor4_IN1=1;
    Motor4_IN2=0;
}

void Turn_B(void)
{
    Motor1_IN1=0;
    Motor1_IN2=1;
    Motor2_IN1=0;
    Motor2_IN2=1;
    Motor3_IN1=0;
    Motor3_IN2=1;
    Motor4_IN1=0;
    Motor4_IN2=1;
}

void Turn_R(void)
{
    Motor1_IN1=1;
    Motor1_IN2=0;
    Motor2_IN1=0;
    Motor2_IN2=1;
    Motor3_IN1=1;
    Motor3_IN2=0;
    Motor4_IN1=0;
    Motor4_IN2=1;
}

void Turn_L(void)
{
    Motor1_IN1=0;
    Motor1_IN2=1;
    Motor2_IN1=1;
    Motor2_IN2=0;
    Motor3_IN1=0;
    Motor3_IN2=1;
    Motor4_IN1=1;
    Motor4_IN2=0;
}
