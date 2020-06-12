# -*- coding: UTF-8 -*-

#170401009 - ATAKAN TÜRKAY
from Kütüphane import functions as kutuphane
from os import path,mkdir,getcwd,chdir
import pickle     #Değişkenleri dosya içerisine dump ederek kaydediyoruz.


def keygen(bit_sayisi):
    kutuphane.anahtar_cifti_olustur(bit_sayisi)  #Anahtar çifti oluşturuluyor.
    with open("publickey.txt", "wb+") as f:      #keylerimizi binary olarak depoluyoruz.O yüzden wb olarak açtık
        pickle.dump(kutuphane.depolayici['n'],f) #write public key
        pickle.dump(kutuphane.depolayici['g'],f) #write public key   
        f.close()
    with open("privatekey.txt", "wb+") as f:       
        pickle.dump(kutuphane.depolayici['n'],f)        #write private key
        pickle.dump(kutuphane.depolayici['lambda'],f)   #write private key
        pickle.dump(kutuphane.depolayici['nü'], f)      #write private key
        f.close()

def encrypt(plaintext,publickey):
    try:
        f = open("publickey.txt")
        d = open("privatekey.txt")
    except IOError:
        print("Privatekey veya publickey bulunamadı lütfen keygen fonksiyonunu çalıştırın.")
        return
    temp_file=0                                         #plaintext içerisindeki verinin int haline dönüştürülmüş versiyonunu tutacak.
    with open(publickey, "rb") as f:                    #verileri dictionary içine kaydediyoruz.
        kutuphane.depolayici['n']=pickle.load(f)        #verileri dictionary içine kaydediyoruz.
        kutuphane.depolayici['g']=pickle.load(f)        #verileri dictionary içine kaydediyoruz.
        kutuphane.depolayici['nkare']=kutuphane.depolayici['n']**2  #nkare nin depolanması işlemleri hızlandırıyor. 
                                                                    #Çünkü nkare fazla kere hesaplanması gereken bir değer. Ve her defasında hesaplamak yavaşlatıyor.
        f.close()
    with open(plaintext,"r") as f:
        temp_file=kutuphane.string_to_int(f.read())     #plaintext içerisindeki verinin int haline dönüştürülmesi.
        print("!!!INFO==>Okunan değer =>",temp_file)
        temp_file=kutuphane.encrypt_helper(temp_file)   #ENCYRPT işlemi
        f.close()
    with open("ciphertext", "w+") as f:
        f.write(str(temp_file))                         #işlem bitince ciphertext olarak kaydediyor.
        f.close()

def decyript(ciphertext,privatekey):
    temp_file=0
    try:
        f = open("publickey.txt")
        d = open("privatekey.txt")
    except IOError:
        print("Privatekey veya publickey bulunamadı lütfen keygen fonksiyonunu çalıştırın.")
        return
        
    with open(privatekey, "rb") as f:
        kutuphane.depolayici['n']=pickle.load(f)        #verileri dictionary içine kaydediyoruz.
        kutuphane.depolayici['lambda']=pickle.load(f)   #verileri dictionary içine kaydediyoruz.
        kutuphane.depolayici['nü'] = pickle.load(f)     #verileri dictionary içine kaydediyoruz.
        kutuphane.depolayici['nkare']=kutuphane.depolayici['n']**2  #nkare nin depolanması işlemleri hızlandırıyor. 
        f.close()
    with open(ciphertext,"r") as f:
        temp_file=int(f.read())
        print("!!!INFO==>Okunan değer =>",temp_file)
        temp_file=kutuphane.decrypt_helper(temp_file)   #DECYRPT
        f.close()
    with open("plaintext2", "w+") as f:
        f.write(kutuphane.int_to_string(temp_file))
        f.close()
    kutuphane.kontrol()                                 #dosyaların özdeşliği kontrolü








keygen(1024)
encrypt("plaintext","publickey.txt")
decyript("ciphertext","privatekey.txt")
