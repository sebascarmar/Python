import numpy as np

class ber:
    def __init__(self, CombPRBS):
        ### 511+1 para simular la carga del dato en el siguiente clock
        self.shifterBER     = np.full(511+1,0) 
        ### Puntero al shifter (p/sincronización)
        self.index_BER      = 0                
        ### Puntero al shifter, en la que se tiene el menor error (p/conteo ber)
        self.latencia       = 0                
        ### Contador de errores (p/sincronización y p/conteo ber)
        self.cuenta_bit_err = 0
        ### Conteador de bits totales (p/conteo de ber, post sincronización)
        self.cuenta_bit_tot = 0
        ### Permite almacenar el menor error para detectar la latencia
        self.error_min      = CombPRBS
        ### Cantindad de combinaciones de la prbs9
        self.combinacionesPRBS = CombPRBS


    def sincroniza(self, i, new_bit_prbs_rx, sym_downsamp):
        ### Ingresa el nuevo bit generado por la prbs al buffer de la BER Rx
        self.shifterBER    = np.roll(self.shifterBER,1)
        self.shifterBER[0] = new_bit_prbs_rx
        
        ### Aumenta la cuenta si son distintos
        self.cuenta_bit_err += self.shifterBER[self.index_BER+1] ^ sym_downsamp
        
        ### Si ya hizo las 511 comparaciones con la misma index_BER, entra
        if(i%self.combinacionesPRBS == 0 and i>0):
            if(self.cuenta_bit_err < self.error_min):
                self.error_min = self.cuenta_bit_err
                self.latencia  = self.index_BER
            
            self.index_BER     += 1
            self.cuenta_bit_err = 0

        return self.latencia


    def cuenta(self, i, new_bit_prbs_rx, sym_downsamp):
        # Ingresa el nuevo símbolo al buffer de la BER Rx
        self.shifterBER    = np.roll(self.shifterBER,1)
        self.shifterBER[0] = new_bit_prbs_rx

        self.cuenta_bit_err += self.shifterBER[self.latencia+1] ^ sym_downsamp
        #print(self.cuenta_bit_err, self.shifterBER[self.latencia] , sym_downsamp)
        #input()
        self.cuenta_bit_tot += 1
        
        return (self.cuenta_bit_err, self.cuenta_bit_tot)

    def imprime(self, i):
        print("i:",i,self.shifterBER[1],self.shifterBER[0:20],self.cuenta_bit_err)
        input()
