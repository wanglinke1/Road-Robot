#include "stm32f10x.h"                  // Device header
#include "USART.h"

/**
   * @brief		指数计算
   * @param		uint32_t x：底数
   * @param		uint32_t y：幂
   * @retval	uint32_t Result
   */
uint32_t Serial_Pow(uint32_t x,uint32_t y)
{
	uint32_t Result=1;
	while(y--)
	{
		Result *= x;
	}
	return Result;
}

/**
   * @brief		串口1初始化函数
   * @param		u32 BaudRate：串口1波特率
   * @retval	无
   */
void USART1_Init(u32 BaudRate)
{
	GPIO_InitTypeDef GPIO_InitStruct;
	USART_InitTypeDef USART_InitStruct;
	NVIC_InitTypeDef NVIC_InitStruct;
	
	//开启时钟
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA,ENABLE);
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_USART1,ENABLE);
	
	//配置GPIO
	GPIO_InitStruct.GPIO_Mode=GPIO_Mode_AF_PP;
	GPIO_InitStruct.GPIO_Pin=GPIO_Pin_9;
	GPIO_InitStruct.GPIO_Speed=GPIO_Speed_50MHz;
	GPIO_Init(GPIOA,&GPIO_InitStruct);
	
	GPIO_InitStruct.GPIO_Mode=GPIO_Mode_IN_FLOATING;
	GPIO_InitStruct.GPIO_Pin=GPIO_Pin_10;
	GPIO_InitStruct.GPIO_Speed=GPIO_Speed_50MHz;
	GPIO_Init(GPIOA,&GPIO_InitStruct);
	
	//配置串口通信协议
	USART_InitStruct.USART_BaudRate=BaudRate;
	USART_InitStruct.USART_HardwareFlowControl=USART_HardwareFlowControl_None;
	USART_InitStruct.USART_Mode=USART_Mode_Rx|USART_Mode_Tx;
	USART_InitStruct.USART_Parity=USART_Parity_No;
	USART_InitStruct.USART_StopBits=USART_StopBits_1;
	USART_InitStruct.USART_WordLength=USART_WordLength_8b;
	USART_Init(USART1,&USART_InitStruct);
	
	//使能串口
	USART_Cmd(USART1,ENABLE);
	
	//开启中断
	USART_ITConfig(USART1,USART_IT_RXNE,ENABLE);
	
	//配置优先级
	NVIC_InitStruct.NVIC_IRQChannel=USART1_IRQn;
	NVIC_InitStruct.NVIC_IRQChannelCmd=ENABLE;
	NVIC_InitStruct.NVIC_IRQChannelPreemptionPriority=0;
	NVIC_InitStruct.NVIC_IRQChannelSubPriority=1;
	NVIC_Init(&NVIC_InitStruct);
}

/**
   * @brief		串口2初始化函数
   * @param		u32 BaudRate：串口2波特率
   * @retval	无
   */
void USART2_Init(u32 BaudRate)
{
	GPIO_InitTypeDef GPIO_InitStruct;
	USART_InitTypeDef USART_InitStruct;
	NVIC_InitTypeDef NVIC_InitStruct;
	
	//开启时钟
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA,ENABLE);
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_USART2,ENABLE);
	
	//配置GPIO
	GPIO_InitStruct.GPIO_Mode=GPIO_Mode_AF_PP;
	GPIO_InitStruct.GPIO_Pin=GPIO_Pin_2;
	GPIO_InitStruct.GPIO_Speed=GPIO_Speed_50MHz;
	GPIO_Init(GPIOA,&GPIO_InitStruct);
	
	GPIO_InitStruct.GPIO_Mode=GPIO_Mode_IN_FLOATING;
	GPIO_InitStruct.GPIO_Pin=GPIO_Pin_3;
	GPIO_InitStruct.GPIO_Speed=GPIO_Speed_50MHz;
	GPIO_Init(GPIOA,&GPIO_InitStruct);
	
	//配置串口通信协议
	USART_InitStruct.USART_BaudRate=BaudRate;
	USART_InitStruct.USART_HardwareFlowControl=USART_HardwareFlowControl_None;
	USART_InitStruct.USART_Mode=USART_Mode_Rx|USART_Mode_Tx;
	USART_InitStruct.USART_Parity=USART_Parity_No;
	USART_InitStruct.USART_StopBits=USART_StopBits_1;
	USART_InitStruct.USART_WordLength=USART_WordLength_8b;
	USART_Init(USART2,&USART_InitStruct);
	
	//使能串口
	USART_Cmd(USART2,ENABLE);
	
	//开启中断
	USART_ITConfig(USART2,USART_IT_RXNE,ENABLE);
	
	//配置优先级
	NVIC_InitStruct.NVIC_IRQChannel=USART2_IRQn;
	NVIC_InitStruct.NVIC_IRQChannelCmd=ENABLE;
	NVIC_InitStruct.NVIC_IRQChannelPreemptionPriority=1;
	NVIC_InitStruct.NVIC_IRQChannelSubPriority=0;
	NVIC_Init(&NVIC_InitStruct);
}

/**
   * @brief		串口3初始化函数
   * @param		u32 BaudRate：串口3波特率
   * @retval	无
   */
