import random
import sys
import time

# NOTE: finaldeki satir kontrolu yap.


def get_random_32_bits():
    random_32_bits = "1"
    for i in range(31):
        t = str(random.randint(0, 1))
        random_32_bits += t
    return random_32_bits


def create_table():
    a = []
    for i in range(256):
        m = i
        for j in range(8):
            if m & 1:
                m ^= 0x1db710640
            m >>= 1
        a.append(m)
    return a


def final(buf, hash):
    #hash_table = create_table()
    hash ^= 0xffffffff
    try:
        for m in buf:
            hash = (hash >> 8) ^ hash_table[(hash & 0xff) ^ m]
    except:
        print("Final fonksiyonunu ozerk kullanmak istiyorsaniz final icinde hash_table in tanimlandigi satiri(29.satir) yorumdan kaldirip, main'den once (89. satirda) yoruma alin. Uyari: boyle yapmaniz kodu oldukca yavaslaticaktir.")
        sys.exit()
    return hash ^ 0xffffffff


def make_b():
    # b rastgele 32 bit sayi
    b = get_random_32_bits()
    b = '0b' + b
    #print("this is b:", b)
    return b


def recreate_hash_until_8_zeros(a):

    ## INITIAL D CREATION: burayi do-while gibi kodladim kotu gorunuyor, ayni kod tekrarlaniyor ama duzeltmeye vakit kalmadi ##
    b = make_b()

    # c toplam
    c = int(a, 2) + int(b, 2)
    c = bin(c)[2:]
    # print(len(c))
    #print("this is c:", c)
    if len(c) == 33:    # 32 bit hash + 32bit rastgele sayi toplami 33 bite tasinca
        c = c[1:]
        # print(len(c))
    #print("this is c:", c)

    # d toplamin hashi
    temp = str(c).encode('UTF-8')
    d = bin(final(temp, 0))[2:].zfill(32)
    #print("this is d:", d)

    while (d[:8] != "00000000"):
        b = make_b()

        # c toplam
        c = int(a, 2) + int(b, 2)
        c = bin(c)[2:]
        # print(len(c))
        #print("this is c:", c)
        if len(c) == 33:    # 32 bit hash + 32bit rastgele sayi toplami 33 bite tasinca
            c = c[1:]
            # print(len(c))
        #print("this is c:", c)

        # d toplamin hashi
        temp = str(c).encode('UTF-8')
        d = bin(final(temp, 0))[2:].zfill(32)
        #print("this is d:", d)

    return d, b[2:]


hash_table = create_table()


filename = input(
    "Ozetini elde etmek istediginiz dosyanin adini giriniz(blok zincirini olusturmak icin 001.txt giriniz.): ")
f = open(filename, "r")
x = f.read().encode('UTF-8')

# a dosya hashimiz
a = bin(final(x, 0))[
    2:].zfill(32)
a = '0b' + a
print("Dosyanizin ozeti:", a[2:])

if (filename == "001.txt"):
    t0 = time.time()
    d = a       # 1.blogun ozeti d'ye atandi.
    for i in range(2, 101):
        # d son dosyanin ozeti, b son kullanilan rastgele 32 bit binary sayi
        d, b = recreate_hash_until_8_zeros(d)
        if (i < 10):
            new_filename = "00" + str(i) + ".txt"
            f = open(new_filename, "w")
            f.write(d)
            f.close()
            f = open("HASHSUM", "a")
            f.write("Blok " + str(i) + ": " + d + " , " + b + "\n")
            f.close()
        elif (i < 100):
            new_filename = "0" + str(i) + ".txt"
            f = open(new_filename, "w")
            f.write(d)
            f.close()
            f = open("HASHSUM", "a")
            f.write("Blok " + str(i) + ": " + d + " , " + b + "\n")
            f.close()
        elif (i == 100):
            new_filename = "100.txt"
            f = open(new_filename, "w")
            f.write(d)
            f.close()
            f = open("HASHSUM", "a")
            f.write("Blok " + str(i) + ": " + d + " , " + b + "\n")
            f.close()
        if time.time() - t0 >= 600:
            print('10 dklik max sure dolmustur.')
            print("gecen sure:", (time.time() - t0))
            sys.exit()
    print("gecen sure:", (time.time() - t0))
