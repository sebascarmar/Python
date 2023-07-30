import time
import serial
import calculadora
import multiplesGraficos
from os import system, name 



#**************************************************************************************************************#
########################################### Definición de funciones ############################################
#**************************************************************************************************************#

def clear():  # Función que permite limpiar la pantalla.
    if name == 'nt': 
        x = system('cls') 
    else: 
        x = system('clear') 

#______________________________________________________________________________________________________________#

def escribePuertoSerie():
    print('********************* ESCRITURA EN PUERTO SERIE *********************')
    print('Ingrese alguno de estos comandos para ser enviados por puerto serie:')
    print('\t 1:    para ejecutar la calculadora')
    print('\t 2:    para ejecutar el multi-plot')
    print('\t exit: para salir\n\t')
    data = input("\t > ")

    pSerie.write(data.encode()) # Función que envía por puerto serie byte a byte lo ingresado.

#______________________________________________________________________________________________________________#

def leePuertoSerie():
    aux = ''
    while ser.inWaiting() > 0:
        read_data = ser.read(1)
        aux += read_data.decode()

    return aux


#**************************************************************************************************************#
############################################## Programa Principal ##############################################
#**************************************************************************************************************#

ser = serial.serial_for_url('loop://', timeout=1)

# ser = serial.Serial(
#     port     = '/dev/ttyUSB1',      #Configurar con el puerto
#     baudrate = 9600,
#     parity   = serial.PARITY_NONE,
#     stopbits = serial.STOPBITS_ONE,
#     bytesize = serial.EIGHTBITS
# )

pSerie.timeout=None  # No espera tiempo alguno por datos.
pSerie.flushInput()  # Limpia buffer de entrada.
pSerie.flushOutput() # Limpia buffer de salida.


while (1):
    escribePuertoSerie()
    clear()
    
    dataIn = leePuertoSerie()
    
    if (inData == '1'):     # Opción 1 del menú.
        calculadora.start()
        clear()
     
    elif(inData == '2'):    # Opción 2 del menú.
        multiplesGraficos.start()
        clear()
     
    elif(inData == 'exit'): # Opción de salir del programa.
        if pSerie.isOpen():
            pSerie.close()
        break
     
    else:                   # Opción por defecto.
        print('Dato no válido')
