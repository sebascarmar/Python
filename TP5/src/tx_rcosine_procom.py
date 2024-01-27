#!/usr/bin/env python
# coding: utf-8

# In[1]:


# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
from tool._fixedInt import *

##  ipython nbconvert --to latex --post PDF <Name.ipynb>

## Parametros generales
T     = 1.0/1.0e9       # Periodo de baudio
Nsymb = 1000            # Numero de simbolos
os    = 8               # Oversampling
## Parametros de la respuesta en frecuencia
Nfreqs = 256            # Cantidad de frecuencias

## Parametros del filtro de caida cosenoidal
beta   = [0.0,0.5,1.0]  # Roll-Off
Nbauds = 16             # Cantidad de baudios del filtro
## Parametros funcionales
Ts = T/os               # Frecuencia de muestreo


# In[2]:


def rcosine(beta, Tbaud, oversampling, Nbauds, Norm):
    """ Respuesta al impulso del pulso de caida cosenoidal """
    t_vect = np.arange(-0.5*Nbauds*Tbaud, 0.5*Nbauds*Tbaud, 
                       float(Tbaud)/oversampling)

    y_vect = []
    for t in t_vect:
        y_vect.append(np.sinc(t/Tbaud)*(np.cos(np.pi*beta*t/Tbaud)/
                                        (1-(4.0*beta*beta*t*t/
                                            (Tbaud*Tbaud)))))

    y_vect = np.array(y_vect)

    if(Norm):
        return (t_vect, y_vect/np.sqrt(np.sum(y_vect**2)))
        #return (t_vect, y_vect/y_vect.sum())
    else:
        return (t_vect,y_vect)


def floatToFixedPoint(rc0_0, rc0_5, rc1_0, fixedOption):
    # Listas vacías.
    fixed0 = []
    fixed1 = []    
    fixed2 = []
    
    # Se crean los ndarrays de numpy de punto fijo. Cada elemento es de la clase DeFixedInt.
    if( fixedOption == 1 ):   # S(8,7) con truncado y saturación
        aux0 = arrayFixedInt(8, 7, rc0_0, signedMode='S', roundMode='trunc', saturateMode='saturate')
        aux1 = arrayFixedInt(8, 7, rc0_5, signedMode='S', roundMode='trunc', saturateMode='saturate')
        aux2 = arrayFixedInt(8, 7, rc1_0, signedMode='S', roundMode='trunc', saturateMode='saturate')
        print("Punto Fijo S(8,7) truncado\n.")
    elif( fixedOption == 2 ): # S(8,7) con redondeo y saturación
        aux0 = arrayFixedInt(8, 7, rc0_0, signedMode='S', roundMode='round', saturateMode='saturate')
        aux1 = arrayFixedInt(8, 7, rc0_5, signedMode='S', roundMode='round', saturateMode='saturate')
        aux2 = arrayFixedInt(8, 7, rc1_0, signedMode='S', roundMode='round', saturateMode='saturate')
        print("Punto Fijo S(8,7) redondeo\n.")
    elif( fixedOption == 3 ): # S(3,2) con truncado y saturación
        aux0 = arrayFixedInt(3, 2, rc0_0, signedMode='S', roundMode='trunc', saturateMode='saturate')
        aux1 = arrayFixedInt(3, 2, rc0_5, signedMode='S', roundMode='trunc', saturateMode='saturate')
        aux2 = arrayFixedInt(3, 2, rc1_0, signedMode='S', roundMode='trunc', saturateMode='saturate')
        print("Punto Fijo S(3,2) con truncado\n.")
    elif( fixedOption == 4 ): # S(3,2) con redondeo y saturación
        aux0 = arrayFixedInt(3, 2, rc0_0, signedMode='S', roundMode='round', saturateMode='saturate')
        aux1 = arrayFixedInt(3, 2, rc0_5, signedMode='S', roundMode='round', saturateMode='saturate')
        aux2 = arrayFixedInt(3, 2, rc1_0, signedMode='S', roundMode='round', saturateMode='saturate')
        print("Punto Fijo S(3,2) con redondeo\n.")
    elif( fixedOption == 5 ): # S(6,4) con truncado y saturación
        aux0 = arrayFixedInt(6, 4, rc0_0, signedMode='S', roundMode='trunc', saturateMode='saturate')
        aux1 = arrayFixedInt(6, 4, rc0_5, signedMode='S', roundMode='trunc', saturateMode='saturate')
        aux2 = arrayFixedInt(6, 4, rc1_0, signedMode='S', roundMode='trunc', saturateMode='saturate')
        print("Punto Fijo S(6,4) con truncado\n.")
    elif( fixedOption == 6 ): # S(6,4) con redondeo y saturación
        aux0 = arrayFixedInt(6, 4, rc0_0, signedMode='S', roundMode='round', saturateMode='saturate')
        aux1 = arrayFixedInt(6, 4, rc0_5, signedMode='S', roundMode='round', saturateMode='saturate')
        aux2 = arrayFixedInt(6, 4, rc1_0, signedMode='S', roundMode='round', saturateMode='saturate')
        print("Punto Fijo S(6,4) con redondeo\n.")
    else:
        return (rc0_0, rc0_5, rc1_0)

    # Las listas vacías se llenan con los elementos fixeados. Estos objetos pasan como clases float64.
    for i in range(len(rc0_0)):
            fixed0.append(aux0[i].fValue)
    for i in range(len(rc0_0)):
        fixed1.append(aux1[i].fValue)
    for i in range(len(rc0_0)):
        fixed2.append(aux2[i].fValue)

    # Las listas son convertidas a ndarray de numpy, que ya posee objetos de tipo float64.
    rc0_0_fixed = np.array(fixed0)
    rc0_5_fixed = np.array(fixed1)
    rc1_0_fixed = np.array(fixed2)   

    return (rc0_0_fixed, rc0_5_fixed, rc1_0_fixed)


