#Reber Ferhat Uluca - 170401053

import random
import math
import filecmp

def EEA(a, b): #Extended euclidean algorithm
  
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  b, y0, x0

def lcm(x, y): #Least common multiple
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

def miller_rabin_primality_test(p, s=5):
    if p == 2: # 2 is the only prime that is even
        return True
    if not (p & 1): # n is a even number and can't be prime
        return False

    p1 = p - 1
    u = 0
    r = p1

    while r % 2 == 0:
        r >>= 1
        u += 1

    def witness(a):
        """
        Returns: True, if there is a witness that p is not prime.
                False, when p might be prime
        """
        z = pow(a, r, p)
        if z == 1:
            return False

        for i in range(u):
            z = pow(a, 2**i * r, p)
            if z == p1:
                return False
        return True

    for i in range(s):
        a = random.randrange(2, p-2)
        if witness(a):
            return False

    return True

def generate_primes(n):

    #2**(n-1) is smallest number that is n bit length, 2**n-1 is largest number that is n bit length
    x = random.randrange(2**(n-1), 2**n - 1)

    while not miller_rabin_primality_test(x):
        x = random.randrange(2**(n - 1), 2**n - 1)

    return x

def keygen(b):
    if b%2 != 0:
        print("bit lenght must be even")
        return

    b = b // 2

    if b<=4:
        print("bit lenght must be larger than 8")
        return

    while True:
        p = generate_primes(b)
        q = generate_primes(b)
        n = p * q
        if (len(bin(n))-2) == b*2:
            break

    totient = (p - 1)*(q - 1)
    
    while True:
        e = random.randrange(1, totient)
        if math.gcd(e, totient) == 1:

            gcd, s, t = EEA(totient, e)
            d = t % totient

            if len(bin(d).lstrip("0b")) != b*2:
                continue
            break

    privatekey = open("privatekey.txt", "w")
    privatekey.write(str(n) + '\n')
    privatekey.write(str(d) + '\n')
    privatekey.close()

    publickey = open("publickey.txt", "w")
    publickey.write(str(n) + '\n')
    publickey.write(str(e) + '\n')
    publickey.close()

def encrypt(plaintext, publickey):
    try:
        pk = open(publickey, "r")
    except:
        print("you must run the keygen function first!")
        return
    try:
        pt = open(plaintext, "r")
    except:
        print("plaintext file doesn't exist!")
        return

    n = int(pk.readline())
    e = int(pk.readline())
    pk.close()

    message = pt.read()
    pt.close()

    cipher = ""
    for c in message:
        m = ord(c)
        cipher += str(pow(m, e, n)) + ":"

    f = open("ciphertext", "w")
    f.writelines(cipher)
    f.close()

def decrypt(ciphertext, privatekey):
    try:
        pk = open(privatekey, "r")
    except:
        print("you must run the keygen function first!")
        return
    try:
        ct = open(ciphertext, "r")
    except:
        print("ciphertext file doesn't exist!")
        return

    n = int(pk.readline())
    d = int(pk.readline())
    pk.close()

    cipher = ct.read()
    ct.close()

    message = ""
    parts = cipher.split(":")
    for part in parts:
        if part:
            c = int(part)
            message += chr(pow(c, d, n))

    f = open("plaintext2", "w")
    f.writelines(message)
    f.close()

    if not filecmp.cmp("plaintext", "plaintext2"):
        print("plaintext and plaintext2 files are not identical")
    else:
        print("plaintext and plaintext2 files are identical")
