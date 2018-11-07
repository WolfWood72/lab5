import Coder
from  Gost_28147_89 import Gost_28147_89
import numpy as np
import itertools as it

class Devis_Price(Coder.Coder):
    def __init__(self,  block_size=64, change_bit_mode=None):
        super(Devis_Price, self).__init__()
        self.change_bit_mode = change_bit_mode
        self._block_size = block_size
        self.gost_coder = Gost_28147_89()
        self.n_block = 1


    def bit_encode(self, message, iv, key1, key2):
        length_mess = len(message)
        C = []
        for n in range(0, length_mess, self._block_size):
            P = message[n: n + self._block_size]
            if n == 0:
                tt = iv
            else:
                tt = C[-1]

            #print("{}:  {}".format(n, str(tt)))
            mess = self._XorBitList(tt, P)
            C.append(self.gost_coder.bit_encode(mess, key1)[0])
        #print(C)
        return  self.gost_coder.bit_encode(list(it.chain.from_iterable(C)),key2)[0],None


    def bit_decode(self, code, iv, key1, key2):
        length_mess = len(code)

      #  C = [ code[i*self.__block_size: (i+1)* self.__block_size] for i in range(0, length_mess// self.__block_size+1)]
        code = self.gost_coder.bit_decode(code,key2)[0]

        C = [code[i * self._block_size: (i + 1) * self._block_size] for i in
             range(0, length_mess // self._block_size + 1)]
        #print(C)
        M = []
        for n in range(0, length_mess, self._block_size):
            P = code[n: n + self._block_size]
            D = self.gost_coder.bit_decode(P, key1)[0]
            if n == 0:
                F = iv
            else:
                F = C[n // self._block_size - 1]

           # print("{}:  {}".format(n, str(F)))
            mess = self._XorBitList(F, D)
            M.append(mess)
        return list(it.chain.from_iterable(M)),None



