#Berat Kanar 160401059


import time

#Ozet alma fonksiyonu.
def ozet(data):
    data_bytes = bytes(data, "ascii")

    veri=(''.join(["{0:b}".format(x) for x in data_bytes])) #ascii karşılıgını aldıgımız verileri düzenledik.
    veri_bytes=veri.zfill(64) #64 bite tamamladık.
    
    veri_bytes_32_first = veri_bytes[:32]
    veri_bytes_32_last = veri_bytes[32:]

    
    xor = (bin(int(veri_bytes_32_first[2:]) ^ int(veri_bytes_32_last[2:]))[2:]).zfill(128) #İlk ve son 32 biti xOR ladık ve 128 bite tamamladık.
    
    xor_first64 = xor[:64]
    xor_last64 = xor[64:]
    
    xor2 = (bin(int(xor_first64,2) ^ int(xor_last64,2)))[2:34] #İlk 64 ve son 64 biti bir kez daha xorladık ve ilk 32 bitini aldık.
    
    return xor2


while(1):
    print("""---Menü---
          1-Özet Alma
          2-Doğrula """)
    secim = input("Secim:")

    if(int(secim)==1):
        
        veri = input("Özeti Alınacak Veri:")
        data_to_write = ozet(veri)   #Kullanıcının girdiği karakterlerin özetini aldık.

        file=open("golge.txt",'w')   
        file.write(data_to_write)    
        file.close()

        break

    elif(int(secim)==2):

        #golge.txt icindeki özet değerini karşılaştırma için aldık.
        golge = open('golge.txt','r')
        ozet_golge=int(golge.read())
        golge.close()
        
        
        fileName = input("Dosya Adi:") #Kullanıcıdan dosya ismini aldık ve satırları okuduk.
        file = open(fileName,'r')
        rows=file.readlines()
        
        flag=0 #İlk anda eşleşme olmadığı için flag 0.
        for row in rows:
            hashed=int(ozet(row[:6]))  #Her satırın ilk 6 karakterini ozet alma fonksiyonuna yolladık.
            if(hashed==ozet_golge):    #Gelen ozet degerini golge içindeki değerle karşılaştırdık.
                flag=1
                print("Eşleşme bulundu eşleşen değer: ",hashed)
                print("Program 5 saniye içinde sonlanacak..")
                time.sleep(5)
                exit(1)
                
        if(flag==0):  #Eşleşme yok.
            print("Eşleşme bulunamadı..5 saniye içinde program sonlanacak..")
            time.sleep(5)
            exit(1)
        
    

        





 
