#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
import math


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

def allprimes(n):
    """bir sayıdan küçük bütün asal sayıları dizi olarak döndüren fonksiyon"""
    primes=[]
    for i in range(2,n+1):
        primes.append(i)
    for x in range(0,int(n/2)+1):
        if(primes[x]!=0):
            for i in range(x+primes[x],n-1,primes[x]):
                primes[i]=0
    primes.sort()
    return(primes[primes.count(0):])


def is_prime(n, k):
    """bir sayının (kesin olmamakla birlikte) asal olup olmadığını kontrol eden fonksiyon (Miller-Rabin)"""
    if n == 2 or n == 3:
        return True 
    if n <= 1 or n % 2 == 0:
        return False

    d = n - 1; 
    while (d % 2 == 0): 
        d //= 2; 

    for i in range(k): 
        if (not miller_test(d, n)): 
            return False;  
    
    return True


def miller_test(d, n):
    a = random.randrange(2, (n-2))
    x = pow(a, d, n)
    if x == 1 or x == (n - 1): return True
    
    i = d 
    while i != n - 1:
        x = pow(x, 2, n)
        i *=2
        if (x == 1): return False
        if (x == n - 1): return True
    return False

def generate_random_prime_numbers(bit):
    """ Verilen bit uzunluğuna göre bir asal sayı oluşturur"""
    while True:
        number = random.getrandbits(int(bit))
        if(is_prime(number,bit)):
            return number

def legendre_symbol(x, p):
    """ a, p sayılarının legendre symbol değerlerini döndürür"""
    ls = pow(x, (p - 1) // 2, p)
    if(ls == 1): return 1
    elif (ls == 0): return 0
    else: return -1


def quadratic_non_residue(p, q):
    """ p ve q sayıları için legendre sembolü -1 olan ortak bir sayı döndürür"""
    x = 0
    while ((legendre_symbol(x, p) != -1) and (legendre_symbol(x, q) != -1)):
        x = random.randint(1, p)

    return x


def string_to_bits(text):
    """ Verilen stringi bitlere çevirir"""
    return ''.join(format(ord(i), 'b').zfill(9) for i in text)



def bits_to_string(bits):
    """ Verilen bitleri stringe çevirir"""
    string = ""
    for i in range(0, len(bits), 9):
        string += chr(int(bits[i:i+9],2))
    return string


