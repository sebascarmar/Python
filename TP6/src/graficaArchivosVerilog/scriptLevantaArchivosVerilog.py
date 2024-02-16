import numpy as np
import matplotlib.pyplot as plt
import funciones as fn


Nbauds = 6
os     = 4
NBFrac = 6


# Nombre del archivo
filter_out_I        = "Salida_filtro_I.txt"
filter_out_Q        = "Salida_filtro_Q.txt"
sym_down_samp_I_ph0 = "Salida_down_samp_I_ph0.txt"
sym_down_samp_Q_ph0 = "Salida_down_samp_Q_ph0.txt"
sym_down_samp_I_ph1 = "Salida_down_samp_I_ph1.txt"
sym_down_samp_Q_ph1 = "Salida_down_samp_Q_ph1.txt"
sym_down_samp_I_ph2 = "Salida_down_samp_I_ph2.txt"
sym_down_samp_Q_ph2 = "Salida_down_samp_Q_ph2.txt"
sym_down_samp_I_ph3 = "Salida_down_samp_I_ph3.txt"
sym_down_samp_Q_ph3 = "Salida_down_samp_Q_ph3.txt"

# Lista para almacenar los números enteros firmados
LOG_FILTER_OUT_I = []
LOG_FILTER_OUT_Q = []

LOG_RX_DW_SAM_I_PH0  = []
LOG_RX_DW_SAM_I_PH1  = []
LOG_RX_DW_SAM_I_PH2  = []
LOG_RX_DW_SAM_I_PH3  = []
               
LOG_RX_DW_SAM_Q_PH0  = []
LOG_RX_DW_SAM_Q_PH1  = []
LOG_RX_DW_SAM_Q_PH2  = []
LOG_RX_DW_SAM_Q_PH3  = []

### LECTURA DE ARCHIVOS DE LA SALIDA DE LOS FILTROS
# Abrir el archivo en modo de lectura
with open(filter_out_I, "r") as archivo:
    # Leer cada línea del archivo
    for linea in archivo:
        # Convertir la línea a un entero firmado
        num = int(linea.strip(), 2)  # Convertir de binario a entero
        if linea[0] == '0':  # Si el primer bit es 0, entonces es positivo
            LOG_FILTER_OUT_I.append((num)/(2**NBFrac))
        else:  # Si el primer bit es 1, convertir a negativo (complemento a 2)
            LOG_FILTER_OUT_I.append((num - (1 << len(linea.strip())))/(2**NBFrac))

# Abrir el archivo en modo de lectura
with open(filter_out_Q, "r") as archivo:
    # Leer cada línea del archivo
    for linea in archivo:
        # Convertir la línea a un entero firmado
        num = int(linea.strip(), 2)  # Convertir de binario a entero
        if linea[0] == '0':  # Si el primer bit es 0, entonces es positivo
            LOG_FILTER_OUT_Q.append((num)/(2**NBFrac))
        else:  # Si el primer bit es 1, convertir a negativo (complemento a 2)
            LOG_FILTER_OUT_Q.append((num - (1 << len(linea.strip())))/(2**NBFrac))


### LECTURA DE ARCHIVOS DE SIMBOLOS DOWN-SAMPLEADOS

# Fase 0 - I
with open(sym_down_samp_I_ph0, "r") as archivo:
    # Leer cada línea del archivo
    for linea in archivo:
        # Convertir la línea a un entero firmado
        num = int(linea.strip(), 2)  # Convertir de binario a entero
        if linea[0] == '0':  # Si el primer bit es 0, entonces es positivo
            LOG_RX_DW_SAM_I_PH0.append((num)/(2**NBFrac))
        else:  # Si el primer bit es 1, convertir a negativo (complemento a 2)
            LOG_RX_DW_SAM_I_PH0.append((num - (1 << len(linea.strip())))/(2**NBFrac))

# Fase 0 - Q
with open(sym_down_samp_Q_ph0, "r") as archivo:
    # Leer cada línea del archivo
    for linea in archivo:
        # Convertir la línea a un entero firmado
        num = int(linea.strip(), 2)  # Convertir de binario a entero
        if linea[0] == '0':  # Si el primer bit es 0, entonces es positivo
            LOG_RX_DW_SAM_Q_PH0.append((num)/(2**NBFrac))
        else:  # Si el primer bit es 1, convertir a negativo (complemento a 2)
            LOG_RX_DW_SAM_Q_PH0.append((num - (1 << len(linea.strip())))/(2**NBFrac))


