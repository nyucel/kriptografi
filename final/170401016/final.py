import os.path
import sys
import binascii
import random
import time


rotate = [
    131, 234, 148, 165, 180, 159, 216, 207, 187, 254,
    166, 140, 200, 151, 184, 199, 133, 163, 205, 211,
    193, 217, 216, 201, 198, 240, 244, 149, 164, 128,
    223, 206, 134, 133, 249, 145, 224, 176, 218, 168,
    202, 248, 252, 138, 167, 146, 248, 135, 157, 247,
    186, 210, 201, 228, 135, 174, 185, 167, 241, 228,
    255, 135, 191, 203
]


def generate_random(n):
    return random.randrange(2**(n - 1), 2**n)


def hex_to_binary(hex_code):
    bin_code = bin(hex_code)[2:]
    padding = (4-len(bin_code) % 4) % 4
    return '0'*padding + bin_code


def solaDaireselKaydir(k, bits):
    bits = bits % 32
    k = k % (2**32)
    upper = (k << bits) % (2**32)
    result = upper | (k >> (32-(bits)))
    return(result)


def blokBol(blok, chunks):

    size = len(blok)//chunks

    return [int.from_bytes(blok[size*i: size*(i+1)], byteorder='little') for i in range(0, chunks)]


def isle_F(a, b, c, d, M, s, t):

    f = ((b & c) | ((~b) & d))
    r = solaDaireselKaydir((a + f + M + t), s)

    return b + r


def isle_G(a, b, c, d, M, s, t):

    g = ((b & d) | (c & (~d)))
    r = solaDaireselKaydir((a + g + M + t), s)
    return b + r


def isle_H(a, b, c, d, M, s, t):

    h = (b ^ c ^ d)
    r = solaDaireselKaydir((a + h + M + t), s)
    return b + r


def isle_I(a, b, c, d, M, s, t):

    i = (c ^ (b | (~d)))
    r = solaDaireselKaydir((a + i + M + t), s)
    return b + r


def decimal_to_hexadecimal(num):
    bighex = "{0:02x}".format(num)
    binver = binascii.unhexlify(bighex)
    result = "{0:02x}".format(int.from_bytes(binver, byteorder='little'))
    return result


def bit_length(text):
    return len(text)*8


