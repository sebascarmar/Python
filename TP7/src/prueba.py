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
    if inputData == 'exit':
        ser.close()
        exit()
    elif(inputData == 'leer'):
        start = 0b00000101
        func = 0x55
        
        trama =[start,
                func ]
        
        for elemento in trama:
            ser.write(elemento.to_bytes(1, byteorder='big'))
            time.sleep(1) 
        
        print("Waiting for input data")
        time.sleep(1)
        
        readData = ser.read(1)
        if(int.from_bytes(readData,byteorder='big') == 85): #0x55 funcion leer
            readData = ser.read(1)
            out = str(int.from_bytes(readData,byteorder='big'))
            print(ser.inWaiting())
            if out != '':
                print (">>" + out)
        else:
            print("Error en el comunicación")

        
    elif(inputData == 'escribir'):
        
        inputData = input("  << colores: ")	
        if(inputData == 'a'):
            byte1 = 0x0A
            byte2 = 0x57
        elif(inputData == 'b'):
            byte1 = 0x0F
            byte2 = 0x21
        
        start = 0b00000101
        func = 0xAA
        trama =[start,
                func,
                byte1,
                byte2]
        
        for elemento in trama:
            ser.write(elemento.to_bytes(1, byteorder='big'))
            time.sleep(1) 

        time.sleep(1)
        readData = ser.read(1)
        if(int.from_bytes(readData,byteorder='big') != 170): #0xAA funcion escribir
            print("Error en el comunicación")
        
    else:
        ser.write(inputData.encode())
        time.sleep(1)

