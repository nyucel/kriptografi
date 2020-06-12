#!/usr/bin/python3
# -*- coding: utf-8 -*-

#Fahrettin Orkun Incili - 150401013 - Schmidt-Samoa

from random import randint
import math, os

"""
Ek fonksiyonlar:
isprime
lcm 
bit_length
string_to_binary
binary_to_decimal
binary_to_string
generate_prime
issame
"""


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

def lcm(x,y):
    """en küçük ortak katı bulan fonksiyon"""
    if x > y:
        greater = x
    else:
        greater = y

    while True:
        if ((greater % x == 0) and (greater % y == 0)):
            lcm = greater
            break
        greater += 1

    return lcm
def decimal_to_binary(decimal):
    """decimal değeri binary değere çeviren fonksiyon"""
    string=""
    binary=string.join(bin(decimal).split("b"))

    return binary

def bit_length(n):
    """negatif olmayan bir tamsayının bit boyutunu döndürür
       https://stackoverflow.com/questions/2654149/bit-length-of-a-positive-integer-in-python"""
    bits = 0
    while n >> bits: bits += 1
    return bits


def string_to_binary(string):
    """string'i binary'e çevirip bu değeri döndüren fonksiyon"""
    binary = ""
    for i in string:
        binary += "".join(f"{ord(i):08b}")
    return binary

def binary_to_decimal(binary):
    """binary'i decimal'e çeviren fonksiyon"""
    binary=str(binary)[::-1]
    decimal,index = 0,0
    for i in binary:
        decimal+=pow(2,index)*int(i)
        index+=1
    return decimal

def binary_to_string(binary):
    """binary'i string'e çevirip bu değeri döndüren fonksiyon"""
    string= ''

    for i in range(0, len(binary), 8):

        tmp = int(binary[i:i + 8])
        decimal = binary_to_decimal(tmp)
        string += chr(decimal)


    return string

def generate_prime(n):
    """
        Üretilecek anahtarın istenilen bit uzunluğunda olabilmesi için rastgele,
    seçilen asal sayıların bit değerlerini belli bir uzunlukta tutmalıyız.
    Bu algoritmada açık_anahtar = (p^2)*q olduğundan p'yi n/4 bit, q'yu ise n/2 bit almalıyız.
    32 bit uzunluğunda anahtar için p 8 bit, q ise 16 bit olmalı
    """
    primes = []
    if_first, if_second = 0, 0

    #Formüldeki p asal sayısının olması gereken bit uzunluğunda alabileceği min değer(8bit için 1000 0000)
    first_prime_min = pow(2, (n // 4) - 1)
    first_prime_max = sum([pow(2, i) for i in range(n // 4)])#max değer(8bit için 1111 1111)

    #Formüldeki q asal sayısının olması gereken bit uzunluğunda alabileceği min değer(8bit için 1000 0000 )
    second_prime_min = pow(2, (n // 2) - 1)
    second_prime_max = sum([pow(2, i) for i in range(n // 2)])#max değer(8bit için 1111 1111)

    while True:
            """Istenilen bit uzunluğuna uygun rastgele tamsayılar üretilir. Anahtarın 32 bit istenmesi durumunda
            first prime 8 bit, second prime 16 bit uzunluğunda olacak"""
            first_prime = randint(first_prime_min,first_prime_max)
            second_prime = randint(second_prime_min,second_prime_max)

            """seçilen iki asalın biri n/4 diğeri ise n/2 bit olmalıydı.
            first_prime'ın(p) ya da second_prime'ın(q) üst üste seçilmemesi için
            if_first ve if_second kontrolleri kullandım.Bu şekilde aynı bit değerine
            ikinci asal listeye eklenmiyor."""
            if isprime(first_prime)==1 and if_first==0:
                primes.append(first_prime)
                if_first=1
            if isprime(second_prime)==1 and if_second==0:
                primes.append(second_prime)
                if_second=1


            if (len(primes)==2):

                break
    if bit_length(primes[0])!=n//4:
        """keygen fonksiyonunda p değişkenine n/4,q değişkenine n/2 bitlik asal atanacak
        formül ile uyumlu olması için((p^2)*q) primes[0]=p,primes[1]=q olacak şekilde listeyi düzenliyorum."""
        primes.reverse()

    return primes
def issame(plaintext,plaintext2):

    with open(plaintext, "r") as file:
        text1=file.read()
    with open(plaintext2,"r") as file:
        text2=file.read()

    if text1==text2:
        print("Dosyaların içerikleri aynı.")
    else:
        print("Dosyaların içerikleri aynı değil.")




#-----------------------------------------------------------------------------------


def keygen(n):

    p,q = generate_prime(n)#rastgele 2 asal seçimi
    lcm_primes = lcm((p - 1), (q - 1))

    public_key = (p ** 2) * q
    private_key = public_key%lcm_primes


    with open("publickey.txt",'w') as publickey_file:
        publickey_file.write(str(public_key))

    with open("privatekey.txt",'w') as privatekey_file:
        privatekey_file.write(str(private_key))
        privatekey_file.write("\n"+str(p*q))


def encrypt(plaintext, publickey):
    if not os.path.exists("./publickey.txt"):
        print("Public key tanımlanmamış.Lütfen önce 'keygen' fonksiyonunu cağırın.")
        exit()

    publickey_file= open(publickey,"r")
    public_key = int(publickey_file.read())

    plaintext= open(plaintext,"r").read()

    plaintext_binary = string_to_binary(plaintext)
    plaintext_decimal = binary_to_decimal(plaintext_binary)



    encrypted_text = pow(plaintext_decimal,public_key,public_key)


    with open("ciphertext.txt", 'w') as cipher:
       cipher.write(str(encrypted_text))


def decrypt(ciphertext, privatekey):
    if not os.path.exists("./privatekey.txt"):
        print("Private key tanımlanmamış.Lütfen önce 'keygen' fonksiyonunu cağırın.")
        exit()

    with open(privatekey, "r") as privatekey_file:
        private_keys=privatekey_file.readlines()
        d, pq = int(private_keys[0]), int(private_keys[1])



    ciphertext = open(ciphertext, "r").read()

    decrypt_text = pow(int(ciphertext),d,pq)
    decrypt_text_binary=decimal_to_binary(decrypt_text)
    decrypt_text_string=binary_to_string(decrypt_text_binary)



    with open("plaintext2.txt", "w") as plain:
        plain.write(str(decrypt_text_string))




n =int(input("bit uzunluğunu giriniz:"))
keygen(n)
encrypt("plaintext.txt","publickey.txt")
decrypt("ciphertext.txt","privatekey.txt")
issame("plaintext.txt","plaintext2.txt")
