def strtobin(text): 
    return "".join(["0"*(10-len(i))+i[2:] for i in list(map(bin,bytearray(text.encode())))]) 
    #gelen string'i binary'e çevirip string halinde '0b' kısımları olmadan return eden fonksiyon

def bintoint(x): #binary -> int dönüşümü
    return int(x,2)
    
def inttobin(x): #int -> binary dönüşümü ('0b' kısmı olmadan)
    return bin(x)[2:]
    
def xor(a,b): #mantıksal XOR işlemi
    xorf=lambda a,b : "0" if a==b else "1" #2 adet karakter için XOR fonksiyonu
    return "".join([xorf(a[i],b[i]) for i in range(0,len(a))]) #xorf fonksiyonun a,b için uygulanması

def andl(a,b): #mantıksal AND işlemi
    andf=lambda a,b : "1" if a==b and a=="1" else "0" #2 adet karakter için AND fonksiyonu
    return "".join([andf(a[i],b[i]) for i in range(0,len(a))]) #andf fonksiyonun a,b için uygulanması

def orl(a,b): #mantıksal OR işlemi
    orf=lambda a,b : "0" if a==b and a=="0" else "1" #2 adet karakter için OR fonksiyonu
    return "".join([orf(a[i],b[i]) for i in range(0,len(a))]) #orf fonksiyonun a,b için uygulanması

def notl(a): #mantıksal değili
    ters=lambda x : "0" if x=="1" else "1" # "0"->"1" "1"->"0" yapan fonksiyon
    return "".join([ters(i) for i in a]) #ters fonksiyonunun her karaktere uygulanması

def leftrotate(x,t=1): # x'i t kadar mantıksal left rotate eden fonksiyon
    # t belirtilmemişse 1 bit left rotate yapıyor
    if len(x)<2: 
        return
    if t==0: # t=0 olduğunda fonksiyonu tekrar çağırmayı bırakıyor
        return x
    return leftrotate(x[1:]+x[0],t-1) #recursive olarak t-1 ve 1 bit left rotate halini fonksiyona geri yolluyor

def addx(list): # listedeki tüm binary değerleri toplayan fonksiyon
    ret=0
    for l in list:
        ret=ret+int(l,2) #değerleri 10'luk tabanda topluyor     
    return bin(ret)[2:] #dönüş değerini '0b' kısmı olmadan binarye çevirerek yolluyor

def ozet(text):
    if len(text)!=6: #karakter uzunluğu 6'ya eşit mi kontrolü
        return
    
    data=strtobin(text) #her harfin 8 bit uzunluğunda binary halinin birleşimi
    lenl=len(data) #orjinal bit uzunluğu

    A="01100111"
    B="11101111"
    C="10011000"
    D="00010000"
    #4 adet değişkenin başlangıç değeri (değişkenler değiştirilirse farklı özet değerler üretilir)
    
    n1=128 #data'nın listeye dönüştürülmeden ulaşacağı uzunluk

    data=data+"1" #data'nın sonuna "0"lar eklenmeden önce "1" eklenmesi

    data=data + "0"*(112-len(data)) #data'nın uzunluğu 112 bit olana kadar 0 ekleme

    data=data + (16-len(inttobin(lenl)))*"0"+inttobin(lenl) #orjinal uzunluğun 16 bit halde data'nın sonuna eklenmesi
    #data'nın toplam uzunluğu 128 bit oldu
    
    n=8 #data'nın kaç bitlik parçalara bölüneceği
    
    datachunk=[data[i:i+n] for i in range(0,len(data),n)] #data'nın son halini 8 bitlik parçalara bölüp listeye ekleme
    
    for i in range(16,80):
        a0,a1,a2,a3=datachunk[i-3],datachunk[i-8],datachunk[i-14],datachunk[i-16]
        d=xor(xor(xor(a0,a1),a2),a3) # d = ((datachunk[i-3] XOR datachunk[i-8]) XOR datachunk[i-14]) XOR datachunk[i-16]
        d=leftrotate(d) #sonucun bir bit sola döndürülmesi
        datachunk.append(d) #listeye yeni oluşturulan elemanın eklenmesi
    #listenin eleman sayısını 16'dan 80'e ulaştırana kadar işlem yapma

    for i in range(0,80): #listenin tüm elemanları için işlem döngüsü
        if i in range(0,20): # 0-19 indeksli elemanlar için yapılacak işlem
            F=orl(andl(B,C),andl(notl(B),D)) # F = (B AND C) OR (!B AND D)
            k="10011001" #sabit
        elif i in range(20,40): # 20-39 indeksli elemanlar için yapılacak işlem
            F=xor(xor(B,C),D) # F = B XOR C XOR D
            k="10100001" #sabit
        elif i in range(40,60): # 40-59 indeksli elemanlar için yapılacak işlem
            F=orl(orl(andl(B,C),andl(B,D)),andl(C,D)) # F = (B AND C) OR (B AND D) OR (C AND D)
            k="11011100" #sabit
        elif i in range(60,80): # 60-79 indeksli elemanlar için yapılacak işlem
            F=xor(xor(B,C),D) # F = B XOR C XOR D (2. işlemin aynısı, k sabiti farklı)
            k="11010110" #sabit

        temp=addx([leftrotate(A,5),F,D,k,datachunk[i]]) # A(5 bit left rotate) + F + D + k + 8 bitlik veri
        temp=temp[len(temp)-8:] #toplama işleminden sonra oluşan sonucun son 8 biti
        D=C
        C=leftrotate(B,30)
        B=A
        A=temp
        # döngü'ye devam etmeden önce A,B,C,D değişkenlerinin değiştirilmesi
    #döngü sonu

    #liste'deki 80 eleman üzerinden sırayla işlemler yaparak 4 adet 8 bitlik değer elde edildi
    return A+B+C+D #4 adet 8 bitlik değer birleştirilerek 32 bitlik değer döndürüldü

