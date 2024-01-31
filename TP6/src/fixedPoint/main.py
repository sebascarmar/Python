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


########################## Obtención del filtro ##########################
(t,rc) = fn.rcosine(beta, T,os,Nbauds,Norm=False)

# Cuantiza los coeficientes del filtro
rc_fix          = arrayFixedInt(8, 7, rc, signedMode='S', roundMode='trunc', saturateMode='saturate')

# Los valores cuantizados los convierte a float64 para gráficas
rc_fix_float64  = fn.arrayFix_to_arrayFloat(rc_fix)

print(rc)
print(rc_fix_float64)

# Gráfica de la respuesta al impulso.
plt.figure(figsize=[14,7])
plt.plot(t,rc_fix_float64,'ro-',linewidth=2.0,label=r'$\beta=0.5$')
plt.legend()
plt.grid(True)
plt.xlabel('Muestras')
plt.ylabel('Magnitud')

plt.show()


################### Respuesta en frecuencia del filtro ###################
[Mag,Fas,Fq] = fn.resp_freq(rc_fix_float64, Ts, Nfreqs) #[magnitud, fase, freq]

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
prbs9I = prbs9(0x1AA)
prbs9Q = prbs9(0x1FE)

symI = []
symQ = []
for i in range(Nsymb):
    symI.append(1 if(prbs9I.get_new_symbol()) else -1)
    symQ.append(1 if(prbs9Q.get_new_symbol()) else -1)

# Cuantiza los símbolos generados
symI_fix = arrayFixedInt(8, 7, symI, signedMode='S', roundMode='trunc', saturateMode='saturate')
symQ_fix = arrayFixedInt(8, 7, symQ, signedMode='S', roundMode='trunc', saturateMode='saturate')

# Los valores cuantizados los convierte a float64 para gráficas
symI_fix_float64 = fn.arrayFix_to_arrayFloat(symI_fix)
symQ_fix_float64 = fn.arrayFix_to_arrayFloat(symQ_fix)


#################### Gráfica de bits símbolos generados ##################

plt.figure(figsize=[10,6])
plt.subplot(2,1,1)
plt.plot(symI_fix_float64,'o')
plt.xlim(0,20)
plt.grid(True)
plt.subplot(2,1,2)
plt.plot(symQ_fix_float64,'o')
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
