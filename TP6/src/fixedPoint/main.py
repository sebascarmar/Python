import numpy as np
import matplotlib.pyplot as plt
from tool._fixedInt import *
import funciones as fn
from prbs9 import prbs9
from poly_filter import filtro
from ber import ber



############################### Parámetros ###############################
T     = 1.0/25.0e6    # Periodo de baudio
Nsymb = 262144        # Para la sim. completa, descom. lín.13 y cambiar el 4 por 511 en lin.148
                      #511 comp. p/cada 511 simb. (sincronizar) y 1022 simb. p/contar ber.
#Nsymb = 7155          # 4 comp. p/cada 511 simb. (sincro.) y 5110 p/contar ber.
os    = 4             # Over-salmpling

Nfreqs = 256          # Cantidad de frecuencias

beta   = 0.5          # Roll-Off
Nbauds = 6            # Cantidad de baudios del filtro

Ts = T/os             # Frecuencia de muestreo

NBTot  = 8            # Cuantización: bits totales
NBFrac = 6            # Cuantización: bits fraccionales

CombPRBS = (2**9)-1


LOG_COEF_FILTRO         = []
LOG_PRBS_I_TX           = []
LOG_PRBS_Q_TX           = []
LOG_FILTER_OUT_I        = []
LOG_FILTER_OUT_Q        = []
LOG_RX_I_DW_SAM         = []
LOG_RX_Q_DW_SAM         = []


################################ BER en Tx ###############################
### Instancia objeto para generación de símbolos para cada lane
prbs9I = prbs9([0, 1, 0, 1, 0, 1, 0, 1, 1]) # Seed: 0x1AA
prbs9Q = prbs9([0, 1, 1, 1, 1, 1, 1, 1, 1]) # Seed: 0x1FE

################################# Filtro #################################
### Coeficientes del filtro
(t,rc) = fn.rcosine(beta, T,os,Nbauds,Norm=False)
### Cuantiza los coeficientes
rc   = arrayFixedInt(NBTot, NBFrac, rc, 'S', 'trunc', 'saturate')
### Loguea los coeficientes
for i in range(len(rc)):
    LOG_COEF_FILTRO.append(rc[i].fValue)

### Instancia objeto de filtro para cada lane
filtradoI = filtro(rc, Nbauds, os, Nsymb, NBTot, NBFrac)
filtradoQ = filtro(rc, Nbauds, os, Nsymb, NBTot, NBFrac)

### Buffer temporal para almacenar el resultado de cada convoloución
sym_I_out_filter = 0.0
sym_Q_out_filter = 0.0

############################## Down-sampler ##############################
### Registro de 4 fases para cada lane. Usa un lugar más para poder
###representar hardware (carga el dato 1 clock después)
shifDwSam_I = np.zeros(os+1)
shifDwSam_Q = np.zeros(os+1)

############################### Slicer ###################################
### Regi. del slicer (el lugar extra sirve para simular la carga del dato)
buff_slicer_I = np.full(2,0)
buff_slicer_Q = np.full(2,0)

################################# PRBS Rx ################################
### Instancia prbs para el Rx con las mismas semillas que el Tx
prbs9I_rx = prbs9([0, 1, 0, 1, 0, 1, 0, 1, 1]) # Seed: 0x1AA
prbs9Q_rx = prbs9([0, 1, 1, 1, 1, 1, 1, 1, 1]) # Seed: 0x1FE

################################## BER Rx ################################
### Instanica los contadores de BER para cada lane. Cada buffer es de 511
ber_I = ber(CombPRBS)
ber_Q = ber(CombPRBS)

########################## Contadores y selectores #######################
sel_phase_4_dwsam = 2 # 0, 1, 2 o 3
index_dw_samp     = sel_phase_4_dwsam + 1 # Debido a que el reg. es más grande

latencia_I = 0  ;  bit_err_I = 0  ;  bit_tot_I = 0
latencia_Q = 0  ;  bit_err_Q = 0  ;  bit_tot_Q = 0



