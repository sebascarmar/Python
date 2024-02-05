import numpy as np
from tool._fixedInt import *

class filtro:

    def __init__(self, rc, Nbauds, os, Nsymb, NBTot, NBFrac):
        ### Shifreg del filtro
        self.shifterFIR = np.full(Nbauds,0)
        ### Conjunto de coeficientes correspondientes a cada fase del filtro 
        self.coef_ph0 = []
        self.coef_ph1 = []
        self.coef_ph2 = []
        self.coef_ph3 = []
        for i in range(0,Nbauds*os,os):
            self.coef_ph0.append(rc[i])
            self.coef_ph1.append(rc[i+1])
            self.coef_ph2.append(rc[i+2])
            self.coef_ph3.append(rc[i+3])
        ### Productos parciales
        prod_parcial = np.zeros(6)
        self.prod_parcial = arrayFixedInt(NBTot, NBFrac, prod_parcial, 'S', 'trunc', 'saturate')
        ### Sumas parciales y final
        self.sum_lvl1_a = DeFixedInt(NBTot+1, NBFrac, 'S', 'trunc', 'saturate')
        self.sum_lvl1_b = DeFixedInt(NBTot+1, NBFrac, 'S', 'trunc', 'saturate')
        self.sum_lvl1_c = DeFixedInt(NBTot+1, NBFrac, 'S', 'trunc', 'saturate')
        self.sum_lvl2   = DeFixedInt(NBTot+2, NBFrac, 'S', 'trunc', 'saturate')
        self.sum_lvl3   = DeFixedInt(NBTot+3, NBFrac, 'S', 'trunc', 'saturate')
        ### Saturación y truncado
        sym_out   = np.zeros(Nsymb*os)
        self.sym_out   = arrayFixedInt(NBTot, NBFrac, sym_out, 'S', 'trunc', 'saturate')
        ### Contadores
        self.phase_counter = 0



    def convol(self, i, new_symb):
        menos = DeFixedInt(2, 1, 'S', 'trunc', 'saturate')
        menos.value = -1.0
        
        if(i%4 == 0):
            # Ingresa el nuevo símbolo al shifter del Filtro
            self.shifterFIR    = np.roll(self.shifterFIR,1)
            self.shifterFIR[0] = new_symb
        
        
        for j in range(6):
            if(self.phase_counter == 0):
                #prod_parcial[j].value =  -1*coef_ph0[j].fValue if(shifterFIR[j]==1) else coef_ph0[j].fValue
                self.prod_parcial[j].assign( menos*self.coef_ph0[j] if(self.shifterFIR[j]) else self.coef_ph0[j] )# S(8,6)
            elif(self.phase_counter == 1):                                                               
                #prod_parcial[j].value =  -1*coef_ph1[j].fValue if(shifterFIR[j]==1) else coef_ph1[j].fValue
                self.prod_parcial[j].assign( menos*self.coef_ph1[j] if(self.shifterFIR[j]) else self.coef_ph1[j] )# S(8,6)
            elif(self.phase_counter == 2):                                                              
                #prod_parcial[j].value =  -1*coef_ph2[j].fValue if(shifterFIR[j]==1) else coef_ph2[j].fValue
                self.prod_parcial[j].assign( menos*self.coef_ph2[j] if(self.shifterFIR[j]) else self.coef_ph2[j] )# S(8,6)
            elif(self.phase_counter == 3):                                                             
                #prod_parcial[j].value =  -1*coef_ph3[j].fValue if(shifterFIR[j]==1) else coef_ph3[j].fValue
                self.prod_parcial[j].assign( menos*self.coef_ph3[j] if(self.shifterFIR[j]) else self.coef_ph3[j] )# S(8.6)
        
        ### Actualiza contador (elección) de las fases
        self.phase_counter = self.phase_counter+1 if(self.phase_counter<3) else 0
         
        ### Sumas parciales y final para obtener la salida del filtro
        self.sum_lvl1_a.assign( self.prod_parcial[0]+self.prod_parcial[1] )# resulta S(9,6)
        self.sum_lvl1_b.assign( self.prod_parcial[2]+self.prod_parcial[3] )# resulta S(9,6)
        self.sum_lvl1_c.assign( self.prod_parcial[4]+self.prod_parcial[5] )# resulta S(9,6)
        self.sum_lvl2  .assign( self.sum_lvl1_a + self.sum_lvl1_b )# resulta S(10,6)
        self.sum_lvl3  .assign( self.sum_lvl2 + self.sum_lvl1_c   )# resulta S(11,6)
         
        ### Saturación y truncado para obtener la salida final
        self.sym_out[i].assign( self.sum_lvl3 )# resulta S(8,6)
        
        return self.sym_out[i].fValue
