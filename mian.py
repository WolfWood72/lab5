
from BC_coder import BC_coder
from Devis_Price import Devis_Price

import argparse
import sys


change_bit_mode = ["messege", "key", "iv"]

parser = argparse.ArgumentParser()
parser.add_argument("-encode", "-encode", action='store_true',
                    help="input file", required=False)
parser.add_argument("-decode","-decode",  action='store_true',
                    help="input file", required=False)


parser.add_argument("-method", type=str, choices=['BC', 'DP'],
                    help="method of encrypt")


parser.add_argument("-input_file", type=str,
                    help="file with input message")
parser.add_argument("-output_file", type=str,
                    help="file with output message")
parser.add_argument("-key_file", type=str,
                    help="file with key for Feistel net")
parser.add_argument("-iv_file", type=str,
                    help="file with iv")

parser.add_argument("-change_bit_mode", type=str,
                    help="change_bit_mode",choices=change_bit_mode,default="messege")



namespace = parser.parse_args(sys.argv[1:])


try:
    change_bit_mode = namespace.change_bit_mode

    coder_dict = {
        "BC": BC_coder,
        "DP": Devis_Price

    }
    coder = coder_dict[namespace.method](change_bit_mode=namespace.change_bit_mode)


    if not namespace.decode and not namespace.encode:
        raise ValueError("must have decode or encode param")
    if namespace.decode and namespace.encode:
        raise ValueError("must have only one of encode and deocde param")

    with open(namespace.input_file, "r", encoding="utf-8") as f:
        messege = f.read()

    with open(namespace.key_file, "r", encoding="utf-8") as f:
        key = f.read()
        if "\n" in key and namespace.method == "DP":
            key = tuple(key.split("\n"))
        else:
            key = (key.split("\n")[0] , )


    with open(namespace.iv_file, "r", encoding="utf-8") as f:
        iv = f.read()



    if namespace.encode:
        encoded_mes = coder.encoding(messege,iv, *key)
        print("Закодированное сообщение: '{}'".format(encoded_mes))

        with open(namespace.output_file, "w", encoding="utf-8") as f:
            f.write(encoded_mes)
      #  coder.make_plot(list(range(len(coder.graph_info))), coder.graph_info)
    elif namespace.decode:
        decoded_mes = coder.decoding(messege, iv, *key)
        print("Расшифрованное сообщение: '{}'".format(decoded_mes))


        with open(namespace.output_file, "w", encoding="utf-8") as f:
            f.write(decoded_mes)


except Exception as e:
    print(str(e))
    exit("err")













