import random
from time import time

def xor(x, y):
    a = int(x, 2) ^ int(y, 2)
    b = '{0:0{1}b}'.format(a, len(x))
    return b

def txt_name(i):
    if i < 10:
        name = "00" + str(i) + ".txt"
    elif i < 100:
        name = "0" + str(i) + ".txt"
    else:
        name = str(i) + ".txt"
    return name

def right_rotate(input, d):
    Rfirst = input[0: len(input) - d]
    Rsecond = input[len(input) - d:]

    return Rsecond + Rfirst

def random_32():
    r = ""
    while len(r) != 32 :
        r += str(random.randint(0,1))
    return r

def xor_l(list):
    xor_list = []
    if len(list) == 1:
        return list
    elif len(list) == 2:
        a = list[0]
        b = list[1]
        y = int(a, 2) ^ int(b, 2)
        x = '{0:0{1}b}'.format(y, len(a))
        xor_list.append(x)
    else:
        for i in range(0, len(list) - 1, 2):
            a = list[i]
            b = list[i + 1]
            y = int(a, 2) ^ int(b, 2)
            x = '{0:0{1}b}'.format(y, len(a))
            xor_list.append(x)
    return xor_list

def final(file):
    dosya = open(file,"r")
    file_text = dosya.read()
    dosya.close()
    if (file == "001.txt"): #eger ilk dosya ise binary yapıyoruz
        binary_text = ''.join(format(ord(x), '08b') for x in file_text)
    else:
        binary_text = file_text
    data = "1101110010011001011101001010101010010111001001100101110111000101"
    i = 0
    while i != 16:
        binary_text += data

        while (len(binary_text) % 128 != 0):  # bit sayısını 128'e veya katına tamamlamak için listenin sonuna 1'ler ekledik
            binary_text += "1"

        binary_text = right_rotate(binary_text, 32)  # 32 bit sağa dondurduk
        i += 1
    bit_list = [binary_text[i:i + 16] for i in range(0, len(binary_text), 16)]  # 16 bitlik parçalar halinde listeye çevirdik

    for i in range(0, (len(bit_list) // 2) - 1):  # liste elemanlarının yerini değistirdik
        temp = bit_list[i]
        bit_list[i] = bit_list[len(bit_list) - 1]
        bit_list[len(bit_list) - 1] = temp

    copy_list_1 = bit_list.copy()
    xor_list = []
    for i in range(0, len(bit_list)//2): #listeyi xor'ladık
        xor_list = xor_l(copy_list_1)
        copy_list_1 = xor_list

    xor1 = copy_list_1[0]

    ozet1 = xor(xor(xor(xor(xor1, data[:16]), data[16:32]), data[32:48]), data[48:64])
    ozet1 = right_rotate(ozet1, 3)
    ozet2 = xor(xor(xor(xor(xor1, data[48:64]), data[32:48]), data[16:32]), data[:16])
    ozet2 = right_rotate(ozet2, 3)
    ozet = ozet1 + ozet2

    return ozet

hashsum = open("HASHSUM.txt", "w")
zaman = time()+600
for i in range(1,100):

    file_p = txt_name(i)
    ozet = final(file_p)

    while True:

        if time() > zaman: break
        rand = random_32()
        sum = int(ozet, 2) + int(rand, 2)
        file_name = txt_name(i+1)
        file = open(file_name, "w+")
        file.write(str(bin(sum)[2:].zfill(32)))
        file.close()
        ozet_2 = final(file_name)

        if(ozet_2[:8] == "00000000"):
            rand_ozet = "Random : " + rand + " Ozet : " +ozet_2 + "\n"
            hashsum.writelines(rand_ozet)
            print("oldu")
            break
        else:
            print("olmadı")
hashsum.close()








