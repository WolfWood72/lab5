import Coder
from  Gost_28147_89 import Gost_28147_89
import numpy as np
import itertools as it

class BC_coder(Coder.Coder):
    def __init__(self,  block_size=64, change_bit_mode=None):
        super(BC_coder, self).__init__()
        self.change_bit_mode = change_bit_mode
        self._block_size = block_size
        self.gost_coder = Gost_28147_89()
        self.n_block = 3


    def bit_encode(self, message, iv , key ):
   #     iv = [0]*64

        length_mess = len(message)
        C = []
     #   print(message)
     #   print(key)
     #   print(iv)
        for n in range(0, length_mess, self._block_size):
            P = message[n: n + self._block_size]
            if n == 0:
                tt = iv
            else:
                tt = [0]*64
                for j in range(0, len(C)):
                  #  print("{}:  {}".format(n, str(tt)))
                  #  print("{}:  {}".format(n, str(C[j])))
                    tt = self._XorBitList(tt,C[j])
     #       print("{}:  {}".format(n, str(tt)))
            mess = self._XorBitList(tt, P)
            C.append(self.gost_coder.bit_encode(mess, key)[0])
    #    print(C[1:])
        return list(it.chain.from_iterable(C)),None


    def bit_decode(self, code, iv , key):
     #   iv = [0]*64
        length_mess = len(code)
      #  print(code)
      #  print(key)
      #  print(iv)
        C = [code[i*self._block_size: (i + 1) * self._block_size] for i in range(0, length_mess // self._block_size + 1)]
       # print(C)
        M = []
        for n in range(0, length_mess, self._block_size):
            P = code[n: n + self._block_size]
            D = self.gost_coder.bit_decode(P, key)[0]
            if n == 0:
                F = iv
            else:
                F = [0]*64
                for j in range(0,len(M)):
                 #   print("{}:  {}".format(n, str(F,)))
                 #   print("{}:  {}".format(n, str(C[j])))
                    F = self._XorBitList(F,C[j])
           # print("{}:  {}".format(n, str(F)))
            mess = self._XorBitList(F, D)
            M.append(mess)
        return list(it.chain.from_iterable(M)),None



