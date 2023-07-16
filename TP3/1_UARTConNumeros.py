import time
import serial
import calculadora
import multiplesGraficos

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

#print(ser.timeout)

print('Ingrese alguno de estos comandos para ser enviados por puerto serie:')
print('\t 1: para ejecutar la calculadora')
print('\t 2: para ejecutar el multi-plot')
print('\t exit: para salir\n\t')

while 1 :
    data = input("ToSent (type 'exit' to quit): ")
    if (data == 'exit'):
        if ser.isOpen():
            ser.close()
        break
    else:
        ser.write(data.encode())
        #time.sleep(2)
        out = ''
        #print("Info: ",ser.inWaiting())
        while ser.inWaiting() > 0:
            read_data = ser.read(1)
            #print(read_data)
            out += read_data.decode()
            #print("Info: ",ser.inWaiting())
        if out=='1':
            calculadora.start()
        elif out=='2':
            multiplesGraficos.start()

        if out != '':
            print(">> " + out)

