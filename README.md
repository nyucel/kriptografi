# Pailler Kriptosistemi Python 3 ile uygulanışı

## Table of Contents

- [Çalışma hakkında](#about)
- [Hazırlayanlar](#getting_started)
- [Dosya dizin yapısı ve çalıştırma](#structure)



## Ödev hakkında <a name = "about"></a>

Necdet Yucel (nyucel) hocamızın verdiği Kriptografi dersinin vize ödevi olan Paillier Cryptosystem'in  python3 ile uygulanışıdır

## Hazırlayanlar <a name = "getting_started"></a>

170401009 - ATAKAN TÜRKAY

170401028 - EMİR ALİ KIVRAK


## Dosya dizin yapısı ve çalıştırma<a name = "structure"></a>

```bash
├── Paillier-Cryptosystem
│   ├── Kutuphane
|          ├── functions.py
|
├── pailler.py 
├── plaintext
├── chippertext (program calıstıgında olusacak)
├── publickey.txt (program calıstıgında olusacak)
├── privatekey.txt (program calıstıgında olusacak)
└── .gitignore
```

*Şifrelenecek metin* ana dizinde bulunan plaintext dosyasına yazılır

pailler.py dosyası içinde ana class yapıları ve ödev olan üç ana fonksiyon bulunuyor bu üç ana fonksiyon Kutuphane dizini altındaki functions.py dosyasında bulunan büyük sayılar ile baş etme ve asal sayı ile ilgili fonksiyonlardan yardım alıyor.

chippertext publickey.txt ve privatekey.txt dosyaları program çalışırken oluşturulacak.

*pailler.py* dosyasının sonunda fonksiyonlar halihazırda çağırıldığından direk pailler.py dosyasını çalıştırmak kodu çalıştıracaktır
````
keygen(1024) 
encrypt("plaintext","publickey.txt")
decyript("ciphertext","privatekey.txt")
