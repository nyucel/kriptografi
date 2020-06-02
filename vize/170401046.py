# Oguz KAYA 170401046   Merkle-Hellman
import random

def gcd(p,q):

    while (q != 0):
        p, q = q, p%q
    return p

def is_coprime(x, y):    # iki sayının aralarında asal olup olmadıgını kontrol eden fonksiyon
    return gcd(x, y) == 1

def Convert(string):     # stringi liste haline getiren foksiyon
    li = list(string.split(" "))
    return li

def Binary(text):
    binary = ""
    for i in text:
       binary += ' '.join(f"{ord(i):08b}") + ' '
    return binary

def extended_gcd(a, b):
    lastremainder, remainder = abs(a), abs(b)
    x, lastx, y, lasty = 0, 1, 1, 0
    while (remainder):
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient * x, x
        y, lasty = lasty - quotient * y, y
    return lastremainder, lastx * (-1 if a < 0 else 1), lasty * (-1 if b < 0 else 1)

def mod_inv(a, m):      # moduler ters alan fonksiyon
    g, x, y = extended_gcd(a, m)
    return x % m

def file_cmp(plaintext,plaintext2):  # iki dosyanın ozdesligini kontrol eden fonksiyon

    file = open(plaintext, "r")
    text = file.read()
    file.close()

    file = open(plaintext2, "r")
    text2 = file.read()
    file.close()

    if(text == text2):
        return 1
    return 0

def keygen(n):
    w = [1]
    for i in range(n-1):
        total = sum(w)
        z = random.randint(total + 1, total + 2)
        w.append(z)
    total = sum(w)
    q = random.randint(total + 1, total + 10)
    while(1):
        r = random.randint(2,q-1)
        if(is_coprime(q,r)):
            break
    B = []
    for i in range(len(w)):
        B.append((w[i] * r) % q)
    publickey = open("publickey.txt", "w")
    for i in B:
        publickey.write(str(i) + ' ')
    privatekey = open("privatekey.txt", "w")
    for i in w:
        privatekey.write(str(i) + ' ')
    privatekey.write('\n' + str(q) + '\n')
    privatekey.write(str(r))
    publickey.close()
    privatekey.close()

def encrypt(plaintext, publickey):
    try:
        f = open("publickey.txt")
    except FileNotFoundError:
        print("Once keygen fonksiyonunu calistiriniz")
        exit(0)
    plaintext = open(plaintext,"r")
    plainliststr = Convert(Binary(plaintext.read()))
    plainlistint = []
    for i in range(0, len(plainliststr)-1):
        plainlistint.append(int(plainliststr[i]))
    publickey = open(publickey,"r")
    publiclist_str = Convert(publickey.read())
    publiclist_int = []
    for i in range(n):
        publiclist_int.append(int(publiclist_str[i]))
    cipher = 0
    for i in range(n):
        cipher += publiclist_int[i] * plainlistint[i]
    ciphertext = open("ciphertext.txt", "w")
    ciphertext.write(str(cipher))
    ciphertext.close()

def decrypt(ciphertext,privatekey):
    try:
        f = open("privatekey.txt")
    except FileNotFoundError:
        print("Once keygen fonksiyonunu calistiriniz")
        exit(0)
    privatekey = open(privatekey,"r")
    w_str = Convert(privatekey.readline())
    q = int(privatekey.readline())
    r = int(privatekey.readline())
    w_int = []
    for i in range(len(w_str)-1):
        w_int.append(int(w_str[i]))
    ciphertext = open(ciphertext,"r")
    cipher = int(ciphertext.read())
    a = (cipher * (mod_inv(r,q))) % q
    for i in range(1, len(w_int)+1):
        if (a >= w_int[-i]):
            a -= w_int[-i]
            w_int[-i] = 1
        else:
            w_int[-i] = 0

    binaryplain = ''
    for i in range (len(w_int)):
        binaryplain += str(w_int[i])

    str_data = ''
    for i in range(0, len(binaryplain), 8):
        temp_data = binaryplain[i:i + 8]
        decimal_data = int(temp_data,2)
        str_data +=  chr(decimal_data)

    plaintext2 = open("plaintext2.txt","w")
    plaintext2.write(str_data)
    plaintext2.close()

    if(file_cmp("plaintext.txt","plaintext2.txt")):
        print("Dosyalar ozdestir")

n = int(input("bit buyuklugunu giriniz : "))
keygen(n)
encrypt("plaintext.txt","publickey.txt")
decrypt("ciphertext.txt","privatekey.txt")
