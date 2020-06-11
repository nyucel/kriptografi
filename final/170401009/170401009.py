#!/usr/bin/env python
# -*- coding: utf-8 -*-
#170401009 ATAKAN TÜRKAY

# x = txt.zfill(10) # 10 karakter uzunluğunda 0 döşemek için
# bin(10) binary halini görmek için
# '{0:b}'.format(10)   binary halini görmek için


# '{0:b}'.format(random.randint(2**31,2**32-1))  #32 bitlik rastgele bir sayı oluşturuyor.
# '{:b}'.format(int(hashlib.md5("ata".encode()).hexdigest(),16)).zfill(128) hex->int->binary

import hashlib
import random
import binascii
import time


def final(dosya): #todo hash fonksiyonu değiştirilecek
    # return '{:b}'.format(int(hashlib.md5(dosya).hexdigest(), 16)).zfill(128)
    return int(hashlib.md5(dosya).hexdigest(), 16)

class blockchain: #todo burayı tamamla
    def __init__(self,baslangic=1,bitis=100):
        self.baslangic = baslangic
        self.bitis = bitis
    def zincirle(self):
        print("Zincirleme İşlemi Başladı")
        for i in range(self.baslangic,self.bitis+1):
            temp = blok(i)
            temp.calistir()
            print("{} OK!".format(i))

    def kontrol_et(self): #todo zincirde bozulma olup olmadığını kontrol ediyor.
        pass


class blok:
    def __init__(self, blok_numarası):
        self.blok_numarası = str(blok_numarası).zfill(3)
        self.uzanti = "txt"
        self.rastgele = random.randint(2 ** 31, 2 ** 32 - 1)  # 32 bitlik rastgele bir sayı oluşturuyor.
        self.oncekibloknumara = str(blok_numarası - 1).zfill(3)
        self.oncekiblokhash = 0
        self.blokhash = 0

    def calistir(self):
        if self.blok_numarası == '001':
            return
        elif int(self.blok_numarası) > 1 and int(self.blok_numarası) <= 100:
            self.hash_onceki()
            self.blok_kaydet()
            self.hash_blok()
            self.hashsum_kaydet()
            return
        else:
            print("Blok numarasında hata oluştu")

    def hash_onceki(self):
        f = open("{}.{}".format(self.oncekibloknumara, self.uzanti), "rb")
        a = f.read()
        f.close()
        self.oncekiblokhash=final(a)

    def hash_blok(self):
        f = open("{}.{}".format(self.blok_numarası, self.uzanti), "rb")
        a = f.read()
        f.close()
        self.blokhash = final(a)

    def blok_kaydet(self):
        f = open("{}.{}".format(self.blok_numarası, self.uzanti), "w")
        toplam = self.oncekiblokhash + self.rastgele
        f.write('{:b}'.format(toplam).zfill(128))
        f.close()

    def hashsum_kaydet(self):
        f = open("HASHSUM", "a")
        if int(self.blok_numarası) == 2:
            f.write("BLOK | RASTGELE SAYI | BLOĞUN KENDİ HASHI\n")
        f.write("{} | {} | {} \n".format(self.blok_numarası, '{:b}'.format(self.rastgele).zfill(32), '{:b}'.format(self.blokhash).zfill(128))) #todo hash fonksiyonunu değiştirince zfilleri değiştir.
        f.close()


if __name__ == "__main__":
     bchain = blockchain()
     bchain.zincirle()