#Fase 1 - I
with open(sym_down_samp_I_ph1, "r") as archivo:
    # Leer cada línea del archivo
    for linea in archivo:
        # Convertir la línea a un entero firmado
        num = int(linea.strip(), 2)  # Convertir de binario a entero
        if linea[0] == '0':  # Si el primer bit es 0, entonces es positivo
            LOG_RX_DW_SAM_I_PH1.append((num)/(2**NBFrac))
        else:  # Si el primer bit es 1, convertir a negativo (complemento a 2)
            LOG_RX_DW_SAM_I_PH1.append((num - (1 << len(linea.strip())))/(2**NBFrac))

#Fase 1 - Q
with open(sym_down_samp_Q_ph1, "r") as archivo:
    # Leer cada línea del archivo
    for linea in archivo:
        # Convertir la línea a un entero firmado
        num = int(linea.strip(), 2)  # Convertir de binario a entero
        if linea[0] == '0':  # Si el primer bit es 0, entonces es positivo
            LOG_RX_DW_SAM_Q_PH1.append((num)/(2**NBFrac))
        else:  # Si el primer bit es 1, convertir a negativo (complemento a 2)
            LOG_RX_DW_SAM_Q_PH1.append((num - (1 << len(linea.strip())))/(2**NBFrac))


#Fase 2 - I
with open(sym_down_samp_I_ph2, "r") as archivo:
    # Leer cada línea del archivo
    for linea in archivo:
        # Convertir la línea a un entero firmado
        num = int(linea.strip(), 2)  # Convertir de binario a entero
        if linea[0] == '0':  # Si el primer bit es 0, entonces es positivo
            LOG_RX_DW_SAM_I_PH2.append((num)/(2**NBFrac))
        else:  # Si el primer bit es 1, convertir a negativo (complemento a 2)
            LOG_RX_DW_SAM_I_PH2.append((num - (1 << len(linea.strip())))/(2**NBFrac))

#Fase 2 - Q
with open(sym_down_samp_Q_ph2, "r") as archivo:
    # Leer cada línea del archivo
    for linea in archivo:
        # Convertir la línea a un entero firmado
        num = int(linea.strip(), 2)  # Convertir de binario a entero
        if linea[0] == '0':  # Si el primer bit es 0, entonces es positivo
            LOG_RX_DW_SAM_Q_PH2.append((num)/(2**NBFrac))
        else:  # Si el primer bit es 1, convertir a negativo (complemento a 2)
            LOG_RX_DW_SAM_Q_PH2.append((num - (1 << len(linea.strip())))/(2**NBFrac))


#Fase 3 - I
with open(sym_down_samp_I_ph3, "r") as archivo:
    # Leer cada línea del archivo
    for linea in archivo:
        # Convertir la línea a un entero firmado
        num = int(linea.strip(), 2)  # Convertir de binario a entero
        if linea[0] == '0':  # Si el primer bit es 0, entonces es positivo
            LOG_RX_DW_SAM_I_PH3.append((num)/(2**NBFrac))
        else:  # Si el primer bit es 1, convertir a negativo (complemento a 2)
            LOG_RX_DW_SAM_I_PH3.append((num - (1 << len(linea.strip())))/(2**NBFrac))

#Fase 3 - Q
with open(sym_down_samp_Q_ph3, "r") as archivo:
    # Leer cada línea del archivo
    for linea in archivo:
        # Convertir la línea a un entero firmado
        num = int(linea.strip(), 2)  # Convertir de binario a entero
        if linea[0] == '0':  # Si el primer bit es 0, entonces es positivo
            LOG_RX_DW_SAM_Q_PH3.append((num)/(2**NBFrac))
        else:  # Si el primer bit es 1, convertir a negativo (complemento a 2)
            LOG_RX_DW_SAM_Q_PH3.append((num - (1 << len(linea.strip())))/(2**NBFrac))



