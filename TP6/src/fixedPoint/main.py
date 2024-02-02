import numpy as np
import matplotlib.pyplot as plt
from tool._fixedInt import *
import funciones as fn
from prbs9 import prbs9



############################### Parámetros ###############################
T     = 1.0/25.0e6    # Periodo de baudio
Nsymb = 1000          # Numero de simbolos
os    = 4             # Over-salmpling

Nfreqs = 256          # Cantidad de frecuencias

beta   = 0.5          # Roll-Off
Nbauds = 6            # Cantidad de baudios del filtro

Ts = T/os             # Frecuencia de muestreo

NBTot  = 8            # Cuantización: bits totales
NBFrac = 6            # Cuantización: bits fraccionales

NRegFilter = 5        # Cantidad de registros del shifter del filtro


########################## Obtención del filtro ##########################
(t,rc) = fn.rcosine(beta, T,os,Nbauds,Norm=False)

# Cuantiza los coeficientes del filtro
rc     = arrayFixedInt(NBTot, NBFrac, rc, signedMode='S', roundMode='trunc', saturateMode='saturate')


#print(rc)
#print(rc_float64)

# Gráfica de la respuesta al impulso.
plt.figure(figsize=[14,7])
plt.plot(t,fn.arrFixToFloat(rc),'ro-',linewidth=2.0,label=r'$\beta=0.5$')
plt.legend()
plt.grid(True)
plt.xlabel('Muestras')
plt.ylabel('Magnitud')

#plt.show()


################### Respuesta en frecuencia del filtro ###################
[Mag,Fas,Fq] = fn.resp_freq(fn.arrFixToFloat(rc), Ts, Nfreqs) #[magnitud, fase, freq]

### Gráfica de Bode
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



################################## PRBS ##################################
prbs9I = prbs9(0x1AA)
prbs9Q = prbs9(0x1FE)

symI = np.zeros(Nsymb)
symQ = np.zeros(Nsymb)
for i in range(Nsymb):
    symI[i] = (1 if(prbs9I.get_new_symbol()) else -1)
    symQ[i] = (1 if(prbs9Q.get_new_symbol()) else -1)

# Cuantiza los símbolos generados
symI = arrayFixedInt(NBTot, NBFrac, symI, signedMode='S', roundMode='trunc', saturateMode='saturate')
symQ = arrayFixedInt(NBTot, NBFrac, symQ, signedMode='S', roundMode='trunc', saturateMode='saturate')

#print(symI)
#print(symI)
#print(symI_fix_float64)

#################### Gráfica de bits símbolos generados ##################

plt.figure(figsize=[10,6])
plt.subplot(2,1,1)
plt.plot(fn.arrFixToFloat(symI),'o')
plt.xlim(0,20)
plt.grid(True)
plt.subplot(2,1,2)
plt.plot(fn.arrFixToFloat(symQ),'o')
plt.xlim(0,20)
plt.grid(True)
plt.xlim(0,20)
#plt.show()



######################### Up-sampling y filtrado #########################
symI_out = fn.upsamp_and_filter(NRegFilter, NBTot, NBFrac, Nbauds, os, Nsymb, rc, symI)

symQ_out = fn.upsamp_and_filter(NRegFilter, NBTot, NBFrac, Nbauds, os, Nsymb, rc, symQ)

# Gráfica de la salida del filtro
plt.figure(figsize=[10,6])

plt.subplot(2,1,1)
plt.plot(fn.arrFixToFloat(symI_out),'g-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta)
plt.xlim(1000,1250)
plt.grid(True)
plt.legend()
plt.xlabel('Muestras')
plt.ylabel('Magnitud')

plt.subplot(2,1,2)
plt.plot(fn.arrFixToFloat(symQ_out),'g-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta)
plt.xlim(1000,1250)
plt.grid(True)
plt.legend()
plt.xlabel('Muestras')
plt.ylabel('Magnitud')

#plt.show()



############################# Diagrama de Ojo ############################
fn.eyediagram(fn.arrFixToFloat(symI_out)[100:len(symI_out)-100],os,5,Nbauds)
fn.eyediagram(fn.arrFixToFloat(symQ_out)[100:len(symQ_out)-100],os,5,Nbauds)



############################## Constelación ##############################
offset = 0
plt.figure(figsize=[6,6])
plt.plot(fn.arrFixToFloat(symI_out)[100+offset:len(symI_out)-(100-offset):int(os)],
         fn.arrFixToFloat(symQ_out)[100+offset:len(symQ_out)-(100-offset):int(os)],
         '.',linewidth=2.0)
plt.xlim((-2, 2))
plt.ylim((-2, 2))
plt.grid(True)
plt.xlabel('Real')
plt.ylabel('Imag')

plt.show()