###########################################################################################
#                                 Respuesta temporal                                      #
###########################################################################################

# In[3]:

### Calculo de tres pulsos con diferente roll-off
(t,aux_rc0_0) = rcosine(beta[0], T,os,Nbauds,Norm=False)
(t,aux_rc0_5) = rcosine(beta[1], T,os,Nbauds,Norm=False)
(t,aux_rc1_0) = rcosine(beta[2], T,os,Nbauds,Norm=False)

# Se cuantiza con opciones:
#       1) S(8,7) trunc     5) S(6,4) trunc
#       2) S(8,7) round     6) S(6,4) round
#       3) S(3,2) trunc     7) Full Resolution
#       4) S(3,2) round
(rc0_0, rc0_5, rc1_0) = floatToFixedPoint(aux_rc0_0, aux_rc0_5, aux_rc1_0, 6)

#print (np.sum(rc0_0**2),np.sum(rc0_5**2),np.sum(rc1_0**2))

### Generacion de las graficas
plt.figure(figsize=[14,7])
plt.plot(t,rc0_0,'ro-',linewidth=2.0,label=r'$\beta=0.0$')
plt.plot(t,rc0_5,'gs-',linewidth=2.0,label=r'$\beta=0.5$')
plt.plot(t,rc1_0,'k^-',linewidth=2.0,label=r'$\beta=1.0$')
plt.legend()
plt.grid(True)
#plt.xlim(0,len(rc0_0)-1)
plt.xlabel('Muestras')
plt.ylabel('Magnitud')

symb00    = np.zeros(int(os)*3+1);symb00[os:len(symb00)-1:int(os)] = 1.0
rc0_0Symb00 = np.convolve(rc0_0,symb00);
rc0_5Symb00 = np.convolve(rc0_5,symb00);
rc1_0Symb00 = np.convolve(rc1_0,symb00);

