

class prbs9:

    def __init__(self, seed):
        self.reg = seed

    def get_new_symbol(self):
        # Calcula el nuevo bit de entrada al registro
        next_in  = ((self.reg>>4)^(self.reg>>8)) & 0b000000001
        # Desplaza el registro e ingresa el nuevo bit con LSB
        self.reg = ((self.reg<<1)|next_in) & 0b111111111
        # Obtiene el bit más significativo, que es la salida
        next_out = (self.reg>>8) & 0b000000001

        return next_out