void USART3_Init(u32 BaudRate)
{
	GPIO_InitTypeDef GPIO_InitStruct;
	USART_InitTypeDef USART_InitStruct;
	NVIC_InitTypeDef NVIC_InitStruct;
	
	//开启时钟
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB,ENABLE);
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_USART3,ENABLE);
	
	//配置GPIO
	GPIO_InitStruct.GPIO_Mode=GPIO_Mode_AF_PP;
	GPIO_InitStruct.GPIO_Pin=GPIO_Pin_10;
	GPIO_InitStruct.GPIO_Speed=GPIO_Speed_50MHz;
	GPIO_Init(GPIOB,&GPIO_InitStruct);
	
	GPIO_InitStruct.GPIO_Mode=GPIO_Mode_IN_FLOATING;
	GPIO_InitStruct.GPIO_Pin=GPIO_Pin_11;
	GPIO_InitStruct.GPIO_Speed=GPIO_Speed_50MHz;
	GPIO_Init(GPIOB,&GPIO_InitStruct);
	
	//配置串口通信协议
	USART_InitStruct.USART_BaudRate=BaudRate;
	USART_InitStruct.USART_HardwareFlowControl=USART_HardwareFlowControl_None;
	USART_InitStruct.USART_Mode=USART_Mode_Rx|USART_Mode_Tx;
	USART_InitStruct.USART_Parity=USART_Parity_No;
	USART_InitStruct.USART_StopBits=USART_StopBits_1;
	USART_InitStruct.USART_WordLength=USART_WordLength_8b;
	USART_Init(USART3,&USART_InitStruct);
	
	//使能串口
	USART_Cmd(USART3,ENABLE);
	
	//开启中断
	USART_ITConfig(USART3,USART_IT_RXNE,ENABLE);
	
	//配置优先级
	NVIC_InitStruct.NVIC_IRQChannel=USART3_IRQn;
	NVIC_InitStruct.NVIC_IRQChannelCmd=ENABLE;
	NVIC_InitStruct.NVIC_IRQChannelPreemptionPriority=1;
	NVIC_InitStruct.NVIC_IRQChannelSubPriority=0;
	NVIC_Init(&NVIC_InitStruct);
}

/**
   * @brief		发送字节
   * @param		uint8_t data：Byte
   * @retval	无
   */
void USART1_SendBits(uint8_t data)
{
	USART1->DR = data;
	while(USART_GetFlagStatus(USART1,USART_FLAG_TXE) == RESET);
}

/**
   * @brief		发送字节
   * @param		uint8_t data：Byte
   * @retval	无
   */
void USART2_SendBits(uint8_t data)
{
	USART2->DR = data;
	while(USART_GetFlagStatus(USART2,USART_FLAG_TXE) == RESET);
}

/**
   * @brief		发送字节
   * @param		uint8_t data：Byte
   * @retval	无
   */
void USART3_SendBits(uint8_t data)
{
	USART3->DR = data;
	while(USART_GetFlagStatus(USART3,USART_FLAG_TXE) == RESET);
}

/**
   * @brief		发送数组
   * @param		uint8_t *Array：数组首地址
   * @param		uint8_t Length：数组长度
   * @retval	无
   */
void USART1_SendArray(uint8_t *Array,uint8_t Length)
{
	uint8_t i;
	for(i=0;i<Length;i++)
	{
		USART1_SendBits(Array[i]);
	}
}

/**
   * @brief		发送数组
   * @param		uint8_t *Array：数组首地址
   * @param		uint8_t Length：数组长度
   * @retval	无
   */
void USART2_SendArray(uint8_t *Array,uint8_t Length)
{
	uint8_t i;
	for(i=0;i<Length;i++)
	{
		USART2_SendBits(Array[i]);
	}
}

/**
   * @brief		发送数组
   * @param		uint8_t *Array：数组首地址
   * @param		uint8_t Length：数组长度
   * @retval	无
   */
void USART3_SendArray(uint8_t *Array,uint8_t Length)
{
	uint8_t i;
	for(i=0;i<Length;i++)
	{
		USART3_SendBits(Array[i]);
	}
}

/**
   * @brief		发送字符串
   * @param		uint8_t *String：字符串首地址
   * @retval	无
   */
void USART1_SendString(uint8_t *String)
{
	uint8_t i;
	for(i=0;String[i]!='\0';i++)
	{
		USART1_SendBits(String[i]);
	}
}

/**
   * @brief		发送字符串
   * @param		uint8_t *String：字符串首地址
   * @retval	无
   */
void USART2_SendString(uint8_t *String)
{
	uint8_t i;
	for(i=0;String[i]!='\0';i++)
	{
		USART2_SendBits(String[i]);
	}
}

/**
   * @brief		发送字符串
   * @param		uint8_t *String：字符串首地址
   * @retval	无
   */
void USART3_SendString(uint8_t *String)
{
	uint8_t i;
	for(i=0;String[i]!='\0';i++)
	{
		USART3_SendBits(String[i]);
	}
}

/**
   * @brief		发送数字(字符串形式)
   * @param		uint32_t Number：数字
   * @param		uint8_t Length：长度
   * @retval	无
   */
void USART1_SendNum(uint32_t Number,uint8_t Length)
{
	uint8_t i;
	for(i=0;i<Length;i++)
	{
		USART1_SendBits(Number/Serial_Pow(10,Length-i-1)%10 + '0');
	}
}

/**
   * @brief		发送数字(字符串形式)
   * @param		uint32_t Number：数字
   * @param		uint8_t Length：长度
   * @retval	无
   */
void USART2_SendNum(uint32_t Number,uint8_t Length)
{
	uint8_t i;
	for(i=0;i<Length;i++)
	{
		USART2_SendBits(Number/Serial_Pow(10,Length-i-1)%10 + '0');
	}
}

/**
   * @brief		发送数字(字符串形式)
   * @param		uint32_t Number：数字
   * @param		uint8_t Length：长度
   * @retval	无
   */
void USART3_SendNum(uint32_t Number,uint8_t Length)
{
	uint8_t i;
	for(i=0;i<Length;i++)
	{
		USART3_SendBits(Number/Serial_Pow(10,Length-i-1)%10 + '0');
	}
}
