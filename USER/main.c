#include "stm32f10x.h"
#include "USART.h"
#include "PWM.h"
#include "Motor.h"
#include "TB6612.h"
#include <stdlib.h>
uint8_t i=0;
Motor_Speed Motor_s;
USART_Data_TypeDef USART_Data;
int16_t reconstruct_int16(uint8_t high_byte, uint8_t low_byte) {
    // 合并高低字节为uint16_t
    int16_t combined = (int16_t )((high_byte << 8) | low_byte);
    
    // 强制转换为int16_t，自动处理补码
    return (int16_t)combined;
}

uint16_t Compare1 = 0;
uint16_t Compare2 = 0;
uint16_t Compare3 = 0;
uint16_t Compare4 = 0;

int main(void)
{	
    NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);		//优先级初始化
    USART1_Init(115200);
    // 初始化 TIM2：PA2、PA3 引脚，对应 TIM2_CH3、TIM2_CH4
    STM32_PWM_Configuration(TIM2, 32768, 0,
                            GPIOA, GPIO_Pin_2|GPIO_Pin_3);
    STM32_PWM_Configuration(TIM3, 32768, 0,
                            GPIOB, GPIO_Pin_0|GPIO_Pin_1);
//    delay_init();
    TB6612_GPIO_Init();
    Turn_F();
    TIM_SetCompare3(TIM2,0);
    TIM_SetCompare4(TIM2,0);
    TIM_SetCompare3(TIM3,0);
    TIM_SetCompare4(TIM3,0);
    while(1)
	{
//        if(USART_Data.USART1_RxFlag == 1)
//        {
//            TIM_SetCompare3(TIM2,Compare);
//            TIM_SetCompare4(TIM2,Compare);
//            TIM_SetCompare3(TIM3,Compare);
//            TIM_SetCompare4(TIM3,Compare);
//            USART_Data.USART1_RxFlag = 0;
//        }
	    if(USART_Data.USART1_RxFlag == 1)
        {
            int16_t Temp = USART_Data.USART1_RxPacket[0] << 8 | USART_Data.USART1_RxPacket[1];
            if(Temp == 0x00)
            {
                USART1_SendBits(0x01);
            }
            if(Temp >= 0)
            {
                Motor1_IN1=1;
                Motor1_IN2=0;
            }
            else
            {
                Motor1_IN1=0;
                Motor1_IN2=1;
            }
            Compare1 = (uint16_t)(abs(Temp));
            
            TIM_SetCompare3(TIM2, Compare1);
            
            Temp = USART_Data.USART1_RxPacket[2] << 8 | USART_Data.USART1_RxPacket[3];
            if(Temp >= 0)
            {
                Motor2_IN1=1;
                Motor2_IN2=0;
            }
            else
            {
                Motor2_IN1=0;
                Motor2_IN2=1;
            }
            Compare2 = (uint16_t)(abs(Temp));
            TIM_SetCompare4(TIM2, Compare2);
            
            Temp = USART_Data.USART1_RxPacket[4] << 8 | USART_Data.USART1_RxPacket[5];
            if(Temp >= 0)
            {
                Motor3_IN1=1;
                Motor3_IN2=0;
            }
            else
            {
                Motor3_IN1=0;
                Motor3_IN2=1;
            }
            Compare3 = (uint16_t)(abs(Temp));
            TIM_SetCompare3(TIM3, Compare3);
            
            Temp = USART_Data.USART1_RxPacket[6] << 8 | USART_Data.USART1_RxPacket[7];
            if(Temp >= 0)
            {
                Motor4_IN1=1;
                Motor4_IN2=0;
            }
            else
            {
                Motor4_IN1=0;
                Motor4_IN2=1;
            }
            Compare4 = (uint16_t)(abs(Temp));
            TIM_SetCompare4(TIM3, Compare4);
            
//            for(i=0;i<4;i++)
//            {
//                Motor_s.compare4[i]=reconstruct_int16(USART_Data.USART1_RxPacket[2*i],USART_Data.USART1_RxPacket[2*i+1]);
//            }
//            Motor_judgedirc();
//            Motor_SetDirc();
//            delay_ms(100);
//            SetCompare_Motor();
//            if(Motor_s.compare4[0] == 0x0356)
//            {
//                USART1_SendBits(0xff);
//            }
            USART1_SendArray(USART_Data.USART1_RxPacket,8);
            USART_Data.USART1_RxFlag =0;
            
            
        }

        

	}
}

void USART1_IRQHandler(void)
{
//    if(USART_GetITStatus(USART1,USART_IT_RXNE) == SET)
//	{
//        uint8_t RX1Data = USART_ReceiveData(USART1);
//        if(RX1Data == 0x00)
//        {
//            Compare -= 1000;
//        }
//        else if(RX1Data == 0x01)
//        {
//            Compare += 1000;
//        }
//        USART_Data.USART1_RxFlag = 1;
//        USART_ClearITPendingBit(USART1,USART_IT_RXNE);
//    }
	static uint8_t RX1State=0;
	static uint8_t pRX1Packet=0;
	USART_Data.USART1_RxFlag = 0;
	if(USART_GetITStatus(USART1,USART_IT_RXNE) == SET)
	{

		uint8_t RX1Data = USART_ReceiveData(USART1);
		if(RX1State == 0)				//接收包头
		{
			if(RX1Data == 0xFF)
			{
				RX1State =1;
			}
		}
        else if(RX1State==1)
        {
            if(RX1Data==0x01)
            {
                RX1State=2;
                pRX1Packet=0;
            }
            else
            {
                RX1State=0;
            }
        }
		else if(RX1State == 2)			//接收数据
		{
			USART_Data.USART1_RxPacket[pRX1Packet] = RX1Data;
			pRX1Packet++;
			if(pRX1Packet>=8)						
			{
				RX1State=3;
			}
		}
		else if(RX1State == 3)						//接收包尾
		{
			if(RX1Data == 0xFE)
			{
				RX1State = 0;
				USART_Data.USART1_RxFlag = 1;
			}
		}
		USART_ClearITPendingBit(USART1,USART_IT_RXNE);
	}
}
