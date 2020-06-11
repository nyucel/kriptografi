import random, time, sys
from datetime import datetime

def final(dosya): # 32 bitlik ozet degeri donduren ozet fonksiyonu

    dosya = open(dosya, "r")
    icerik = dosya.read()
    dosya.close()

    icerikBit = bin(int(icerik))[2:].zfill(32)

    anahtar = bin(4242424242)[2:].zfill(32)

    for i in range(5):
        birinci = icerikBit[0:16]
        ikinci = icerikBit[16:32]

        islem1 = int(ikinci, 2) * int(anahtar)
        islem2 = int(birinci, 2) * islem1

        islem = islem1 ^ islem2
        islem = bin(int(islem))[2::].zfill(16)
        icerikBit = str(islem) + birinci

    ozet = str(icerikBit)[:32]
    return ozet

def rastgeleSayiOlustur(bit): # Parametre olarak aldigi bit sayisinde rastgele sayi olusturan fonksiyon
    return str(bin(random.getrandbits(bit))[2:].zfill(bit))

def sonrakiBlok(blok):  # Olusturulacak bir sonraki blok adini donduren fonksiyon

    sonraki = str(int(blok[:3]) + 1)
    yeniBlok = ""
    if (len(sonraki) == 1):
        yeniBlok = "00" + sonraki + ".txt"
    elif (len(sonraki) == 2):
        yeniBlok = "0" + sonraki + ".txt"
    elif (len(sonraki) == 3):
        yeniBlok = sonraki + ".txt"
    return yeniBlok

def hashsumEkle(rastgeleSayi, ozet): #v HASHSUM adli dosyaya blok icin olusturulan rastgele sayiyi ve blok ozet degerini ekleyen fonksiyon

    hashsum = open("HASHSUM.txt", "a")
    hashsum.write(str(rastgeleSayi) + "\t" + str(ozet) + "\n")
    hashsum.close()

def blokzincir(blok): # Blokzincir mekanizmasını calistiran fonksiyon

    baslangic = datetime.now().minute

    i = 0
    while(i < 99):
        ozet = final(blok)

        yeniBlokAd = sonrakiBlok(blok)
        yeniBlok = open(yeniBlokAd, "w")

        rastgeleSayi = rastgeleSayiOlustur(32)
        yeniOzet = str(bin(int(ozet, 2) + int(rastgeleSayi, 2))[2:].zfill(32))[0:32]
        yeniOzet = "00000000" + yeniOzet[8:]

        yeniBlok.write(str(int(yeniOzet, 2)))
        yeniBlok.close()

        hashsumEkle(rastgeleSayi, yeniOzet)
        print(yeniBlokAd + " >> blok olustu")
        blok = yeniBlokAd
        i = i + 1

        bitis = datetime.now().minute

        if (bitis > baslangic):
            if ((bitis - baslangic) >= 10):
                print("\n>> 10 dk'lik calisma suresi doldugu icin program sonlandirildi..")
                sys.exit(1)
        elif(bitis < baslangic):
            if ((bitis - baslangic + 60) >= 10):
                print("\n>>10 dk'lik calisma suresi doldugu icin program sonlandirildi..")
                sys.exit(1)


# ******************************************** ÇALIŞTIRMA ********************************************** #

print("\n----------------- BLOKZINCIR MEKANIZMASI -----------------\n")

hashsum = open("HASHSUM.txt", "w")
hashsum.write("Rastgele Sayi\t\t\t\tOzet Degeri\n\n")
hashsum.close()

blokzincir("001.txt")

print("\n** Butun bloklar olusturuldu..")
