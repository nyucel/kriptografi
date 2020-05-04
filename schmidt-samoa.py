# -*- coding: utf-8 -*-

# Schmidt-Samoa

# Ayça Nur Budak    150401041
# Birhan Berk Oktay 170401075
# Ramazan Şahin     170401069

# Wikipedia kullanıcı adı = Aycanurbudak

import random

def okek(a, b):
  # Ortak katlarının en küçüğünü bulan fonksiyon
  return a * b // obeb(a, b)

def obeb(a, b):
  # Ortak bölenlerinin en büyüğünü bulan fonksiyon
  if a == 0:
    return b
  return obeb(b % a, a)

def allprimes(n):
  # Bir sayıdan küçük bütün asal sayıları dizi olarak döndüren fonksiyon
  primes = []
  for i in range(2, n + 1):
    primes.append(i)
  for x in range(0, int(n / 2) + 1):
    if(primes[x] != 0):
      for i in range(x + primes[x], n - 1, primes[x]):
        primes[i] = 0
  primes.sort()
  return(primes[primes.count(0):])

def rabinMiller(n):
  # Olasılıksal asallık testi
  s = n - 1
  t = 0
  while(s % 2 == 0):
    s = s // 2
    t += 1
  for trials in range(5):
    a = random.randrange(2, n - 1)
    v = pow(a, s, n)
    if(v != 1):
      i = 0
      while v != (n - 1):
        if(i == t - 1):
          return False
        else:
          i = i + 1
          v = (v ** 2) % n
  return True

def isprime(n):
  # 32 bit üzeri anahtar üretimlerinde daha hızlı sonuç alabilmek için rabin miller asallık testi kullanıyoruz.
  if (n < 2):
    return False
  lowPrimes = allprimes(1000)
  if n in lowPrimes:
    return True
  for prime in lowPrimes:
    if (n % prime == 0):
      return False
  return rabinMiller(n)

def stringBinary(metin):
  # String değerini binary ye çeviren fonksiyon
  binaryMetin = ""
  for i in metin:
    binaryMetin += "".join(f"{ord(i):08b}")
  return binaryMetin

def integerBinary(n):
  # Integer değerini binary ye çeviren fonksiyon
  nBinary = ""
  nBinary = str(bin(n))[2:] # 0b olmadan
  return nBinary

def binaryString(binary):
  # Binary değerini string e çeviren fonksiyon
  blok = []
  metin = ""
  for i in range(0, len(binary), 8):
    blok.append(binary[i:i+8])
  for char in blok:
    metin += chr(int(char, 2))
  return metin

def ayniMi(plaintext, plaintext2):
  # İki text dosyasının içeriğinin aynı olup olmadığını True/False döndüren fonksiyon
  f = open(plaintext, "r")
  metin = f.read()
  f.close()

  f = open(plaintext2, "r")
  metin2 = f.read()
  f.close()

  if(metin == metin2):
    return True
  return False

# -----------------------------------

def keygen(n):
  # Girilen n sayısı plaintext dosyasındaki karakter sayısının en az 4 katı olmak zorundadır. Örneğin 4 karakterlik bir metin için en az 17 girilmelidir. Aksi takdirde mod almadan dolayı metin kaybedilir.
  # n bite yakın asal sayı 2^(n-1) ile 2^n arasında üretiliyor. Açık anahtar n bitten daha büyük olabilir.
  while True:
    p = random.randrange(2 ** (n - 1), 2 ** n)
    if(isprime(p)):
      break
  while True:
    q = random.randrange(2 ** (n - 1), 2 ** n)
    if(isprime(q)):
      if(q == p):
        continue
      break
  acikAnahtar = p ** 2 * q
  gizliAnahtar = pow(acikAnahtar, -1, okek(p - 1, q - 1))

  f = open("publickey.txt", "w+")
  f.write(str(acikAnahtar))
  f.close()

  f = open("privatekey.txt", "w+")
  f.write(str(gizliAnahtar) + " " + str(p) + " " + str(q)) # Gizli anahtar, p ve q değerleri privatekey dosyasına yazılır. p ve q değerleri deşifrelemede kullanılacağı için eklenmiştir.
  f.close()

# -----------------------------------

def encrypt(plaintext, publickey):
  # Düz metin önce binary tabana çevrilir. Her bir karakterin 8 bitlik karşılığı yan yana yazılır ve oluşan yeni sayı decimale çevrilir. Bu sayı üzerinden şifreleme işlemi gerçekleştirilir.
  try:
    f = open(publickey, "r")
    acikAnahtar = int(f.read())
  except IOError:
    print("Publickey bulunamıyor. keygen fonksiyonunu çalıştırınız.")
  finally:
    f.close()

  try:
    f = open(plaintext, "r")
    duzMetin = f.read()
  except IOError:
    print("Düz metin bulunamıyor. plaintext.txt oluşturun.")
  finally:
    f.close()

  f = open("ciphertext.txt", "w+")
  binaryMetin = stringBinary(duzMetin)
  metinDecimal = int(binaryMetin, 2)
  ciphertext = str(pow(metinDecimal, acikAnahtar, acikAnahtar))
  f.write(ciphertext)
  f.close()

# -----------------------------------

def decrypt(ciphertext, privatekey):
  # Gizli anahtar, p ve q değerleri privatekey dosyasından alınır.
  try:
    f = open(privatekey, "r")
    dizi = []
    for i in f.read().split():
      dizi.append(i)
    gizliAnahtar = int(dizi[0])
    p = int(dizi[1])
    q = int(dizi[2])
  except IOError:
    print("Privatekey bulunamıyor. keygen fonksiyonunu çalıştırınız.")
  finally:
    f.close()

  try:
    f = open(ciphertext, "r")
    ciphertext = int(f.read())
  except IOError:
    print("ciphertext bulunamıyor. encrypt fonksiyonunu çalıştırınız.")
  finally:
    f.close()
  # ciphertext deşifrelenir. Oluşan değer binary e çevrilir. Bu binary değer de düz metine döndürülür.
  f = open("plaintext2.txt", "w+")
  n =  pow(ciphertext, gizliAnahtar, p*q)
  nBinary = integerBinary(n)
  
  if(len(nBinary) % 8 != 0):  # Düz metinde şifreleme yaparken eğer ilk karakterin 8 bitlik karşılığı 0 ile başlıyor ise decimale çevrim yaparken bu 0 kaybediliyor. Bunu önlemek amacıyla karakter uzunluğunu 8 in katı haline getirilir.
    nBinary = "0" + nBinary

  metin = binaryString(nBinary)
  f.write(metin)
  f.close()
  print("plaintext ile plaintext2 özdeş mi: " , ayniMi("plaintext.txt", "plaintext2.txt"))

# -----------------------------------

print("Anahtar uzunluğu giriniz: ")
n = int(input(""))

keygen(n)
encrypt("plaintext.txt","publickey.txt")
decrypt("ciphertext.txt", "privatekey.txt")


