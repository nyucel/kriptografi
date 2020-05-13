#Selin KURT 160401014
#Merkle-Hellman Kriptosistemi utf-8

import random
import os

def keygen(n):
    
    f = open("plaintext.txt", "r")
    text = f.read()
    f.close()
    if n != (len(text)-1)*8:
        print("Girdiginiz anahtar boyutu ile plaintext'iniz sifrelenemez.Girilen anahtar boyutu (plaintext*8) olmalidir.")
        exit()

    w = [2]
    toplam = 2
    for i in range(n-1):
        w.append(random.randint(toplam+1, toplam+10))
        toplam = toplam + w[i+1]
    
    q = random.randint(toplam+1, toplam+100)
    
    #r sayisi belirlerken q ile aralarinda asallik kontrolu yapmamak icin diziye ekledigim bazi asal sayilar arasindan sececegim
    asalsayilar = [101, 107, 113, 127, 131, 137, 139, 149, 151]
    r = random.choice(asalsayilar)
    
    B = []
    for j in range(n):
        B.append((w[j]*r)%q)
    
#   print("gizli anahtar:", w, q, r)
#   print("acik anahtar:",B)
    
    dosya = open('publickey.txt','w')    
    for k in B:
        dosya.write("%d," %k)
    dosya.close()

    dosya = open('privatekey.txt','w')
    for i in w:
        dosya.write("%d,"%i)
    dosya.write("\n")
    dosya.write(str(q))
    dosya.write("\n")
    dosya.write(str(r))
    dosya.close()

def stringToBinary(string):
  
    binary = ""
    for i in string:
        binary += "".join(f"{ord(i):08b}")
    return binary

def encrypt(plaintext, publickey):

    if os.path.exists("./publickey.txt")==False:
        print("Once keygen() fonksiyonunu calistiriniz.!!!")
        exit()
    
    f = open(plaintext, "r")
    f1 = open(publickey, "r")
    
    plainText = stringToBinary(f.read())
    acikAnahtar = f1.read().split(',') 
    c = 0
    
    for i in range(len(acikAnahtar)-1):
        c = c + int(plainText[i])*int(acikAnahtar[i])
    
    f2 = open("ciphertext.txt","w")
    f2.write(str(c))
    f2.close()

#bu iki fonksiyon moduler ters almak icindir
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('moduler ters bulunamadi')
    else:
        return x % m

def binaryToString(binary):

    dizi = []
    string = ""
    for i in range(0, len(binary), 8):
        dizi.append(binary[i:i+8])
    for j in dizi:
        string += chr(int(j, 2))
    return string

def decyrpt(ciphertext,privatekey):

    if os.path.exists("./privatekey.txt")==False:
        print("Once keygen() fonksiyonunu calistiriniz.!!!")
        exit()

    f = open(ciphertext, "r")
    f1 = open(privatekey, "r")

    c = f.read()
    pr = f1.read().split('\n')
    
    w = pr[0].split(',')
    q = pr[1]
    r = pr[2]

    modulerters = modinv(int(r), int(q))
    c2 = (int(c)*modulerters)%int(q)
    metin = []
    for i in range(len(w)-1):
        if int(w[len(w)-i-2])<= c2:
            metin.append(1)
            c2 = c2-int(w[len(w)-i-2])
        else:
            metin.append(0)
    
    yenimetin = metin[::-1]
    st = ""
    
    for i in yenimetin:
        st += str(i)

    sonuc = binaryToString(st)

    plaintext2 = open("plaintext2.txt", "w")
    plaintext2.write(sonuc)
    plaintext2.close() 
     
    plaintext2 = open("plaintext2.txt", "r")
    plaintext = open("plaintext.txt", "r")
    
    x = plaintext2.read()
    y = plaintext.read()
    y = y[:(len(y)-1)] 
    if x==y:
        print("Dosyalar ozdestir.")
    else:
        print("Dosyalar ozdes degildir.")
      
keygen(40)
encrypt("plaintext.txt", "publickey.txt")
decyrpt("ciphertext.txt","privatekey.txt")
