# Berkant Duman 160401048
import base64
import math
import time
import random

MOD = 2**8
FILL = 8

def string_to_bits(text):
    return ''.join(format(ord(i), 'b').zfill(FILL) for i in text)


def split_array_by_size(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs


def expand_to_128(data):
    original_data = data
    if len(data) < 112:
        data += "1"
        data += "0" * (112 - len(data))
    data += bin(len(original_data) % (2**16))[2:].zfill(16)
    return data


def binary_and(x, y):
    return (bin(int(x, 2) & int(y, 2))[2:]).zfill(FILL)


def binary_or(x, y):
    return (bin(int(x, 2) | int(y, 2))[2:]).zfill(FILL)


def binary_xor(x, y):
    return (bin(int(x, 2) ^ int(y, 2))[2:]).zfill(FILL)


def binary_not(x):
    return ''.join("0" if i == "1" else "1" for i in x)


def binary_left_rotate(x, times):
    if times == 0:
        return x
    else:
        return binary_left_rotate(x[1:]+x[0], times-1)


def final(file):
    s = [7, 3, 5, 13,  7, 3, 5, 13,  7, 3, 5, 13,  7, 3, 5, 13, 5,  9, 4, 20,  5,  9, 4, 20,  5,  9, 4, 20,  5,  9, 4, 20,
         4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23, 6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21] #Rotate değerleri

    try:
        f = open(file, "r")
        data = f.read()
        bits = string_to_bits(data)
    except:
        print("Dosya Bulunamadı")

    K = []
    for i in range(64):
        K.append(math.floor(2**8 * abs(math.sin(i + 1))))

    a0 = "00110011"
    b0 = "01110001"
    c0 = "11011101"
    d0 = "00010000"

    M = split_array_by_size(expand_to_128(bits), 8)
    A, B, C, D = a0, b0, c0, d0
    for i in range(64):
        if i in range(0, 15):
            F = binary_or(binary_and(B, C), binary_and(binary_not(B), D))
            g = i
        elif i in range(16, 31):
            F = binary_or(binary_and(D, B), binary_and(binary_not(D), C))
            g = (5*i + 1) % 16
        elif i in range(32, 47):
            F = binary_xor(binary_xor(B, C), D)
            g = (3*i + 5) % 16
        elif i in range(32, 47):
            F = binary_xor(C, binary_or(B, binary_not(D)))
            g = (7*i) % 16

        F = bin((int(F, 2) + K[i] + int(M[g], 2) +
                 int(A, 2)) % MOD)[2:].zfill(FILL)

        A = D
        D = C
        C = B
        B = bin(
            (int(B, 2) + int(binary_left_rotate(F, s[i]), 2)) % MOD)[2:].zfill(FILL)

    a0 = bin((int(a0, 2) + int(A, 2)) % MOD)[2:].zfill(FILL)
    b0 = bin((int(b0, 2) + int(B, 2)) % MOD)[2:].zfill(FILL)
    c0 = bin((int(c0, 2) + int(C, 2)) % MOD)[2:].zfill(FILL)
    d0 = bin((int(d0, 2) + int(D, 2)) % MOD)[2:].zfill(FILL)

    return a0 + b0 + c0 + d0


def check_block(block, random_number):
    binary = bin((block + random_number) % (2**32))[2:].zfill(32)
    if "1" in binary[0:8]:
        return False
    else:
        return binary


def blockchain():
    end_time = time.time() + 600
    hashsum = open("HASHSUM", "w")
    for i in range(2, 101):
        while time.time() <= end_time:
            
            if(i == 2):
                previous_block = final(str(i-1).zfill(3) + ".txt")
            else:
                previous_block_file = open((str(i-1).zfill(3) + ".txt"), "r")
                previous_block = previous_block_file.read()

            random_number = random.getrandbits(32)
            while not check_block(int(previous_block, 2), random_number):
                random_number = random.getrandbits(int(32))

            new_hash = check_block(int(previous_block, 2), random_number)
            new_block = open((str(i).zfill(3) + ".txt"), "w")
            new_block.write(new_hash)
            new_block.close()

            h_sum = "Blok: " + (str(i).zfill(3) + ".txt") + "  Random Sayı: " + str(random_number) + "  " + "Özet Değeri: " + new_hash + "\n"
            hashsum.write(h_sum)
            break;

    hashsum.close()    
    print("Program sona erdi.")


blockchain()
