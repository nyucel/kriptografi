from gmpy2 import invert

import math
from random import randrange
import random
import os
import time


r = 305
# Block size, tek sayi olmak zorundadır.
# Aralarında asallık kontrolünden kurtulmak için asal seçilmesi faydalıdır.
# Şifreleyeceğiniz mesaj r den kucuk olmak zorundadır.


def generate_random(n):
    """
    n bitlik tek(odd) bir rastgele sayi olusturan fonksiyon.

    Arguments:
        n (int) : olusturulacak sayinin bit lengthi

    Returns:
        int : bir sayi, rastgele uretilmis , tek(odd)
    """
    return randrange(2**(n - 1), 2**n) | 1


def rabin_miller(p):
    s = 5
    if p == 2:
        return True
    if not (p & 1):
        return False

    p1 = p - 1
    u = 0
    r = p1

    while r % 2 == 0:
        r >>= 1
        u += 1

    def witness(a):
        z = pow(a, r, p)
        if z == 1:
            return False

        for i in range(u):
            z = pow(a, 2**i * r, p)
            if z == p1:
                return False
        return True

    for i in range(s):
        a = random.randrange(2, p-2)
        if witness(a):
            return False

    return True


def keygen(n):
    """
    baneloh kriptosistemine uygun sekilde public ve private keyleri olusturup
    bunlari publickey.txt ve privatekey.txt dosyalarina yazan fonksiyon.

    Arguments:
        n (int) : olusturulacak anahtar boyutu
    """
    p = q = y = x = None

    while True:
        p = generate_random(n//2)
        if (p-1) % r == 0 and rabin_miller(p) and math.gcd(r, int((p-1)/r)) == 1:
            break

    while True:
        q = generate_random(n//2)
        if rabin_miller(q) and math.gcd(r, int(q-1)) == 1:
            break

    n_ = p * q
    phi = (p-1) * (q-1)

    while True:
        y = randrange(1, n_)
        if math.gcd(y, n_) == 1:
            x = pow(y, phi * invert(r, n_) % n_, n_)
            if x != 1:
                break

    with open("publickey.txt", "w+") as publickey_file:
        publickey_file.write(
            str(n_) + '\n' +
            str(y)

        )

    with open("privatekey.txt", "w+") as privatekey_file:
        privatekey_file.write(
            str(n_) + '\n' +
            str(phi) + '\n' +
            str(x)
        )


def encrypt(plaintext, publickey_txt):
    """
    plaintext pathindeki dosyanin icerigini publickey_txt dosyasindan okudugu
    public keyleri kullanaarak encrypt leyip ciphertext.txt dosyasina yazan
    fonksiyon.

    Arguments:
        plaintext (str) : sifrelenecek mesajin bulundugu dosyanin pathi
        publickey_txt (str) : sifrelemede kullanilacak public keylerin \
            okunacagi dosyanin pathi
    """
    if not os.path.exists(publickey_txt):
        print(
            'hata: publickey_txt bulunamadı, lütfen önce keygen fonksiyonunu \
                çalıştırınız.')
        exit()

    if not os.path.exists(plaintext):
        print('hata: plaintext dosyası bulunamadı, lütfen önce bu dosyayı \
            şifrelenecek mesaj ile birliklte kendiniz oluşturun')
        exit()

    with open(publickey_txt, 'r') as publickey_file:
        n_, y = publickey_file.read().split('\n')
        n_, y = int(n_), int(y)

    with open(plaintext, 'r') as plain_file:
        message = int(plain_file.readline().split('\n')[0])

    u = None
    while True:
        u = randrange(1, n_)
        if math.gcd(y, n_) == 1:
            break

    ciphertext = pow(y, message, n_) * pow(u, r, n_) % n_

    with open('ciphertext.txt', 'w+') as ciphertext_file:
        ciphertext_file.write(str(ciphertext))


def decrypt(ciphertext, privatekey_txt):
    """ciphertext 

    Arguments:
        ciphertext (str) : ciphertext in yazili oldugu dosyanin pathi
        privatekey_txt (str) : privatekey lerin yazili oldugu dosyanin pathi

    Returns:
        bool :  True if plaintext1.txt is equal to plaintext2.txt, 
                False otherwise
    """
    if not os.path.exists(privatekey_txt):
        print(
            'hata: privatekey_txt bulunamadı, lütfen önce keygen fonksiyonunu \
                çalıştırınız.')
        exit()

    if not os.path.exists(ciphertext):
        print(
            'hata: ciphertext.txt bulunamadı, lütfen önce keygen fonksiyonunu \
                çalıştırınız.')
        exit()

    with open(privatekey_txt, 'r') as p_file:
        n_, phi, x = p_file.read().split('\n')
        n_, phi, x = int(n_), int(phi), int(x)

    with open(ciphertext, 'r') as c_file:
        c = int(c_file.readline().split('\n')[0])

    a = pow(c, phi * invert(r, n_) % n_, n_)
    for i in range(r-1):
        if pow(x, i, n_) == a:
            break

    with open("plaintext2.txt", 'w+') as plaintext2_file:
        plaintext2_file.write(str(i))

    same = is_same("plaintext.txt", "plaintext2.txt")
    print(same)
    return same


def is_same(file1, file2):
    """
    Tek satırdan oluştuğu kabul edilen dosyaların içeriklerini kıyaslayıp 
    aynı olup olmadıklarını geri döndüren fonksiyon. 

    Arguments:
        file1 (str) : The first file's path
        file2 (str) : The second fıleis path

    Returns:
        bool : The return value, True if file1 is identical to file2, False otherwise.
    """

    if not os.path.exists(file1):
        print(
            'hata: Karşılaştırmak için kullanacağınız ilk dosya bulunamadı.')
        exit()

    if not os.path.exists(file2):
        print(
            'hata: Karşılaştırmak için kullanacağınız ikinci dosya bulunamadı.')
        exit()

    f1 = open(file1, 'r')
    f2 = open(file2, 'r')

    t1 = f1.readline().split('\n')[0]
    t2 = f2.readline().split('\n')[0]

    if t1 == t2:
        return True
    else:
        return False


t1 = time.time()
keygen(32)
encrypt("plaintext.txt", "publickey.txt")
decrypt("ciphertext.txt", "privatekey.txt")
t2 = time.time()
print('calisma suresi:', t2-t1)
