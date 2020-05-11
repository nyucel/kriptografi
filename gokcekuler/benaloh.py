#Gökçe Kuler
import random
import math
import os
import hashlib

def isprime(a):

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
def rabinMiller(n):
  s = n - 1
  t = 0
  while(s % 2 == 0):
    s = s // 2
    t += 1
  for trials in range(5):
    a = random.randrange(2, n - 1)
    v = pow(a, s, n)
    if(v != 1):
      i = 0
      while v != (n - 1):
        if(i == t - 1):
          return False
        else:
          i = i + 1
          v = (v ** 2) % n
  return True
def keygen(n):
     while True: 
        p = random.randrange(2 ** (n - 1), 2 ** n)
        if(isprime(p)):
            break
     while True:
        q = random.randrange(2 ** (n - 1), 2 ** n)
        if(isprime(q)):
            if(q == p):
                continue
        break
     fi=(p-1) *(q-1)
     r=p*q
     y=random.randint(1,r)
     x=(y ** (fi//n)) % r

     with open("publickey.txt", 'w+') as publickey:
         publickey.writelines(str(y) + '\n')
         publickey.writelines(str(r) + '\n')
     publickey.close()

     with open("privatekey.txt",'w+') as privatekey:
        privatekey.writelines(str(fi) + '\n')
        privatekey.writelines(str(x) + '\n')
     privatekey.close()
def encrypting(plaintext,publickey): 
    dosyakontrolplaintext= os.path.isfile("./plaintext")
    if(dosyakontrolplaintext== False):
        print("Şifrelenecek plaintext dosyası yok. Lütfen önce plaintext dosyasını oluşturun")
        exit
    else:
        dosyakontrolpublickey= os.path.isfile("./publickey.txt")
        if(dosyakontrolpublickey== False):
            print("lütfen önce keygen fonksiyonunu çalıştırın")
            exit
        else:
            with open("plaintext",'r') as plaintext:
                plaintexticerik=int(plaintext.read())
            plaintext.close()
            publickeydosya=open("publickey.txt",'r+')
            y=int(publickeydosya.readline())
            r=int(publickeydosya.readline())
            publickeydosya.close()


            u=random.randint(-r,r)     
            chippertexticerik= ((y ** (plaintexticerik)) * (u ** r) ) % r 
            with open("chippertext",'w+') as chippertext:
                chippertext.writelines(str(chippertexticerik))
            chippertext.close() 

def decrypt(chipertext, privatekey):
        dosyakontrolpublickey= os.path.isfile("./privatekey.txt")
        if(dosyakontrolpublickey== False):
            print("lütfen önce keygen fonksiyonunu çalıştırın")
            exit

        else:
            with open("chippertext", 'r+') as chippertext:
                chippertexticerik=int(chippertext.read())
            chippertext.close()
            privatekey=open("privatekey.txt",'r+')
            fi=int(privatekey.readline())
            x=int(privatekey.readline())
            privatekey.close()
                        
            with open("plaintext",'r+') as plaintext:
                plaintexticerik=int(plaintext.read())
            plaintext.close()

            publickeydosya=open("publickey.txt",'r+')
            r=int(publickeydosya.readline())
            a=(x**plaintexticerik) %r
            
            with open("plaintext2",'w+') as plaintext2:
                plaintext2.writelines(str(a))
            plaintext2.close()
            with open("plaintext2",'r+') as plaintext2:
                plaintext2icerik=int(plaintext2.read())
            plaintext2.close()



            hash_obj1=hashlib.md5(str(plaintexticerik).encode())
            print(hash_obj1)

            hash_obj2=hashlib.md5(str(plaintext2icerik).encode())
            print(hash_obj2)

            if(hash_obj1==hash_obj2):
                print("Dosyalar özdeştir")
            else:
                print("Dosyalar özdeş değildir")

            
n=int(input("Anahtar boyutunu giriniz:"))
keygen(n)
encrypting("plaintext","publickey.txt")
decrypt("chippertext","privatekey.txt")




















