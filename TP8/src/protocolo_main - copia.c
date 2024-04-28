
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
		if(data_in[0] != 0x01)												// Si data_in [0] no comienza con 0x01
		{
			read(stdin,&data_in[0],1);										// Espera hasta comenzar en 0x01
		}
		else
		{
			read(stdin,&data_in[1],1);										// Se recibe data_in [1] 
			switch(data_in[1])
			{
				// Reset
		   	   	case 0xAA:
		   			read(stdin,&data_in[1],1);									// Son leds en 0, no se usan 
		   		   	read(stdin,&data_in[2],1);

					data_in[1] = 0x0A;

		            value = (u32) ((data_in[1]<<8) | data_in[2])&0x0000FFFF;	// Arma trama solo con leds 
		            XGpio_DiscreteWrite(&GpioOutput, 1, value);					// Enciende leds

		            data_in[1] = 0xAA;											// Actualiza valor
		            while(XUartLite_IsSending(&uart_module)){}					// Envía data_in [1]: opcion
		            XUartLite_Send(&uart_module, &(data_in[1]),1);

				// Tx
		   	   	case 0xBB:
		   			read(stdin,&data_in[1],1);									// Son leds en 0, no se usan 
		   		   	read(stdin,&data_in[2],1);

					data_in[1] = 0x0B;

		            value = (u32) ((data_in[1]<<8) | data_in[2])&0x0000FFFF;	// Arma trama solo con leds 
		            XGpio_DiscreteWrite(&GpioOutput, 1, value);					// Enciende leds

		            data_in[1] = 0xBB;											// Actualiza valor
		            while(XUartLite_IsSending(&uart_module)){}					// Envía data_in [1]: opcion
		            XUartLite_Send(&uart_module, &(data_in[1]),1);

				// Rx
		   	   	case 0xCC:
		   			read(stdin,&data_in[1],1);									// Son leds en 0, no se usan 
		   		   	read(stdin,&data_in[2],1);

					data_in[1] = 0x0C;

		            value = (u32) ((data_in[1]<<8) | data_in[2])&0x0000FFFF;	// Arma trama solo con leds 
		            XGpio_DiscreteWrite(&GpioOutput, 1, value);					// Enciende leds

		            data_in[1] = 0xCC;											// Actualiza valor
		            while(XUartLite_IsSending(&uart_module)){}					// Envía data_in [1]: opcion
		            XUartLite_Send(&uart_module, &(data_in[1]),1);
				
				// Fase
		   	   	case 0xDD:
		   			read(stdin,&data_in[1],1);									// Son leds en 0, no se usan 
		   		   	read(stdin,&data_in[2],1);

					data_in[1] = 0x0D;

		            value = (u32) ((data_in[1]<<8) | data_in[2])&0x0000FFFF;	// Arma trama solo con leds 
		            XGpio_DiscreteWrite(&GpioOutput, 1, value);					// Enciende leds

		            data_in[1] = 0xDD;											// Actualiza valor
		            while(XUartLite_IsSending(&uart_module)){}					// Envía data_in [1]: opcion
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
