import random, time, sys
from datetime import datetime

def final(dosya):

    file = open(dosya, "r")
    data = file.read()
    file.close()

    dataBit = bin(int(data))[2:].zfill(32)

    key = bin(171717171717)[2:].zfill(32)

    for i in range(5):
        firstBit = dataBit[0:16]
        secondBit = dataBit[16:32]

        islem1 = int(secondBit, 2) * int(key)
        islem2 = int(firstBit, 2) * islem1

        islem = islem1 ^ islem2
        islem = bin(int(islem))[2::].zfill(16)
        dataBit = str(islem) + firstBit

    summary = str(dataBit)[:32]
    return summary

def randomNumberGenerate(n):
    return str(bin(random.getrandbits(n))[2:].zfill(n))

def sonrakiBlok(blok):

    sonraki = str(int(blok[:3]) + 1)
    yeniBlok = ""
    if (len(sonraki) == 1):
        yeniBlok = "00" + sonraki + ".txt"

    elif (len(sonraki) == 2):
        yeniBlok = "0" + sonraki + ".txt"

    elif (len(sonraki) == 3):
        yeniBlok = sonraki + ".txt"

    return yeniBlok

def hashsumEkle(random, summary):

    hashsum = open("HASHSUM.txt", "a")
    hashsum.write(str(random) + "\t" + str(summary) + "\n")
    hashsum.close()

def blokzincir(blok):

    baslangic = datetime.now().minute

    i = 0
    while(i < 99):
        summary = final(blok)

        yeniBlokAd = sonrakiBlok(blok)
        yeniBlok = open(yeniBlokAd, "w")

        randomNumber = randomNumberGenerate(32)
        yeniOzet = str(bin(int(summary, 2) + int(randomNumber, 2))[2:].zfill(32))[0:32]
        yeniOzet = "00000000" + yeniOzet[8:]

        yeniBlok.write(str(int(yeniOzet, 2)))
        yeniBlok.close()

        hashsumEkle(randomNumber, yeniOzet)
        blok = yeniBlokAd
        i = i + 1

        bitis = datetime.now().minute

        if ((bitis - baslangic) >= 10):
            print("Çalışma süresi 10 dakikayı geçtiği için program sonlandırıldı")
            sys.exit(1)



blokzincir("001.txt")