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
                 
    
    while True:
        print('\033[1;4mMENÚ PRINCIPAL\033[0m'        )        
        print('¿Qué acción desea realizar?'          )
        print('   Leds  : modificar estado de leds'  )
        print('   Switch: verificar estado de switch')
        print('   Exit  : salir del programa'        )
        print('')

        opcion = input('Opción ingresada: ')
        opcion = opcion.lower()
    
        while (opcion != 'leds' and opcion != 'switch' and opcion != 'exit'):
            print('\033[91mOpción incorrecta. Por favor, ingrese una opción válida\033[0m')
            opcion = input('Opción ingresada: ')

            opcion = opcion.lower()



        if opcion   == 'leds':
            # Se modifican los leds
            gestionar_leds(leds, ser, opcion)
            print("\033[1;90mRegresando al menú principal...\033[0m \n")
           

        elif opcion == 'switch':
            print('\033[93mAdvertencia: la lectura de los Switch resetea el estado de los leds\033[0m')
            print('¿Desea continuar?')
            verif = input('Y/N: ').lower()

            if(verif =='y'):
                print("\033[1;90mComprobando estado de switches...\033[0m")
                
                # Se envía la trama
                transmisor(ser, opcion, leds)
                
                print("\033[1;90mEsperando información...\033[0m")

                # Se recibe el estado de los switchs
                receptor(ser, opcion, leds)
            

        elif opcion == 'exit':
            print("\033[1;90mSaliendo del programa...\033[0m")
            ser.close()
            exit()
            
        
       

################### MENÚ DE LEDS ###################
def gestionar_leds(leds, ser, opcion):
    # Se guarda el estado anterior de los leds
    leds_anterior = copy.deepcopy(leds)
    
    while True:
        print('')
        print('\033[1;4mMenú Leds\033[0m')
        print("1. Modificar leds")
        print("2. Imprimir el estado de los leds")
        print("3. Enviar datos y regresar al menú principal")
        print('4. Regresar al menú principal')

        opcion_led = input("Seleccione una opción: ")

        # Si se ingresa una opción no válida
        while opcion_led not in {'1', '2', '3', '4'}:
            print ('\033[91mOpción incorrecta. Por favor, ingrese una opción válida\033[0m')
            opcion_led = input("Seleccione una opción: ")
        


        #Se modifican los leds
        if (opcion_led == "1"):
            modificar_led(leds)
            
        # Se imprime el estado actual de los leds
        elif(opcion_led == "2"):
            imprimir_estado_leds(leds, leds_anterior)

        #Se encienden los leds modificados
        elif(opcion_led == "3"):
            print("\033[1;90mModificando leds...\033[0m")
            # Se realizan los cambios
            transmisor(ser, opcion, leds)
            valid = receptor  (ser, opcion, leds)
            # Si receptor presenta error, no se encenderán los leds
            if (valid == 1):
                # Se revierten los cambios realizados
                for i in range(len(leds)):
                    for j in range(len(leds[i])):
                        leds[i][j] = leds_anterior [i][j]
            else:
                leds_anterior = copy.deepcopy(leds)

            # Imprime estado de leds
            imprimir_estado_leds(leds, leds_anterior)

            return

       # Se regresa la menú principal
        else:
            print('\033[93mAdvertencia: si regresa al menú principal, se descartarán los últimos cambios realizados\033[0m')
            print('¿Desea continuar?')
            verif = input('Y/N: ').lower()
            if (verif == 'y'):
                
                # Se revierten los cambios realizados
                for i in range(len(leds)):
                    for j in range(len(leds[i])):
                        leds[i][j] = leds_anterior [i][j]

                return
        


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


