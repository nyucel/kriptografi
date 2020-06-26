# -*- coding: utf-8 -*-
#Fahrettin Orkun İncili - 150401013

import sys

def menu():

    print("""
    
            1-) Özet al.
            2-) Özeti doğrula.
    """)
    choice=input("Hangi işlemi yapmak istiyorsunuz?:")

    if choice=="1":

        value=input("6 karakterlik girdiniz:")

        if len(value)==6:

            write_to_file(ozet(value))
        else:
            print("""***UYARI:Girdi 6 karakterden oluşmalıdır.***
            """)
            menu()
    elif choice=="2":
        file=input("Özet değeri doğrulaması için dosyanın adını ya da tam yolunu yazınız:")
        verify(file)
    else:
        print("***Geçersiz seçim.***")
        menu()

def write_to_file(ozet):
    """parametre olarak verilen değeri dosyaya yazan fonksiyon"""
    with open("golge.txt","w") as file:
        file.write(ozet)
    print("golge.txt oluşturuldu.")

def string_to_binary(string):
    """string'i binary'e çevirip bu değeri döndüren fonksiyon"""
    binary = ""
    for i in string:
        binary += "".join(f"{ord(i):08b}")
    return binary

def binary_to_decimal(binary):
    """binary değeri decimale çeviren fonksiyon"""
    binary=str(binary)[::-1]
    decimal,index = 0,0
    for i in binary:
        decimal+=pow(2,index)*int(i)
        index+=1
    return decimal
def create_matrix(list):
    "parametre olarak gönderilen listeyi matrise çeviren fonksiyon"
    matrix = [[i for i in j] for j in list]
    return matrix

def det(matrix):
    """Sıfırıncı satır için 3x3'lük matrisin determinantını döndüren fonksiyon
       a b c
       d e f =>  det=|A|=(e*i-f*h)*a + (-(d*i-f*g)*b) + (d*h-e*g)*c
       g h i              cofactorA  |     cofactorB   |   cofactorC
       cofactor0=minor0,cofactor1=-minor1,cofactor2=minor2
    """
    a,b,c=matrix[0]
    cofactorA = (matrix[1][1]*matrix[2][2]-matrix[1][2]*matrix[2][1])*a
    cofactorB = -(matrix[1][0]*matrix[2][2]-matrix[1][2]*matrix[2][0])*b
    cofactorC = (matrix[1][0]*matrix[2][1]-matrix[1][1]*matrix[2][0])*c



    return cofactorA+cofactorB+cofactorC

def bit_length(n):
    """negatif olmayan bir tamsayının bit boyutunu döndürür
       https://stackoverflow.com/questions/2654149/bit-length-of-a-positive-integer-in-python"""
    bits = 0
    while n >> bits: bits += 1
    return bits
def ozet(value):
    value_list=list()
    for i in value:
        """parametre olarak gönderilen 6 karakterlik girdinin her karakterini ayrı ayrı binarye çevirip
        bir listeye atıyorum"""
        value_list.append(string_to_binary(i))

    """oluşan her bit değerini ayırıp matrise yerleştiriyorum."""
    matrix=create_matrix(value_list)
    value_list.clear()

    """oluşan matriste her sütünu bir 8 bitlik binary değer olarak alıp tekrar listeye atıyorum"""
    for i in range(8):
        col_binary = ""
        for j in range(6):
            col_binary+=matrix[j][i]
        value_list.append(col_binary)
    """oluşan yeni binary listesindeki her değeri decimale çevirip decimal_list'e atıyorum."""
    decimal_list = list()
    for i in value_list:
        decimal_list.append(binary_to_decimal(i))
    """sütunlardan yeni decimal değerler ürettiğim için yeni listenin boyutu 8 oldu.
    Bu listeyi 9 elemana tamamlayıp 3x3'lük matris oluşturabilmek için listenin sonuna sırayla
    girdideki her bir karakteri ascii değerini ekledim.Aynı işlemi listenin ilk elemanına da yaptım."""
    ozet_list = list()
    for j in range(6):
        if j!=0:
            """girdinin her bir karakteri için farklı matris oluşturulduğundan her seferinde
            matrisin son ve ilk elemanı işlem sırasındaki karakterin ascii değeriyle değiştiriliyor."""
            decimal_list.remove(decimal_list[-1])

        decimal_list.append(ord(value[j]))#listenin sonuna işlem sırasındaki karakterin asci değerinin eklendiği yer
        decimal_list[0]=ord(value[j])#ilk elemana işlem sırasındaki karakteri ascii değerinin eklendiği yer

        #oluşan listeyi 3x3lük matrise dönüştürüyorum.
        random_letters_matrix = [[decimal_list[i] for i in range(j * 3, (j * 3) + 3)] for j in range(3)]
        #oluşan matrisin determantı hesaplanıyor.
        determinant_result=det(random_letters_matrix)
        """oluşturulan her matrisin determinant değeri girdi karakterlerinin ascii değerleri ile sırasıyşa
        xorlanıyor ve bu değerler toplanıyor.Çıkan sonuç listeye ekleniyor.
        Bu işlem her karakter için yapılıyor."""
        for i in value:
            determinant_result+=determinant_result^ord(i)


        ozet_list.append(abs(determinant_result))
    ozet_sum=sum(ozet_list)


    ozet_length=bit_length(ozet_sum)

    """özet değerini 32 bit olacak şekilde kaydırıyorum"""
    if ozet_length>32:
        ozet_sum=ozet_sum>>(ozet_length-32)
    elif ozet_length<32:
        ozet_sum=ozet_sum<<(32-ozet_length)

    return hex(ozet_sum)[2:]
def verify(file):
    try:
        with open("golge.txt", "r") as golge:
            ozet_degeri = golge.read()
    except Exception:
        print("""
            ***Lütfen önce herhangi bir girdinin özetini oluşturunuz.
            (golge.txt bulunamadı)***
            """)
        menu()
    try:
        with open(file,"r") as check:
            data=check.read().split()
        for d in data:
            if len(d) == 6:
                if ozet_degeri == ozet(d):
                    print("Dosyadaki '{}' değerinin özeti girdinin özet değeri ile eşleşiyor.".format(d))
    
    except Exception:
        print("***Dosya bulunamadı.***")
        menu()


menu()

