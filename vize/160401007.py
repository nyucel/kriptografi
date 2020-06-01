#Gizem Ozgun
#Schmidt-Samoa



#!/usr/bin/python3
# -*- coding: utf-8 -*-
import math,sys
import cmath
from random import randint
import random

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

def lcm(x, y):
   if x > y:
       greater = x
   else:
       greater = y
   while(True):
       if((greater % x == 0) and (greater % y == 0)):
           lcm = greater
           break
       greater += 1
   return lcm

def bit_length(n):
    bits = 0
    while n >> bits: bits += 1
    return bits

def binary_to_decimal(binary):

    binary=str(binary)[::-1]
    decimal,index = 0,0
    for i in binary:
        decimal+=pow(2,index)*int(i)
        index+=1
    return decimal

def binary_to_string(binary):

    string= ''

    for i in range(0, len(binary), 8):

        tmp = int(binary[i:i + 8])
        decimal = binary_to_decimal(tmp)
        string += chr(decimal)

    return string


def asal_olustur(n):
    #Schmidt-Samoa algoritmasgida public key = (p**2)=*q oldugu icin p-> n/4 bit, q-> n/2 
    #bit olmalı. 32 bit uzunlugunda bir anahtar icin p=8bit q=16bit olmalidir.
    #anahtar boyutu icin n bazi durumlarda ornegin 8 girildiginde bu bit degeri tutmayabiliyor
    #noktali sayi elde edilebiliyor.
    asal = []
    if_first, if_second = 0, 0
    p_min = pow(2, (n // 4) - 1)
    p_max = sum([pow(2, i) for i in range(n // 4)])
    q_min = pow(2, (n // 2) - 1)
    q_max = sum([pow(2, i) for i in range(n // 2)])
    while True:

            p_prime = randint(p_min,p_max)
            q_prime = randint(q_min,q_max)
            if isprime(p_prime)==1 and if_first==0:
                primes.append(p_prime)
                if_first=1
            if isprime(q_prime)==1 and if_second==0:
                primes.append(q_prime)
                if_second=1


            if (len(asal)==2):
                print("istenilen asallar elde edildi.")
                break
    if bit_length(asal[0])!=n//4:
         asal.reverse()

    return asal


def keygen(n):

    p=asal_olustur(n)
    q=asal_olustur(n)

    public_key = pow(p,2) * q
    private_key = (public_key ** -1 ) %  lcm((p-1),(q-1))
    print private_key
    print public_key

    with open ("publickey.txt", 'w') as public:
        public.write(str(public_key))
    with open("privatekey.txt",'w') as private:
        private.write(str(private_key))
        private.write("\n"+str(q)
        private.write("\n"+str(p)


def encrypt(plaintext, publickey.txt):

    public=open(publickey,"r")
    public_key=int(public.read())
    plaintext= open(plaintext,"r").read()
    plaintext_binary = functions.string_to_binary(plaintext)
    plaintext_decimal = functions.binary_to_decimal(plaintext_binary)
    encryted=pow("plaintext.txt",public_key,public_key)
    encrypted_text = str(pow(int(plaintext),public_key,public_key))
    with open("chiper.txt",'w') as chiper:
        chiper.write(str(encrypted_txt))


def decrypt(chipertext, privatekey):
   
    with open(private_key, "r") as privatekey:
        private_keys=private.readlines()
        d, pq = float(private_keys[0]), int(private_keys[1])
           ciphertext = open(ciphertext, "r").read()
    print("CIPHER:",int(ciphertext))
    print("D:",d)
    decrypt_text = str(pow(int(ciphertext),d) % pq)
    print("DES:",decrypt_text)

    with open("plaintext2.txt", "w") as plain:
        plain.write(str(decrypt_text))


n =int(input("anahtar boyutu icin bit giriniz:"))
keygen(n)
encrypt("plaintext.txt","publickey.txt")
decrypt("ciphertext.txt","privatekey.txt")

