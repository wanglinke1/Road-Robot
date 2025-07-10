#ifndef __USART_H__
#define __USART_H__

typedef struct{
	uint8_t USART1_RxPacket[10];
	uint8_t USART1_TxPacket[10];
	uint8_t USART1_RxFlag;
	uint8_t USART1_State;
	uint8_t USART1_pPacket;
	
	uint8_t USART2_RxPacket[9];
	uint8_t USART2_TxPacket[8];
	uint8_t USART2_RxFlag;
	uint8_t USART2_State;
	uint8_t USART2_pPacket;
	
	uint8_t USART3_RxPacket[9];
	uint8_t USART3_TxPacket[8];
	uint8_t USART3_RxFlag;
	uint8_t USART3_State;
	uint8_t USART3_pPacket;
}USART_Data_TypeDef;	

extern USART_Data_TypeDef USART_Data;

void USART1_Init(u32 BaudRate);
void USART1_SendBits(uint8_t data);
void USART1_SendArray(uint8_t *Array,uint8_t Length);
void USART1_SendString(uint8_t *String);
void USART1_SendNum(uint32_t Number,uint8_t Length);
void USART1_SendPacket(uint8_t data);

void USART2_Init(u32 BaudRate);
void USART2_SendBits(uint8_t data);
void USART2_SendArray(uint8_t *Array,uint8_t Length);
void USART2_SendString(uint8_t *String);
void USART2_SendNum(uint32_t Number,uint8_t Length);
void USART2_SendPacket(uint8_t data);

void USART3_Init(u32 BaudRate);
void USART3_SendBits(uint8_t data);
void USART3_SendArray(uint8_t *Array,uint8_t Length);
void USART3_SendString(uint8_t *String);
void USART3_SendNum(uint32_t Number,uint8_t Length);
void USART3_SendPacket(uint8_t data);

#endif
