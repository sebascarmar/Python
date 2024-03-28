
#include <stdio.h>
#include <string.h>
#include "xparameters.h"
#include "xil_cache.h"
#include "xgpio.h"
#include "platform.h"
#include "xuartlite.h"
#include "microblaze_sleep.h"

#define PORT_IN	 		XPAR_AXI_GPIO_0_DEVICE_ID //XPAR_GPIO_0_DEVICE_ID
#define PORT_OUT 		XPAR_AXI_GPIO_0_DEVICE_ID //XPAR_GPIO_0_DEVICE_ID

//Device_ID Operaciones
#define def_SOFT_RST            0
#define def_ENABLE_MODULES      1
#define def_LOG_RUN             2
#define def_LOG_READ            3

XGpio GpioOutput;
XGpio GpioParameter;
XGpio GpioInput;
u32 GPO_Value;
u32 GPO_Param;
XUartLite uart_module;

//Funcion para recibir 1 byte bloqueante
//XUartLite_RecvByte((&uart_module)->RegBaseAddress)

int main()
{
	int Status;
	GPO_Value=0x00000000;
	GPO_Param=0x00000000;
	unsigned char data_in[3] = {'\0'};
	u32           value;

	init_platform();

	XUartLite_Initialize(&uart_module, 0);


	Status=XGpio_Initialize(&GpioInput, PORT_IN);
	if(Status!=XST_SUCCESS)
        return XST_FAILURE;

	Status=XGpio_Initialize(&GpioOutput, PORT_OUT);
	if(Status!=XST_SUCCESS)
		return XST_FAILURE;

	XGpio_SetDataDirection(&GpioOutput, 1, 0x00000000);
	XGpio_SetDataDirection(&GpioInput, 1, 0xFFFFFFFF);


	while(1)
	{
		if(data_in[0] != 0x05)
		{
			read(stdin,&data_in[0],1);
		}
		else
		{
			read(stdin,&data_in[1],1);
			switch(data_in[1])
			{
		   	   case 0x55:
				   XGpio_DiscreteWrite(&GpioOutput,1, (u32) 0x00000000);
				   value = XGpio_DiscreteRead(&GpioInput, 1);
				   data_in[2]=(char)(value&(0x0000000F));

				   while(XUartLite_IsSending(&uart_module)){}
				   XUartLite_Send(&uart_module, &(data_in[1]),1);

				   while(XUartLite_IsSending(&uart_module)){}
				   XUartLite_Send(&uart_module, &(data_in[2]),1);
				   break;

		   	   case 0xAA:
		   		   read(stdin,&data_in[1],1);
		   		   read(stdin,&data_in[2],1);

		            value = (u32) ((data_in[1]<<8) | data_in[2])&0x0000FFFF;
		            XGpio_DiscreteWrite(&GpioOutput, 1, value);

		            data_in[1] = 0xAA;
		            while(XUartLite_IsSending(&uart_module)){}
		            XUartLite_Send(&uart_module, &(data_in[1]),1);

		   	   default:
		   		   while(XUartLite_IsSending(&uart_module)){}
		   		   XUartLite_Send(&uart_module, &(data_in[1]),1);
			} // fin switch funcion
		   data_in[0]=!'\0';


		}// fin del else

	}// find del while
	
	cleanup_platform();
	return 0;
}