### Gráfica de la salida del filtro
maxim1 = 6000 if(len(LOG_FILTER_OUT_I)>6000) else len(LOG_FILTER_OUT_I)
maxim2 = 6000 if(len(LOG_FILTER_OUT_Q)>6000) else len(LOG_FILTER_OUT_Q)

plt.figure(figsize=[10,6])

plt.subplot(2,1,1)
plt.plot(LOG_FILTER_OUT_I[510:maxim1],'g-',linewidth=2.0,label=r"Filtro I") #Para sim. comp.
plt.xlim(1000,1250)
plt.grid(True)
plt.legend()
plt.xlabel('Muestras')
plt.ylabel('Magnitud')

plt.subplot(2,1,2)
plt.plot(LOG_FILTER_OUT_Q[510:maxim2],'g-',linewidth=2.0,label=r"Filtro Q") #Para sim. comp.
plt.xlim(1000,1250)
plt.grid(True)
plt.legend()
plt.xlabel('Muestras')
plt.ylabel('Magnitud')



### Diagrama de Ojo 
fn.eyediagram(LOG_FILTER_OUT_I[0:maxim1],os,5,Nbauds) 
fn.eyediagram(LOG_FILTER_OUT_Q[0:maxim2],os,5,Nbauds)



### Constelación 
maxim1 = 6000 if(len(LOG_RX_DW_SAM_I_PH0)>6000) else len(LOG_RX_DW_SAM_I_PH0)
maxim2 = 6000 if(len(LOG_RX_DW_SAM_Q_PH0)>6000) else len(LOG_RX_DW_SAM_Q_PH0)
maxim3 = 6000 if(len(LOG_RX_DW_SAM_I_PH1)>6000) else len(LOG_RX_DW_SAM_I_PH1)
maxim4 = 6000 if(len(LOG_RX_DW_SAM_Q_PH1)>6000) else len(LOG_RX_DW_SAM_Q_PH1)
maxim5 = 6000 if(len(LOG_RX_DW_SAM_I_PH2)>6000) else len(LOG_RX_DW_SAM_I_PH2)
maxim6 = 6000 if(len(LOG_RX_DW_SAM_Q_PH2)>6000) else len(LOG_RX_DW_SAM_Q_PH2)
maxim7 = 6000 if(len(LOG_RX_DW_SAM_I_PH3)>6000) else len(LOG_RX_DW_SAM_I_PH3)
maxim8 = 6000 if(len(LOG_RX_DW_SAM_Q_PH3)>6000) else len(LOG_RX_DW_SAM_Q_PH3)

plt.figure(figsize=[8,8])

plt.subplot(2,2,1)
plt.plot(LOG_RX_DW_SAM_I_PH0[4:maxim1],
         LOG_RX_DW_SAM_Q_PH0[4:maxim2],
         '.',linewidth=2.0,
         label=r"Fase 0")
plt.xlim((-2, 2))
plt.ylim((-2, 2))
plt.grid(True)
plt.legend()
plt.ylabel('Imag')

plt.subplot(2,2,2)
plt.plot(LOG_RX_DW_SAM_I_PH1[4:maxim3],
         LOG_RX_DW_SAM_Q_PH1[4:maxim4],
         '.',linewidth=2.0,
         label="Fase 1")
plt.xlim((-2, 2))
plt.ylim((-2, 2))
plt.grid(True)
plt.legend()

plt.subplot(2,2,3)
plt.plot(LOG_RX_DW_SAM_I_PH2[4:maxim5],
         LOG_RX_DW_SAM_Q_PH2[4:maxim6],
         '.',linewidth=2.0,
         label=r"Fase 2")
plt.xlim((-2, 2))
plt.ylim((-2, 2))
plt.grid(True)
plt.legend()
plt.xlabel('Real')
plt.ylabel('Imag')

plt.subplot(2,2,4)
plt.plot(LOG_RX_DW_SAM_I_PH3[4:maxim7],
         LOG_RX_DW_SAM_Q_PH3[4:maxim8],
         '.',linewidth=2.0,
         label=r"Fase 3")
plt.xlim((-2, 2))
plt.ylim((-2, 2))
plt.grid(True)
plt.legend()
plt.xlabel('Real')

plt.show()
