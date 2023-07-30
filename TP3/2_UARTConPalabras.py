import time
import serial
import calculadora
import multiplesGraficos
from os import system, name 



#**************************************************************************************************************#
########################################### Definición de funciones ############################################
#**************************************************************************************************************#

def clear(): 
    if name == 'nt': 
        x = system('cls') 
    else: 
        x = system('clear') 


def escribePuertoSerie():
    print('Ingrese alguno de estos comandos para ser enviados por puerto serie:')
    print('\t calculadora: para ejecutar dicho script')
    print('\t multiplot: para ejecutar dicho script')
    print('\t exit: para salir\n\t')
    data = input("\t > ")
    ser.write(data.encode())


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

ser.isOpen()
ser.timeout=None
ser.flushInput()
ser.flushOutput()


while (1):
    escribePuertoSerie()
    clear()
    
    dataIn = leePuertoSerie()
    
    if (dataIn == 'calculadora'):
        calculadora.start()
        clear()
     
    elif(dataIn == 'multiplot'):
        multiplesGraficos.start()
        clear()
     
    elif(dataIn == 'exit'):
        if ser.isOpen():
            ser.close()
        break
     
    else:
        print('Dato no válido')
