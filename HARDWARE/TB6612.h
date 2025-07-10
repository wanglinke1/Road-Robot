#ifndef __TB6612_H
#define __TB6612_H	 
#include "sys.h"                  // Device header
               // Device header

#define Motor1_IN1 PAout(4)
#define Motor1_IN2 PCout(4)
#define Motor2_IN1 PCout(2)
#define Motor2_IN2 PAout(5)
#define Motor3_IN1 PFout(15)
#define Motor3_IN2 PFout(13)
#define Motor4_IN1 PFout(9)
#define Motor4_IN2 PFout(11)

void TB6612_GPIO_Init(void);
void Turn_F(void);
void Turn_B(void);
void Turn_R(void);
void Turn_L(void);
		 		
                
#endif

