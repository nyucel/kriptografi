#Berkant Duman No:160401048
import random
import functions
import math



def keygen(bit):
    p = functions.generate_random_prime_numbers(bit)
    q = functions.generate_random_prime_numbers(bit)
    x = functions.quadratic_non_residue(p, q)
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
    bits = functions.string_to_bits(readText)
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
        if functions.legendre_symbol(int(c), p) == 1 and functions.legendre_symbol(int(c), q) == 1:
            
            decryptedBits += "0"
        else:
            decryptedBits += "1"
    plainText2 = open ("plaintext2", "w")
    plainText2.write(functions.bits_to_string(decryptedBits))
    plainText2.close()

    plainText = open("plaintext", "r")
    plainText2 = open("plaintext2", "r")

    if(plainText2.read() == plainText.read()):
        print("İki metin birbirleri ile aynı.")
    else:
        print("İki metin birbirlerinden farkılı.")



#keygen(int(input("Bit uzunluğunu giriniz:")))
#encrypt("plaintext", "publickey.txt")
#decrypt("ciphertext", "privatekey.txt")