# Opciones para modificar LEDs
def modificar_led(leds):
    print('¿Qué led desea modificar? 1,2,3,4')
    num_led = input('>>')

    # Si se ingresa una opción no válida
    while (num_led not in {'1', '2', '3', '4'}):
        print ('\033[91mERROR: número de led inválido\033[0m')
        print('¿Qué led desea modificar? 1,2,3,4')
        num_led = input('>>')

    num_led = int(num_led) - 1                                          # Convertir a índice

    print('¿Desea encender o apagar el led?')
    accion = input('>>')
    accion = accion.lower()

    while (accion.lower() not in {'encender', 'apagar'}):
        print ('\033[91mAcción incorrecta. Por favor, ingrese una opción válida\033[0m')
        accion = input('>>')
        accion = accion.lower()
    
    print('¿Qué color desea' , accion, '? ¿Rojo, Verde o Azul?       ')
    print('Separe por "," si desea', accion,'encender más de un color')
    color = input('>>').lower()
    


    # Si se ingresa más de un color
    if "," in color:
        color_mul = []
        
        # Dividir la entrada por comas y eliminar los espacios en blanco
        color_mul = [c.strip() for c in color.split(",")]

        # Verificar cada color ingresado
        for c in color_mul:
            if c not in {'rojo', 'verde', 'azul'}:
                color_incorrecto = True
                break
            else:
                color_incorrecto = False

        while (len(color.split(",")) > 3) or color_incorrecto == True:
            if(len(color.split(",")) > 3):
                print ('\033[91mERROR: ingresó más de tres colores. Por favor, ingrese una cantidad válida\033[0m')
            else:
                print ('\033[91mERROR: ingresó un color incorrecto. Por favor, ingrese un color válico\033[0m')

            print('¿Qué color desea' , accion, '? ¿Rojo, Verde o Azul?       ')
            print('Separe por "," si desea', accion,'encender más de un color')
            color = input('>>').lower()
            

            # Dividir la entrada por comas y eliminar los espacios en blanco
            color_mul = [c.strip() for c in color.split(",")]

            # Verificar cada color ingresado
            for c in color_mul:
                if c not in {'rojo', 'verde', 'azul'}:
                    color_incorrecto = True
                    break
                else:
                    color_incorrecto = False

            
        for i in range(len(color_mul)):
            accion_leds(color_mul[i], num_led, leds, accion)

    # Si solo se ingresa un color
    else:
        while (color not in {'rojo', 'verde', 'azul'}):
            print ('\033[91mColor incorrecto. Por favor, ingrese un color válido (solo uno)\033[0m')
            color = input('>>')
            color = color.lower()

        accion_leds(color, num_led, leds, accion)
        

    return

# Función que enciende o apaga los LEDs
def accion_leds(color, num_led, leds, accion):
    colores = {"azul": 0, "verde": 1, "rojo": 2}          # [AZUL VERDE ROJO]
    col_led = colores[color]
        
    # Verificar si se puede realizar la acción
    # Si se seleccionó encender
    if (accion == "encender"):
        if leds[num_led][col_led] == 0:
            leds[num_led][col_led] = 1
            print('\033[92mEl led ', num_led + 1, 'se encenderá en color', color, '\033[0m')
            
        else:
            print('\033[93mAdvertencia: el led', num_led + 1, 'ya está encendido en color', color, '\033[0m')
            
    # Si se seleccionó apagar
    else:  
        if leds[num_led][col_led] == 1:
            leds[num_led][col_led] = 0
            print('\033[92mEl led ', num_led + 1, 'se apagará en color', color, '\033[0m')

        else:
            print('\033[93mAdvertencia: el led', num_led + 1, 'ya está apagado en color', color, '\033[0m')
    
    return

# Función que arma la trama a enviar
def armar_trama(opcion, leds):
    start = 0b00000101

    if opcion == 'leds':
        func = 0xAA
        
        # Convierte cada fila de LEDs en un número binario
        led_1 = (int(leds[0][2]) and 0b1) << 2 | (int(leds[0][1]) and 0b1) << 1 | (int(leds[0][0]) and 0b1) 
        led_2 = (int(leds[1][2]) and 0b1) << 2 | (int(leds[1][1]) and 0b1) << 1 | (int(leds[1][0]) and 0b1)
        led_3 = (int(leds[2][2]) and 0b1) << 2 | (int(leds[2][1]) and 0b1) << 1 | (int(leds[2][0]) and 0b1)
        led_4 = (int(leds[3][2]) and 0b1) << 2 | (int(leds[3][1]) and 0b1) << 1 | (int(leds[3][0]) and 0b1)


        # Concatena los valores en una variable de 32 bits
        byte_1 = (0b00000000   | (led_4 << 1) | (led_3 >> 2)) & (0x00FF)
        byte_2 = ((led_3 << 6) | (led_2 << 3) | led_1)        & (0x00FF)

        trama =[start,
                func,
                byte_1,
                byte_2]
        

    else:        
        func  = 0x55
        trama = [start,
                 func]

    return trama    

# Funcion que imrpime el estado de los LEDs
def imprimir_estado_leds(leds, leds_anterior):
    if leds == leds_anterior:
        print(Fore.WHITE + 'Estado actual de los LEDs:')
        print(Fore.WHITE + ' B  G  R')
        print(Fore.WHITE + "\n".join(map(str, leds)))

    else:
        print(Fore.YELLOW + 'Estado actual de los LEDs:')
        print(Fore.YELLOW + ' B  G  R')
        print(Fore.YELLOW + "\n".join(map(str, leds)))
        print('')
        print('\033[93mNota: leds aún no modificados\033[0m')


main()
