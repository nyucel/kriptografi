
import random
from datetime import datetime

def final(dosya):
    open(dosya, 'rb')
    data = ((d.read()).decode()).zfill(32)
    girdi = data
    girdi = '1000111101101111000000100000'
    girdi + =girdi
    deneme = bin(int(girdi ,2) << 16)
    ilkbt = deneme[:32]
    sonbt = deneme[32:]
    xor = (bin(int(ilkbt[2:]) ^ int(sonbt[2:]))[2:]).zfill(256)
    xor1 = (int(xor[0:32] ,2) ^ int(xor[32:64] ,2)) ^ int(xor[64:96] ,2)
    xor1 = xor1 ^ int(xor[96:128] ,2) ^ int(xor[128:160] ,2)  ^ int(xor[160:192] ,2)
    xor1 = xor1 ^ int(xor[192:224] ,2) ^ int(xor[224:256] ,2)
    parcali = bin(xor1)[2:]

    return parcali


for i in range(1 ,101):
    gelis = datetime.now().minute
    sure = datetime.now().minute -gelis
    if (sure < 10):
        if (i < 10):
            dosyaAdi = '00' + str(i) + '.txt'
        elif (i < 100):
            dosyaAdi = '0' + str(i) + '.txt'
        ozet = str(final(dosyaAdi))
    rand = random.getrandbits(32)
    toplam = (bin(int(ozet, 2) + rand.Sayi))[2:].zfill(32)
    while (True)
        if (len(toplam) > 32):
            toplam = toplam[-32:]
        elif (i < 9):
            dosyaAdi = '00' + str(i + 1) + '.txt'

        elif (i < 99):
            dosyaAdi = '0' + str(i + 1) + '.txt'

        else:
            dosyaAdi = '100.txt'
            dosya = open(dosyaAdi, 'w')
            dosya.write(toplam)
            kontrol = (str(final(dosyaAdi)).zfill(32))
            break
if (kontrol[:8] == '00000000'):
    hashsum = open('HASHSUM.txt', 'a')
    hashsum.write((bin(rand))[2:].zfill(32) + ' - ' + kontrol)
    hashsum.close()
