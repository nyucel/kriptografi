#Enes Nurullah KENDİRCİ
#Şahan Can SARKI
#Berat KANAR

import random
import filecmp as fc
def gcd(a,b): 
    if a == 0: 
        return b 
    return gcd(b % a, a) 
  
def lcm(a,b): 
    return (a*b) // gcd(a,b) 
  


def isprime(number): #FermatPrimalityTest
    if (number > 1):
        for time in range(3):
            randomNumber = random.randint(2, number)-1
            if ( pow(randomNumber, number-1, number) != 1 ):
                return False
        
        return True
    else:
        return False  

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
   
def multiplicative_inverse(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def reverse_while_loop(s): #stringi ters çevirme
    s1 = ''
    length = len(s) - 1
    while length >= 0:
        s1 = s1 + s[length]
        length = length - 1
    return s1

def keygen(n):
    bit1 = 2**(n-1) - 1 
    bit2 = 2**n - 1
    
    p = 1
    while(not isprime(p)):                   # asal sayı olmadığı sürece
        p = random.randint(bit1, bit2) # rasgale n'bit sayı deniyoruz.
    
    q = 1
    while((not isprime(q)) or q == p):       # asal sayı olmadığı ve p'ye eşit olduğu sürece
        q = random.randint(bit1, bit2)# rasgale n'bit sayı deniyoruz.
    print('baslangic')
    x = p * q                                # algoritmadki n'imiz
    An = lcm((p - 1), (q - 1))               # λ(n)
    print('deneme')
    e = 65537                                # Hamming Ağırlığına sahip e değerleri daha verimli şifreleme sağlar.
    if(gcd(e, An) != 1 and An>4294967297):   # eboblarının 1 olup olmadığı kontrol ediliyor değilse yeni e'mizi belirliyor
        e = 4294967297
    elif(gcd(e, An) != 1):                   #e değerimiz λ(n) küçük olmak zorunda olduğundan her ihtimale karşı hata mesajı koyduk
        raise "uygun key üretilemedi bir daha deneyin error:1/65537"
    
    d = multiplicative_inverse(e, An)        # d*e ≡1(mod(λ(n)))
    
    publicDosya = open('publickey.txt', 'w') #publickey dosyasını hazırladık
    publicDosya.write(str(x))
    publicDosya.write('\n')
    publicDosya.write(str(e))
    publicDosya.close
    
    privateDosya = open('privatekey.txt', 'w')#privatekey dosyasını hazırladık
    privateDosya.write(str(d))
    privateDosya.write('\n')
    privateDosya.write(str(p))
    privateDosya.write('\n')
    privateDosya.write(str(q))
    privateDosya.write('\n')
    privateDosya.write(str(An))
    privateDosya.close()
        
    
def encrypt(plaintext, publickey):            #plaintext'in plaintext.txt dosyası olarak geldiğini varsaydık.
    pt = open(plaintext)                      #gelen dosyaları açtık
    pk = open(publickey)
    
    n = int(pk.readline())                    #dosya içeriklerini kullanacağımız değişkenlere aktardık
    key = int(pk.readline())
    plainString = pt.read()
    
    cipher = [str((ord(char) ** key) % n) for char in plainString]
                                              #plainStringteki her char'ı asciiye çevirip şifreledik ve cipher listesine doldurduk
    for k in range(len(cipher)):              #aradaki boşlukları 0'larla doldurduk
        cipher[k] = cipher[k].zfill(len(str(n))) #şifreleme sırasında mod(n) yaptığımız için n'den uzun olamazlar. n'in boyu kadar 0'la doldurduk.
    
    dosya = open('ciphertext.txt', 'w')       #ciphertext.txt dosyasına şifrelenmiş mesajı yazdık
    for i in cipher:
        dosya.write(str(i))
    dosya.close()        
    
def decrypt(ciphertext, privatekey):          #ciphertext'in ciphertext.txt dosyası olarak geldiğini varsaydık.
    
    ct = open(ciphertext)                     #gelen dosyaları açtık
    pk = open(privatekey)
    
    key = int(pk.readline())                  #dosya içeriklerini kullanacağımız değişkenlere aktardık
    p = int(pk.readline())
    q = int(pk.readline())
    An = int(pk.readline())
    n = p * q
    ciphertextStr = ct.read()
    
    plain2 = []                               #plain2 için liste
    cUzunluk = len(ciphertextStr)             
    
    while(cUzunluk > 0):                      #ciphertext boyunca (sondan başa şeklinde)
        nUzunluk = len(str(n))                
        toplam = ''
        while(nUzunluk > 0):                  #her bir harfin asciideki karşılığının boyu n kadar olduğundan
            toplam += ciphertextStr[cUzunluk - 1] #n'in boyu  kadar sayıyı str(toplam) içerisine atıyoruz
            nUzunluk += -1
            cUzunluk += -1
        toplam = reverse_while_loop(toplam)   #tersten gittiğimiz için sayıyı tersçeviriyoruz
        c = int(toplam)                       
        plain2.append(chr(pow(c, key, n)))    #şifreyi çözüp plain2listesine yerleştiriyoruz
    plain2.reverse()                          #tersten gittiğimiz için yine bir ters çevirme işlemi yapıyoruz
    
    dosya = open('plaintext2.txt', 'w')       #plaintext2 dosyasına yazıyoruz
    for i in plain2:
        dosya.write(str(i))
    dosya.close()
    
    if fc.cmp("plaintext.txt", "plaintext2.txt"):
        print("plaintext ve plaintext2 dosyaları özdeş")
    else:
        print("plaintext ve plaintext2 dosyaları özdeş değil.")

#TEST
keygen(1024)
encrypt('plaintext.txt', 'publickey.txt')
decrypt('ciphertext.txt', 'privatekey.txt')
