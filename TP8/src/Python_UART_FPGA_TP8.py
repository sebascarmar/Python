import time
import serial
import sys
import copy
import matplotlib.pyplot as plt

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
   
    # Estado inicial de las variables
    fase  = 0             
    Tx    = 1
    Rx    = 1

    
    while True:
        print('\033[1;4mMENÚ PRINCIPAL\033[0m     ')        
        print('¿Qué acción desea realizar?        ') #cantidad bits i_data     recibe datos?
        print('1) Reseteo del sistema             ') #0                        no
        print('2) Habilitar/Deshabilitar Tx       ') #1                        no      
        print('3) Habilitar/Deshabilitar Rx       ') #1                        no
        print('4) Cambiar fase                    ') #2                        no
        print('5) Capturar y graficar BER         ') #0    
        print('6) Logueo de memoria               ') #0    
        print('7) Comprobación estado de memoria  ') #0
        print('8) Leer y graficar datos de memoria') #0
        print('9) Salir del programa              ')
        print('')

        opcion = input('Opción ingresada: ')

        # Verifica que no se ingrese una letra o numero fuera de rango
        while (opcion.isalpha() or int(opcion) < 1 or int(opcion) > 9):
            print('\033[91mOpción incorrecta. Por favor, ingrese una opción válida\033[0m')
            opcion = input('Opción ingresada: ')
            
        ########## Reset ##########
        if (int(opcion) == 1):
            print("\033[1;90mReseteando sistema...\033[0m")                    
            transmisor (ser, opcion)
            error = receptor_test(ser, opcion)
            if(error == 0):
                print("\033[1;90mEl sistema fue reseteado exitosamente\033[0m")
            
            else:
                print("\033[91mNo fue posible resetear el sistema\033[0m")

        ########## Tx ##########
        elif (int(opcion) == 2):
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
            
            transmisor (ser, opcion)
            error = receptor_test (ser, opcion)
            if(error == 0):
                print("\033[1;90mTx modificado\033[0m")
            
            else:
                print("\033[91mNo fue posible modificar Tx\033[0m")

        ########## Rx ##########
        elif (int(opcion) == 3):
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

            transmisor (ser, opcion)
            error = receptor_test (ser, opcion)
            if(error == 0):
                print("\033[1;90mRx modificado\033[0m")
            
            else:
                print("\033[91mNo fue posible modificar Rx\033[0m")

        ########## Fase ##########
        elif (int(opcion) == 4):
            print("\033[1;90mLa fase actual es", fase, ". ¿Qué fase desea colocar?\033[0m")
            fase = input('>> ')

            while (opcion.isalpha() or int(fase) < 0 or int(fase) > 3):
                print('\033[91mOpción incorrecta. Por favor, ingrese una valor entero entre 0 y 3\033[0m')
                fase = input('Opción ingresada: ')

            fase   = int(fase)

            transmisor (ser, opcion, fase)
            error = receptor_test (ser, opcion)
            if(error == 0):
                print("\033[1;90mLa fase fue modificada\033[0m")
            
            else:
                print("\033[91mNo fue posible modificar la fase\033[0m")
           
        ########## Captura y grafica BER ##########
        elif (int(opcion) == 5):
            print("\033[1;90mCapturando BER...\033[0m")                    
            transmisor (ser, opcion)
            error = receptor_test (ser, opcion)

            if(error == 0):
                print("\033[1;90mRecibiendo datos para graficar\033[0m")
                BER_data = get_data (ser, opcion)
                error = receptor_test (ser, opcion)

                if(error == 0):
                    graficar_data(BER_data)

                else:
                    print("\033[91mError al recibir los datos\033[0m")                   
            
            else:
                print("\033[91mNo fue posible loguear la memoria\033[0m")

        ########## Logueo de memoria ##########
        elif (int(opcion) == 6):                 
            transmisor (ser, opcion)
            print("\033[91mLlenando memoria...\033[0m")
            error = receptor_test (ser, opcion)

            if(error == 0):   
                print("\033[91mLogueo de memoria finalizado\033[0m")

            else:
                print("\033[91mNo fue posible el logueo de la memoria\033[0m")


        ########## Comprobación estado de memoria ##########
        elif (int(opcion) == 7):
            print("\033[1;90mComprobando estado de memoria..\033[0m")                    
            transmisor (ser, opcion)
            error = receptor_test (ser, opcion)

            if(error == 0):
                estado_mem = get_data(ser, opcion)
                error = receptor_test (ser, opcion)

                if(error == 0 and estado_mem == 0):
                    print("\033[1;34mMemoria vacía\033[0m")

                elif(error == 0 and estado_mem == 1):
                    print("\033[1;34mMemoria llena\033[0m") 

                else:
                    print("\033[91mError al verificar estado de memoria\033[0m")
            
            else:
                print("\033[91mError al verificar estado de memoria\033[0m")
                     

        ########## Leer y graficar datos de memoria ##########
        elif (int(opcion) == 8):                 
            transmisor (ser, opcion)
            error = receptor_test (ser, opcion)
            
            if(error == 0):
                print("\033[1;90mRecibiendo datos para graficar...\033[0m")
                data_mem = get_data(ser, opcion)
                error = receptor_test (ser, opcion)

                if(error == 0):
                    graficar_data(data_mem)

                else:
                    print("\033[91mError al recibir los datos\033[0m")                   
            
            else:
                print("\033[91mNo fue posible leer los datos de la memoria\033[0m")


        ########## Salida ##########
        elif (int(opcion) == 9):
            print("\033[1;90mSaliendo del programa...\033[0m")
            ser.close()
            exit()
            
 
       

