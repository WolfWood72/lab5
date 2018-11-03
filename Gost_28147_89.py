
import numpy as np
import matplotlib.pyplot as plt
import Coder



class Gost_28147_89(Coder.Coder):
    def __init__(self, type_key="gost_key", num_rounds=32, block_size=64, change_bit_mode=None, change_bit_index=None):
        super().__init__()
        self.__block_size = block_size
        self.__type_key = type_key
        self.__num_rounds = num_rounds

        self.__key_dict = {"gost_key": self.__gost_key
                           }
        self.get_key = self.__key_dict[type_key]
        self.change_bit_mode = change_bit_mode
        self.change_bit_index = change_bit_index
        self.graph_info = None
        self.KEY_LENGTH = 256
        self.SUBKEY_LENGTH = 32
        self.SUBKEY_ORDER = [1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,8,7,6,5,4,3,2,1]
        self.S = [
            [4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3],
            [14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9],
            [5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11],
            [7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3],
            [6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2],
            [4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14],
            [13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12],
            [1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12]

        ]




    def __gost_key(self, key, i , mode= 'encode'):
        return key[(self.SUBKEY_ORDER[i]-1)*32: self.SUBKEY_ORDER[i]*32]


    def __make_round(self, left, right, key):
        temp = self._XorBitList(right, key)
        tt = []
        for i in range(8):
            s_index = self._BitListToInt(temp[i * 4: (i + 1) * 4])
            tt.append(self._IntToBitList(self.S[i][s_index], 4))
        tt = list(np.array(tt).ravel())

        tt = self._CycleArrayShift(tt, 11)

        swap = right.copy()
        right = self._XorBitList(tt, left)
        left = swap.copy()
        return left, right


    def bit_encode(self, b_messege, key):
        history_round = []
        code = b_messege
        length_mess = len(b_messege)
        for i in range(self.__num_rounds):
            temp = []
            for n in range(0, length_mess, self.__block_size):
                block = code[n: n + self.__block_size]
                N = len(block) // 2
                Right = block[N:]
                Left = block[:N]
                # print("round {}".format(i))
                Right, Left = self.__make_round(Left.copy(), Right.copy(), self.get_key(key, i))
                if not i != 31:
                    temp += Left + Right
                else:
                    temp += Right + Left
            history_round.append(temp)
            code = temp
        return code, history_round


    def bit_decode(self, bit_code, key ):
        length_code = len(bit_code)
        mess = []

        for n in range(0, length_code, self.__block_size):
            block = bit_code[n: n + self.__block_size]
            N = len(block) // 2

            Right = block[:N]
            Left = block[N:]

            for i in range(self.__num_rounds - 1, -1, -1):
                Right, Left = self.__make_round(Right, Left, self.get_key(key, i))
            mess += Left + Right
        return mess,None
