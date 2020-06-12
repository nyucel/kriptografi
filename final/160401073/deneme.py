import random
import array
import time

def generate32bitStringFromDecimal(decimal):
    not32bit =  bin(decimal).replace("0b", "")
    boyut = len(not32bit)
    zero = 32 - boyut
    fixed32bit = ""
    for i in range(zero):
        fixed32bit = fixed32bit + "0"
    for i in range(boyut):
        fixed32bit = fixed32bit + not32bit[i]
    return fixed32bit
def generateRandom32Bit():
    p = random.getrandbits(32)
    get_bin = lambda x, n: format(x, 'b').zfill(n)
    return get_bin(p,32)

def bitwiseAnd(partX,partY):
    res = ""
    if len(partX) == len(partY):
        for i in range(len(partX)):
            res = res + str(int(partX[i]) & int(partY[i]))
        return (res)
    else:print("Hata and")

def bitwiseOr(partX,partY):
    res = ""
    if len(partX) == len(partY):
        for i in range(len(partX)):
            res = res + str(int(partX[i]) | int(partY[i]))
        return (res)
    else:print("Hata or")

def bitwiseXor(partX,partY):
    res = ""
    if len(partX) == len(partY):
        for i in range(len(partX)):
            res = res + str(int(partX[i]) ^ int(partY[i]))
        return (res)
    else:print("Hata xor")

def bitwiseNot(partX):
    mask = "11111111"
    res = ""
    if len(partX) == len(mask):
        for i in range(len(partX)):
            res = res + str(int(partX[i]) ^ int(mask[i]))
        return (res)
    else:print("Hata not")

def functionNyks(partX,partY,partZ):
    return bitwiseOr(bitwiseAnd(partX,partY),bitwiseAnd(bitwiseNot(partX),partZ))

def functionMiro(partX,partY,partZ):
    return bitwiseOr(bitwiseAnd(partX,partZ),bitwiseAnd(bitwiseNot(partZ),partY))

def functionRita(partX,partY,partZ):
    return bitwiseXor(bitwiseXor(partX,partY),partZ)

def functionFindik(partX,partY,partZ):
    return bitwiseXor(partY,bitwiseOr(partX,bitwiseNot(partZ)))

def getFunction(i,partX,partY,partZ):
    if i%4 == 0:
        return functionNyks(partX,partY,partZ)
    elif i%4 == 1:
        return functionMiro(partX,partY,partZ)
    elif i%4 == 2:
        return functionRita(partX,partY,partZ)
    else:
        return functionFindik(partX,partY,partZ)

def bitwiseAddition(partX,partY):
    res = ""
    add = 0
    for i in range(len(partX)-1,-1,-1):
        flag = int(partX[i]) + int(partY[i]) + add
        if flag >= 2:
            add = 1
            res = res + str(flag % 2)
        else:
            add = 0
            res = res + str(flag)

    return ''.join(reversed(res))

def bitwiseRightShift(k,partX):
    k = int(k % (len(partX)/2))
    partXlist = []
    for i in range(len(partX)):
        partXlist.append(partX[i])
    for i in range(k):
        for j in range(len(partX)-1,0,-1):
            partXlist[j] = partXlist[j-1]
        partXlist[0] = 0
    newPart = ""
    for char in partXlist:
        newPart = newPart +  str(char)
    return newPart


def getK(i):
    K = [
        "00100111",
        "10010110",
        "01000110",
        "10101001",
        "00010011",
        "10100011",
        "01101011",
        "10100101"
    ]
    return K[i%8]

def loadM(partX,partY,partZ,partQ):
    M = [
        partX,
        partY,
        partZ,
        partQ
    ]
    return M

def bitControl(unCheck):
    if unCheck[0:8] == "00000000":
        return True
    else:
        return False

def getM(M,i):
    return M[i%4]

def hash(beforeHash):
    partA = beforeHash[0:8]
    partB = beforeHash[8:16]
    partC = beforeHash[16:24]
    partD = beforeHash[24:32]
    M = loadM(partA, partB, partC, partD)
    for i in range(16):
        partHash = bitwiseAddition(partB,
                                   bitwiseRightShift(i + 1,
                                                     bitwiseAddition(getK(i),
                                                                     bitwiseAddition(getM(M, i),
                                                                                     bitwiseAddition(partA,
                                                                                                     getFunction(i,
                                                                                                                 partB,
                                                                                                                 partC,
                                                                                                                 partD))))))

        partA = partD
        partD = partC
        partC = partB
        partB = partHash

    afterHash = partA + partB + partC + partD
    return afterHash

def final(filepath):
    f = open(filepath, "r")
    beforeHash = f.read(32)
    f.close()
    return hash(beforeHash)

def main():
    f = open("HASHSUM.txt", "w")
    f.write("BlokNo        RastgeleSayi             OncekiBlokOzeti")
    f.close()
    startTime = time.time()
    for i in range(99):
        if (time.time() - startTime > 600):
            print("Hata...Süre asimi")
            break
        filepathRead = "%.3d" % (i+1)
        hashed = final("%s.txt" % (filepathRead))
        flag = False
        while flag is not True:
            random = generateRandom32Bit()
            beforeHash = bitwiseAddition(random, hashed)
            afterHash = hash(beforeHash)
            flag = bitControl(afterHash)
        filepathWrite = "%.3d" % (i+2)
        f = open("%s.txt" % (filepathWrite), "w")
        f.write(afterHash)
        f.close()
        f = open("HASHSUM.txt", "a")
        hashSum = "\n%.3d %s %s" % (i+2,random,hashed)
        f.write(hashSum)
        f.close()

main()