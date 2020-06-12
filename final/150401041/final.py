# Ayça Nur Budak - 150401041

import random
import time
import os
from os import path

def bit_tamamla(x):
  if(len(x) < 32): #parametre ile gelen 32 bitten kucukse 32 bite tamamla
    x = (32-len(x))*"0"+x
  return x

def intten_ikilige(x):
  x = str(bin(x)) #parametre ile gelen sayiyi ikilik tabana cevir
  ikilik = ""
  for i in range(2,len(str(x))):
    ikilik = ikilik+x[i]
  return bit_tamamla(ikilik) #32 bit olarak dondur

def ilk_sekiz_bit(x):
  for i in range(8): #ilk 8 biti 0 mi kontrol et
    if(x[i] == "0"):
      continue
    else:
      return False
  return True

def isim(i):
  if(0 < i and i < 10): #dosya ismini formatla
    return "00"+str(i)
  if(9 < i and i < 100):
    return "0"+str(i)
  return str(i)

def final(dosya):
  f = open(dosya,"rb") #dosyanin 32 bitlik ozetini al
  r = str(f.readlines())
  c1 = 0xcc9e2d51
  c2 = 0x1b873593
  length = len(r)
  h1 = 0
  roundedEnd = (length & 0xfffffffc)
  for i in range(0, roundedEnd, 4):
    k1 = (ord(r[i]) & 0xff) | ((ord(r[i + 1]) & 0xff) << 8) | ((ord(r[i + 2]) & 0xff) << 16) | (ord(r[i + 3]) << 24)
    k1 *= c1
    k1 = (k1 << 15) | ((k1 & 0xffffffff) >> 17)
    k1 *= c2
    h1 ^= k1
    h1 = (h1 << 13) | ((h1 & 0xffffffff) >> 19)
    h1 = h1 * 5 + 0xe6546b64
  k1 = 0
  val = length & 0x03
  if val == 3:
      k1 = (ord(r[roundedEnd + 2]) & 0xff) << 16
  if val in [2, 3]:
      k1 |= (ord(r[roundedEnd + 1]) & 0xff) << 8
  if val in [1, 2, 3]:
      k1 |= ord(r[roundedEnd]) & 0xff
      k1 *= c1
      k1 = (k1 << 15) | ((k1 & 0xffffffff) >> 17)
      k1 *= c2
      h1 ^= k1
  h1 ^= length
  h1 ^= ((h1 & 0xffffffff) >> 16)
  h1 *= 0x85ebca6b
  h1 ^= ((h1 & 0xffffffff) >> 13)
  h1 *= 0xc2b2ae35
  h1 ^= ((h1 & 0xffffffff) >> 16)
  return intten_ikilige(h1 & 0xffffffff)

#-----------------------------------

def zincir_olustur():
  if(path.exists("HASHSUM.txt")):
    os.remove("HASHSUM.txt")
  for i in range(1,100):
    o = final(isim(i)+".txt") # Ozet degeri
    while True:
      sinir = 600
      if(time.time()-ilk > sinir):
        print("Program sonlandirildi!")
        exit(1)
      r = intten_ikilige(random.randint(0,2**32)) # Rastgele 32 bit
      t = int(o,2) + int(r,2) # Ozet + Rastgele
      if(t >= 2**32):
        continue
      f = open(isim(i+1)+".txt", "w")
      f.write(str(intten_ikilige(t)))
      f.close()
      if(ilk_sekiz_bit(final(isim(i + 1)+".txt")) == True):
        f = open("HASHSUM.txt","a")
        f.write(str(i+1) + " nolu blogun degerleri" + "\n")
        f.write("Rast = "+r+"\n")
        f.write("Ozet = "+final(isim(i + 1)+".txt")+"\n\n")
        f.close()
        f = open(isim(i+1)+".txt", "w")
        f.write(str(intten_ikilige(t)))
        f.close()
        break
    
ilk = time.time()
zincir_olustur()