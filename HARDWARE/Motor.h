#ifndef __MOTOR_H__
#define __MOTOR_H__
#include "stm32f10x.h"                  // Device header
             // Device header

typedef struct{
	uint16_t compare4[4];
    uint8_t dirc4[4];
}Motor_Speed;

extern Motor_Speed Motor_s;

void SetCompare_Motor(void);
void Motor_judgedirc(void);
void Motor_SetDirc(void);



#endif
