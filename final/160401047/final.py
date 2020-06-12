#Batuhan Bagceci - 160401047

import random
import signal

def final(filename):
    file = open(filename, "rb")
    key = file.read()
    file.close()
    key = str(key)[2:-5]

    sayi1 = 0b11001100100111100010110101010001
    sayi2 = 0b00011011100001110011010110010011
    r1 = 15
    r2 = 13
    m = 5
    n = 0b11100110010101000110101101100100

    leng = len(key)
    hash = 0

    byte = (leng & 0b11111111111111111111111111111100)
    for i in range(0, byte, 4):
      num = (ord(key[i]) & 0b11111111) | ((ord(key[i + 1]) & 0b11111111) << 8) | ((ord(key[i + 2]) & 0b11111111) << 16) | (ord(key[i + 3]) << 24)
      num = num * sayi1
      num = (num << r1) | ((num & 0b11111111111111111111111111111111) >> (32-r1))
      num = num * sayi2
      hash = hash ^ num
      hash = (hash << r2) | ((hash & 0b11111111111111111111111111111111) >> (32-r2))
      hash = hash * m + n

    num = 0

    j = (leng & 3)
    if(j == 3):
        num = (ord(key[byte + 2]) & 0b11111111) << 16

    if((j == 2) or (j==3)):
        num = num | (ord(key[byte + 1]) & 0b11111111) << 8

    if((j == 1) or (j == 2) or (j==3)):
        num = num | ord(key[byte]) & 0b11111111
        num = num * sayi1
        num = (num << r1) | ((num & 0b11111111111111111111111111111111) >> (32-r1))
        num = num * sayi2
        hash = hash ^ num

    hash = hash ^ leng
    hash = hash ^ ((hash & 0b11111111111111111111111111111111) >> 16)
    hash = hash * 0b10000101111010111100101001101011
    hash = hash ^ ((hash & 0b11111111111111111111111111111111) >> 13)
    hash = hash * 0b11000010101100101010111000110101
    hash = hash ^ ((hash & 0b11111111111111111111111111111111) >> 16)

    return format((hash & 0b11111111111111111111111111111111), "032b")

def blockchain():
    signal.alarm(600)

    hashsum = open("HASHSUM", "w")
    hashsum.close()

    hash = int(final("001.txt"), 2)

    for i in range(2, 101):
        hashsum = open("HASHSUM", "a")

        while(True):
            randomnum = random.getrandbits(32)
            next = open("{0:03}".format(i)+".txt", "w")
            next.write(format(hash+randomnum, "0b"))
            next.close()
            hash = int(final("{0:03}".format(i)+".txt"), 2)
            if(hash >> 24 == 0):
                break

        hashsum.write("{0:03}".format(i)+".txt "+"Random: "+format(randomnum, "032b")+" ")
        hashsum.write("Hash: "+format(hash, "032b")+"\n")
        hashsum.close()

blockchain()
