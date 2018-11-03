import Coder
from  Gost_28147_89 import Gost_28147_89
import numpy as np
import itertools as it

class BC_coder(Coder.Coder):
    def __init__(self, IV=64*[0], block_size=64, change_bit_mode=None, change_bit_index=None):
        self.change_bit_mode = change_bit_mode
        self.change_bit_index = change_bit_index
        self.__block_size = block_size
        self.gost_coder = Gost_28147_89( change_bit_mode=self.change_bit_mode, change_bit_index=self.change_bit_index)
        self.__IV = 64*[0] #self.__make_format(IV)



    def bit_encode(self, message, key):
        length_mess = len(message)
        C = [self.__IV]
        for n in range(0, length_mess, self.__block_size):
            P = message[n: n + self.__block_size]
            tt = self.__IV
            for j in range(0,n//self.__block_size + 1):
                tt = self._OrBitList(tt,C[j])
            mess = self._XorBitList(tt, P)
            C.append(self.gost_coder.bit_encode(mess, key)[0])
        return list(it.chain.from_iterable(C[1:])),None


    def bit_decode(self, code, key):
        length_mess = len(code)
        C = [self.__IV]
        for n in range(0, length_mess, self.__block_size):
            P = code[n: n + self.__block_size]
            D = self.gost_coder.bit_decode(P, key)[0]

            F = self.__IV
            for j in range(0,n//self.__block_size + 1):
                F = self._OrBitList(F,C[j])
            mess = self._XorBitList(F, D)
            C.append(mess)
        return list(it.chain.from_iterable(C[1:])),None



