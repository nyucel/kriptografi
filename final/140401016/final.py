import random
import time

def generate_bit(n):
    p = random.getrandbits(n)
    bin = format(p, 'b').zfill(n)
    return bin

def and_bit(block1, block2):
    res = ""
    if len(block1) == len(block2):
        for i in range(len(block1)):
            res = res + str(int(block1[i]) & int(block2[i]))
        return (res)
    else:
        print("AND Operation Failure!")

def or_bit(block1, block2):
    res = ""
    if len(block1) == len(block2):
        for i in range(len(block1)):
            res = res + str(int(block1[i]) | int(block2[i]))
        return (res)
    else:
        print("OR Operation Failure!")

def xor_bit(block1, block2):
    res = ""
    if len(block1) == len(block2):
        for i in range(len(block1)):
            res = res + str(int(block1[i]) ^ int(block2[i]))
        return (res)
    else:
        print("XOR Operation Failure!")

def not_bit(block):
    mask = "11111111"
    res = ""
    if len(block) == len(mask):
        for i in range(len(block)):
            res = res + str(int(block[i]) ^ int(mask[i]))
        return (res)
    else:
        print("NOT Operation Failure!")

def add_bit(block1, block2):
    res = ""
    add = 0
    for i in range(len(block1)-1, -1, -1):
        flag = int(block1[i]) + int(block2[i]) + add
        if flag >= 2:
            add = 1
            res = res + str(flag % 2)
        else:
            add = 0
            res = res + str(flag)
    return ''.join(reversed(res))

def right_shift_bit(k, block):
    k = int(k % (len(block) / 2))
    block_list = []
    for i in range(len(block)):
        block_list.append(block[i])
    for i in range(k):
        for j in range(len(block)-1, 0, -1):
            block_list[j] = block_list[j-1]
        block_list[0] = 0
    result_block = ""
    for e in block_list:
        result_block = result_block + str(e)
    return result_block

def select_next_function(i, block1, block2, block3):
    if i%4 == 0:
        return or_bit(and_bit(block1, block2), and_bit(block1, not_bit(block3)))
    elif i%4 == 1:
        return xor_bit(xor_bit(block1, block2), block3)
    elif i%4 == 2:
        return or_bit(and_bit(not_bit(block1), block2), and_bit(block3, block2))
    else:
        return or_bit(or_bit(and_bit(block1,block2),and_bit(block1,block3)),and_bit(block2,block3))

def k_value(i):
    K = ["10010011","11000010","11001100","01000100",
        "01011010","00101001","01101001","10001110"]
    return K[i%8]

def check_first_eight(unCheck):
    if unCheck[0:8] == "00000000":
        return True
    return False

def hash(before_hash):
    block1 = before_hash[0:8]
    block2 = before_hash[8:16]
    block3 = before_hash[16:24]
    block4 = before_hash[24:32]
    W = [block1, block2, block3, block4]
    for i in range(32):
        f_result = select_next_function(i,block1,block2,block3)
        shifted_block1 = right_shift_bit(i+1,block1)
        w = W[i%4]
        k = k_value(i)

        operated = add_bit(k,add_bit(w,add_bit(shifted_block1,add_bit(block4,f_result))))

        block4 = block3
        block3 = right_shift_bit(i+1,block2)
        block2 = block1
        block1 = operated

    hashed = block1 + block2 + block3 + block4
    return hashed

def final(filepath):
    f = open(filepath, "r")
    before_hash = f.read()
    f.close()
    return hash(before_hash)

def start_block_chain():
    f = open("HASHSUM.txt", "w")
    f.write("NO        RASTGELE-SAYI                    ONCEKI-BLOK-OZETI")
    f.close()
    start_time = time.time()
    for i in range(99):
        if(time.time()-start_time > 600):
            print("10DK süre sınırı aşıldı.")
            break
        filepath_read = "%.3d" % (i + 1)
        hashed = final("%s.txt" % (filepath_read))
        flag = False
        while flag is False:
            random = generate_bit(32)
            before_hash = add_bit(random, hashed)
            after_hash = hash(before_hash)
            flag = check_first_eight(after_hash)
        filepath_write = "%.3d" % (i + 2)
        f = open("%s.txt" % (filepath_write), "w")
        f.write(after_hash)
        f.close()
        f = open("HASHSUM.txt", "a")
        hashSum = "\n%.3d %s %s" % (i + 2, random, hashed)
        f.write(hashSum)
        f.close()

start_block_chain()

