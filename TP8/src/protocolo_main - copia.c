
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
	unsigned char data_in[3]  = {'\0'};
	unsigned char data_mem[4] = {'\0'};
	u32			  i_data    ;
	unsigned char i_func    ;
	u64           i_bit_err_I = 0x1111222233334444;
    u64           i_bit_err_Q = 0x5555666677778888;
	u64           i_bit_tot_I = 0xAAAABBBBCCCCDDDD;
    u64           i_bit_tot_Q = 0xEEEEFFFFFFFFEEEE;
	u32           i_read_data_from_mem = 0xF0F0F0F0;




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
		if(data_in[0] != 0xBB)								// Si data_in [0] no comienza con 0xBB (da error con 0x01)
		{
			read(stdin,&data_in[0],1);						// Espera hasta comenzar en 0xBB
		}
		else												 
		{
			read(stdin,&data_in[1],1);						// Se lee el segundo byte recibido
			switch(data_in[1])
			{
				// Reset
		   			read(stdin,&data_in[1],1);									// Sobreesbribe, lee el tercer 
		   		   	read(stdin,&data_in[2],1);									// y cuarto byte

		            value = (u32) ((data_in[1]<<8) | data_in[2])&0x0000FFFF;	// Arma trama solo con leds 
		            XGpio_DiscreteWrite(&GpioOutput, 1, value);					// Enciende leds

		            data_in[1] = 0xAA;											// Actualiza valor
		            while(XUartLite_IsSending(&uart_module)){}					// Envía data_in [1]: opcion 
		            XUartLite_Send(&uart_module, &(data_in[1]),1);				// para comprobacion

				// Tx
		   	   	case 0xBB:
		   			read(stdin,&data_in[1],1);									// Sobreesbribe, lee el tercer
		   		   	read(stdin,&data_in[2],1);									// y cuarto byte

		            value = (u32) ((data_in[1]<<8) | data_in[2])&0x0000FFFF;	// Arma trama solo con leds 
		            XGpio_DiscreteWrite(&GpioOutput, 1, value);					// Enciende leds

		            data_in[1] = 0xBB;											// Actualiza valor
		            while(XUartLite_IsSending(&uart_module)){}					// Envía data_in [1]: opcion
		            XUartLite_Send(&uart_module, &(data_in[1]),1);				// para comprobacion

				// Rx
		   	   	case 0xCC:
		   			read(stdin,&data_in[1],1);									// Sobreesbribe, lee el tercer
		   		   	read(stdin,&data_in[2],1);									// y cuarto byte

		            value = (u32) ((data_in[1]<<8) | data_in[2])&0x0000FFFF;	// Arma trama solo con leds 
		            XGpio_DiscreteWrite(&GpioOutput, 1, value);					// Enciende leds

		            data_in[1] = 0xCC;											// Actualiza valor
		            while(XUartLite_IsSending(&uart_module)){}					// Envía data_in [1]: opcion
		            XUartLite_Send(&uart_module, &(data_in[1]),1);				// para comprobacion
				
				// Fase
		   	   	case 0xDD:
		   			read(stdin,&data_in[1],1);									// Sobreesbribe, lee el tercer
		   		   	read(stdin,&data_in[2],1);									// y cuarto byte

		            value = (u32) ((data_in[1]<<8) | data_in[2])&0x0000FFFF;	// Arma trama solo con leds 
		            XGpio_DiscreteWrite(&GpioOutput, 1, value);					// Enciende leds

		            data_in[1] = 0xDD;											// Actualiza valor
		            while(XUartLite_IsSending(&uart_module)){}					// Envía data_in [1]: opcion
		            XUartLite_Send(&uart_module, &(data_in[1]),1);				// para comprobacion


				// Guardar datos en memoria
				// Mostrar resultados

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
// Función que envia los impulsos necesarios para obtener la BER y luego enviarla
void get_BER(int i, unsigned char i_func, u32 i_data)
{
	uint32_t data_mem = 0;								

	for (int j = 0; j < i; ++j)
	{
		write_GPIO(i_func, i_data);									// Impulos para obtener 32 bits
		data_mem = (uint32_t)(XGpio_DiscreteRead(&GpioInput, 1));	// Leo los bits

		send_data(data_mem)						        			// Envio 32 bits
	}
}


// Función que envia los impulsos necesarios para leer la memoria y luego enviarla
void get_data(unsigned short int i, unsigned char i_func)
{
	uint32_t data_mem = 0;								

	for (unsigned short int j = 0; j < i; ++j)
	{
		write_GPIO(i_func, j);										// Impulos para obtener 32 bits
		data_mem = (uint32_t)(XGpio_DiscreteRead(&GpioInput, 1));	// Leo los bits

		send_data(data_mem)						        			// Envio 32 bits
	}
}


// Función que separa de a 1 byte y los envía
void send_data(uint32_t data_ber)
{
	uint32_t byte_ber [4] = {'\0'};

	byte_ber[0] = (data_ber >> 24)&0xFF;							// Separo en bytes
	byte_ber[1] = (data_ber >> 16)&0xFF;
	byte_ber[2] = (data_ber >> 8 )&0xFF;
	byte_ber[3] = (data_ber      )&0xFF;

	for(int i = 0; i < 4; ++i)
	{
		while(XUartLite_IsSending(&uart_module)){}					// Envía 1 byte
		XUartLite_Send(&uart_module, &(byte_ber[i]),2);
	}

}
