# Medya HAN - 170401040
# PAILLIER SIFRELEMESİ

import random
import math

def ebob(a, b):
  while b > 0:
    a, b = b, a % b
  return a

def ekok(a, b):
  return a * b // ebob(a, b)

def L(u, n):
  return ((u - 1) // n)

def asal_mi(u, T): # Asal olup olmama kontrolu yapan fonksiyon
    v = 0
    w = u - 1
    while(w % 2 == 0):
        v += 1
        w = w // 2
    for _ in range(1, T + 1):
        sonraki = False
        a = random.randint(2, u - 1)
        b = pow(a, w, u)
        if(b == 1 or b == u - 1):
            sonraki = True
            continue
        for _ in range(1, v):
            b = (b ** 2) % u
            if(b == u - 1):
                sonraki = True
                break
            if(b == 1):
                return False
        if(not sonraki):
            return False
    return True

def asal_olustur(bit): # Verilen bite gore asal sayi olusturan fonksiyon
    taban = (1 << bit) + 1
    tavan = (1 << (bit + 1)) - 1

    while(True):
        asal = random.randint(taban, tavan)
        if(asal % 2 == 1 and asal_mi(asal, 15)):
            return asal

def tersini_al(a, n): # Bir sayinin tersini almaya yaran fonksiyon
    s, eski_s = 0, 1
    t, eski_t = 1, 0
    r, eski_r = n, a

    while r != 0:
        q = eski_r // r
        eski_r, r = r, eski_r - q * r
        eski_s, s = s, eski_s - q * s
        eski_t, t = t, eski_t - q * t

    return (eski_s % n)

def g_olustur(n): # g anahtarini rastgele olusturan fonksiyon
    g = random.randint(1, n - 1)
    while(ebob(g, n) != 1):
        g = random.randint(1, n - 1)
    return g

def textToDecimal(text): # Bir text mesajini decimal hale donusturen fonksiyon
    liste = []
    yeni = []
    for i in text:
        liste.append(format(ord(i)))

    for j in liste:
        if (len(j) == 2):
            yeni.append("0")
            yeni.append(j)
        else:
            yeni.append(j)
    return ''.join(yeni)

def decimalToText(decimal): # Decimal haldeki mesaji tekrardan text haline getiren fonksiyon
    liste = []
    yeni = []
    i = 0
    while(i != len(decimal)):
        liste.append(''.join(decimal[i: (i + 3)]))
        i = i + 3
    for j in liste:
        yeni.append(chr(int(j)))
    return ''.join(yeni)

def keygen(bit): # publickey ve privatekey olmak uzere n,g,Lambda ve Mu anahtarlarini olusturan fonksiyon
    p = asal_olustur(int(bit / 2))
    q = asal_olustur(int(bit / 2))
    while(ebob(p * q, (p - 1) * (q - 1)) != 1):
        p = asal_olustur(int(bit / 2))
        q = asal_olustur(int(bit / 2))
    n = p * q

    Lambda = ekok(p-1, q-1)

    g = g_olustur(n*n) # Rastgele bir g sayisi olusturulur
    while(ebob(L(pow(g, Lambda, n*n), n), n) != 1):
        g = g_olustur(n*n)

    k = L(pow(g, Lambda, n*n), n)
    Mu = tersini_al(k, n) % n

    publickey = open("publickey.txt", "w")
    publickey.write(str(n) + "\n")
    publickey.write(str(g))
    publickey.close()

    privatekey = open("privatekey.txt", "w")
    privatekey.write(str(Lambda) + "\n")
    privatekey.write(str(Mu))
    privatekey.close()

    print("Keygen:\n")
    print("p: ", p)
    print("q: ", q)
    print("n: ", n)
    print("g: ", g)
    print("Lambda: ", Lambda)
    print("Mu: ", Mu)
    print("\n** Anahtarlar olusturuldu..")


def encrypt(plaintexttxt, publickeytxt):
    try:
        publickey = open(publickeytxt, "r")
    except FileNotFoundError:
        print("Sifreleyecek anahtar bulunmadigindan ilk olarak keygen(n) fonksiyonu cagirilmalidir..")

    n = int(publickey.readline())
    g = int(publickey.readline())
    publickey.close()

    plaintext = open(plaintexttxt, "r") # En basta girilen mesaj decimala cevrilir
    mesaj = plaintext.readline()
    m = int(textToDecimal(mesaj))
    plaintext.close()

    if(m < 0 or m >= n):
        raise Exception("Mesaj 0'dan kucuk ve n'den buyuk olamaz..")

    r = asal_olustur(int(math.log2(n))) # Rastgele bir r asal sayisi olusturulur
    while(r > n - 1):
        r = asal_olustur(int(math.log2(n)))

    c = (pow(g, m, n*n) * pow(r, n, n*n)) % (n*n)
    ciphertext = open("ciphertext", "w")
    ciphertext.write(str(c))
    ciphertext.close()

    print("\n================================\nEncrypt:\n")
    print("r: ", r)
    print("ciphertext: ", c)
    print("\n** Sifreleme islemi yapildi..")

def decrypt(ciphertexttxt, privatekeytxt):
    try:
        privatekey = open(privatekeytxt, "r")
    except FileNotFoundError:
        print("Sifreleyecek anahtar bulunmadigindan ilk olarak keygen(n) fonksiyonu cagirilmalidir..")

    try:
        ciphertext = open(ciphertexttxt, "r")
    except FileNotFoundError:
        print("Desifrelenecek ciphertext bulunmadigindan ilk olarak encrypt() fonksiyonu cagirilmalidir..")

    try:
        publickey = open("publickey.txt", "r")
    except FileNotFoundError:
        print("Sifreleyecek anahtar bulunmadigindan ilk olarak keygen(n) fonksiyonu cagirilmalidir..")

    Lambda = int(privatekey.readline())
    Mu = int(privatekey.readline())
    privatekey.close()

    n = int(publickey.readline())
    publickey.close()

    c = int(ciphertext.readline())
    ciphertext.close()

    if(ebob(c, n*n) != 1):
        print("Hatali ciphertext..")

    if(c < 1 or c >= n*n or ebob(c, n*n) != 1):
        raise Exception("Ciphertext Z*n^2 grubunun icinde yer almali..")

    m = (L(pow(c, Lambda, n*n), n) * Mu) % n
    mesaj = decimalToText(str(m)) # Decimal haldeki m mesaji text hale getirilir

    plaintext2 = open("plaintext2", "w") # Desifrelenen mesaj plaintext2 dosyasina yazilir
    plaintext2.write(str(mesaj))
    plaintext2.close()

    print("\n================================\nDecrypt:\n")
    print("mesaj: ", mesaj)
    print("\n** Desifreleme islemi yapildi..")

    plaintext = open("plaintext", "r")
    plaintext2 = open("plaintext2", "r")

    icerik = plaintext.readline()
    icerik2 = plaintext2.readline()

    plaintext.close()
    plaintext2.close()

    if (icerik == icerik2):
        print("\n================================\nKONTROL:\n\nYapilan sifreleme ve desifreleme islemleri dogrudur..")



# PAILLIER SIFRELEMESI CALISTIRMA #

print("PAILLIER SIFRELEMESI\n================================\n")

mesaj = input("Sifrelenecek mesaj: ")

plaintext = open("plaintext", "w")
plaintext.write(str(mesaj))
plaintext.close()

print("""\n================================\n\nKullanilacak Fonksiyonlar:\n\n- keygen(n)\n- encrypt("plaintext", "publickey.txt")\n- decrypt("ciphertext", "privatekey.txt")\n\n================================\n""")

n = int(input("Bit sayisini giriniz: "))
print("\n================================")
keygen(n)
encrypt("plaintext", "publickey.txt")
decrypt("ciphertext", "privatekey.txt")
