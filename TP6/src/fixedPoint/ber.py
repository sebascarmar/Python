import numpy as np

class ber:
    def __init__(self, CombPRBS):
        self.shifterBER = np.full(511,0)
        self.index_BER = 0
        self.cuenta_bit_err=CombPRBS
        self.error_min = CombPRBS
        self.combinacionesPRBS = CombPRBS
        self.latencia=0
        self.cuenta_bit_tot = 0


    def sincroniza(self, i, new_bit_rx, sym_downsamp):
        # Ingresa el nuevo símbolo al buffer de la BER Rx
        self.shifterBER    = np.roll(self.shifterBER,1)
        self.shifterBER[0] = new_bit_rx

        self.cuenta_bit_err += self.shifterBER[self.index_BER] ^ sym_downsamp
        
        if(i%self.combinacionesPRBS == 0 and i>0):
            if(self.cuenta_bit_err < self.error_min):
                self.error_min = self.cuenta_bit_err
                self.latencia = self.index_BER
            
            self.index_BER += 1
            self.cuenta_bit_err = 0

        return self.latencia


    def cuenta(self, i, new_bit_rx, sym_downsamp):
        # Ingresa el nuevo símbolo al buffer de la BER Rx
        self.shifterBER    = np.roll(self.shifterBER,1)
        self.shifterBER[0] = new_bit_rx

        self.cuenta_bit_err += self.shifterBER[self.latencia] ^ sym_downsamp
        #print(self.cuenta_bit_err, self.shifterBER[self.latencia] , sym_downsamp)
        #input()
        self.cuenta_bit_tot += 1
        
        return (self.cuenta_bit_err, self.cuenta_bit_tot)
