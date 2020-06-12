import random
from time import time

#160401019

def final(dosya):
    f=open(dosya,"r")
    k=f.read()
    sayi=DecimaltoBinary(int(k))
    length = DecimaltoBinary(len(sayi))

    while (len(sayi)%32 != 0):
        if( (len(sayi)+4) % 32 == 0):
            sayi = sayi + length[10:14]
            break
        sayi = sayi +"0"
    parca = int(len(sayi) / 4)

    while(parca >= 8):
        A = sayi[0:parca]
        B = sayi[parca:parca*2]
        C = sayi[parca*2:parca*3]
        D = sayi[parca*3:parca*4]

        A = xor(A,B)
        B = xor(B,C)
        C = xor(C,D)
        D = xor(D,A)

        if(parca != 8):

            sayi = or_islemi(A,C) + and_islemi(B,D)
            while (len(sayi) % 32 != 0):            #ikiye boldukten sonra 32nin kati olmaktan cikarsa
                if ((len(sayi) + 4) % 32 == 0):     #32nin katı olacak sekilde yeniden uzatilir
                    sayi = sayi + length[10:14]
                    break
                sayi = sayi + "0"

        else:
            for i in range(32):
                if (i < 8):
                    temp = xor(B, C)
                    temp2 = and_islemi(temp, D)
                    B = xor(B, temp2)
                elif (i > 8 and i < 16):
                    temp = xor(B, C)
                    temp2 = or_islemi(temp, D)
                    C = and_islemi(C, temp2)

                elif (i > 16 and i < 24):
                    temp = xor(A, C)
                    temp2 = and_islemi(temp, A)
                    D = xor(D, temp2)

                elif (i > 24 and i < 32):
                    temp = xor(D, C)
                    temp2 = or_islemi(temp, B)
                    A = and_islemi(A, temp2)
                sayi = D + B + C + A

        parca = int(parca / 2)

    return(sayi)


def xor(x,y):
    sonuc=""
    for i in range(0,len(x)):
        if x[i]==y[i]:
            sonuc+="0"
        else:
            sonuc+="1"
    return sonuc

def and_islemi(x,y):
    sonuc=""
    for i in range(0,len(x)):
        if x[i]==y[i] and x[i]=="1":
            sonuc +="1"
        else:
            sonuc += "0"
    return sonuc

def or_islemi(x,y):
    sonuc=""
    for i in range(0,len(x)):
        if x[i]==y[i] and x[i]=="0":
            sonuc+="0"
        else:
            sonuc+="1"
    return sonuc


def DecimaltoBinary(num):
    return "{0:016b}".format(num)


hashsum = open("HASHSUM", "w")
sure = time() + 60
for s in range(2,101):
    if sure < time():
        print("10 dk icinde tamamlanamadi")
        break
    ozet = final("001.txt")
    sira = "{0:03}".format(s)
    dosya = str(sira)+"txt"
    while True:
        f = open(dosya,"w")
        r=DecimaltoBinary(random.getrandbits(32))
        x = ozet+r
        f.write(x)
        f.close()
        ozet2=final(dosya)
        #print("Dosya:" + dosya + "OZET2:" + ozet2)
        if("1" in ozet2[:8]):
            continue
        else:
            icerik = ("Dosya adi:" + dosya + " Random bitler:" + (32 - len(r)) * "0" + str(r) + " Ozet:" + ozet2 + "\n")
            hashsum.writelines(icerik)
            break