def final(path):
    message = None
    try:
        with open(path, 'rb') as f:
            message = f.read()
    except:
        print(f'{path} dosyasi bulunamadi')
        return

    len_message = (len(message) * 8) % (2**16)
    message = message + b'\x80'
    padding = (112 - (len_message+8) % 128) % 128
    padding //= 8
    message = message + b'\x00'*padding + \
        len_message.to_bytes(2, byteorder='little')
    len_message = len(message) * 8
    number_of_iterations = len_message//128

    A = 103
    B = 239
    C = 152
    D = 16

    adcb = {
        "a": A,
        "d": D,
        "c": C,
        "b": B
    }

    for i in range(0, number_of_iterations):

        adcb["a"], adcb["b"], adcb["c"], adcb["d"] = A, B, C, D

        block = message[i*64:(i+1)*64]
        boluk_blok = blokBol(block, 16)

        for j in range(64):
            if j < 16:
                if j % 4 == 0:
                    adcb["a"] = isle_F(adcb["a"], adcb["b"], adcb["c"],
                                       adcb["d"], boluk_blok[j], 7, rotate[j])
                elif j % 4 == 1:
                    adcb["d"] = isle_F(adcb["d"], adcb["a"], adcb["b"],
                                       adcb["c"], boluk_blok[j], 12, rotate[j])
                elif j % 4 == 2:
                    adcb["c"] = isle_F(adcb["c"], adcb["d"], adcb["a"],
                                       adcb["b"], boluk_blok[j], 17, rotate[j])
                else:
                    adcb["b"] = isle_F(adcb["b"], adcb["c"], adcb["d"],
                                       adcb["a"], boluk_blok[j], 22, rotate[j])

            elif j < 32:  # 16 dan basliyor
                if j % 4 == 0:
                    adcb["a"] = isle_G(adcb["a"], adcb["b"], adcb["c"],
                                       adcb["d"], boluk_blok[(1+4*((j-16)//4)) % 16], 5, rotate[j])

                elif j % 4 == 1:
                    adcb["d"] = isle_G(adcb["d"], adcb["a"], adcb["b"],
                                       adcb["c"], boluk_blok[(6+4*((j-16)//4)) % 16], 9, rotate[j])

                elif j % 4 == 2:
                    adcb["c"] = isle_G(adcb["c"], adcb["d"], adcb["a"],
                                       adcb["b"], boluk_blok[(11+4*((j-16)//4)) % 16], 14, rotate[j])
                else:
                    adcb["b"] = isle_G(adcb["b"], adcb["c"], adcb["d"],
                                       adcb["a"], boluk_blok[(4*((j-16)//4)) % 16], 20, rotate[j])

            elif j < 48:

                if j % 4 == 0:
                    adcb["a"] = isle_H(adcb["a"], adcb["b"], adcb["c"],
                                       adcb["d"], boluk_blok[(5+12*((j-32)//4)) % 16], 4, rotate[j])

                elif j % 4 == 1:
                    adcb["d"] = isle_H(adcb["d"], adcb["a"], adcb["b"],
                                       adcb["c"], boluk_blok[(8+12*((j-32)//4)) % 16], 11, rotate[j])

                elif j % 4 == 2:
                    adcb["c"] = isle_H(adcb["c"], adcb["d"], adcb["a"],
                                       adcb["b"], boluk_blok[(11+12*((j-32)//4)) % 16], 16, rotate[j])
                else:
                    adcb["b"] = isle_H(adcb["b"], adcb["c"], adcb["d"],
                                       adcb["a"], boluk_blok[(14+12*((j-32)//4)) % 16], 23, rotate[j])

            else:
                if j % 4 == 0:
                    adcb["a"] = isle_I(adcb["a"], adcb["b"], adcb["c"],
                                       adcb["d"], boluk_blok[(12*((j-48)//4)) % 16], 6, rotate[j])

                elif j % 4 == 1:
                    adcb["d"] = isle_I(adcb["d"], adcb["a"], adcb["b"],
                                       adcb["c"], boluk_blok[(7+12*((j-48)//4)) % 16], 10, rotate[j])

                elif j % 4 == 2:
                    adcb["c"] = isle_I(adcb["c"], adcb["d"], adcb["a"],
                                       adcb["b"], boluk_blok[(14+12*((j-48)//4)) % 16], 15, rotate[j])
                else:
                    adcb["b"] = isle_I(adcb["b"], adcb["c"], adcb["d"],
                                       adcb["a"], boluk_blok[(5+12*((j-48)//4)) % 16], 21, rotate[j])

        A = (A + adcb["a"]) % (2**8)
        B = (B + adcb["b"]) % (2**8)
        C = (C + adcb["c"]) % (2**8)
        D = (D + adcb["d"]) % (2**8)

    result = decimal_to_hexadecimal(
        A) + decimal_to_hexadecimal(B)+decimal_to_hexadecimal(C)+decimal_to_hexadecimal(D)
    return result


def binary_addition(a, b):
    return bin(int(a, 2) + int(b, 2))[2:]


def blockchain():
    t0 = time.time()
    if not os.path.exists('001.txt'):
        print('001.txt dosyasi bulunamadi. Dosyayi sizin icin otomatik olusturuyorum...')

        with open('001.txt', 'w+') as txt:
            # 170401016 in binary
            txt.write('00001010001010000001110011111000')

    hashsum_file = open('HASHSUM', 'w+')

    for i in range(1, 100):
        if time.time() - t0 >= 600:
            print('bize ayrilan surenin sonuna gelmis bulunmaktayiz :).')
            break

        prev_path = '0'*(3-len(str(i))) + str(i) + '.txt'
        next_path = '0'*(3-len(str(i+1))) + str(i+1) + '.txt'

        hashsum = final(prev_path)
        hashsum_binary = hex_to_binary(int(hashsum, 16))

        while True:
            rand = generate_random(32)
            rand_binary = bin(rand)[2:]

            hashsum_plus_rand = binary_addition(hashsum_binary, rand_binary)

            with open(next_path, 'w+') as txt_next:
                txt_next.write(hashsum_plus_rand)

            next_chain_hashsum = final(next_path)

            if next_chain_hashsum[:2] == '00':
                hashsum_file.write(
                    f'{next_path} dosyasi olusturulurken kullanilan random sayi: {str(rand)}, olusturulan blogun ozet degeri: 0x{next_chain_hashsum}\n')
                break

    hashsum_file.close()


blockchain()
