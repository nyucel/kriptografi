
#Sevda Avcılar - 170401054

def decimaltobin(a):
    return "{:7b}".format(a)

def xor(a,b):
    ret=""
    i=0
    while i<len(b):
        if a[i]==b[i]:
            ret=ret+"0"
        else:
            ret=ret+"1"
        i=i+1
    return ret


def ozet(sifre):
    i = 0
    sayi2 = []
    liste = []
    while (i <= 5):
        a = ord(sifre[i])
        bin = decimaltobin(a)
        if (i == 0):
            sayi2.append(bin)
        elif (i == 1):
            sonuc = xor(sayi2[0], bin)
            sayi2.append(sonuc)
        else:
            j = 0
            while (j < len(sayi2)):
                sonuc = xor(sayi2[j], bin)
                sayi2[j] = sonuc
                j = j + 1
            sonuc = xor(sayi2[i - 1], sayi2[i - 2])
            sayi2.append(sonuc)
        i = i + 1
    sayi2=''.join(sayi2)
    return sayi2[0:32]


def dogrulayici(dosya):
    f=open(dosya,"r")
    liste=f.read().split("\n")
    f.close()
    f=open("golge.txt","r")
    golge=f.read().split("\n")
    f.close()
    i=0
    bulunan=[]
    while i<len(liste):
        if(len(liste[i])==6):
            ozetdeger=ozet(liste[i])
            j=0
            while j<len(golge):
                if(golge[j]==ozetdeger):
                    bilgi="Golgedeki " + golge[j] + " değerinin karşılığı: " + liste[i]
                    bulunan.append(bilgi)
                    break
                j=j+1
        i=i+1
    if(len(bulunan)==0):
        print("Belgedeki hiçbir özet uyuşmadı.")
    else:
        i=0
        while i<len(bulunan):
            print(bulunan[i])
            i=i+1

while True:
    print("*************************")
    print("Özet değeri almak için 1")
    print("Doğrulamak için 2")
    komut=input(str("İşleminizi giriniz:"))

    if(komut=="1"):
        sifre=input(str("6 karakterli girdiyi giriniz: "))
        if(len(sifre)!=6):
            print("Girdinin uzunluğu 6 değildir. Yeniden deneyiniz.")
            continue
        sonuc=ozet(sifre)
        f = open("golge.txt", "a")
        yazi = sonuc + "\n"
        f.writelines(yazi)
        f.close()
        break
    elif(komut=="2"):
        girdi=input(str("Dosya adını yazınız: "))
        dogrula=dogrulayici(girdi)
        break
    else:
        print("Yanlış bir komut girdiniz. Yeniden deneyiniz.")
