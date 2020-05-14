#Berkant Duman No:160401048
import random
import math


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



def keygen(bit):
    p = generate_random_prime_numbers(bit)
    q = generate_random_prime_numbers(bit)
    x = quadratic_non_residue(p, q)
    n = p * q

    public = open("publickey.txt","w")
    private = open("privatekey.txt","w")

    public.write("x= " + str(x) + "\n")
    public.write("N= " + str(n))
    private.write("q= " + str(q) + "\n")
    private.write("p= " + str(p))

    
def encrypt(plaintext, publickey):
    text = open(plaintext, "r")
    try:
        publicKey = open (publickey, "r")
    except:
        print("Anahtarlar bulunamadı, lütfen önce keygen fonksiyonunu çağırınız.")
        return
    readText = text.read()
    bits = string_to_bits(readText)
    lines = publicKey.readlines()
    
    x = int(lines[0][3:])
    N = int(lines[1][3:])
    encryptedBits = []
    
    for m in bits:
        y = random.randrange(2, N)
        while math.gcd(y, N) != 1 :
            y = random.randrange(2, N)
       
        c = ((y**2)*(x**int(m))) % N
        encryptedBits.append(c)

    ciphertext = open("ciphertext", "w")
    for i in encryptedBits:
        ciphertext.write(str(i) + "\n")
    

def decrypt(ciphertext, privatekey):
    cipherText = open(ciphertext, "r")
    try:
        privateKey = open(privatekey, "r")
    except:
        print("Anahtarlar bulunamadı, lütfen önce keygen fonksiyonunu çağırınız.")
        return

    encryptedBits = []
    lines = privateKey.readlines()
    q = int(lines[0][3:])
    p = int(lines[1][3:])
    
    for i in cipherText.readlines():
        encryptedBits.append(int(i))
    
    decryptedBits = ""
    for c in encryptedBits:
        if legendre_symbol(int(c), p) == 1 and legendre_symbol(int(c), q) == 1:
            
            decryptedBits += "0"
        else:
            decryptedBits += "1"
    plainText2 = open ("plaintext2", "w")
    plainText2.write(bits_to_string(decryptedBits))
    plainText2.close()

    plainText = open("plaintext", "r")
    plainText2 = open("plaintext2", "r")

    if(plainText2.read() == plainText.read()):
        print("İki metin birbirleri ile aynı.")
    else:
        print("İki metin birbirlerinden farkılı.")



keygen(int(input("Bit uzunluğunu giriniz:")))
encrypt("plaintext", "publickey.txt")
decrypt("ciphertext", "privatekey.txt")
