
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
		   	   	case 0x01:
		   	   		i_func = data_in[1];

					i_data = 0x00 & 0x7FFFFF;
					write_GPIO(i_func, i_data);
				
					i_data = 0x01 & 0x7FFFFF;				// i_data para levantar nuevamente reset
					write_GPIO(i_func, i_data);


					write_GPIO(0x00, i_data);									// Campo función puesto a 0
				
					// Comprobación de transmisión
		            while(XUartLite_IsSending(&uart_module)){}					// Envía data_in [1]: opcion
		            XUartLite_Send(&uart_module, &(i_func),1);

				// Tx, Rx, Fase
		   	   	case 0x02:
		   	   	case 0x03:
		   	   	case 0x04:
		   			read(stdin,&data_in[2],1);									// Recibe el tercer byte

		   			i_func = data_in[1];

					i_data = data_in[2]& 0x7FFFFF;
					write_GPIO(i_func, i_data);


					write_GPIO(0x00, i_data);									// Campo función puesto a 0

					// Comprobación de transmisión
		            while(XUartLite_IsSending(&uart_module)){}					// Envía data_in [1]: opcion
		            XUartLite_Send(&uart_module, &(i_func),1);

				// Captura y envia BER
				case 0x05:
					i_func = data_in[1];

					// Comprobación de transmisión
		            while(XUartLite_IsSending(&uart_module)){}					// Envía data_in [1]: opcion
		            XUartLite_Send(&uart_module, &(i_func),1);


					i_data = 0x01 & 0x7FFFFF;
					write_GPIO(i_func, i_data);

					i_data = 0x00 & 0x7FFFFF;				  					// i_data para bajar bit capturar BER
					// Obtiene las BER
					get_BER(8, i_func, i_data)									// Hace un bucle de 8 veces para obtener la BER
																				// Dentro del buche, las envía


					write_GPIO(0x00, i_data);									// Campo función puesto a 0

					// Comprobación de transmisión
		            while(XUartLite_IsSending(&uart_module)){}					// Envía data_in [1]: opcion
		            XUartLite_Send(&uart_module, &(i_func),1);


				// Logueo memoria 
				case 0x06:
		   	   		i_func = data_in[1];


					i_data = 0x01 & 0x7FFFFF;
					write_GPIO(i_func, i_data);

					i_data = 0x00 & 0x7FFFFF;									// i_data para bajar bit capturar y loguear memoria
					write_GPIO(i_func, i_data);


					write_GPIO(0x00, i_data);									// Campo función puesto a 0

					// Comprobación de transmisión
		            while(XUartLite_IsSending(&uart_module)){}					// Envía data_in [1]: opcion
		            XUartLite_Send(&uart_module, &(i_func),1);


				//Chequeo memoria
				case 0x07:
		   		
		   			i_func = data_in[1];

					// Comprobación de transmisión
		            while(XUartLite_IsSending(&uart_module)){}					// Envía data_in [1]: opcion
		            XUartLite_Send(&uart_module, &(i_func),1);


					i_data = 0x00 & 0x7FFFFF;
					write_GPIO(i_func, i_data);
					
					// Se sobreescribe i_data
					i_data = (uint32_t)(XGpio_DiscreteRead(&GpioInput, 1));		// Compruebo si se lleno la memoria

					while(XUartLite_IsSending(&uart_module)){}
					XUartLite_Send(&uart_module, &(i_data),1);					// Envio bit


					write_GPIO(0x00, i_data);									// Campo función puesto a 0

					// Comprobación de transmisión
		            while(XUartLite_IsSending(&uart_module)){}					// Envía data_in [1]: opcion
		            XUartLite_Send(&uart_module, &(i_func),1);


				// Lee memoria
				case 0x08:
					i_func = data_in[1];

					// Comprobación de transmisión
		            while(XUartLite_IsSending(&uart_module)){}					// Envía data_in [1]: opcion
		            XUartLite_Send(&uart_module, &(i_func),1);


					i_data = 0x00 & 0x7FFFFF;

					get_data(32769,  i_func);							// Hace un bucle de 32769 veces para obtener la memoria
																		// Dentro del buche, las envía


					write_GPIO(0x00, i_data);									// Campo función puesto a 0

					// Comprobación de transmisión
					while(XUartLite_IsSending(&uart_module)){}					// Envía data_in [1]: opcion
					XUartLite_Send(&uart_module, &(i_func),1);

		   	   default:
			   		data_in[1] = 0xAA;
					while(XUartLite_IsSending(&uart_module)){}
					XUartLite_Send(&uart_module, &(data_in[1]),1);

			} // fin switch funcion
		   data_in[0]=!'\0';
		   data_in[1]=!'\0';


		}// fin del else

	}// find del while

	cleanup_platform();
	return 0;
}



void write_GPIO(unsigned char i_func, u32 i_data)
{

	u32           value;
	unsigned char i_enable;

	for (int i = 0; i < 3; ++i) {

		i_enable = (i == 1) ? 0x01 : 0x00;

		value = (u32) (i_func << 24) | (i_enable) << 23 | (i_data);
		XGpio_DiscreteWrite(&GpioOutput, 1, value);
	}

/*
	BLOQUE QUE ENVIA UNO DE LOS BYTES (106) ESCRITOS EN GPIO A LA UART
	value = (u32) (i_func << 24) | (i_enable) << 23 | (i_data);
	value_test[0] = (value >> 24)&0xFF;
	value_test[1] = (value >> 16)&0xFF;
	value_test[2] = (value >> 8)&0xFF;
	value_test[3] = (value)&0xFF;

	// Comprobación de transmisión al ciircuito DSP
	while(XUartLite_IsSending(&uart_module)){}					// Envía data_in [1]: opcion
	XUartLite_Send(&uart_module, &(value_test[1]),1);
*/
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
		XUartLite_Send(&uart_module, &(byte_ber[i]),1);
	}

}
