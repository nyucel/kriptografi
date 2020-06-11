# İsmail ALTAY 170401038

import math
import random

r = 3271

def egcd(a,b):
    if(a == 0):
        return(b,0,1)
    else:
        c,d,e = egcd(b % a, a)
        return(c, e - (b // a) * d, d)

def modInvert(a,b):
    c,d,e = egcd(a,b)

    if c != 1:
        raise Exception('moduler ters bulunamadi')
    else:
        return d % b

def randomInteger(n):
    return random.randrange(2 ** (n-1), 2 ** n) | 1

def RabinMiller(f):
    s = 5
    if(f == 2):
        return 1

    if not (f & 1):
        return 0
    p = f-1
    u = 0
    r = f-1

    while (r%2 == 0):
        r >>= 1
        u+=1

    def Control(a):
        z = pow(a, r, f)
        if z == 1:
            return 0
        for i in range(u):
            z = pow(a, (2**i) * r, f-1)
            if z == p:
                return 0
        return 1
    for i in range(s):
        a = random.randrange(2, p-2)
        if Control(a):
            return 0
    return 1

def Keygen(n):

    while True:
        p = randomInteger(n//2)
        if (p - 1) % r == 0 and RabinMiller(p) and math.gcd(r, int((p - 1) / r)) == 1:
            break

    while True:
        q = randomInteger(n//2)
        if RabinMiller(q) and math.gcd(r, int(q - 1)) == 1:
            break

    N = p * q
    phi = (p - 1) * (q - 1)

    while True:
        y = random.randrange(1, N)
        if math.gcd(y, N) == 1:
            x = pow(y, phi * modInvert(r, N) % N, N)
            if x != 1:
                break

    publicKeyFile = open("publickey.txt", "w+")
    publicKeyFile.write(str(N) + "\n" + str(y))
    publicKeyFile.close()

    privateKeyFile = open("privatekey.txt", "w+")
    privateKeyFile.write(str(phi) + "\n" + str(x) + "\n" + str(N))
    privateKeyFile.close()

def encrypt(plaintext, publickeytxt):
    try:
        open(publickeytxt, "r")
    except FileNotFoundError:
        print("Anahtar çiftleri oluşturulmadan şifrelme işlemi yapılamaz. Lütfen önce Keygen fonksiyonunu çalıştırın.")
    else:
        publicKeyFile = open(publickeytxt, "r")
        N, y = publicKeyFile.read().split("\n")
        N = int(N)
        y = int(y)
        publicKeyFile.close()

        plainTextFile = open(plaintext, "r")
        plainCopy = int(plainTextFile.read().split("\n")[0])
        plainTextFile.close()

        while True:
            u = random.randrange(1, int(N))
            if math.gcd(y, N) == 1:
                break

    cipherText = pow(y, plainCopy, N) * pow(u, r, N) % N

    cipherTextFile = open("ciphertext.txt", "w+")
    cipherTextFile.write(str(cipherText))
    cipherTextFile.close()

def decrypt(ciphertext, privatekeytxt):
    try:
        open(privatekeytxt, "r")

    except FileNotFoundError:
        print("Anahtar çiftleri oluşturulmadan deşifreleme işlemi yapılamz. Lütfen önce Keygen fonksiyonunu çalıştırın.")
    else:
        privateKeyFile = open(privatekeytxt, "r")
        phi, x, N = privateKeyFile.read().split("\n")
        phi, x, N = int(phi), int(x), int(N)
        privateKeyFile.close()

        cipherTextFile = open(ciphertext, "r")
        cipherCopy = int(cipherTextFile.read())

        a = pow(cipherCopy, (phi * modInvert(r, N)) % N, N)
        for i in range(r -1):
            if(pow(x, i, N) == a):
                break

        plainText2File = open("plaintext2.txt", "w+")
        plainText2File.write(str(i))
        plainText2File.close()

        plain2File = open("plaintext2.txt", "r")
        plain1File = open("plaintext.txt", "r")

        plain1 = plain1File.read().split("\n")[0]
        plain2 = plain2File.read().split("\n")[0]

        if plain1 == plain2:
            print("Dosyalar Özdeştir..")
        else:
            print("Dosyalar özdeş değildir..")

n = int(input("Oluşturulmak istenen anahtar çiftlerinin bit uzunluğunu girin: "))
Keygen(n)
encrypt("plaintext.txt","publickey.txt")
decrypt("ciphertext.txt", "privatekey.txt")
