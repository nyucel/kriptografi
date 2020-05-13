#Ahmet Faruk Albayrak
#Can Sözbir - 170401016
#REQUIRES PYTHON 3.8 OR ABOVE!
#Tested on Pop!_OS 20.04 LTS x86_64 & Kali 2020.1b
import math
import os
import time
from random import randrange
from functions import isprime
print("REQUIRES PYTHON 3.8 OR ABOVE!")

r = 1321
# r => Block size, tek sayi olmak zorundadır.
# Aralarında asallık kontrolünden kurtulmak için asal seçilmesi sarttir.
# Şifreleyeceğiniz mesaj r den kucuk olmak zorundadır.


def generate_random(n):
    """
    n bitlik tek(odd) bir rastgele sayi olusturan fonksiyon.

    Arguments:
        n (int) : olusturulacak sayinin bit uzunlugu

    Returns:
        (int) : rastgele uretilmis tek tamsayi
    """
    return randrange(2**(n - 1), 2**n) | 1


def keygen(n):
    """
    Benaloh kriptosistemi ile public, private anahtarlari olusturup
    sirasiyla publickey.txt, privatekey.txt dosyalarina yazar.
    Arguments:
        n (int) : anahtar bit uzunlugu
    """
    p = q = y = x = None

    while True:
        p = generate_random(n // 2)
        if (p - 1) % r == 0 and isprime(p) == 1 and math.gcd(r, int((p - 1) / r)) == 1:
            break

    while True:
        q = generate_random(n // 2)
        if isprime(q) == 1 and math.gcd(r, int(q - 1)) == 1:
            break

    n_ = p * q
    phi = (p - 1) * (q - 1)

    while True:
        y = randrange(1, n_)
        if math.gcd(y, n_) == 1:
            x = pow(y, phi * pow(r, -1, n_) % n_, n_)
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
    plaintext.txt dosyasinin icerigini publickey.txt dosyasindan okudugu
    public anahtarlari kullanarak sifreleyip ciphertext.txt dosyasina yazar.
    Arguments:
        plaintext (str) : sifrelenecek mesajin bulundugu dosyanin yolu
        publickey_txt (str) : sifrelemede kullanilacak public anahtarlarin \
            okunacagi dosyanin yolu
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

    mes = []
    with open(plaintext, 'r') as plain_file:
        for message_line in plain_file:
            if message_line != '':
                for char in message_line:
                    mes.append(int(ord(char)))

    u = None
    while True:
        u = randrange(1, n_)
        if math.gcd(y, n_) == 1:
            break

    with open('ciphertext.txt', 'w+') as ciphertext_file:
        for m in mes:
            ciphertext = pow(y, m, n_) * pow(u, r, n_) % n_
            ciphertext_file.write(str(ciphertext) + " ")


def decrypt(ciphertext, privatekey_txt):
    """
    ciphertext dosyasinin icerigini privatekey.txt dosyasinin
    icindeki anahtari kullanarak cozer ve plaintext2.txt dosyasina yazar.
    Arguments:
        ciphertext (str) : sifrelenmis plaintext'in yazili oldugu dosyanin yolu
        privatekey_txt (str) :privatekey anahtarlarinin bulundugu dosyanin yolu
    Returns:
        bool :  plaintext.txt, plaintext2.txt ile özdeş ise True
                aksi halde False döndürür.
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
        ciphertext_file = c_file.readline().split(
            '\n')[0].split(" ")[:-1]

    with open("plaintext2.txt", 'w+') as plaintext2_file:
        for c_text in ciphertext_file:
            a = pow(int(c_text), phi * pow(r, -1, n_) % n_, n_)
            for i in range(r - 1):
                if pow(x, i, n_) == a:
                    break
            # print(i, chr(i))
            plaintext2_file.write(str(chr(i)))

    same = is_same("plaintext.txt", "plaintext2.txt")
    print(same)
    return same


def is_same(path1, path2):
    """
    Dosyaların içeriklerini kıyaslayıp aynı olup
    olmadıklarını geri döndüren fonksiyon.

    Arguments:
        file1 (str) : Kiyaslanacak kaynagin yolu
        file2 (str) : Kiyaslanan ciktinin yolu

    Returns:
        bool : file 1, file 2 ile ayniysa True, degilse False dondurur.
    """

    if not os.path.exists(path2):
        print(
            'hata: Karşılaştırmak için kullanacağınız ilk dosya bulunamadı.')
        exit()

    if not os.path.exists(path1):
        print(
            'hata: Karşılaştırmak için kullanacağınız ikinci dosya bulunamadı.')
        exit()
    with open(path1, "r") as f1:
        l1 = f1.read().split('\n')

    with open(path2, "r") as f2:
        l2 = f2.read().split('\n')

    while "" in l1:
        l1.remove("")

    while "" in l2:
        l2.remove("")

    if len(l1) != len(l2):
        return False

    for elem_1, elem_2 in zip(l1, l2):
        if elem_1 != elem_2:
            return False

    return True


# Test:
"""
t1 = time.time()
keygen(32)
encrypt("plaintext.txt", "publickey.txt")
decrypt("ciphertext.txt", "privatekey.txt")
t2 = time.time()
print('calisma suresi:', t2 - t1)
"""
