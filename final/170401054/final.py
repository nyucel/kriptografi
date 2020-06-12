#Sevda Avcılar - 170401054

import uuid
import time
import random

def DecimaltoBinary(num):
    return "{0:0b}".format(num)

def DecimaltoBinary16(num):
    return "{0:016b}".format(num)


def xor(a,b):
    sonuc=""
    for i in range(0,len(a)):
        if a[i]==b[i]:
            sonuc=sonuc+"0"
        else:
            sonuc=sonuc+"1"
    return sonuc


def orop(a,b):
    sonuc=""
    for i in range(0,len(a)):
        if a[i]==b[i] and a[i]=="0":
            sonuc=sonuc+"0"
        else:
            sonuc=sonuc+"1"
    return sonuc


def andop(a,b):
    sonuc=""
    for i in range(0,len(a)):
        if a[i]==b[i] and a[i]=="1":
            sonuc=sonuc+"1"
        else:
            sonuc=sonuc+"0"
    return sonuc


def final(dosya):
    f=open(dosya,"r")
    k=f.read()
    sayi=DecimaltoBinary(int(k))
    sayi = sayi + "1"
    uzunluk=len(sayi)
    while True:
        if(len(str(sayi))+16)%128==0:
            length=DecimaltoBinary16(uzunluk)
            sayi=sayi+length
            print(len(sayi))
            break
        sayi=sayi+"0"
    i = 0
    print(sayi)
    sonhal1=sayi
    k=0
    cozum3=""
    while k<len(str(sayi)):
        while i < 32:
            A = sonhal1[k:k+32]
            B = sonhal1[k+32:k+64]
            C = sonhal1[k+64:k+96]
            D = sonhal1[k+96:k+128]
            if (i < 8):
                D= D[::-1]
                sonuc1 = orop(B,D)
                sonuc2 = xor(sonuc1, A)
                sonhal1 = str(D) + str(sonuc2) + str(sonuc1) + str(A)
                print(sonhal1)
            elif (i >= 8 and i < 16):
                C = C[::-1]
                sonuc1 = andop(C,D)
                sonuc2 = xor(A, sonuc1)
                sonhal1 = str(C)+ str(sonuc1) + str(sonuc2) + str(D)
                print(sonhal1)
            elif (i >= 16 and i < 24):
                B=B[::-1]
                sonuc1 = orop(B, C)
                sonuc2 = xor(A, sonuc1)
                sonhal1 = str(B) + str(sonuc2) + str(C) + str(sonuc1)
                print(sonhal1)
            elif (i >= 24):
                A=A[::-1]
                sonuc1 = andop(C, D)
                sonuc2 = xor(A, sonuc1)
                sonhal1 = str(A)+ str(sonuc2) + str(sonuc1) + str(D)
                print(sonhal1)
            i = i + 1
        print(sonhal1)
        k=k+128
        cozum3=cozum3+sonhal1
        print(cozum3)
    uzunluk=len(sonhal1)
    while uzunluk>32:
        cozum1=sonhal1[0:int(uzunluk/2)]
        cozum2=sonhal1[int(uzunluk/2):int(uzunluk)]
        cozum3=xor(cozum1,cozum2)
        uzunluk=uzunluk/2
    return cozum3


def isim(i):
    if i<10:
        name="00"+str(i)+".txt"
    elif i<100:
        name="0"+str(i)+".txt"
    elif i==100:
        name=str(i)+".txt"
    return name

def blockchain():
    hashsum=open("HASHSUM","w")
    sure = time.time() + 600
    i=2
    while i<=100:
        if sure < time.time():
            break
        ilk = final("001.txt")
        dosya = isim(i)
        while True:
            file = open(dosya, "w")
            sayi = DecimaltoBinary(random.getrandbits(32))
            x = ilk + sayi
            file.write(x)
            file.close()
            ozetler = final(dosya)
            if ("1" in ozetler[:8]):
                continue
            else:
                yazi = ((32 - len(sayi)) * "0" + str(r) + " / " + ozetler + "\n")
                hashsum.writelines(yazi)
                break
        i=i+1


blockchain()