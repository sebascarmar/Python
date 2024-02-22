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



def gestionar_leds(leds):
    print('¿Qué led desea modificar? 1,2,3,4')
    num_led = input('<<')

    while (num_led not in {'1', '2', '3', '4'}):
        print ('\033[91mERROR: número de led inválido\033[0m')
        print('¿Qué led desea modificar? 1,2,3,4')
        num_led = input('<<')

    num_led = int(num_led) - 1                                          # Convertir a índice

    print('¿Desea encender o apagar el led?')
    accion = input('<<')

    while (accion.lower() not in {'encender', 'apagar'}):
        print ('\033[91mAcción incorrecta. Por favor, ingrese una opción válida\033[0m')
        accion = input('<<')
    
    print('¿Qué color desea' , accion, '? Rojo, Verde o Azul?')
    color = input('<<')

    while (color.lower() not in {'rojo', 'verde', 'azul'}):
        print ('\033[91mColor incorrecto. Por favor, ingrese un color válido\033[0m')
        color = input('<<')


    # Verificar si se puede realizar la acción
    # Si se seleccionó encender
    if accion == "encender":
        if leds[num_led][{"azul": 0, "verde": 1, "rojo": 2}[color]] == 1:
           print('\033[91mERROR: el led', num_led + 1, 'ya está encendido en color', color, '\033[0m')
        else:
            leds[num_led][{"azul": 0, "verde": 1, "rojo": 2}[color]] = 1
            print('\033[92mEl led ', num_led + 1, 'se encenderá en color', color, '\033[0m')
              
    # Si se seleccionó apagar
    else:  
        if leds[num_led][{"azul": 0, "verde": 1, "rojo": 2}[color]] == 0:
            print('\033[91mERROR: el led', num_led + 1, 'ya está apagado en color', color, '\033[0m')
        else:
            leds[num_led][{"azul": 0, "verde": 1, "rojo": 2}[color]] = 0
            print('\033[92mEl led ', num_led + 1, 'se aágará en color', color, '\033[0m')


    # Imprimir estado actual de los LEDs
    print("Estado actual de los LEDs:")
    for i, estado in enumerate(leds, start=1):
        print('LED ', i, ':', estado)
    
    return


def armar_trama(opcion, leds):
    start = 0b00000101

    if(opcion.lower() == 'leds'):
        func = 0b11111111
        trama = [start,
                 func]
        for led in leds:
            trama.extend(led)
    else:
        func = 0b00000000
        trama = [start,
                 func]
    
    print(trama)

    return trama    

