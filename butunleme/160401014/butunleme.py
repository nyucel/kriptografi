#Selin KURT 160401014

def string_to_binary(string):
  
    binary = ""
    for i in string:
        binary += "".join(f"{ord(i):08b}")
    return binary

def xor(x, y):
    ans = ""
    for i in range(len(x)):
        if x[i] == "0" and y[i] == "1" or x[i] == "1" and y[i] == "0":
            ans += "1"
        else:
            ans += "0"
    return ans

def ozet_al(veri):
    bin_veri = string_to_binary(str(veri))

    #binary e çevrilen 48 bitlik veri a,b,c,d olarak 4 parçaya bölünüyor
    a = bin_veri[0:12]
    b = bin_veri[12:24]
    c = bin_veri[24:36]
    d = bin_veri[36:48]

    #a,b,c,d parçalarına kendi aralarında xor işlemi uygulanır
    a = xor(b, c)
    b = xor(c, d)
    c = xor(d, a)
    d = xor(b, c)

    #a,b,c,d parçalarından 32 bitlik bir özet değeri elde edilir
    bin_ozet = a+c+b[0:4]+d[4:8]
#    print("binary ozet", bin_ozet, len(bin_ozet))
    
    ozet = hex(int(bin_ozet, 2))
    hex_ozet = ozet[2:]
    while(len(hex_ozet)<8): #ilk karakter 0 ise gözükmeyeceği için tekrar ekliyorum
        hex_ozet = '0'+hex_ozet
    
    dosya = open('golge.txt', 'w')
    dosya.write(hex_ozet)
    dosya.close()
    
    return hex_ozet

islem = int(input("Ozet degeri almak icin 1'e, dogrulama islemi icin 2'ye basiniz: "))

if(islem==1):
    veri = input("Bir veri giriniz: ")
    print(ozet_al(veri))

elif(islem==2):
    dosya_adi = input("Dosya adi giriniz: ")
    try:
        f = open(dosya_adi, "r")
        dizi = f.readlines()
        dosya = open("golge.txt", "r")
        golge = dosya.read()
        dosya.close()
        for satir in dizi:
            ozet_degeri = ozet_al(satir[:-1])
            if(golge==ozet_degeri):
                print(satir[:-1], "ozet degeri golge.txt ile eslesti !!!")
            
            else:
                print(satir[:-1], "icin eslesme yok")
    except:
        print("Dosya ile ilgili bir hata olustu")
    finally:
        f.close()
