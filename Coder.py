import matplotlib.pyplot as plt
import numpy as np



'''
Функция для данного декоратора должна принимать массив с ключом и сообщением в двоичном виде
 Должна возвращать массив с зашифрованным сообщением в двоичном виде и массив с состоянием сообщения для раунда
'''
def form_input(func):
    def wrapper(self, *args, **kwargs):
        arg = []
        for a in args:
            arg.append(self.make_format(a))
      #  while len(bit_mess)%64 != 0:
      #      bit_mess = [0] + bit_mess
        code,hist1 = func(self, *tuple(arg,), **kwargs)
       # print("{}: {}".format("s",str(code)))
        if self.change_bit_mode:
            mode = "encoding" if "encoding" in str(func) else "decoding"
            N = min(len(arg[self.d[self.change_bit_mode]]),self.n_block*self._block_size)
            graph_info = [[] for i in range(self.n_block)]
            for position in range(0,N):
                arg = self.change_info(arg, self.change_bit_mode, position)
                changed_code, hist2 =  func(self, *tuple(arg,), **kwargs)
                #print("{}: {}".format(position, str(changed_code)))
                for block in range(0,self.n_block):
                    graph_info[block].append(sum(map(lambda x: abs(x[0] - x[1]), list(zip(code[block*self._block_size: (block+1)*self._block_size], changed_code[block*self._block_size: (block+1)*self._block_size])))))

            for block in range(0, self.n_block):
                self.make_plot(range(len(graph_info[block])), graph_info[block], "{}_block{}_{}".format(self.change_bit_mode, str(block) , mode))

        res = ""
        for i in range(0, len(code), 16):
            tmp = ''.join(str(j) for j in code[i: i + 16])
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
        self.d = {  "messege" : 0,
               "iv"      : 1,
               "key"     : 2
        }

    def make_format(self, value, n_bit=16):
        _format = '0' + str(n_bit) + 'b'
        value.encode('utf-8')
        return [int(j) for j in ''.join(format(ord(i), _format) for i in value)]

    def __change_bit(self, text, ind):
        if text[ind] == 1:
            text[ind] = 0

        else:
            text[ind] = 1
        return text

    def change_info(self, args, key, change_bit_index):
        args[self.d[key]] = self.__change_bit(args[self.d[key]], change_bit_index)
        return args

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

    def make_plot(self, X, Y, name="plot"):
        fig = plt.figure()
        plt.plot(X, Y)
        plt.xlabel("position")  # Метка по оси x в формате TeX
        plt.ylabel("bit")  # Метка по оси y в формате TeX
        plt.savefig("img/plot_{}.png".format(name))
        plt.close(fig)


    @form_input
    def encoding(self,*args, **kwargs):
        return self.bit_encode(*args, **kwargs)

    @form_input
    def decoding(self, *args, **kwargs):
        return self.bit_decode(*args, **kwargs)


    def bit_encode(self, *args, **kwargs):
        pass


    def bit_decode(self, *args, **kwargs):
        pass