def menu(islem=0): #program çalıştırıldığında çalışacak ana menü fonksiyonu
    if islem==0:
        islem=int(input("Menü:\n1 - Ozet alma\n2 - Ozet dogrulama\n3 - Çıkış\nİşlem seçiniz (1-2-3): "))

    if islem==1: # özet alma seçeneği
        text=input("Özet değeri alınacak 6 karakter giriniz: ")
        if (len(text))==6: #karakter uzunluğu kontrolü
            oz=ozet(text)
            print("Özet değeri: ",oz) 
            try: #dosya oluştururken hata kontrolü
                f=open("golge.txt","w") # "golge.txt" dosyasının Write modunda açılması
            except:
                print("Dosya oluşturulamadı.") # dosya oluşturulamama hatası
            else:
                f.write(oz)
                f.close()
                print("Özet değerini içeren golge.txt oluşturuldu.")
        else:
            print("Karakter uzunluğu 6 olmalıdır")
            menu(1) #karakter uzunluğu 6 değilse tekrar giriş istenmesi

    elif islem==2: #özet doğrulama seçeneği
        text=input("Kontrol edilecek dosya adınını yazınız: ")
        try:
            f = open(text,"r") #girilen dosyanın açılması
        except:
            print(text,"açılamadı.\nYeniden giriş yapınız.")
            menu(2) #dosya açılamazsa tekrar giriş istenmesi 
            return
        else:
            satirlar=f.read().split() #dosyadaki her satırı listeye ekleme
            f.close()

        try:
            f = open("golge.txt","r") # golge.txt açılması
        except:
            print("golge.txt bulunamadı, önce özet değeri alınız.")
            menu(1) # golge.txt yoksa oluşturulması için 1. menü seçeneğinin çalıştırılması
            menu(2) # golge.txt oluşturulduktan sonra 2. menü seçeneğinin baştan çalıştırılması
            return
        else:
            kontrol=f.read() # golge.txt 'nin içeriğinin kontrol değişkenine aktarılması
            f.close()
        
        data=[[s[i:i+6] for i in range(0,len(s),6)] for s in satirlar]
        #satırlardaki yazıların 6 karakterlik parçalara bölünmesi
        dataozet=[[ozet(s[i:i+6]) for i in range(0,len(s),6)] for s in satirlar]
        #data listesindeki elemanlarının hepsinin özetinin alınması
        bulundu=False # eşleşme bulunup bulunmadığını tutan değişken
        for i,d in enumerate(dataozet): #dataozet listesinin elemanlarının indis numaraları ile birlikte döngüsü
            for j,p in enumerate(d): #dataozet listesinin içerisindeki listenin elemanlarının indis numaraları ile birlikte döngüsü
                if p==kontrol: # eşleşme kontrolü
                    print(i+1,".Satır",j+1,".Sütunda eşleşme bulundu.\nEşleşen karakterler: ",data[i][j])
                    #eşleşme olan satırın ve sütunun yazdırılması, eşleşen karakterlerin yazdırılması
                    bulundu=True
                    break
        if not bulundu: #eşleşme bulunmadıysa ekrana yazdırma
            print(text,"dosyasındaki karakterlerin özeti ile golge.txt içerisindeki özet arasında eşleşme bulunamadı.")

    elif islem==3: #çıkış seçeneği
        return
    
    else: #menüde olmayan bir işlem girilmesi
        print("Gecerli bir islem girmediniz.")
        menu() #menünün tekrar çalıştırılması
    
    return

if __name__ == "__main__": #dosya import edilmediyse çalıştırıldığında menüyü başlatma
    menu()
