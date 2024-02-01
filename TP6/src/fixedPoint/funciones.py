import numpy as np
import matplotlib.pyplot as plt
from tool._fixedInt import *

def rcosine(beta, Tbaud, oversampling, Nbauds, Norm):
    """ Respuesta al impulso del pulso de caida cosenoidal """
    t_aux = np.arange(-0.5*Nbauds*Tbaud, 0.5*Nbauds*Tbaud, 
                       float(Tbaud)/oversampling)
    t_vect = []
    for i in range(oversampling*Nbauds): # Asegura la cant. de coef.
        t_vect.append(t_aux[i])


    y_vect = []
    for t in t_vect:
        y_vect.append(np.sinc(t/Tbaud)*(np.cos(np.pi*beta*t/Tbaud)/
                                        (1-(4.0*beta*beta*t*t/
                                            (Tbaud*Tbaud)))))

    y_vect = np.array(y_vect)

    if(Norm):
        #return (t_vect, y_vect/np.sqrt(np.sum(y_vect**2))) #normalia la energía del filtro
        return (t_vect, y_vect/y_vect.sum())
    else:
        return (t_vect,y_vect)



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
    #plt.show()



def arrFixToFloat(vect):
    aux = []
    for i in range(len(vect)):
        aux.append(vect[i].fValue)

    return aux



def upsamp_and_filter(NRegFilter, NBTot, NBFrac, Nbauds, os, Nsymb, rc, sym):
    # Registro de desplazamiento del filtro RC
    shifter = np.zeros(NRegFilter+1)
    shifter = arrayFixedInt(NBTot, NBFrac, shifter, signedMode='S', roundMode='trunc', saturateMode='saturate')
    
    # Obtención de las distintas fases del filtro RC
    coef_ph0 = []
    coef_ph1 = []
    coef_ph2 = []
    coef_ph3 = []
    for i in range(0,Nbauds*os,os):
        coef_ph0.append(rc[i])
        coef_ph1.append(rc[i+1])
        coef_ph2.append(rc[i+2])
        coef_ph3.append(rc[i+3])
        #print(i, int(i/4), rc[i].fValue)
    #coef_ph0 = arrayFixedInt(NBTot, NBFrac, coef_ph0, signedMode='S', roundMode='trunc', saturateMode='saturate')
    #coef_ph1 = arrayFixedInt(NBTot, NBFrac, coef_ph1, signedMode='S', roundMode='trunc', saturateMode='saturate')
    #coef_ph2 = arrayFixedInt(NBTot, NBFrac, coef_ph2, signedMode='S', roundMode='trunc', saturateMode='saturate')
    #coef_ph3 = arrayFixedInt(NBTot, NBFrac, coef_ph3, signedMode='S', roundMode='trunc', saturateMode='saturate')
     
     
     
    #print(coef_ph0)
    #print(coef_ph1)
    #print(coef_ph2)
    #print(coef_ph3)
    #print("\n")
     
    #Productos parciales
    prod_parcial = np.zeros(6)
    prod_parcial = arrayFixedInt(2*NBTot, 2*NBFrac, prod_parcial, signedMode='S', roundMode='trunc', saturateMode='saturate')
    # Sumas parciales y final
    sum_lvl1_a = DeFixedInt(roundMode='trunc',signedMode = 'S',intWidth=2*NBTot+1,fractWidth=2*NBFrac,saturateMode='saturate')
    sum_lvl1_b = DeFixedInt(roundMode='trunc',signedMode = 'S',intWidth=2*NBTot+1,fractWidth=2*NBFrac,saturateMode='saturate')
    sum_lvl1_c = DeFixedInt(roundMode='trunc',signedMode = 'S',intWidth=2*NBTot+1,fractWidth=2*NBFrac,saturateMode='saturate')
    sum_lvl2   = DeFixedInt(roundMode='trunc',signedMode = 'S',intWidth=2*NBTot+2,fractWidth=2*NBFrac,saturateMode='saturate')
    sum_lvl3   = DeFixedInt(roundMode='trunc',signedMode = 'S',intWidth=2*NBTot+3,fractWidth=2*NBFrac,saturateMode='saturate')
    # Saturación y truncado
    sym_out   = np.zeros(Nsymb*os)
    sym_out   = arrayFixedInt(NBTot, NBFrac, sym_out, signedMode='S', roundMode='trunc', saturateMode='saturate')
    # Contadores
    next_sym      = 0
    phase_counter = 0
     
        
    for i in range(os*Nsymb):
        # Ingresa símbolo al shifter
        if(i%4 == 0):
            shifter    = np.roll(shifter,1)
            shifter[0] = sym[next_sym]
            next_sym += 1
        
     
        #print(phase_counter, next_sym, "\n")
     
        # Realiza los productos del shifter con los coeficientes de las fases del filtro
        for j in range(6):
            if(phase_counter == 0):
                prod_parcial[j].assign( shifter[j] * coef_ph0[j]) # resulta S(16,12)
                #print("ph0",prod_parcial[j].fValue, "\t", shifter[j].fValue,"\t", coef_ph0[j].fValue)
            elif(phase_counter == 1):
                prod_parcial[j].assign( shifter[j] * coef_ph1[j]) # resulta S(16,12)
                #print("ph1",prod_parcial[j].fValue,"\t",  shifter[j].fValue,"\t", coef_ph1[j].fValue)
            elif(phase_counter == 2):
                prod_parcial[j].assign(shifter[j] * coef_ph2[j]) # resulta S(16,12)
                #print("ph2",prod_parcial[j].fValue, "\t",shifter[j].fValue,"\t", coef_ph2[j].fValue)
            elif(phase_counter == 3):
                prod_parcial[j].assign(shifter[j] * coef_ph3[j]) # resulta S(16,12)
                #print("ph3",prod_parcial[j].fValue,"\t", shifter[j].fValue,"\t", coef_ph3[j].fValue)
     
        # Actualiza contador (elección) de las fases
        phase_counter = phase_counter+1 if(phase_counter<3) else 0
     
        # Sumas parciales y final para obtener la salida del filtro
        sum_lvl1_a = prod_parcial[0]+prod_parcial[1] # resulta S(17,12)
        sum_lvl1_b = prod_parcial[2]+prod_parcial[3] # resulta S(17,12)
        sum_lvl1_c = prod_parcial[4]+prod_parcial[5] # resulta S(17,12)
        sum_lvl2   = sum_lvl1_a + sum_lvl1_b # resulta S(18,12)
        sum_lvl3   = sum_lvl2 + sum_lvl1_c   # resulta S(19,12)
     
        # Saturación y truncado para obtener la salida final
        sym_out[i].assign(sum_lvl3)         # resulta S(8,6)
     
        #input()
        #print(i)
        
        
        #print(symI_out)
        #print(filter_reg_I)

    return sym_out
