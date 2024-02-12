import numpy as np
import matplotlib.pyplot as plt
from tool._fixedInt import *
import funciones as fn



############################### Parámetros ###############################
T     = 1.0/25.0e6    # Periodo de baudio
Nsymb = 1000          # Numero de simbolos
os    = 4             # Over-salmpling

Nfreqs = 256          # Cantidad de frecuencias

beta   = 0.5          # Roll-Off
Nbauds = 8            # Cantidad de baudios del filtro

Ts = T/os             # Frecuencia de muestreo


########################## Obtención del filtro ##########################
(t,rc) = fn.rcosine(beta, T,os,Nbauds,Norm=False)
#print(rc)

# Gráfica de la respuesta al impulso.
plt.figure(figsize=[14,7])
plt.plot(t,rc,'ro-',linewidth=2.0,label=r'$\beta=0.5$')
plt.legend()
plt.grid(True)
plt.xlabel('Muestras')
plt.ylabel('Magnitud')

plt.show()


################### Respuesta en frecuencia del filtro ###################
[Mag,Fas,Fq] = fn.resp_freq(rc, Ts, Nfreqs) #[magnitud, fase, freq]

### Gráfica de Bode
plt.figure(figsize=[14,6])
plt.semilogx(Fq, 20*np.log10(Mag),'r', linewidth=2.0, label=r'$\beta=0.0$')
plt.axvline(x=(1./Ts)/2.,color='k',linewidth=2.0)
plt.axvline(x=(1./T)/2.,color='k',linewidth=2.0)
plt.axhline(y=20*np.log10(0.5),color='k',linewidth=2.0)
plt.legend(loc=3)
plt.grid(True)
plt.xlim(Fq[1],Fq[len(Fq)-1])
plt.xlabel('Frequencia [Hz]')
plt.ylabel('Magnitud [dB]')

plt.show()



################################## PRBS ##################################
symbolsI = 2*(np.random.uniform(-1,1,Nsymb)>0.0)-1;
symbolsQ = 2*(np.random.uniform(-1,1,Nsymb)>0.0)-1;



############################### Up-Sampling ##############################
zsymbI = np.zeros(os*Nsymb); zsymbI[1:len(zsymbI):int(os)]=symbolsI
zsymbQ = np.zeros(os*Nsymb); zsymbQ[1:len(zsymbQ):int(os)]=symbolsQ

# Gráfica de bits transmitidos
plt.figure(figsize=[10,6])
plt.subplot(2,1,1)
plt.plot(zsymbI,'o')
plt.xlim(0,20)
plt.grid(True)
plt.subplot(2,1,2)
plt.plot(zsymbQ,'o')
plt.xlim(0,20)
plt.grid(True)
plt.xlim(0,20)
plt.show()



################ Convolución de los símbolos con el filtro ###############
symb_outI = np.convolve(rc,zsymbI,'same')
symb_outQ = np.convolve(rc,zsymbQ,'same')

#symb_outI = symb_outI/np.std(symb_outI)
#symb_outQ = symb_outQ/np.std(symb_outQ)

# Gráfica de la salida del filtro
plt.figure(figsize=[10,6])

plt.subplot(2,1,1)
plt.plot(symb_outI,'g-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta)
plt.xlim(1000,1250)
plt.grid(True)
plt.legend()
plt.xlabel('Muestras')
plt.ylabel('Magnitud')

plt.subplot(2,1,2)
plt.plot(symb_outQ,'g-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta)
plt.xlim(1000,1250)
plt.grid(True)
plt.legend()
plt.xlabel('Muestras')
plt.ylabel('Magnitud')

plt.show()



############################# Diagrama de Ojo ############################
fn.eyediagram(symb_outI[100:len(symb_outI)-100],os,5,Nbauds)
fn.eyediagram(symb_outQ[100:len(symb_outQ)-100],os,5,Nbauds)



############################## Constelación ##############################
offset = 2
plt.figure(figsize=[6,6])
plt.plot(symb_outI[100+offset:len(symb_outI)-(100-offset):int(os)],
         symb_outQ[100+offset:len(symb_outQ)-(100-offset):int(os)],
         '.',linewidth=2.0)
plt.xlim((-2, 2))
plt.ylim((-2, 2))
plt.grid(True)
plt.xlabel('Real')
plt.ylabel('Imag')

plt.show()



######################### Estimación de BER ##############################
plt.figure(figsize=[10,6])
plt.plot(np.correlate(symbolsI,2*(symb_outI[3:len(symb_outI):int(os)]>0.0)-1,'same'))
plt.show()
