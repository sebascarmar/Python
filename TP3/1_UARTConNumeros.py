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
    while pSerie.inWaiting() > 0: # Lee puerto serie hasta que no hallan más datos por leer. Lo anexa en 'aux'.
        inByte = pSerie.read(1)
        aux += inByte.decode()

    return aux


#**************************************************************************************************************#
############################################## Programa Principal ##############################################
#**************************************************************************************************************#

clear()

pSerie = serial.serial_for_url('loop://', timeout=1)

pSerie.timeout=None  # No espera tiempo alguno por datos.
pSerie.flushInput()  # Limpia buffer de entrada.
pSerie.flushOutput() # Limpia buffer de salida.


while (1):
    escribePuertoSerie()
    clear()
    
    inData = leePuertoSerie()
    
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