################################## Bucle #################################
for i in range(Nsymb*os):
    
    ################ PRBS Tx
    if(i%os == 0):
        ### Lane I
        new_bit_I_tx = prbs9I.get_new_symbol()
        ### Lane Q
        new_bit_Q_tx = prbs9Q.get_new_symbol()
        ### Logueo de bits generados
        LOG_PRBS_I_TX.append(-1 if(new_bit_I_tx) else 1)
        LOG_PRBS_Q_TX.append(-1 if(new_bit_Q_tx) else 1)

    ################ Upsampling y filtrado
    #### Lane I
    sym_I_out_filter = filtradoI.convol(i, new_bit_I_tx)
    #### Lane Q
    sym_Q_out_filter = filtradoQ.convol(i, new_bit_Q_tx)
    ### Logue los bits transmitidos
    LOG_FILTER_OUT_I.append(sym_I_out_filter)
    LOG_FILTER_OUT_Q.append(sym_Q_out_filter)

    ################ Down-sampling 
    ### Lane I: actualiza registro de down-sampling
    shifDwSam_I = np.roll(shifDwSam_I,1)
    shifDwSam_I[0] = sym_I_out_filter
    ### Lane Q: actualiza registro de down-sampling
    shifDwSam_Q = np.roll(shifDwSam_Q,1)
    shifDwSam_Q[0] = sym_Q_out_filter
    
    ################ Slicer
    ### Buffer de slicer con simulación de un clock de demora en cargar el dato
    ###en ambos lanes.
    if(i%os == 0):
        ### Lane I: desplaza (carga el signo para la siguiente comparación)
        ###         detecta el signo de la comp. siguiente de la siguiente
        buff_slicer_I    = np.roll(buff_slicer_I, 1)
        buff_slicer_I[0] = 0 if(shifDwSam_I[index_dw_samp]>=0.0) else 1
        ### Lane Q: desplaza (carga el signo para la siguiente comparación)
        ###         detecta el signo de la comp. siguiente de la siguiente
        buff_slicer_Q    = np.roll(buff_slicer_Q, 1)
        buff_slicer_Q[0] = 0 if(shifDwSam_Q[index_dw_samp]>=0.0) else 1
        ### Loguea los símbolos down-sampleandos
        LOG_RX_I_DW_SAM.append(shifDwSam_I[index_dw_samp])
        LOG_RX_Q_DW_SAM.append(shifDwSam_Q[index_dw_samp])

    ################ BER Rx
    if(i%os == 0):
        ### Lane I: PRBS Rx genera un nuevo símbolo
        new_bit_I_rx = prbs9I_rx.get_new_symbol()
        ### Lane Q: PRBS Rx genera un nuevo símbolo
        new_bit_Q_rx = prbs9Q_rx.get_new_symbol()
        
        ### Sincroniza con los 1eros 4*511 símbolos downsampleados
        if(i<=CombPRBS*511*os ):
            ### Lane I: sincroniza
            latencia_I = ber_I.sincroniza( i, new_bit_I_rx, buff_slicer_I[1] )
            ### Lane Q: sincroniza
            latencia_Q = ber_Q.sincroniza( i, new_bit_Q_rx, buff_slicer_Q[1] )
        ### Conteo de errores y de bits totales
        else:
            ### Lane I: cuenta
            (bit_err_I, bit_tot_I)=ber_I.cuenta( i, new_bit_I_rx, buff_slicer_I[1] )
            ### Lane Q: cuenta
            (bit_err_Q, bit_tot_Q)=ber_Q.cuenta( i, new_bit_Q_rx, buff_slicer_Q[1] )




print("BER_I =",bit_err_I/bit_tot_I, " - Latencia_I =", latencia_I)
print("BER_Q =",bit_err_Q/bit_tot_Q, " - Latencia_Q =", latencia_Q)

####################### Escritura de datos para VM #######################
## Escribe los coeficientes como una cadena en su represetnación binaria (para Verilog)
#with open('CoefFilter.dat', 'w') as binString:
#    for i in range(len(rc)):
#        binString.write((format(int(rc[i].fValue*(2**NBFrac)), '08b')[-8:] 
#                         if(rc[i].fValue>0.0) else 
#                         format((1 << 8) + int(rc[i].fValue*(2**NBFrac)), '08b')[-8:])
#                         + '\n')

with open('CoefFilter.txt', 'w') as archivo:
    for i in range(len(rc)):
        archivo.write(str(int(rc[i].fValue*(2**NBFrac))) + '\n')

### Bits generados por las PRBS
with open('VM_I_PRBS_Tx.txt', 'w') as archivo:
    for i in range(len(LOG_PRBS_I_TX)):
        archivo.write(str(0 if(LOG_PRBS_I_TX[i]>0) else 1) + '\n')

with open('VM_Q_PRBS_Tx.txt', 'w') as archivo:
    for i in range(len(LOG_PRBS_Q_TX)):
        archivo.write(str(0 if(LOG_PRBS_Q_TX[i]>0) else 1) + '\n')

### Salida de los filtros - convolución
with open('VM_I_FilterOut.txt', 'w') as archivo:
    for i in range(len(LOG_FILTER_OUT_I)):
        archivo.write(str(int(LOG_FILTER_OUT_I[i]*(2**NBFrac))) + '\n')

with open('VM_Q_FilterOut.txt', 'w') as archivo:
    for i in range(len(LOG_FILTER_OUT_Q)):
        archivo.write(str(int(LOG_FILTER_OUT_Q[i]*(2**NBFrac))) + '\n')

