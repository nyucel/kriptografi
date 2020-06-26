#Gizem Özgün / 160401007

# -*- coding: utf-8 -*-
import sys
 

def str_to_binary(string):      #string'i binary'e ceviren fonksiyon

    binary = ""
    for i in string:
        binary += "".join(f"{ord(i):08b}")
    return binary


def binary_to_dec(binary):      #binary'i decimale ceviren fonksiyon

    binary=str(binary)[::-1]
    decimal,index = 0,0
    for i in binary:
        decimal+=pow(2,index)*int(i)
        index+=1
    return decimal


def decimal_to_hex(decimal) :   #decimali hexadecimale ceviren fonksiyon
    hexa = hex(decimal)
    return hexa


def hex_to_ascii(hex):          #hexadecimale cevrilen her bir karakteri asciiye ceviren fonksiyon
    ascii = list()
    for h in hex[2:]:
        ascii.append(ord(h))
    return ascii

def get_bit_length(n):          #bit uzunlugunu bulan fonksiyon
    bit=0
    while (n):
        n >>= 1
        bit += 1
    return bit

def ozet(string):
    asci_list = list()
    ozet=1
    for i in string :
             binary = str_to_binary(i)
             decimal = binary_to_dec(binary)
             hexa = decimal_to_hex(decimal)
             asci_list += hex_to_ascii(hexa)
    for i in asci_list:
        ozet *= i
    
    #ozet 32 bit olana kadar kaydırılıyor.
    while get_bit_length(ozet)!=32:
        if get_bit_length(ozet)<32:
            ozet=ozet<<1

        else:
            ozet=ozet>>1
    return ozet


def menu():
    secenek = input("Uygulamak istediginiz secenegin numarasini  giriniz:\n Menu:\n1 - Ozet alma\n2 - Ozet dogrulama\n3 - Cikis\n ")
    if secenek == "1": 
        value = input("Ozet degeri alinacak 6 karakterlik bir girdi giriniz:")
        if len(value)==6:  
             golge = open("golge.txt","w")
             golge.write(str(ozet(value)))         #girilen karakter ozet_alma fonksiyonuna gonderilip ozet deger golge.txt'e yaziliyor
             golge.close() 
             print("golge.txt olusturuldu")
        else:
             print("Lutfen 6 karakter uzunlugunda bir girdi giriniz.")
             menu()

    elif secenek == "2": 
        value = input("Kontrol etmek istediginiz dosya adini giriniz:")
        try:
            new_file= open(value, 'r')              #kullanicinin girdigi dosya okunuyor
            golge = open('golge.txt', 'r')          #golge.txt aciliyor
            golge_ozet= golge.read()
            for i in new_file:
                new_ozet= ozet(i)               #yeni dosya ve golgenin icerigi karsilastiriliyor
                if(new_ozet == golge_ozet):
                    print("Eslesen deger: " + new_ozet)
                    golge.close()
                    new_file.close()
                    break
                else:
                    print("Eslesen deger bulunamadi")
        except:
            print("dosya hatasi")

            

    elif secenek == "3":
        print("Cikis yapiliyor")
        sys.exit()

    else:
        print("Lutfen menude olan gecerli rakamlardan birini girin!")
        menu()

if __name__ == "__main__":
    menu()
