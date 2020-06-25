import random
from datetime import datetime
#Ogrenci No: 160401059

#Hash fonksiyonu.
def final(file):
    with open(file, 'rb') as d:
        data = ((d.read()).decode()).zfill(32)
    veri = data
    veri = '10000000010110000011000010010010' + veri
    
    rotated1 = bin(int(veri,2) << 16)   #16 bit sola öteleme işlemi yaptık.
    bitFirst = rotated1[:32]
    bitLast = rotated1[32:]
    
    xor = (bin(int(bitFirst[2:]) ^ int(bitLast[2:]))[2:]).zfill(256) #ilk ve son 32 biti xorlayıp 256 bite tamamladık.
    xor2 = (int(xor[0:31],2) ^ int(xor[31:63],2)) ^ int(xor[63:95],2) ^ int(xor[95:127],2) ^ int(xor[127:159],2)  ^ int(xor[159:191],2) ^ int(xor[191:223],2) ^ int(xor[223:255],2)
    
    rotated2=xor2 >> 5 #5 bit sağa öteleme yaptık.
    
    hashed = bin(rotated2)[2:]
    
     
    return hashed

#Blok oluşturma ve özet,random sayı değerlerini hashsum'a yazma.
def w_hashedData(i):
    if(i<10):
            fileName = '00' + str(i) + '.txt'
    elif(i<100):
            fileName = '0' + str(i) + '.txt'
    hashed = str(final(fileName))    
    
    while(1):
        randomBits = random.getrandbits(32)
        toplam = (bin(int(hashed,2) + randomBits))[2:].zfill(32)
        if(len(toplam) > 32):
            toplam = toplam[-32:]
        if(i<9):
            fileName = '00' + str(i+1) + '.txt'
            file = open(fileName,'w')
        elif(i<99):
            fileName = '0' + str(i+1) + '.txt'
            file = open(fileName,'w')
        else:
            fileName = '100.txt'
            file = open(fileName,'w')
        
        file.write(toplam)
        kontrol = (str(final(fileName)).zfill(32))
        if(kontrol[:8] == '00000000'):   #İLK 8 BİT SIFIR KONTROLÜ
            hashsum = open('HASHSUM.txt','a')
            hashsum.write((bin(randomBits))[2:].zfill(32) + ' ---- ' + kontrol + '\n') #Random bitlerin ilk 2 karakterini atıyoruz.
            hashsum.close()
            break




#-----ÇALIŞTIRMA KISMI------

time1 = datetime.now().minute        #Çalıştırmaya başlamadan önceki zamanı ve döngünün her adımında ne kadar süre geçtiğini hesaplıyoruz 10 dk geçmemek için.
for i in range(1,101):
    if(datetime.now().minute - time1 < 10):
        w_hashedData(i)
    else:
        print("Time limit reached...")    

        