offsetPot = os*((Nbauds//2)-1) + int(os/2)*(Nbauds%2) + 0.5*(os%2 and Nbauds%2)

plt.figure(figsize=[14,7])
plt.subplot(3,1,1)
plt.plot(np.arange(0,len(rc0_0)),rc0_0,'r.-',linewidth=2.0,label=r'$\beta=0.0$')
plt.plot(np.arange(os,len(rc0_0)+os),rc0_0,'k.-',linewidth=2.0,label=r'$\beta=0.0$')
plt.stem(np.arange(offsetPot,len(symb00)+offsetPot),symb00,label='Bits',use_line_collection=True)
plt.plot(rc0_0Symb00[os::],'--',linewidth=3.0,label='Convolution')
plt.legend()
plt.grid(True)
#plt.xlim(0,35)
plt.ylim(-0.2,1.4)
plt.xlabel('Muestras')
plt.ylabel('Magnitud')
plt.title('Rcosine - OS: %d'%int(os))

#plt.figure()
plt.subplot(3,1,2)
plt.plot(np.arange(0,len(rc0_5)),rc0_5,'r.-',linewidth=2.0,label=r'$\beta=0.5$')
plt.plot(np.arange(os,len(rc0_5)+os),rc0_5,'k.-',linewidth=2.0,label=r'$\beta=0.5$')
plt.stem(np.arange(offsetPot,len(symb00)+offsetPot),symb00,label='Bits',use_line_collection=True)
plt.plot(rc0_5Symb00[os::],'--',linewidth=3.0,label='Convolution')
plt.legend()
plt.grid(True)
#plt.xlim(0,35)
plt.ylim(-0.2,1.4)
plt.xlabel('Muestras')
plt.ylabel('Magnitud')
#plt.title('Rcosine - OS: %d'%int(os))

#plt.figure()
plt.subplot(3,1,3)
plt.plot(np.arange(0,len(rc1_0)),rc1_0,'r.-',linewidth=2.0,label=r'$\beta=1.0$')
plt.plot(np.arange(os,len(rc1_0)+os),rc1_0,'k.-',linewidth=2.0,label=r'$\beta=1.0$')
plt.stem(np.arange(offsetPot,len(symb00)+offsetPot),symb00,label='Bits',use_line_collection=True)
plt.plot(rc1_0Symb00[os::],'--',linewidth=3.0,label='Convolution')
plt.legend()
plt.grid(True)
#plt.xlim(0,35)
plt.ylim(-0.2,1.4)
plt.xlabel('Muestras')
plt.ylabel('Magnitud')
#plt.title('Rcosine - OS: %d'%int(os))

plt.show()


###########################################################################################
#                             Respuesta en frecuencia                                     #
###########################################################################################

# In[4]:


def resp_freq(filt, Ts, Nfreqs):
    """Computo de la respuesta en frecuencia de cualquier filtro FIR"""
    H = [] # Lista de salida de la magnitud
    A = [] # Lista de salida de la fase
    filt_len = len(filt)

    #### Genero el vector de frecuencias
    freqs = np.matrix(np.linspace(0,1.0/(2.0*Ts),Nfreqs))
    #### Calculo cuantas muestras necesito para 20 ciclo de
    #### la mas baja frec diferente de cero
    Lseq = 20.0/(freqs[0,1]*Ts)

    #### Genero el vector tiempo
    t = np.matrix(np.arange(0,Lseq))*Ts

    #### Genero la matriz de 2pifTn
    Omega = 2.0j*np.pi*(t.transpose()*freqs)

    #### Valuacion de la exponencial compleja en todo el
    #### rango de frecuencias
    fin = np.exp(Omega)

    #### Suma de convolucion con cada una de las exponenciales complejas
    for i in range(0,np.size(fin,1)):
        fout = np.convolve(np.squeeze(np.array(fin[:,i].transpose())),filt)
        mfout = abs(fout[filt_len:len(fout)-filt_len])
        afout = np.angle(fout[filt_len:len(fout)-filt_len])
        H.append(mfout.sum()/len(mfout))
        A.append(afout.sum()/len(afout))

    return [H,A,list(np.squeeze(np.array(freqs)))]


# In[5]:


### Calculo respuesta en frec para los tres pulsos
[H0,A0,F0] = resp_freq(rc0_0, Ts, Nfreqs)
[H1,A1,F1] = resp_freq(rc0_5, Ts, Nfreqs)
[H2,A2,F2] = resp_freq(rc1_0, Ts, Nfreqs)

### Generacion de los graficos
plt.figure(figsize=[14,6])
plt.semilogx(F0, 20*np.log10(H0),'r', linewidth=2.0, label=r'$\beta=0.0$')
plt.semilogx(F1, 20*np.log10(H1),'g', linewidth=2.0, label=r'$\beta=0.5$')
plt.semilogx(F2, 20*np.log10(H2),'k', linewidth=2.0, label=r'$\beta=1.0$')

plt.axvline(x=(1./Ts)/2.,color='k',linewidth=2.0)
plt.axvline(x=(1./T)/2.,color='b',linewidth=2.0)
plt.axhline(y=20*np.log10(0.5),color='b',linewidth=2.0)
plt.legend(loc=3)
plt.grid(True)
plt.xlim(F2[1],F2[len(F2)-1])
plt.xlabel('Frequencia [Hz]')
plt.ylabel('Magnitud [dB]')
plt.show()


###########################################################################################
#                         Convolución del filtro con símbolos                             #
###########################################################################################

# In[6]:

# PRBS
symbolsI = 2*(np.random.uniform(-1,1,Nsymb)>0.0)-1;
symbolsQ = 2*(np.random.uniform(-1,1,Nsymb)>0.0)-1;

#label = 'Simbolos: %d' % Nsymb
#plt.figure(figsize=[14,6])
#plt.subplot(1,2,1)
#plt.hist(symbolsI,label=label)
#plt.legend()
#plt.xlabel('Simbolos')
#plt.ylabel('Repeticiones')
#plt.subplot(1,2,2)
#plt.hist(symbolsQ,label=label)
#plt.legend()
#plt.xlabel('Simbolos')
#plt.ylabel('Repeticiones')
#
#plt.show()


# In[7]:

# Up-sampling before convolution
zsymbI = np.zeros(os*Nsymb); zsymbI[1:len(zsymbI):int(os)]=symbolsI
zsymbQ = np.zeros(os*Nsymb); zsymbQ[1:len(zsymbQ):int(os)]=symbolsQ

plt.figure(figsize=[10,6])
plt.subplot(2,1,1)
plt.plot(zsymbI,'o')
plt.xlim(0,20)
plt.grid(True)
plt.subplot(2,1,2)
plt.plot(zsymbQ,'o')
plt.xlim(0,20)
plt.grid(True)

plt.show()


# In[8]:


# # Calculo de tres pusos con diferente roll-off
# (t,rc0_01) = rcosine(0.1, T,os,Nbauds,Norm=True)
# (t,rc0_05) = rcosine(0.5, T,os,Nbauds,Norm=True)
# # Generacion de las graficas
# plt.figure()
# plt.plot(rc0_01,'o-r',linewidth=2.0,label=r'$\beta=0.1$')
# plt.plot(rc0_05,'s-g',linewidth=2.0,label=r'$\beta=0.5$')
# plt.legend()
# plt.grid(True)
# plt.xlim(0,len(rc0_01)-1)
# plt.xlabel('Muestras')
# plt.ylabel('Magnitud')
# #plt.show()


# In[13]:

# Convolution between coefs. and symbols
symb_out_B00I = np.convolve(rc0_0,zsymbI,'same'); symb_out_B00Q = np.convolve(rc0_0,zsymbQ,'same')
symb_out_B05I = np.convolve(rc0_5,zsymbI,'same'); symb_out_B05Q = np.convolve(rc0_5,zsymbQ,'same')
symb_out_B10I = np.convolve(rc1_0,zsymbI,'same'); symb_out_B10Q = np.convolve(rc1_0,zsymbQ,'same')

plt.figure(figsize=[10,6])
plt.subplot(2,1,1)
plt.plot(symb_out_B00I,'r-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[0])
plt.plot(symb_out_B05I,'g-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[1])
plt.plot(symb_out_B10I,'k-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[2])
plt.xlim(1000,1250)
plt.grid(True)
plt.legend()
plt.xlabel('Muestras')
plt.ylabel('Magnitud')

plt.subplot(2,1,2)
plt.plot(symb_out_B00Q,'r-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[0])
plt.plot(symb_out_B05Q,'g-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[1])
plt.plot(symb_out_B10Q,'k-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[2])
plt.xlim(1000,1250)
plt.grid(True)
plt.legend()
plt.xlabel('Muestras')
plt.ylabel('Magnitud')

#plt.figure(figsize=[10,6])
#plt.plot(np.correlate(symbolsI,2*(symb_out_B00I[3:len(symb_out_B00I):int(os)]>0.0)-1,'same'))

plt.show()


###########################################################################################
#                                   Diagrama de ojo                                       #
###########################################################################################

# In[14]:


def eyediagram(data, n, offset, period):
    span     = 2*n
    segments = int(len(data)/span)
    xmax     = (n-1)*period
    xmin     = -(n-1)*period
    x        = list(np.arange(-n,n,)*period)
    xoff     = offset

    plt.figure()
    for i in range(0,segments-1):
        plt.plot(x, data[(i*span+xoff):((i+1)*span+xoff)],'b')       
    plt.grid(True)
    plt.xlim(xmin, xmax)
    plt.show()


# In[15]:


eyediagram(symb_out_B00I[100:len(symb_out_B00I)-100],os,5,Nbauds)
eyediagram(symb_out_B00Q[100:len(symb_out_B00Q)-100],os,5,Nbauds)

eyediagram(symb_out_B05I[100:len(symb_out_B05I)-100],os,5,Nbauds)
eyediagram(symb_out_B05Q[100:len(symb_out_B05Q)-100],os,5,Nbauds)

eyediagram(symb_out_B10I[100:len(symb_out_B10I)-100],os,5,Nbauds)
eyediagram(symb_out_B10Q[100:len(symb_out_B10Q)-100],os,5,Nbauds)

plt.show()

#plt.show(block=False)
#raw_input("Press Enter")
#plt.close()


###########################################################################################
#                                    Constelaciones                                       #
###########################################################################################

# In[16]:

# Los arrays se recorren de a hasta b en pasos de a c (array[a:b:c])

offset = 6
plt.figure(figsize=[6,6])
plt.plot(symb_out_B00I[100+offset:len(symb_out_B00I)-(100-offset):int(os)],
         symb_out_B00Q[100+offset:len(symb_out_B00Q)-(100-offset):int(os)],
             '.',linewidth=2.0)
plt.xlim((-2, 2))
plt.ylim((-2, 2))
plt.grid(True)
plt.xlabel('Real')
plt.ylabel('Imag')

plt.figure(figsize=[6,6])
plt.plot(symb_out_B05I[100+offset:len(symb_out_B05I)-(100-offset):int(os)],
         symb_out_B05Q[100+offset:len(symb_out_B05Q)-(100-offset):int(os)],
             '.',linewidth=2.0)
plt.xlim((-2, 2))
plt.ylim((-2, 2))
plt.grid(True)
plt.xlabel('Real')
plt.ylabel('Imag')

plt.figure(figsize=[6,6])
plt.plot(symb_out_B10I[100+offset:len(symb_out_B10I)-(100-offset):int(os)],
         symb_out_B10Q[100+offset:len(symb_out_B10Q)-(100-offset):int(os)],
             '.',linewidth=2.0)
plt.xlim((-2, 2))
plt.ylim((-2, 2))
plt.grid(True)
plt.xlabel('Real')
plt.ylabel('Imag')

plt.show()


# In[ ]:




