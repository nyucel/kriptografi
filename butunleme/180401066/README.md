# Kriptografi Bütünleme Ödevi

### Kullanım

* Program çalıştırıldığında aşağıdaki menüden bir işlem numarası girmeniz gerekir.
```
Menü:
1 - Ozet alma
2 - Ozet dogrulama
3 - Çıkış
İşlem seçiniz (1-2-3):
```
1 - 2 - 3 seçeneklerinden biri girilmelidir.

##### 1 - Özet alma

```
Menü:
1 - Ozet alma
2 - Ozet dogrulama
3 - Çıkış
İşlem seçiniz (1-2-3): 1
Özet değeri alınacak 6 karakter giriniz:
```
6 karakterlik bir girdi girilmesi beklenmektedir.
Eğer farklı uzunlukta girdi girilirse tekrar girdi istenir.

6 karakter girildiğinde program aşağıdaki çıktıları verip golge.txt dosyasına özet değerini yazar ve son bulur.

```
Özet değeri alınacak 6 karakter giriniz: 421322
Özet değeri:  11110000101000101010110001001100
Özet değerini içeren golge.txt oluşturuldu.
```

##### 2 - Özet doğrulama
Özet doğrulama işleminin gerçekleşmesi için önceden golge.txt dosyası oluşturulmuş olmalıdır. Eğer golge.txt mevcut değilse program 1 - Özet alma işlemini başlatır.
Eğer golge.txt mevcutsa kullanıcıdan bir dosya girmesi beklenir.
```
İşlem seçiniz (1-2-3): 2
Kontrol edilecek dosya adınını yazınız: deneme.txt
```
Dosya bulunamadıysa tekrar dosya adı girme işlemi başlatılır.
Eğer dosya mevcutsa eşleşme kontrolü başlar.

örnek deneme.txt içeriği:
```
asdljodenemeljflkasglkşadg
asdlkjıgklxzcvklxzvkzxşlvas
lkj43wjklweklrfjdsxv8923jısdklgsd
dslkmjgvlksjdjoılk325rklsdakljfaşlkdsg
```
golge.txt içeriği "deneme" girdisinin özeti olduğunda eşleşme bulunacağı için aşağıdaki çıktıyı verir.
```
Kontrol edilecek dosya adınını yazınız: deneme.txt
1 .Satır 2 .Sütunda eşleşme bulundu.
Eşleşen karakterler:  deneme
```

golge.txt dosyasının içeriği "kripto" kelimesinin özeti olduğunda eşleşme bulunmayacağı için aşağıdaki çıktıyı verir.
```
Kontrol edilecek dosya adınını yazınız: deneme.txt
deneme.txt dosyasındaki karakterlerin özeti ile golge.txt içerisindeki özet arasında eşleşme bulunamadı.
```

### Çalışma
butunleme.py dosyası içerisinde yazdığım tüm fonksiyon ve kodların açıklamasını yorum satırı olarak açıkladım.

2 - Özet doğrulama kısmında girilen dosyayı önce satırlara bölüp listeye ekliyor, daha sonra bu listeleri 6 karakterlik parçalara bölüp iç içe listeler oluşturuyor.
Kontrolü bu 6 karakterlik parçaların özet değerleri ile yapıyor.
Ekran çıktısı olarak belirttiği satır sütun numaraları eşleşen özet değerinin dosyanın kaçıncı satırının kaçıncı parçası olduğunu gösteriyor. 

Örnek:
deneme.txt içeriği:

```
asdljodenemeljflkasglkşadg
asdlkjıgklxzcvklxzvkzxşlvas
lkj43wjklweklrfjdsxv8923jısdklgsd
dslkmjgvlksjdjoılk325rklsdakljfaşlkdsg
```

Parçalanmış hali:

```
[['asdljo', 'deneme', 'ljflka', 'sglkÅŸ', 'adg'], 
['asdlkj', 'Ä±gklx', 'zcvklx', 'zvkzxÅ', 'Ÿlvas'], 
['lkj43w', 'jklwek', 'lrfjds', 'xv8923', 'jÄ±sdk', 'lgsd'], 
['dslkmj', 'gvlksj', 'djoÄ±l', 'k325rk', 'lsdakl', 'jfaÅŸl', 'kdsg']]
```