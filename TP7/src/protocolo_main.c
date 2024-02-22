
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
    init_platform();
    int Status;
    XUartLite_Initialize(&uart_module, 0);
    
    GPO_Value=0x00000000;
    GPO_Param=0x00000000;
    
    Status=XGpio_Initialize(&GpioInput, PORT_IN);
    if(Status!=XST_SUCCESS)
        return XST_FAILURE;
    
    Status=XGpio_Initialize(&GpioOutput, PORT_OUT);
    if(Status!=XST_SUCCESS)
        return XST_FAILURE;
    
    XGpio_SetDataDirection(&GpioOutput, 1, 0x00000000);
    XGpio_SetDataDirection(&GpioInput, 1, 0xFFFFFFFF);
    
    // Variables para lectura de GPIO 
    u32           value     = 0;
    unsigned char datEnviar = '\0';
    // Variables para escritura en GPIO
    unsigned char cabecera[1] = {'\0'};
    unsigned char funcion[1]  = {'a'};
    unsigned char data[2]     = {'\0'};
    u32           conver      = 0;
    
    while(1)
    {
        if(cabecera[0]!=0x05) // Detecta byte de start
        {
            read(stdin,cabecera,1);
        }
        else if(funcion[0]!=0x00 || funcion[0]!=0xFF) // Lee byte de función
        {
            read(stdin,funcion,1);
        }
        else if(funcion[0]==0x00) // Si es función de lectura, lee los switches
        {
            XGpio_DiscreteWrite(&GpioOutput, 1, (u32) 0x00000000);
            value     = XGpio_DiscreteRead(&GpioInput, 1);
            datEnviar = (char) (value&(0x0000000F));
            while(XUartLite_IsSending(&uart_module)){}
            XUartLite_Send(&uart_module, &(datEnviar),1);
        }
        else                      // Si es función de escritura, escribe los leds
        {
            for(unsigned char i=0; i<=1; i++)
                read(stdin,data[i],1);
            
            conver = (u32) ((data[1]<<8) | (data[0]));
            XGpio_DiscreteWrite(&GpioOutput, 1, conver);
        }
        
    }
    
    cleanup_platform();
    return 0;
}
