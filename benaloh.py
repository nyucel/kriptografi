from random import randrange
from functions import isprime
from functions import allprimes
import random
import math

# Benaloh algoritmasinda anahtar uzunlugu tek sayi olmak zorundadir.


def generate_random(n):
    return randrange(2**(n - 1), 2**n) | 1


def miller_rabin_primality_test(p, s=5):
    if p == 2:
        return True
    if not (p & 1):
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


def keygen(n):
    # NOTE: wikipedia da r ile gosterilen parametre, hocanin istegi uzerine burada n olarak alindi
    # NOTE: wikipedia da n ile gosterilen degisken, burada n_ ile gosterildi

    # TODO: raise an exception if n is even

    # NOTE: algoritmanin dogru calistigindan emin olana dek dosya acma kapama islemlerini deaktif edelim.
    # publickey_file = open("publickey.txt", "w+")
    # privatekey_file = open("privatekey.txt", "w+")
    p = q = None

    while True:
        p = generate_random(n//2)
        if miller_rabin_primality_test(p) and (p-1) % n == 0 and math.gcd(n, int((p-1)/n)) == 1:
            break

    while True:
        q = generate_random(n//2)

        if miller_rabin_primality_test(q) and math.gcd(n, int(q-1)) == 1:
            break

    n_ = p * q
    phi = (p-1) * (q-1)

    # TODO: key'leri dosyalara yaz
    # publickey_file.close()
    # privatekey_file.close()
