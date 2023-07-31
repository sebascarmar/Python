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

#--------------------------------------------------------------------------------------------------------------#

def escribePuertoSerie():
   
    #***************** Bucle que permite ingresar el comando y el device ***********************#
    while(1):
        print('********************* ESCRITURA EN PUERTO SERIE *********************')
        print('Ingrese alguno de estos comandos para ser enviados por puerto serie:')
        print('\t calculadora: para ejecutar dicho script')
        print('\t multiplot:   para ejecutar dicho script')
        print('\t exit:        para salir')
        data = input("\t > ")
        device = int(input('\n\t device (0 a 255):\n\t > '))
        
        if(len(data)>65535 or device>255): # Detecta de errores en el ingreso de datos.
            clear()
            print('Dato demasiado largo o device no válido')
        else:
            break

    #**************************** Armado de la trama de datos **********************************#
    BITS_INICIO = 0b101                # Bits de inicio de trama.
    BITS_FIN    = (~BITS_INICIO)&0b111 # Bits de fin. La op. AND obtiene los 3 bits menos signif.
    dataSize   = len(data)             # Largo del dato ingresado.

    # Cabecera de la trama.
    if(dataSize <= 15):         # Caso para tamaño de los datos a enviar PEQUEÑO.
        isShortData = True
        inicioTrama = (BITS_INICIO << 5) | (isShortData << 4) | dataSize # Byte de start.
        
        cabecera = b''.join([inicioTrama.to_bytes(1, byteorder='big'),  # Armado de la cabecera
                             device.to_bytes(1, byteorder='big')])      #como conjunto de bytes.
        
    else: #(dataSize <= 65535)  # Caso para tamaño de los datos a enviar GRANDE.
        isShortData = False
        inicioTrama        = (BITS_INICIO << 5) | (isShortData << 4) | 0x0 # Byte de start.
        
        longSizeHigh = 0x00 | (dataSize >> 8)  # Byte más significativo del tamaño de  datos.
        longSizeLow  = 0x00 | (dataSize & 0xFF)# Byte menos significativo del tamaño de datos.
        
        cabecera = b''.join([inicioTrama.to_bytes(1, byteorder='big'),  # Armado de cabecera 
                             longSizeHigh.to_bytes(1, byteorder='big'), #como conjunto de bytes.
                             longSizeLow.to_bytes(1, byteorder='big'),
                             device.to_bytes(1, byteorder='big')])

    # Cola de la trama.
    finTramaInt = ((BITS_FIN << 5) | (inicioTrama & 0x1F)) & 0xFF
    finTrama = finTramaInt.to_bytes(1, byteorder='big')

    #******************** Envío de la trama completa por puerto serie **************************#
    pSerie.write(cabecera)      # Envío por puerto serie byte a byte la cabecera.
    pSerie.write(data.encode()) # Envío por puerto serie byte a byte los datos ingresados.
    pSerie.write(finTrama)      # Envío por puerto serie byte a byte la cola.

#--------------------------------------------------------------------------------------------------------------#

def leePuertoSerie():
    aux         = ''                   # Buffer que almacena el dato completo leído.
    i           = 1                    # Contador.
    BITS_INICIO = 0b101                # Bits de inicio de trama.
    BITS_FIN    = (~BITS_INICIO)&0b111 # Bits de fin. La op. AND obtiene los 3 bits menos signif.
    startFound  = False                # Banderas.
    sizeFound   = False
    deviceFound = False
    dataReadComplete   = False

    while(pSerie.inWaiting() > 0): 
        inByte = pSerie.read(1) # Lee de a 1 byte el puerto serie.
        
        if(startFound == False):         # Busca y almacena el byte de inicio de trama.
            
            inicioTrama = int.from_bytes(inByte, byteorder='big')
            bitsInicioRecibidos = inicioTrama >> 5
            if(bitsInicioRecibidos == BITS_INICIO):
                startFound = True
                
                isShortData = (inicioTrama >> 4) & 0b1
                if(isShortData == True): # Almacena el tamaño de la trama (caso PEQUEÑO).
                    sizeData = inicioTrama & 0xF
                    sizeFound = True
            
        elif(sizeFound == False):        # Almacena el tamaño de la trama (caso GRANDE).
            
            longSizeHigh = int.from_bytes(inByte, byteorder='big')
            
            inByte = pSerie.read(1)
            longSizeLow = int.from_bytes(inByte, byteorder='big')
            
            sizeData = longSizeHigh<<8 | longSizeLow # Concatena los 2 bytes.
            sizeFound = True
         
        elif(deviceFound == False):      # Almacena el device.
            device = int.from_bytes(inByte, byteorder='big')
            deviceFound = True
         
        elif(dataReadComplete == False): # Lectura de datos.
         
            aux += inByte.decode()
            if(i == sizeData):
                dataReadComplete = True
            i+=1
         
        else:                            # Almacena el fin de la trama.
            finTrama = int.from_bytes(inByte, byteorder='big')

    # Analiza que el byte de fin de la trama sea correcto. En el caso de que no, imprime ERROR.
    if( (finTrama&0b11111)!=(inicioTrama&0b11111) and (inicioTrama>>5)!=(((~finTrama)>>5)&0b111) ):
        print('Error en la trama recibida')

    print('device: ', device)
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
    
    if (inData == 'calculadora'): # Opción 1 del menú.
        calculadora.start()
        clear()
     
    elif(inData == 'multiplot'):  # Opción 2 del menú.
        multiplesGraficos.start()
        clear()
     
    elif(inData == 'exit'):       # Opción de salir del programa.
        if pSerie.isOpen():
            pSerie.close()
        break
     
    else:                         # Opción por defecto.
        print('Dato no válido')
