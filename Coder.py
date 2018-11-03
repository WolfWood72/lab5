import matplotlib.pyplot as plt
import numpy as np



'''
Функция для данного декоратора должна принимать массива с ключом и сообщением в двоичном виде
 Должна возвращать массив с зашифрованным сообщением в двоичном виде и массив с состоянием сообщения для раунда
'''
def form_input(func):
    def wrapper(self, messege, key):

        bit_mess = self.make_format(messege)
        bit_key = self.make_format(key)
        print(len(bit_mess))
      #  while len(bit_mess)%64 != 0:
      #      bit_mess = [0] + bit_mess
        code,hist1 = func(self,bit_mess,bit_key)

        if self.change_bit_mode and hist1:
            changed_mess, changed_key = self.change_info(bit_mess, key)
            changed_code, hist2 = func(changed_mess, changed_key)
            self.graph_info = []
            for i in range(self.__num_rounds):
                self.graph_info.append(sum(map(lambda x: abs(x[0] - x[1]), list(zip(hist1[i], hist2[i])))))
            self.make_plot(range(len(self.graph_info)), self.graph_info)

        res = ""
        for i in range(0, len(code), 15):
            tmp = ''.join(str(j) for j in code[i: i + 15])
            res += chr(int(tmp, 2))

        return res
    return wrapper

def benchmark(func):
    import time
    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        print("Время шифрования: ", time.clock() - t)
        return res
    return wrapper



class Coder:
    def __init__(self):
        pass

    def make_format(self, value, n_bit=15):
        _format = '0' + str(n_bit) + 'b'
        value.encode('utf-8')
        return [int(j) for j in ''.join(format(ord(i), _format) for i in value)]

    def __change_bit(self, text, ind):
        if text[ind] == 1:
            text[ind] = 0

        else:
            text[ind] = 1
        return text

    def change_info(self, text, key):
        if self.change_bit_mode == 'messege':
            return self.__change_bit(text, self.change_bit_index), key
        elif self.change_bit_mode == 'key':
            return text, self.__change_bit(key, self.change_bit_index)
        else:
            return text, key

    def _CycleArrayShift(self, arr, N):
        return list(np.roll(arr,N))

    def _BitListToInt(self, BitList):
        out = 0
        for bit in BitList:
            out = (out << 1) | bit
        return out

    def _IntToBitList(self, n, need_length=None):
        arr = [int(digit) for digit in bin(n)[2:]]
        if need_length:
            while len(arr) != need_length:
                arr = [0] + arr
        return arr

    def _XorBitList(self, a, b):
        return [i ^ j for i, j in zip(a, b)]

    def _OrBitList(self, a, b):
        return [i | j for i, j in zip(a, b)]

    def make_plot(self, X, Y):
        plt.plot(X, Y)
        plt.xlabel("round")  # Метка по оси x в формате TeX
        plt.ylabel("bit")  # Метка по оси y в формате TeX
        plt.savefig("plot_{}.png".format(self.change_bit_mode))


    @form_input
    def encoding(self, message, key):
        return self.bit_encode(message, key)

    @form_input
    def decoding(self, code, key):
        return self.bit_decode(code,key)


    def bit_encode(self, message, key):
        pass


    def bit_decode(self, code, key):
        pass