### Símbolos down-sampleados
with open('VM_I_DownSamp.txt', 'w') as archivo:
    for i in range(len(LOG_RX_I_DW_SAM)):
        archivo.write(str(int(LOG_RX_I_DW_SAM[i]*(2**NBFrac))) + '\n')

with open('VM_Q_DownSamp.txt', 'w') as archivo:
    for i in range(len(LOG_RX_Q_DW_SAM)):
        archivo.write(str(int(LOG_RX_Q_DW_SAM[i]*(2**NBFrac))) + '\n')




################################ Gráficas ################################

### Gráfica de la respuesta al impulso.
plt.figure(figsize=[14,7])
plt.plot(t,LOG_COEF_FILTRO,'ro-',linewidth=2.0,label=r'$\beta=0.5$')
plt.legend()
plt.grid(True)
plt.xlabel('Muestras')
plt.ylabel('Magnitud')

#plt.show()


### Gráfica de Bode
[Mag,Fas,Fq] = fn.resp_freq(LOG_COEF_FILTRO, Ts, Nfreqs) #[magnitud, fase, freq]

plt.figure(figsize=[14,6])
plt.semilogx(Fq, 20*np.log10(Mag),'r', linewidth=2.0, label=r'$\beta=0.0$')
plt.axvline(x=(1./Ts)/2.,color='k',linewidth=2.0)
plt.axvline(x=(1./T)/2.,color='k',linewidth=2.0)
plt.axhline(y=20*np.log10(0.5),color='k',linewidth=2.0)
plt.legend(loc=3)
plt.grid(True)
plt.xlim(Fq[1],Fq[len(Fq)-1])
plt.ylim(-90,15)
plt.xlabel('Frequencia [Hz]')
plt.ylabel('Magnitud [dB]')

#plt.show()


### Gráfica de bits símbolos generados 
plt.figure(figsize=[10,6])
plt.subplot(2,1,1)
#plt.plot(LOG_PRBS_I_TX,'o')
plt.plot(LOG_PRBS_I_TX[127000:len(LOG_PRBS_I_TX)-127000],'o') #Para sim. completa
plt.xlim(0,20) 
plt.grid(True)
plt.subplot(2,1,2)
#plt.plot(LOG_PRBS_Q_TX,'o')
plt.plot(LOG_PRBS_Q_TX[127000:len(LOG_PRBS_Q_TX)-127000],'o') #Para sim. completa
plt.xlim(0,20)
plt.grid(True)
plt.xlim(0,20)

#plt.show()


### Gráfica de la salida del filtro
plt.figure(figsize=[10,6])

plt.subplot(2,1,1)
#plt.plot(LOG_FILTER_OUT_I,'g-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta)
plt.plot(LOG_FILTER_OUT_I[510000:len(LOG_FILTER_OUT_I)-510000],'g-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta) #Para sim. comp.
plt.xlim(1000,1250)
plt.grid(True)
plt.legend()
plt.xlabel('Muestras')
plt.ylabel('Magnitud')

plt.subplot(2,1,2)
#plt.plot(LOG_FILTER_OUT_Q,'g-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta)
plt.plot(LOG_FILTER_OUT_Q[510000:len(LOG_FILTER_OUT_Q)-510000],'g-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta) #Para sim. comp.
plt.xlim(1000,1250)
plt.grid(True)
plt.legend()
plt.xlabel('Muestras')
plt.ylabel('Magnitud')

#plt.show()


### Diagrama de Ojo 
#fn.eyediagram(LOG_FILTER_OUT_I[100:len(LOG_FILTER_OUT_Q)-100],os,5,Nbauds)
#fn.eyediagram(LOG_FILTER_OUT_Q[100:len(LOG_FILTER_OUT_Q)-100],os,5,Nbauds)
fn.eyediagram(LOG_FILTER_OUT_I[510000:len(LOG_FILTER_OUT_I)-510000],os,5,Nbauds) # Para sim. completa
fn.eyediagram(LOG_FILTER_OUT_Q[510000:len(LOG_FILTER_OUT_Q)-510000],os,5,Nbauds) # Para sim. completa



### Constelación 
plt.figure(figsize=[6,6])
#plt.plot(LOG_RX_I_DW_SAM, LOG_RX_Q_DW_SAM,'.',linewidth=2.0)
plt.plot(LOG_RX_I_DW_SAM[118000:len(LOG_RX_I_DW_SAM)-118000], # Para sim. completa
         LOG_RX_Q_DW_SAM[118000:len(LOG_RX_Q_DW_SAM)-118000],
         '.',linewidth=2.0)
plt.xlim((-2, 2))
plt.ylim((-2, 2))
plt.grid(True)
plt.xlabel('Real')
plt.ylabel('Imag')

plt.show()
