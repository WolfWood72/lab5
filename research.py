from Gost_28147_89 import Gost_28147_89
from BC_coder import BC_coder
from Devis_Price import Devis_Price
mes = "acvbbgfdety"
key1 = "12345674564645646545489746513211"
key2 = "12345674564645646545489746513211"[::-1]
iv = "0000"
coder = Devis_Price(change_bit_mode="messege")

#code = coder.encoding(mes,  iv, key1, key2)
#print(code)

code = "屏繰㴡ᒤ㥒區㛍䵿ᕴ趣"
print(coder.decoding(code, iv,key1, key2))
