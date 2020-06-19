"""
    Sena Günay-160401019
    Berfin Okuducu-170401011
    Sevda Avcılar-170401054
"""

import random
def isprime(a):
    """bir sayının asal olup olmadığını kontrol eden fonksiyon"""
    i=3
    if(a<2):
        return(0)
    if a!=2 and a%2==0:
        return(0)
    while i<=a**(1/2):
        if a%i==0:
            return(0)
        i += 2
    return(1)
def legendre_test(x,p):
    s=pow(x,((p-1)//2),p)
    if(s==1):
        return 1
    elif(s==0):
        return 0
    else:
        return -1
def legendre(p,q):
    a=random.randint(0,1000000)
    while(legendre_test(a,p)!=-1 and legendre_test(a,q)!=-1):
        a=random.randint(0,1000000)
    return a

def keygen(a):
    enkucuk=2**(a-1)
    m,enbuyuk=0,0
    while(m<a):
        enbuyuk=enbuyuk+2**(m)
        m=m+1
    p,q=4,4
    while(isprime(p)!=1 ):
        p=int(random.randint(enkucuk,enbuyuk))

    while(isprime(q)!=1):
        q = int(random.randint(enkucuk, enbuyuk))
    n=p*q
    x=legendre(p,q)
    publick=[x,n]
    privatek=[p,q]
    with open("publickey.txt","w") as k:
        for line in publick:
            k.write('%d' % line)
            k.write('\n')
    with open("privatekey.txt", "w") as k:
        for line in privatek:
            k.write('%d' % line)
            k.write('\n')

def ebob(a, b):
    if (b == 0):
        return a
    else:
        return ebob(b, a % b)

def string_to_binary(m):
    return (" ".join(f"{ord(i):08b}" for i in m))
def encrypt(plaintext,publickey):
    try:
        f=open(publickey,"r")
        x=f.readlines()
        a,n=int(x[0]),int(x[1])
        f.close()
        plain=open(plaintext,"r")
        metin=plain.read()
        binary_pt=string_to_binary(metin)
        binary=binary_pt.replace(" ","")
        chiper=open("chipertext.txt","w")
        for i in range(0,len(binary)):
            y=random.randint(0,10000000)
            while((ebob(y,n))!=1):
                y = random.randint(0, 10000000)
            m=int(binary[i])
            s=((y**2)*(a**m))%n
            chiper.write('%d \n' %s)
        chiper.close()
    except(FileNotFoundError):
        print("Anahtar çifti oluşturulmadan şifreleme işlemi yapılamaz.Önce keygen()fonksiyonunu çalıştırın.")

def BinaryToDecimal(binary):
    string = int(binary, 2)
    return string


def decrypt(ciphertext,privatekey):
    try:
        cipher=open(ciphertext,"r")
        c=cipher.readlines()
        cipher.close()

        private=open(privatekey,"r")
        y=private.readlines()
        p,q=int(y[0]),int(y[1])
        private.close()
        m=[]
        for i in range(0,(len(c))):
            x=legendre_test(int(c[i]),p)
            if(x==1):
                m.append(0)
            else:
                m.append(1)
        bin_data="".join(str(i)for i in m)
        str_data = ''
        for i in range(0, len(bin_data), 8):
            temp_data = bin_data[i:i + 8]
            decimal_data = BinaryToDecimal(temp_data)
            str_data = str_data + chr(decimal_data)
        plaintext2 = open("plaintext2.txt", "w")
        plaintext2.write(str_data)
        plaintext2.close()
        file1 = open('plaintext2.txt', 'r')
        lines1=file1.readlines()
        file2 = open('plaintext.txt', 'r')
        lines2=file2.readlines()
        if (lines1== lines2):
            print("plaintext ve plaintext2 dosyaları özdeştir.")
        else:
            print("plaintext ve plaintext2 dosyaları özdeş değildir.")
    except(FileNotFoundError):
        print("Anahtar çifti oluşturulmadan şifreleme işlemi yapılamaz.Önce keygen()fonksiyonunu çalıştırın.")



metin=input("Lütfen şifrelemek istediğiniz metni giriniz:")
plaintext = open("plaintext.txt", "w")
plaintext.write(metin)
plaintext.close()

keygen(32)
encrypt("plaintext.txt","publickey.txt")
decrypt("chipertext.txt","privatekey.txt")