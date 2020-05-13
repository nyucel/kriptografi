#Batuhan Bağçeci - 160401047

from random import getrandbits, randint, randrange
from math import gcd
from base64 import b64encode, b64decode
from os import path
from filecmp import cmp

def MillerRabin(number, testCount=128):
    r = number - 1
    j = 0

    while r % 2 == 0:
        r = r // 2
        j = j + 1

    for i in range(testCount):
        while True:
            randomNumber = randint(2, number)-1
            if randomNumber != 0 and randomNumber != 1:
                break

        rndpow = pow(randomNumber, r, number)
        if (rndpow != 1) and (rndpow != number - 1):
            count = 1
            while (count <= j - 1) and (rndpow != number - 1):
                rndpow = pow(rndpow, 2, number)
                count = count + 1

            if (rndpow != (number - 1)):
                return False

    return True

def inverse(x, m):
    a, b, u = 0, m, 1
    while x > 0:
        q = b // x
        x, a, b, u = b % x, u, x, a - q * u

    if b == 1:
        return a % m

def base64Encode(text):
    text = text.encode('ascii')
    text = b64encode(text)
    text = text.decode('ascii')
    return text

def base64Decode(text):
    text = text.encode('ascii')
    text = b64decode(text)
    text = text.decode('ascii')
    return text

def generatePrime(bits):
    prime = getrandbits(bits)
    prime = prime | (1 << bits - 1) | 1
    while not MillerRabin(prime):
        prime = prime + 2

    return prime

def keygen(n):
    p = generatePrime(int(n/2))
    q = generatePrime(int(n/2))
    while p == q:
        q = generatePrime(int(n/2))

    modulus = p * q

    totient = (p - 1) * (q - 1) // gcd(p - 1, q - 1)

    e = randrange(1, totient)
    while gcd(e, totient) != 1:
        e = randrange(1, totient)

    d = inverse(e, totient)

    public = (modulus, e)
    private = (d, p, q, totient)

    pubkeyfile = open('publickey.txt', 'w')
    for row in public:
        key = base64Encode(str(row))
        pubkeyfile.write(key + '\n')
    pubkeyfile.close()

    prikeyfile = open('privatekey.txt', 'w')
    for row in private:
        key = base64Encode(str(row))
        prikeyfile.write(key + '\n')
    prikeyfile.close()

def encrypt(plaintext, publickey):
    if (path.exists('publickey.txt') and path.exists('privatekey.txt')):
        pubkeyfile = open(publickey, 'r')
        public = pubkeyfile.readlines()
        pubkeyfile.close()

        for row in range (2):
            public[row] = base64Decode(public[row])

        modulus, e = public
        modulus, e = int(modulus), int(e)

        plainfile = open(plaintext, 'r')
        plain = plainfile.read()
        plainfile.close()

        cipher = [str(pow(ord(i), e, modulus)) for i in plain]
        for i in range(len(cipher)):
            cipherstring = ' '.join(cipher)

        cipherfile = open('ciphertext', 'w')
        cipherfile.write(base64Encode(cipherstring))
        cipherfile.close()

    else:
        print('keygen fonksiyonu çalıştırılmalı!')

def decrypt(ciphertext, privatekey):
    if (path.exists('publickey.txt') and path.exists('privatekey.txt')):
        prikeyfile = open(privatekey, 'r')
        private = prikeyfile.readlines()
        prikeyfile.close()

        for row in range (4):
            private[row] = base64Decode(private[row])

        d, p, q, totient = private
        d, modulus = int(d), int(p) * int(q)

        cipherfile = open(ciphertext, 'r')
        cipher = cipherfile.read()
        cipherfile.close()
        cipher = base64Decode(cipher)
        cipher = cipher.split()

        for i in range(len(cipher)):
            cipher[i] = chr(pow(int(cipher[i]), d, modulus))

        plain = ''.join(cipher)
        plainfile = open('plaintext2', 'w')
        plainfile.write(plain)
        plainfile.close()

        if (cmp('plaintext','plaintext2')):
            print('plaintext ve plaintext2 dosyaları özdeş.')

        else:
            print('plaintext ve plaintext2 dosyaları özdeş değil.')

    else:
        print('keygen fonksiyonu çalıştırılmalı!')
