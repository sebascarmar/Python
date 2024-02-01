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

NBTot  = 8
NBFrac = 6
NRegFilter = 5


########################## Obtención del filtro ##########################
(t,rc) = fn.rcosine(beta, T,os,Nbauds,Norm=False)

# Cuantiza los coeficientes del filtro
rc_fix          = arrayFixedInt(NBTot, NBFrac, rc, signedMode='S', roundMode='trunc', saturateMode='saturate')

# Los valores cuantizados los convierte a float64 para gráficas
rc_fix_float64  = fn.arrayFix_to_arrayFloat(rc_fix)

#print(rc)
#print(rc_fix_float64)

# Gráfica de la respuesta al impulso.
plt.figure(figsize=[14,7])
plt.plot(t,rc_fix_float64,'ro-',linewidth=2.0,label=r'$\beta=0.5$')
plt.legend()
plt.grid(True)
plt.xlabel('Muestras')
plt.ylabel('Magnitud')

#plt.show()


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
symI_fix = arrayFixedInt(NBTot, NBFrac, symI, signedMode='S', roundMode='trunc', saturateMode='saturate')
symQ_fix = arrayFixedInt(NBTot, NBFrac, symQ, signedMode='S', roundMode='trunc', saturateMode='saturate')

# Los valores cuantizados los convierte a float64 para gráficas
symI_fix_float64 = fn.arrayFix_to_arrayFloat(symI_fix)
symQ_fix_float64 = fn.arrayFix_to_arrayFloat(symQ_fix)

#print(symI)
#print(symI_fix)
#print(symI_fix_float64)

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
#plt.show()



################ Convolución de los símbolos con el filtro ###############
filter_reg_I = np.zeros(5+1)
filter_reg_Q = np.zeros(5+1)
nb_sym = 0

coef_ph0 = np.zeros(6)
coef_ph1 = np.zeros(6)
coef_ph2 = np.zeros(6)
coef_ph3 = np.zeros(6)
for i in range(0,Nbauds*os,4):
    coef_ph0[int(i/4)] = rc_fix[i].fValue
    coef_ph1[int(i/4)] = rc_fix[i+1].fValue
    coef_ph2[int(i/4)] = rc_fix[i+2].fValue
    coef_ph3[int(i/4)] = rc_fix[i+3].fValue
    #print(i, int(i/4), rc_fix[i].fValue)
phase_counter = 0
prod_parcial  = np.zeros(6)
print(coef_ph0)
print(coef_ph1)
print(coef_ph2)
print(coef_ph3)

for i in range(os*Nsymb):
    # Ingresa símbolo
    if(i%4 == 0):
        filter_reg_I = np.roll(filter_reg_I,1)
        
        filter_reg_I[0] = symI_fix[nb_sym].fValue
        
        nb_sym +=1
        phase_counter = 0

    if(phase_counter == 0):
        prod_parcial[i] = filter_reg_I[i] * coef_ph0[i] # resulta S(16,14)
    if(phase_counter == 1):
        prod_parcial[i] = filter_reg_I[i] * coef_ph1[i] # resulta S(16,14)
    if(phase_counter == 2):
        prod_parcial[i] = filter_reg_I[i] * coef_ph2[i] # resulta S(16,14)
    if(phase_counter == 3):
        prod_parcial[i] = filter_reg_I[i] * coef_ph3[i] # resulta S(16,14)
    
    

    #print(filter_reg_I)

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
