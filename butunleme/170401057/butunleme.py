# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 00:29:55 2020

@author: shnsr
"""
#Şahan Can SARKI 170401057 
def ozet(girdi):
    asci = ''
    for i in range(6):
        asci += (str(ord(girdi[i]))).zfill(3) # ascii ye çevirirken ilk 0 ı koymadığı için ben koydum.
    binAsci = bin(int(asci))[2:].zfill(64)
    
    ilk32 = binAsci[:32]
    son32 = binAsci[32:]
    
    firstXor = bin(int(ilk32[0]) ^ int(son32[0]))[2:]  
    yeni = firstXor # yeni değişkenimiz ilk32 ve son32 nin ilk basamakalrını xorlamakla başlıyor ve aşağıdaki for da daima güncelleniyor.
    for i in range(1,32):
        xor = bin(int(firstXor) ^  (int(ilk32[i]) & int(son32[i])))[2:]
        yeni += xor 
        firstXor = xor

    binAsciReverse = binAsci[len(binAsci)::-1] # yukarıdaki binAsci mizi ters çevirdik.
    #aşağıda binAscinin ters halini aynı döngüye soktuk
    ilk32 = binAsciReverse[:32]
    son32 = binAsciReverse[32:]
    
    firstXor = bin(int(ilk32[0]) ^ int(son32[0]))[2:]
    yeni2 = firstXor
    for i in range(1,32):
        xor = bin(int(firstXor) ^  (int(ilk32[i]) | int(son32[i])))[2:]
        yeni2 += xor 
        firstXor = xor
    yeniXor = bin(int(yeni,2) ^ int(yeni2,2))[2:].zfill(32)
    return yeniXor

while(True):
    cevap = input("Yapılacak işlemi girin \n 1: özet değerini al \n 2: doğrula \n")
    if(cevap == "1"):
        girdi = input("Özel değeri alınacak 6 karakterlik girdi bekleniyor...:")
        dosya = open('golge.txt', 'w+')
        dosya.write(ozet(girdi))            # girdiyi hashleyip dosyaya yazıyoruz.(golge.txt'ye)
        dosya.close()
        break
    elif(cevap == "2"):
        try:
            dosya2 = open('golge.txt','r+') # golge.txt 'yi karşılaştırmak için read olarak açıyoruz.
            golgeIcerik = dosya2.read()
            girdi = input("Uzantısı ile birlikte bir dosya adı giriniz : ")
            dosya = open(girdi , 'r+') # Kullanıcının verdiği dosyayı read olarak açıyoruz
            for i in dosya:
                ozet2 = ozet(i) 
                
                if(ozet2 == golgeIcerik): # karşılaştırma sonucu aynı olursa bunu kullancıya bildiriyoruz
                    print("Bulunan Değer : " + i)
                    print("Bulunan Değerin Hash Karşılığı : " + ozet2)
                    dosya2.close
                    dosya.close()
                    break
            else:
                print("Bir eşleşme bulunmadı...")
                dosya2.close()
                dosya.close()
        except:
            print("Golge.txt  Bulunamadı...")
        break
                
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    