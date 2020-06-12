#170401011 Berfin Okuducu
import math
import random
import sys
import time
def string_to_binary(m):
    return ("".join(f"{ord(i):08b}" for i in m))
def leftrotate(x,t=1):
    if len(x)<2:
        return
    if t==0:
        return x
    return leftrotate(x[1:]+x[0],t-1)
def addx(list):
    ret=0
    for l in list:
        ret=ret+int(l,2)
    return bin(ret)[2:]
def andb(a,b):
    x=""
    for i in range(0,len(a)):
        if(a[i]==1 and b[i]==1):
            x+="1"
        else:
            x+="0"
    return x
def orb(a,b):
    x=""
    for i in range(0,len(a)):
        if(a[i]==0 and b[i]==0):
            x+="0"
        else:
            x+="1"
    return x
def notb(a):
    x=""
    for i in a:
        if(i==1):
            x+="0"
        else:
            x+="1"
    return x
def xor(x, y):
    return '{0:b}'.format(int(x, 2) ^ int(y, 2))


def chunks(messageLength, chunkSize):
    chunkValues = []
    for i in range(0, len(messageLength), chunkSize):
        chunkValues.append(messageLength[i:i + chunkSize])

    return chunkValues
def final(dosya):
    k=[]
    for i in range(0,64):
        a=math.floor((2**32)*abs(math.sin(i+1)))
        a='{0:08b}'.format(a)
        k.append(a)

    f=open(dosya,"r")
    x=f.read()
    a0 = "00000001"
    b0 = "10001001"
    c0 = "11111110"
    d0 = "01110110"
    bitarray=string_to_binary(x)
    temp=bitarray
    bitarray+="1"
    while (len(bitarray) % 128 != 112):
        bitarray += '0'
    bitarray+='{0:016b}'.format(len(temp))
    chunk = chunks(bitarray, 128)
    for eachChunk in chunk:
        words = chunks(eachChunk, 8)
        A=a0
        B=b0
        C=c0
        D=d0
        for i in range(0,64):
            if(0<=i<=15):
                s1=[7, 12, 17, 22]
                F=orb((andb(B,C)),(andb((notb(B)),D)))
                g=i
                z=i%4
                rotate=s1[z]
            elif(16<=i<= 31):
                s2=[5, 9, 14, 20]
                F=orb((andb(D,B)),(andb(C,(notb(D)))))
                g=(5*i+1)%16
                z = i % 4
                rotate = s2[z]
            elif(32<=i<=47):
                s3=[ 4, 11, 16, 23]
                F=xor(xor(C,D),B)
                g=(3*i+5)%16
                z = i % 4
                rotate = s3[z]
            else:
                s4= [6, 10, 15, 21]
                F=xor(orb(B,(notb(D))),C)
                g=(7*i)%16
                z = i % 4
                rotate = s4[z]
            dtemp=D
            D=C
            C=B
            B=addx([B,leftrotate((addx([A,F,k[i],words[g]])),rotate)])
            A=dtemp
        a0 = a0 + A
        a0 = a0[len(a0) - 8:]
        b0 = b0 + B
        b0 = b0[len(b0) - 8:]
        c0 = c0 + C
        c0 = c0[len(c0) - 8:]
        d0 = d0 + D
        d0 = d0[len(d0) - 8:]
    ozet = a0 + b0 + c0 + d0
    return ozet

def isim(i):
    if (i < 10):
        dosya = "00" + str(i) + ".txt"
    elif (10 <= i < 100):
        dosya = "0" + str(i) + ".txt"
    else:
        dosya = "100.txt"
    return dosya
def blokzincir(dosya):
    h=open("HASHSUM",'w')
    son = time.time() + 600
    for i in range(2,101):
        if(time.time()>son):
            print("10 dakika doldu.")
            sys.exit()
        else:
            dosya=isim(i)
            onceki=isim(i-1)
            oncekiozet=final(onceki)
            while True:
                f = open(dosya, 'w+')
                r=random.getrandbits(32)
                x=bin(r)[2:]
                toplam=addx([x,oncekiozet])
                f.write(toplam)
                f.close()
                ozet= final(dosya)
                if "1" in ozet[:8]:
                    continue
                else:
                    yaz = "Dosya:" + dosya + " Random:" + (32 - len(x)) * "0" + str(r) + " Ozet:" + ozet + "\n"
                    h.writelines(yaz)
                    break
    h.close()


blokzincir("001.txt")
