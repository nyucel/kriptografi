import random
from time import time
def dosya_olustur(i):
    dosya = ""
    if i<10:
        dosya = "00"+str(i)+".txt"
    elif i<100:
        dosya = "0"+str(i)+".txt"
    else:
        dosya =str(i)+".txt"
    return dosya    

def random_olustur():
    a=""
    for i in range(32):
        a = a + str(random.randint(0,1))
    return a

def final(deneme,i):
    f = open(deneme,"r")
    oku = f.read()
    if i == 1:
        binary =  ''.join(format(ord(x), '08b') for x in oku)
    else:
        binary = oku
    #print(binary)
    mod = len(binary) % 128
    while (len(binary)%128 != 0):   #bit sayısını 128'e veya katına tamamlamak için listenin sonuna 0'lar ekledik
        binary += "0"
    #print(binary)
    #print(len(binary))
    x = 32
    liste=[]
    for i in range(0,len(binary),x):
      liste.append(binary[i:i + x])

    #print(liste)
    w = len(liste)
    yedekliste=[]
    son_liste = []
    while True:

      if w<=2:
        a = yedekliste[0]
        b = yedekliste[1]
        y = int(a,2) ^ int(b,2)
        son_liste.append('{0:0{1}b}'.format(y,len(a)))
        liste.pop()
        break
      else:
        t=w-1
        for j in range(0,w//2):
          a = liste[j]
          b = liste[j+t]
          y = int(a,2) ^ int(b,2)
          yedekliste.append('{0:0{1}b}'.format(y,len(a)))
          t = t-2
          w /= 2
    return son_liste[0]

sure = time() + 600
i = 1
ozet = final("001.txt",i)
print(ozet)
onceki = ozet
for i in range(2,101):
    while True:
        if time()>sure:
            print("10 dakika doldu.")
            exit()
        rastgele = random_olustur()
        toplam = int(onceki,2) + int(rastgele,2)
        
        x = '{0:0{1}b}'.format(toplam,32)
        dosya = dosya_olustur(i)
        ydosya = open(dosya,"w")
        ydosya.write(x)
        ydosya.close()
        yozet = final(dosya,i)
        print(yozet)
        if yozet[:8] == "00000000":
            break
    ydosya = open(dosya,"r")
    onceki = ydosya.read()
    ydosya.close()
    hashdosya = open("HASHSUM.txt","a")
    hashdosya.write(dosya +" => Random : " +rastgele + "    OZET: "+ yozet +"\n" )
    hashdosya.close()
print("DOSYALAR OLUŞTURULDU..")     
