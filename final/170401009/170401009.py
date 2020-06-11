#!/usr/bin/env python
# -*- coding: utf-8 -*-
#170401009 ATAKAN TÜRKAY

# x = txt.zfill(10) # 10 karakter uzunluğunda 0 döşemek için
# bin(10) binary halini görmek için
# '{0:b}'.format(10)   binary halini görmek için


# '{0:b}'.format(random.randint(2**31,2**32-1))  #32 bitlik rastgele bir sayı oluşturuyor.
# '{:b}'.format(int(hashlib.md5("ata".encode()).hexdigest(),16)).zfill(128) hex->int->binary
#   '{0:x}'.format(122545).zfill(32)
import hashlib
import random
import binascii
import time

def string_to_int(data):
    return int(binascii.hexlify(data.encode('utf-8')).decode("ascii"),16) #byte değerini int değerine çeviriyor..

def int_to_binary(data):
    return '{0:b}'.format(data)
def binary_to_int(data):
    return int(data,2)
def bytes_to_binary(data):
    return int_to_binary(string_to_int(data.decode()))


def left_rotate(x, amount):
    x &= 0xFFFFFFFF
    return ((x<<amount) | (x>>(32-amount))) & 0xFFFFFFFF

def final(dosya): #todo hash fonksiyonu değiştirilecek
    # return '{:b}'.format(int(hashlib.md5(dosya).hexdigest(), 16)).zfill(128)
    magic_numbers = [0xFEE1DEAD, 0xBADDCAFE, 0xDEAD10CC, 0x8BADF00D]
    if type(dosya)!= bytes:
        dosya = dosya.encode()
    uzunluk = len(bytes_to_binary(dosya))
    ekstra = uzunluk % 4    #4 parçaya bölünüyor mu
    dosya = bytes_to_binary(dosya).zfill(ekstra)     #dosyayı 4 e bölünür hale getiriyorum
    parcalar=[[],[],[],[]]
    bit_toplamı=0
    print(uzunluk)
    print(ekstra)
    print(dosya)
    print(parcalar)
    for i in dosya:
        bit_toplamı+=int(i)
        if len(parcalar[0]) <= uzunluk/4:
            print(len(parcalar[0]))
            parcalar[0].append(str(i))
        elif len(parcalar[2]) <= uzunluk/4:
            parcalar[2].append(str(i))
        elif len(parcalar[3]) <= uzunluk/4:
            parcalar[3].append(str(i))
        else:
            parcalar[1].append(str(i))
    print(parcalar)
    parca1="".join(parcalar[0])
    parca2="".join(parcalar[1])
    parca3="".join(parcalar[2])
    parca4="".join(parcalar[3])
    print(parca1,parca2,parca3,parca4)
    parca1 = binary_to_int(parca1) ^ magic_numbers[0]
    print(parca1)
    parca1 >>=bit_toplamı % 7
    print(parca1)
    parca2 = binary_to_int(parca2) ^ magic_numbers[1]
    dosya = parca1+parca2
    dosya << 42
    print(dosya)
    parca3 = binary_to_int(parca3) | magic_numbers[2]
    dosya = dosya+~parca3
    print(dosya)
    parca4 = binary_to_int(parca4) & magic_numbers[3]
    parca4 <<=bit_toplamı % 21
    print(parca4)
    dosya = dosya ^ parca4
    print(dosya)
    dosya = dosya % 2**32
    print(dosya)
    # dosya = int_to_binary(dosya)
    # print(dosya)
    # dosya=dosya.zfill(32) # 32 bite tamamlıyoruz
    return dosya

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
        f.write('{:b}'.format(toplam).zfill(32))
        f.close()

    def hashsum_kaydet(self):
        f = open("HASHSUM", "a")
        if int(self.blok_numarası) == 2:
            f.write("BLOK | RASTGELE SAYI | BLOĞUN KENDİ HASHI\n")
        f.write("{} | {} | {} \n".format(self.blok_numarası, '{:b}'.format(self.rastgele).zfill(32), '{:b}'.format(self.blokhash).zfill(32))) #todo hash fonksiyonunu değiştirince zfilleri değiştir.
        f.close()


if __name__ == "__main__":
     bchain = blockchain()
     bchain.zincirle()
     # a = open("001.txt", "rb")
     # a = a.read()
     # final(a)
