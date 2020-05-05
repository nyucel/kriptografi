# -*- coding: utf-8 -*-
#Python3.8 bağımlılığı vardır.

#Barış Kaan BAYRAM

import random
import sys
import functions

#İlk ve son bitleri 1 olan n bitlik sayı üretir.
def generateBigNumber(n):
    p = random.getrandbits(n)
    p |= (1 << n - 1) | 1
    return p

#Üretilen sayının asallığı kontrol eder.
def generatePrimeNumber(n):
    p = 42
    while not functions.isprime(p):
        p = generateBigNumber(n)
    return p

#n -> bit sayısı
#Anahtar çiftlerini üretir.
#Girilecek anahtar boyutu(bit), şirelenecek karakter boyutundan(bit) fazla olmalıdır. ( m < p )
def keygen(n):
    p = generatePrimeNumber(n)
    q = generatePrimeNumber(n)
    p2 = p * p
    z = p2 * q
    while True:
        g = random.randint(2, z-1)
        if(pow(g, p-1, p2) != 1):
            break

    f_public = open("publickey.txt", "w+")
    f_public.write(str(z) + " " + str(g))
    f_public.close()

    #Açık anahtarın bir parçası olan 'g', decryption işlemi için lazım olduğu için mecburi olarak privatekey dosyasına eklendi.
    f_private = open("privatekey.txt", "w+")
    f_private.write(str(p) + " " + str(q) + " " + str(g))
    f_private.close()

#Plaintext'te var olan karakterleri binary hale çevirir.
def charToBinary(ch):
    return "".join(f"{ord(ch):08b}")

#Plaintext dosyasını şifreler.
def encrypt(plaintext, publickey):
    try:
        f = open(publickey, "r")
        publickeyString = f.read()
    except:
        sys.exit("'publickey' dosyası bulunamadı. Çalıştır keygen(n) .")
    finally:
        f.close()

    z, g = publickeyString.split(" ")

    z = int(z)
    g = int(g)

    try:
        f = open(plaintext, "r")
        plaintextString = f.read()
    except:
        sys.exit("'plaintext' hatası !")
    finally:
        f.close()

    f = open("ciphertext.txt", "w+")
    for i in plaintextString:
        r = random.randint(1, z-1)
        m_binary = charToBinary(i)
        m = int(m_binary, 2)
        c = pow(g, (m + (z * r)), z)
        f.write(str(c) + " ")
    f.close()

def decrypt(ciphertext, privatekey):
    try:
        f = open(ciphertext, "r")
        ciphertextString = f.read()
    except:
        sys.exit("'ciphertext' dosyası bulunamadı !")
    finally:
        f.close()

    try:
        f = open(privatekey, "r")
        privatekeyString = f.read()
    except:
        sys.exit("'privatekey' dosyası bulunamadı. Çalıştır keygen(n) .")
    finally:
        f.close()

    p, q, g = privatekeyString.split(" ")

    p = int(p)
    g = int(g)

    list = ciphertextString.split(" ")
    list.remove('')
    b = int((pow(g, p-1, pow(p,2)) - 1) / p)
    b_ = pow(b, -1, p)

    f_plain2 = open("plaintext2", "w+")

    for i in list:
        c = int(i)
        a = int((pow(c, p-1, pow(p,2)) - 1) / p)
        m = pow(a*b_, 1, p)
        m_char = chr(m)
        f_plain2.write(m_char)
    f_plain2.close()

    correctness = isSame("plaintext", "plaintext2")
    if(correctness):
        print("Başarılı !")
    else:
        print("Başarısız !")


def isSame(plaintext, plaintext2):
    f = open(plaintext, "r")
    plaintextString = f.read()
    f.close()

    f = open(plaintext2, "r")
    plaintextString2 = f.read()
    f.close()

    if (plaintextString == plaintextString2):
        return True
    else:
        return False