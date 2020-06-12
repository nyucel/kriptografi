#Reber Ferhat Uluca - 170401053

import random
import time

def A(x, y, z, d):
    return (~x & y) | (~d & z)
def B(x, y, z, d):
    return (x & ~y) | (d & ~z)
def C(x, y, z, d):
    return (x | (~y)) ^ (d | (~z))
def D(x, y, z, d):
    return ((~x) | y) ^ ((~d) | z)
def E(x, y, z, d):
    return x ^ y ^ z ^ d
def shift(k, bits):
    bits = bits % 8
    k = k % (2 ** 8)
    upper = (k << bits) % (2 ** 8)
    result = upper | (k >> (8 - bits))
    return result

def operation(x, y, z, d, c, s):
    f_a = A(x, y, z, d)
    f_b = B(x, y, z, d)
    f_c = C(x, y, z, d)
    f_d = D(x, y, z, d)
    f_e = E(f_a, f_b, f_c, f_d)
    sh = shift(x+c, s)
    return (f_e + sh) % 2 ** 8

def final(filename):
    f = open(filename, "r")
    msg = f.read()

    bits = []
    for i in msg:
        binary = bin(int(i))[2:]
        while len(binary) < 8:
            binary += '0'                  #padding for each 8 bits
        bits.append(int(binary, 2))

    while len(bits) % 4 != 0:
        padding = 0x00                  #padding for all bits
        bits.append(padding)

    A = 0x67
    B = 0xaf
    C = 0x98
    D = 0x25

    cons = [0xfd, 0xa4, 0x4b, 0xf6, 0xbe,
            0x28, 0xea, 0xd4, 0x48, 0xd9,
            0x49, 0xf6, 0xc0, 0x26, 0xe9, 0xd]

    shifts = [7, 12, 17, 22, 5, 9, 14, 20,
              4, 11, 16, 23, 6, 10, 15, 21]

    for i in range(len(bits)//4):
        for j in range(16):
            x = bits[i * 4 + 0]
            y = bits[i * 4 + 1]
            z = bits[i * 4 + 2]
            d = bits[i * 4 + 3]

            bits[i * 4 + 0] = d
            bits[i * 4 + 1] = operation(x, y, z, d, cons[j], shifts[j])
            bits[i * 4 + 2] = y
            bits[i * 4 + 3] = z

        A = (A + x) % (2 ** 8)
        B = (B + y) % (2 ** 8)
        C = (C + z) % (2 ** 8)
        D = (D + d) % (2 ** 8)

    f.close()
    return '{:008b}'.format(A)+'{:008b}'.format(B)+'{:008b}'.format(C)+'{:008b}'.format(D)

def main():
    start = time.time()

    hashsum = open("HASHSUM", "w")
    hashed = final("001.txt")
    hashsum.write("001.txt ozet:" + hashed)

    for i in range(2, 101):
        if (time.time() - start) >= 10*60:
            print("timed out")
            hashsum.close()
            f.close()
            return

        f = open("{0:03}.txt".format(i), "w")
        x = random.getrandbits(32)
        hashed = int(hashed, 2)
        sum = bin(x + hashed)[2:]
        f.write(sum)
        f.close()

        hash2 = final("{0:03}.txt".format(i))
        while hash2[:8] != "00000000":
            if (time.time() - start) >= 10*60:
                print("timed out")
                hashsum.close()
                f.close()
                return

            f = open("{0:03}.txt".format(i), "w")
            x = random.getrandbits(32)
            sum = bin(x + hashed)[2:]
            f.write(sum)
            f.close()
            hash2 = final("{0:03}.txt".format(i))

        hashsum.write("\n{0:03}.txt".format(i) + " ozet:" + hash2 +
                      " random:" + '{:032b}'.format(x))

        hashed = hash2

    hashsum.close()

if __name__ == "__main__":
    main()