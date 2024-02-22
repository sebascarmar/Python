import time
import serial
import sys

portUSB = sys.argv[1]

ser = serial.Serial(
    port='/dev/ttyUSB{}'.format(int(portUSB)),	#Configurar con el puerto
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

ser.isOpen()
ser.timeout=None
print(ser.timeout)

print ('Ingrese un comando:[0,1,2,3]\r\n')

while 1 :
    inputData = input("<< ")	
    if str(inputData) == 'exit':
        ser.close()
        exit()
    elif(str(inputData) == '3'):
        print ("Wait Input Data")
        ser.write(str(inputData).encode())
        time.sleep(2)
        readData = ser.read(1)
        out = str(int.from_bytes(readData,byteorder='big'))
        print(ser.inWaiting())
        if out != '':
            print (">>" + out)
## Función de menú principal
def main():
    print("\033[1;90mIniciando programa...\033[0m")
    print('')
    
    # Configuración del puerto real
    # portUSB = sys.argv[1]
    # ser = serial.Serial(
    #    port     = '/dev/ttyUSB{}'.format(int(portUSB)),      #Cambiar el nombre del puerto por el correcto
    #    baudrate = 115200,
    #    parity   = serial.PARITY_NONE,
    #    stopbits = serial.STOPBITS_ONE,
    #    bytesize = serial.EIGHTBITS
    #    ser.isOpen()
    #    ser.timeout = None
    #    print(ser.timeout)
    #)
   
    # Configuración del puerto para la simulación
    ser = serial.serial_for_url('loop://', timeout=1)
    ser.flushInput()
    ser.flushOutput()

    leds = [[0, 0, 0] for _ in range(4)]                # Estado inicial de los LEDs

    while True:
        print('\033[1;4mMENÚ PRINCIPAL\033[0m'       )        
        print('¿Qué acción desea realizar?'          )
        print('   Leds  : modificar estado de leds'  )
        print('   Switch: verificar estado de switch')
        print('   Exit  : salir del programa'        )
        print('')

        opcion = input('Opción ingresada: ')

        if opcion.lower()   == 'leds':
            gestionar_leds(leds)
            trama = armar_trama(opcion, leds)

            # Se envía la trama
            print("\033[1;90mEncendiendo leds...\033[0m")
            ser.write(str(trama).encode())
            time.sleep(1)

        elif opcion.lower() == 'switch':
            print("\033[1;90mComprobando estado de switches...\033[0m")
            trama = armar_trama(opcion, leds)

            # Se envía la trama
            ser.write(str(trama).encode())
            time.sleep(2)

            # Se recibe el estado de los switchs
            readData = ser.read(1)
            estado = str(int.from_bytes(readData,byteorder='big'))
            print(ser.inWaiting())
            if estado != '':
                print (">>" + estado)


        elif opcion.lower() == 'exit':
            print("\033[1;90mSaliendo del programa...\033[0m")
            ser.close()
            exit()
        
        else:
            print ('\033[91mOpción incorrecta. Por favor, ingrese una opción válida\033[0m')
    else:
        ser.write(str(inputData).encode())
        time.sleep(1)
