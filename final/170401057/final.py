# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 20:13:52 2020

@author: shnsr
"""
#Şahan Can SARKI -- 170401057


import random

def final(dosya):
    with open(dosya,'rb') as d:
        data = ((d.read()).decode()).zfill(32)
        
    print(data)
    print(len(data))
    
    sonuc = data
    print(sonuc + "\n")
    
    firstBit = sonuc[0:16]
    secondBit = sonuc[16:32]
    cikti16bit = ''
    cikti32bit = ''
    for i in range(16):
        cikti16bit += str(int(firstBit[i]) ^ int(secondBit[i]))
        print("satir 26",bin(int(cikti16bit)))
        print("satir 27",cikti16bit)
        cikti16bit += str(int(cikti16bit[i]) | int(secondBit[i]) & int(firstBit[i]))
        print("satir 30",cikti16bit)
        print("satir 31",data)
        print(hex(int(cikti16bit)) + "----> eski çıktısı" ,hex(int(data)))
    return(bin(int(cikti16bit, 2))[2:].zfill(32))
        
final("001.txt")
        
class Block():
     
    def __init__(self,dosyaAdı,sira,onceki_hash):
        self.dosyaAdı = dosyaAdı
        self.sira = sira
        self.onceki_hash = onceki_hash
    
     
    def yeni_block_olustur(onceki_block,hashcode):
        sira = onceki_block.sira + 1
        
        
        
        rasgele=str(bin(random.getrandbits(32))[2:].zfill(32))
        newBlok=str(bin(int(hashcode,2) + int(rasgele,2))[2:].zfill(32))[0:32]
        newBlok = '00000000' + newBlok[8:]
        if(sira % 10 == sira):
            dosyaAdı = "00"+str(sira)+".txt"
            f = open(dosyaAdı,"w+")
            f.write(newBlok)
            f.close()
        elif(sira % 100 == sira):
            dosyaAdı = "0"+str(sira)+".txt"
            f = open(dosyaAdı,"w+")
            f.write(newBlok)
            f.close()
        else:
            dosyaAdı = str(sira)+".txt"
            f = open(dosyaAdı,"w+")
            f.write(newBlok)
            f.close()
        yeni_block = Block(dosyaAdı = dosyaAdı,sira=sira,onceki_hash=hashcode)
        with open("HASHSUM.txt","a") as file:
            file.writelines(newBlok + " + " + rasgele +"\n")
        return yeni_block
    
    
    
        
    def test_et(self):
        onceki_block = zincir[0]    
        for i in range(2,101):
            yeni_block = Block.yeni_block_olustur(onceki_block,final(onceki_block.dosyaAdı))
            zincir.append(yeni_block)
            onceki_block = yeni_block
            print("{} zincire eklendi!".format(yeni_block))
            print("Hash : {} \n".format(yeni_block.onceki_hash))

 
ilk_block = Block(dosyaAdı = "001.txt",sira=1,onceki_hash="0")
zincir = []
zincir.append(ilk_block)
ilk_block.test_et()