################### FUNCIONES ###################
# Funcion de transmisión de datos
def transmisor (ser, opcion, i_data = None, return_data = None):
    # Se arma la trama
    trama = armar_trama(opcion, i_data)
    
    # Se envía la trama
    for byte in trama:
        ser.write(byte.to_bytes(1, byteorder='big'))
        time.sleep(0.1) 
        
    #ser.flushInput ()          # Al limpiar el buffer un ser.reed inmediato bloquea el programa
    ser.flushOutput()
    return

# Funcion de verificación de recepción de datos
def receptor_test(ser, opcion):
    time.sleep(1)
    readData = ser.read(1)
    error_detec = 0                         # Verificación de comunicación

    # Comprobación de envío de trama
    if (int.from_bytes(readData,byteorder='big') != int(opcion)):
        # print("\033[91mError en la comunicación. Llegó\033[0m", int.from_bytes(readData,byteorder='big'))
        # print('')

        error_detec = 1
    
    else:
        # print("Conexion exitosa. Llego ", int.from_bytes(readData,byteorder='big'))
        error_detec = 0

    # Limpia buffer de entrada y salida
    ser.flushInput ()
    ser.flushOutput()
        
    return error_detec


# Funcion de recepción de datos
def get_data (ser, opcion):
    time.sleep(1)
    return_data = []                        # Variable con los datos 

    ## Recibe la BER
    if (int(opcion) == 5):
        for i in range(4):
            I_Q_data = []
            for j in range(8):
                byte = ser.read(1)
                I_Q_data.append(byte)

            palabra = b''.join(I_Q_data)
            return_data.append(palabra)

    # Se recibe bit de llenado de memoria
    elif (int(opcion) == 7):
        return_data = ser.read(1)
        
    # Se recibe datos de memoria
    else:
        for i in range(32769):
            mem_data = []
            for j in range(4):
                byte = ser.read(1)
                mem_data.append(byte)
            palabra = b''.join(mem_data)
            return_data.append(palabra)               

    # Limpia buffer de entrada y salida
    ser.flushInput ()
    ser.flushOutput()
        
    return return_data


# Función que arma la trama a enviar
def armar_trama(opcion, i_data):
    start = 0xBB
    trama = []
    # i_data = int(i_data)
    opcion = int(opcion)

    # Armado de trama
    # Funciones sin información adicional
    if (opcion == 1 or opcion > 4):
        trama = [start ,
                 opcion]          
        
    # Funciones con i_data
    else:
        trama = [start ,
                 opcion,
                 i_data]

    print(trama)
    return trama    

def graficar_data(datos):
    for i, dato in enumerate(datos):
        plt.plot(dato, label=f'Dato {i+1}')

    # Añadir etiquetas y leyenda
    plt.xlabel('Tiempo')
    plt.ylabel('Valor')
    plt.title('Gráfico de Datos')
    plt.legend()

    # Mostrar el gráfico
    plt.show()


main()
