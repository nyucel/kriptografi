# Birhan Berk Oktay - 170401075

import random
import time

def intBinary(n):
  # Integer degerini binary ye cevirip 32 bit donduren fonksiyon
  nBinary = ""
  nBinary = str(bin(n))[2:] # 0b olmadan
  if(len(nBinary) < 32):
    n = 32 - len(nBinary)
    x = ""
    x = n * "0"
    nBinary = x + nBinary
  return nBinary

def ilk8bit(n):
  # Ilk sekiz bit sifir ise True degilse False donduren fonksiyon
  if(n[:8] == "00000000"):
    return True
  return False

def final(dosya):
  # Jenkins ozetleme algoritmasini kullanarak aldigi dosyadan 32 bitlik deger ureten fonksiyon
  # (Bkz. https://en.wikipedia.org/wiki/Jenkins_hash_function)
  f = open(dosya, "rb")
  r = str(f.readlines())
  hash = 0
  for i in range(len(r)):
    hash += ord(r[i])
    hash &= 0xFFFFFFFF
    hash += hash << 10
    hash &= 0xFFFFFFFF
    hash ^= hash >> 6
    hash &= 0xFFFFFFFF
  hash += hash << 3
  hash &= 0xFFFFFFFF
  hash ^= hash >> 11
  hash &= 0xFFFFFFFF
  hash += hash << 15
  hash &= 0xFFFFFFFF
  return intBinary(hash)

def dosyaadi(i):
  d = ""
  if(i < 100):
    if(i < 10):
      d = "00" + str(i) + ".txt"
    else:
      d = "0" + str(i) + ".txt"
  else:
    d = str(i) + ".txt"
  return d

def blokzincir(i):
  ozet = final(dosyaadi(i))
  while True:
    kontrol = time.time()
    if(kontrol - baslangic > 10 * 60):
      print("Sure bitti!")
      exit(1)
    rastgele = intBinary(random.randint(0, 2**32))
    toplam = int(ozet, 2) + int(rastgele, 2)
    f = open(dosyaadi(i + 1), "w")
    f.write(str(intBinary(toplam)))
    f.close()
    if(toplam >= 2 ** 32):
      continue
    if(ilk8bit(final(dosyaadi(i + 1)))):
      break
  f = open("HASHSUM.txt", "a")
  f.write(str(i + 1) + ".txt icin rastgele = " + rastgele)
  f.write("\n")
  f.write(str(i + 1) + ".txt icin ozet = " + final(dosyaadi(i + 1)))
  f.write("\n\n")
  f.close()
  f = open(dosyaadi(i + 1), "w")
  f.write(str(intBinary(toplam)))
  f.close()

baslangic = time.time()
f = open("HASHSUM.txt", "w")
f.close()

for i in range(1, 100):
  blokzincir(i)