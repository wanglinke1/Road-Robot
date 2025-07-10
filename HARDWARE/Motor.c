#include "stm32f10x.h"                  // Device header
#include "Motor.h"
#include "TB6612.h"
#include <stdlib.h>
void SetCompare_Motor(void)
{
   TIM_SetCompare3(TIM2,Motor_s.compare4[0]);
   TIM_SetCompare4(TIM2,Motor_s.compare4[1]);
   TIM_SetCompare3(TIM3,Motor_s.compare4[2]);
   TIM_SetCompare4(TIM3,Motor_s.compare4[3]);
}

void Motor_judgedirc(void)
{
    uint8_t i;
    for(i=0;i<4;i++)
    {
        if(Motor_s.compare4[i]<=0)
        {
            Motor_s.compare4[i]=abs(Motor_s.compare4[i]);
            Motor_s.dirc4[i]=0;
        }
        else
        {
            Motor_s.dirc4[i]=1;
        }
    }
}

void Motor_SetDirc(void)
{
    if(Motor_s.dirc4[0]==0)
    {
        Motor1_IN1=0;
        Motor1_IN2=1;
    }
    else{
        Motor1_IN1=1;
        Motor1_IN2=0;
    }
    
    if(Motor_s.dirc4[1]==0)
    {
        Motor2_IN1=0;
        Motor2_IN2=1;
    }
    else{
        Motor2_IN1=1;
        Motor2_IN2=0;
    }
    
    if(Motor_s.dirc4[2]==0)
    {
        Motor3_IN1=0;
        Motor3_IN2=1;
    }
    else{
        Motor3_IN1=1;
        Motor3_IN2=0;
    }
    
    if(Motor_s.dirc4[3]==0)
    {
        Motor4_IN1=0;
        Motor4_IN2=1;
    }
    else{
        Motor4_IN1=1;
        Motor4_IN2=0;
    }
}

