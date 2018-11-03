from Gost_28147_89 import Gost_28147_89
from BC_coder import BC_coder

mes = "Show must go on!!!!!!!!!"
key = "12345674564645646545489746513211"

coder = BC_coder()

code = coder.encoding(mes, key)
print(code)
print(coder.decoding(code, key))
