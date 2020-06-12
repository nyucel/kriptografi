#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import getrandbits
import time

# 170401028 - Emir Ali Kıvrak

def rightRotate(n, d):
    return (n >> d) | (n << (len(str(n)) - d)) & 0xFFFFFFFF

def final(file_name):
    operation_numbers = [0xFEE1DEAD, 0xDEAD10CC, 0xBADDCAFE, 0x8BADF00D]

    with open(file_name, "rb") as file:
        f = file.read()  # dosya okundu ve binary hale getirildi

    doldurma_uzunlugu = 0 if len(f) % 4 == 0 else len(
        f) % 4  # dosyayı 4 e parçalayacağım bunun için ne kadar dolgu yapacağımı hesapladım

    if (doldurma_uzunlugu != 0):
        f = f.zfill(32) if len(f) < 32 else f.zfill(len(f) + 4 - doldurma_uzunlugu)

    splitted_arr = []
    f_len = len(f)  # dosyamızın uzunlugu
    f_len_quarter = int(len(f) / 4)  # dosyamızın uzunluğunun çeyreği

    """binary inputumuzu 4 parçaya parçalıyorum"""
    for chunk in range(0, f_len, f_len_quarter):
        splitted_arr.append(f[
                            chunk: chunk + f_len_quarter])  # b'00000000000000000000000170401028' --> [b'00000000', b'00000000', b'00000001', b'70401028']


    """bir takım işlemlere tabi tutalım"""
    for i in range(len(splitted_arr)):
        splitted_arr[i] = int(splitted_arr[i]) | operation_numbers[i % 4- len(operation_numbers)]

    for i in range(len(splitted_arr)):
        splitted_arr[i] = rightRotate(splitted_arr[i],2)

    for i in range(len(splitted_arr)):
        splitted_arr[i] = int(splitted_arr[i]) ^ operation_numbers[i % len(operation_numbers)]

    """"işlemlerin ardından diziyi birleştirelim"""
    number = ""
    for i in range(len(splitted_arr)):
        number += str(splitted_arr[i])

    number = int(number) % 2 ** 32


    return format(number, "b").zfill(32)


class BlockChain:

    def __init__(self, first_file="001.txt", upper_bound=100):
        self.first_file = first_file
        self.upper_bound = upper_bound

        self.lower_bound = 1

    def start_chain(self):
        start_time = time.time()
        while self.lower_bound < self.upper_bound and start_time< time.time()+600: # sınır aşılmamış ve zaman dolmamışsa
            f_name = "00" + str(self.lower_bound) + ".txt" if self.lower_bound < 10 else "0" + str(
                self.lower_bound) + ".txt"

            """İlk hash değeri hesaplandı bu değer sonraki hesaplanan hash değerinin hesaplanmasında kullanılacak"""
            previous_hash = final(f_name)
            self.lower_bound = self.lower_bound + 1


            """final fonksiyonum içine dosya aldığı için eski hash değeri ve random bitlerin toplamını bir dosyaya 
            yazdım """

            """Bir sonraki 'uygun' hashın hesaplanıp yazımı"""
            f_name = "00" + str(self.lower_bound) + ".txt" if self.lower_bound < 10 else "0" + str(
                self.lower_bound) + ".txt"  # ikinci hashin yazılacağı dosyanın adı

            while True:  # 0000000 denk gelene kadar dene, gelirse yaz çık , gelmezse devam
                rand_bits = getrandbits(32)
                with open("temp.txt", "w+") as temp_f:
                    temp_f.write(str(previous_hash + format(rand_bits, "b")))
                current_hash = final("temp.txt")
                if (current_hash[:8] == '00000000'):
                    print("Kurallara uygun oluşturulan bir blok:" + f_name)
                    print("Kurallara uygun oluşturulan bloğun hash değeri" + current_hash)
                    with open(f_name, "w") as f:
                        f.write(current_hash)
                    with open("HASHSUM","a") as hashsum:
                        hashsum.write("Rastgele Sayı : " + str(rand_bits) + "Oluşturulan Hash değeri : " + current_hash.zfill(32) + "\n" )
                    break
                else:
                    continue


b = BlockChain()
b.start_chain()
