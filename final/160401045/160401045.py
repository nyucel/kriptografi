#Gökçe Kuler
import random
import datetime
import sys

def final(dosya):
    with open(dosya,'rb') as d:
        data = ((d.read()).decode()).zfill(33)
    d.close()
    birincibolum=str(data)[0:16]
    ikincibolum=str(data)[16::]
    cikti=''
    for i in range(16):
        cikti += str(int(birincibolum[i]) ^ int(ikincibolum[i]))
        cikti += str(int(birincibolum[i]) ^ int(ikincibolum[i]))
    return (cikti)

def hashsum(ozetdeger,rastgeledeger):
    with open('HASHSUM','a') as hashsum:
        hashsum.write(str(ozetdeger) +"," + str(rastgeledeger) + "\n")

    hashsum.close()


baslangic=datetime.datetime.now().minute
ozet=final('001.txt')
for i in range(2,101):
    dosyaismi="{0:03}".format(i)
    dosya=str(dosyaismi)+".txt"
    rastgelesayi=random.getrandbits(32)
    decimalozet=int(str(ozet),2)
    toplam=decimalozet + rastgelesayi
    binarytoplam=bin(toplam)
    yeniblok=str(binarytoplam)[2:] #yeni üretilen blok
    if(str(yeniblok)[0:9]  != '00000000') : #eğer üretilen bloğun ilk 8 biti 0 değilse bu koşulu sağlayana kadar 32 bit random sayı üretecek alan
        while(str(yeniblok)[0:9] != '00000000'):
            rastgelesayi=random.getrandbits(32)
            toplam=decimalozet+rastgelesayi
            binarytoplam=bin(toplam)
            yeniblok=str(binarytoplam)[2:]
            bitis=datetime.datetime.now().minute
            if((bitis-baslangic)>10):
                 print("Süre doldu")
                 sys.exit()

    with open(dosya,'w') as f:
        f.write(yeniblok)
    
    f.close()
    yeniozet=final(dosya)

    hashsum(yeniozet,rastgelesayi) #yeni oluşan özet değeri ve bu değer oluşturulurken kullanılan random sayıyı HASHSUM dosyasına yazan kısım

    bitis=datetime.datetime.now().minute
    if((bitis-baslangic)>10):
        print("Süre doldu program sonlandı")
        sys.exit()

