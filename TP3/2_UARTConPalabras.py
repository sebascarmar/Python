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
    print('\t calculadora: para ejecutar dicho script')
    print('\t multiplot:   para ejecutar dicho script')
    print('\t exit:        para salir\n\t')
    data = input("\t > ")

    pSerie.write(data.encode()) # Función que envía por puerto serie byte a byte lo ingresado.

#______________________________________________________________________________________________________________#

def leePuertoSerie():
    aux = ''
        aux += read_data.decode()
    while pSerie.inWaiting() > 0: # Lee puerto serie hasta que no hallan más datos por leer. Lo anexa en 'aux'.
        inByte = pSerie.read(1)

    return aux


#**************************************************************************************************************#
############################################## Programa Principal ##############################################
#**************************************************************************************************************#


pSerie = serial.serial_for_url('loop://', timeout=1)

pSerie.timeout=None  # No espera tiempo alguno por datos.
pSerie.flushInput()  # Limpia buffer de entrada.
pSerie.flushOutput() # Limpia buffer de salida.


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
        if pSerie.isOpen():
            pSerie.close()
        break
     
    else:                         # Opción por defecto.
        print('Dato no válido')
