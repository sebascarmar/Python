import numpy as np

class prbs9:

    def __init__(self, seed):
        self.reg = np.array(seed)

    def get_new_symbol(self):
        aux_out = self.reg[8] 
        # Calcula el nuevo bit de entrada al registro
        new_in  = self.reg[4]^self.reg[8]
        # Desplaza el registro e ingresa el nuevo bit con LSB
        self.reg = np.roll(self.reg,1)
        self.reg[0] = new_in

        return aux_out
