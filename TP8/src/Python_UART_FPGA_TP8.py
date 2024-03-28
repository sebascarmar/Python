import time
import serial
import sys
import copy
from colorama import init, Fore

## Función de menú principal
def main():
    print("\033[1;90mIniciando programa...\033[0m")
    print('')
    
    # Configuración del puerto real
    portUSB = sys.argv[1]
    ser = serial.Serial(
       port     = '/dev/ttyUSB{}'.format(int(portUSB)),      #Cambiar el nombre del puerto por el correcto
       baudrate = 115200,
       parity   = serial.PARITY_NONE,
       stopbits = serial.STOPBITS_ONE,
       bytesize = serial.EIGHTBITS
    )

    ser.isOpen()
    ser.timeout = None 
    print(ser.timeout)
   
    # Configuración del puerto para la simulación
    # ser = serial.serial_for_url('loop://', timeout=1)
    # ser.flushInput ()
    # ser.flushOutput()

    leds  = [[0, 0, 0],                                 # Estado inicial de los LEDs
             [0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]]   
                 
    reset = 0
    fase  = 0             
    Tx    = 1
    Rx    = 1

    leds = [[reset, Tx, Rx],                                 # Estado inicial de los LEDs
            [0, 0, 0],
            [0, 0, 0],
    
    while True:
        print('\033[1;4mMENÚ PRINCIPAL\033[0m')        
        print('¿Qué acción desea realizar?   ')
        print('1) Reseteo del sistema        ')
        print('2) Habilitar/Deshabilitar Tx  ')
        print('3) Habilitar/Deshabilitar Rx  ')
        print('4) Cambiar fase               ')
        print('5) Salir del programa         ')
        print('')

        opcion = int(input('Opción ingresada: '))
    
        while (opcion < 1 or opcion > 5):
            print('\033[91mOpción incorrecta. Por favor, ingrese una opción válida\033[0m')
            opcion = int(input('Opción ingresada: '))


        if (opcion == 1):
            print("\033[1;90mReseteando sistema...\033[0m")
            reset = 1
            gestionar_leds(0, 0, reset, leds)
            transmisor    (ser, opcion, leds)

        elif (opcion == 2):
            if(Tx == 1):
                print("\033[1;90mTx se encuentra habilitado. ¿Desea deshabilitarlo?\033[0m")
                opcion_tx = input('Y/N: ').lower()

                if opcion_tx == 'y':
                    print("\033[1;90mDeshabilitando Tx\033[0m")
                    Tx = 0

            else:
                print("\033[1;90mTx se encuentra deshabilitado. ¿Desea habilitarlo?\033[0m") 
                opcion_tx = input('Y/N: ').lower()

                if opcion_tx == 'y':
                    print("\033[1;90mHabilitando Tx\033[0m")
                    Tx = 1

            gestionar_leds(0, 1, Tx, leds)
            transmisor    (ser, opcion, leds)

        elif (opcion == 3):
            if(Rx == 1):
                print("\033[1;90mRx se encuentra habilitado. ¿Desea deshabilitarlo?\033[0m")
                opcion_rx = input('Y/N: ').lower()

                if opcion_rx == 'y':
                    print("\033[1;90mDeshabilitando Rx\033[0m")
                    Rx = 0

            else:
                print("\033[1;90mRx se encuentra deshabilitado. ¿Desea habilitarlo?\033[0m") 
                opcion_rx = input('Y/N: ').lower()

                if opcion_rx == 'y':
                    print("\033[1;90mHabilitando Rx\033[0m")
                    Rx = 1

            gestionar_leds(0, 2, Rx, leds)
            transmisor    (ser, opcion, leds)

        elif (opcion == 4):
            print("\033[1;90mLa fase actual es", fase, ". ¿Qué fase desea colocar?\033[0m")
            fase = int(input('>> '))

            while (fase < 0 or fase > 3):
                print('\033[91mOpción incorrecta. Por favor, ingrese una valor entero entre 0 y 3\033[0m')
                fase = int(input('Opción ingresada: '))
            
            bit1 = fase // 2
            bit2 = fase % 2

            gestionar_leds(1, 0, bit1, leds)
            gestionar_leds(1, 1, bit2, leds)
            transmisor    (ser, opcion, leds)
           
        else:
            print("\033[1;90mSaliendo del programa...\033[0m")
            ser.close()
            exit()
            
        imprimir_estado_leds(leds)    
       

################### MENÚ DE LEDS ###################
def gestionar_leds(fila, columna, valor, leds):
    leds [fila][columna] = valor

################### FUNCIONES ###################
# Funcion de transmisión de datos
def transmisor (ser, opcion, leds):
    # Se arma la trama
    trama = armar_trama(opcion, leds)

    # Se envía la trama
    for byte in trama:
        ser.write(byte.to_bytes(1, byteorder='big'))
        time.sleep(0.1) 

    # ser.flushInput ()          # Al limpiar el buffer un ser.reed inmediato bloquea el programa
    ser.flushOutput()

    return

# Funcion de recepción de datos
def receptor(ser, opcion, leds):
    time.sleep(1)
    readData = ser.read(1)
    error_detec = 0

    # Comprobación de envío de trama
    # Para switch se espera recibir 0x55 (d85)
    if(opcion == 'switch'):
        if (int.from_bytes(readData,byteorder='big') == 85): 
            readData = ser.read(1)
            out = str(int.from_bytes(readData,byteorder='big'))
            print(ser.inWaiting())
            if out != '':
                print (">>" + out)
            
            # Se apagan todos los leds
            leds[:] = [[0] * len(leds[0]) for _ in range(4)]
    
        # Cualquier otro dato recibido, será erroneo
        else:
            print ('\033[91mError en la comunicación\033[0m')
            print('')
            error_detec = 1
    
    # Para leds se espera recibir 0xAA (d170)
    if(opcion == 'leds' and int.from_bytes(readData,byteorder='big') != 170):
        print("Error en el comunicación")
        print('')

        error_detec = 1
    
    # Limpia buffer de entrada y salida
    ser.flushInput ()
    ser.flushOutput()
        
    return error_detec


# Función que arma la trama a enviar
def armar_trama(opcion, leds):
    start = 0x01

    # Reset
    if opcion == 1:
        func = 0xAA

    # Tx
    elif opcion == 2:
        func = 0xBB
    
    # Rx
    elif opcion == 3:
        func = 0xCC

    # Fase
    elif opcion == 4:
        func = 0xDD    

    # Convierte cada fila de LEDs en un número binario
    led_1 = (int(leds[0][2]) and 0b1) << 2 | (int(leds[0][1]) and 0b1) << 1 | (int(leds[0][0]) and 0b1) 
    led_2 = (int(leds[1][2]) and 0b1) << 2 | (int(leds[1][1]) and 0b1) << 1 | (int(leds[1][0]) and 0b1)
    led_3 = (int(leds[2][2]) and 0b1) << 2 | (int(leds[2][1]) and 0b1) << 1 | (int(leds[2][0]) and 0b1)
    led_4 = (int(leds[3][2]) and 0b1) << 2 | (int(leds[3][1]) and 0b1) << 1 | (int(leds[3][0]) and 0b1)


    # Concatena los valores en una variable de 32 bits
    byte_1 = (0b00000000   | (led_4 << 1) | (led_3 >> 2)) & (0x00FF)
    byte_2 = ((led_3 << 6) | (led_2 << 3) | led_1)        & (0x00FF)

    trama =[start ,
            func  ,
            byte_1,
            byte_2]
        
    return trama    

# Funcion que imrpime el estado de los LEDs
def imprimir_estado_leds(leds):
    print(Fore.WHITE + 'Estado actual de los LEDs:')
    print(Fore.WHITE + ' B  G  R')
    print(Fore.WHITE + "\n".join(map(str, leds)))




main()
