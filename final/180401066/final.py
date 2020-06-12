import base64
import random
from time import time

def strtobin(text):
    text=str(text)   
    ret='/'.join(map(bin,bytearray(text.encode()))).split("/")
    retf=[]
    for i in ret:
        i=i[2:]
        while len(i)<8:
            i="0"+i
        retf.append(i)
    return retf

def bintoint(x):
    return int(x,2)

def inttobin(x):
    return bin(x)[2:]

def xor(a,b):
    ret=""
    for i in range(0,len(a)):
        if a[i]==b[i]:
            ret=ret+"0"
        else:
            ret=ret+"1"
    return ret

def andl(a,b):
    ret=""
    for i in range(0,len(a)):
        if a[i]==b[i] and a[i]=="1":
            ret=ret+"1"
        else:
            ret=ret+"0"
    return ret

def orl(a,b):
    ret=""
    for i in range(0,len(a)):
        if a[i]==b[i] and a[i]=="0":
            ret=ret+"0"
        else:
            ret=ret+"1"
    return ret

def notl(a):
    ret=""
    for e in a:
        if e=="1":
            ret=ret+"0"
        else:
            ret=ret+"1"
    return ret

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

def final(dosya):
    try:
        f=open(dosya,"rb")
        data=base64.b64encode(f.read())
    except:
        print("Dosya bulunamadi.")
        return
    f.close()
    liste=strtobin(data)

    lenl=sum([len(e) for e in liste])
    h0="01100111"
    h1="11101111"
    h2="10011000"
    h3="00010000"
    n1=128
    data=""
    for l in liste:
        data=data+l
    data=data+"1"

    while len(data)+16>n1:
        n1=n1*2
    n2=n1-16

    data=data+"0"*(n2-len(data))

    add=inttobin(lenl)
    if len(add)>16:
        add=add[len(add)-16:]
    add=(16-len(add))*"0"+add

    data=data+add
    n=512
    datac=[data[i:i+n] for i in range(0, len(data), n)]
    n=8
    for data in datac:
        datachunk=[data[i:i+n] for i in range(0,len(data),n)]

        for i in range(16,80):
            a0,a1,a2,a3=datachunk[i-3],datachunk[i-8],datachunk[i-14],datachunk[i-16]
            d=xor(xor(xor(a0,a1),a2),a3)
            d=leftrotate(d)
            datachunk.append(d)

        A,B,C,D=h0,h1,h2,h3

        for i in range(0,80):
            if i in range(0,20):
                F=orl(andl(B,C),andl(notl(B),D))
                k="01011010100000100111100110011001"
            elif i in range(20,40):
                F=xor(xor(B,C),D)
                k="01101110110110011110101110100001"
            elif i in range(40,60):
                F=orl(orl(andl(B,C),andl(B,D)),andl(C,D))
                k="10001111000110111011110011011100"
            elif i in range(60,80):
                F=xor(xor(B,C),D)
                k="11001010011000101100000111010110"

            temp=addx([leftrotate(A,5),F,D,k,datachunk[i]])
            temp=temp[len(temp)-8:]
            D=C
            C=leftrotate(B,30)
            B=A
            A=temp

        h0=h0+A
        h0=h0[len(h0)-8:]
        h1=h1+B
        h1=h1[len(h1)-8:]
        h2=h2+C
        h2=h2[len(h2)-8:]
        h3=h3+D
        h3=h3[len(h3)-8:]

    return h0+h1+h2+h3

def kontrol():
    for i in range(2,101):
        dosya=name(i)
        ozet=final(dosya)
        if "1" in ozet[:8]:
            continue
        else:
            print(dosya,"hatali")
            return
    print("Tum ozetler dogru")
    return

def name(i):
    if i<10:
        dosya="00"+str(i)+".txt"
    elif i<100:
        dosya="0"+str(i)+".txt"
    else:
        dosya=str(i)+".txt"
    return dosya

def blockc(dosya):
    h=open("HASHSUM","w")
    son=time()+600
    for i in range(2,101):
        if time()>son:
            print("10 dakika doldu.")
            break
        dosya=name(i)
        onceki=name(i-1)
        ozet=final(onceki)
        while True:
            f=open(dosya,"w")
            r=random.getrandbits(32)
            r=inttobin(r)
            x=addx([r,ozet])
            f.write(x)
            f.close()
            ozet2=final(dosya)
            if "1" in ozet2[:8]:
                continue
            else:
                yaz="Dosya:"+dosya+" Random:"+(32-len(r))*"0"+str(r)+" Ozet:"+ozet2+"\n"
                h.writelines(yaz)
                break
    
    h.close()
    return

blockc("001.txt")