# Kriptografi Bütünleme



**1.** Kodun başlatılması
**2.** Özet değeri
**3.** Özeti doğrula


## Kodun Başlatılması
````
    python3 butunleme.py
````


## Özet Değeri Açıklaması

  


**1)** Kullanıcıdan alınan 6 karakterlik girdinin her harfi binarye dönüştürülür ve bir listeye atanır.Örneğin;
````
    girdi="incili"
    list=["01101001","01101110","01100011","01101001","01101100","01101001"]

    
````

**2)** Binary değerlerden oluşan liste elemanları birer bit şeklinde ayrılıp bir matris oluşturulur.
````
    girdi="incili"
    Birinci adımda oluşturulan liste: ["01101001","01101110","01100011","01101001","01101100","01101001"]
    matrix=[['0', '1', '1', '0', '1', '0', '0', '1'],
            ['0', '1', '1', '0', '1', '1', '1', '0'],
            ['0', '1', '1', '0', '0', '0', '1', '1'],
            ['0', '1', '1', '0', '1', '0', '0', '1'], 
            ['0', '1', '1', '0', '1', '1', '0', '0'], 
            ['0', '1', '1', '0', '1', '0', '0', '1']]
    
````

**3)** Oluşturulan matrisin sütunları alınarak 8 elemanlı ve her elemanı 6 bit olan binary bir liste oluşturulur. 
````
    girdi="incili"
    Birinci adımda oluşturulan liste: ["01101001","01101110","01100011","01101001","01101100","01101001"]
    İkinci adımda oluşturulan matris:
           [['0', '1', '1', '0', '1', '0', '0', '1'],
            ['0', '1', '1', '0', '1', '1', '1', '0'],
            ['0', '1', '1', '0', '0', '0', '1', '1'],
            ['0', '1', '1', '0', '1', '0', '0', '1'], 
            ['0', '1', '1', '0', '1', '1', '0', '0'], 
            ['0', '1', '1', '0', '1', '0', '0', '1']]
      
      yeni liste:  ['000000', '111111', '111111', '000000', '110111', '010010', '011000', '101101']
        
````

**4)** Oluşturulan yeni listenin her bir elemanı decimale çevrilir.
````
    
      Üçüncü adımda oluşturulan liste:  ['000000', '111111', '111111', '000000', '110111', '010010', '011000', '101101']
     
      decimal liste: [0, 63, 63, 0, 55, 18, 24, 45]
````

**5)** Decimal liste 8 elemanlıdır.Determinat hesabı yapılacağı için listeye girdinin o an ki karakterinin ascii karşılığı eklenir.Ek olarak listenin ilk
elemanına karakterin ascii karşılığı atanır.Her karakter için ayrı matrisler oluşturulur.
```
      girdi="incili"
      decimal liste: [0, 63, 63, 0, 55, 18, 24, 45]
      Karakterlerin ascii karşılıkları: i=105,n=110,c=99,i=105,l=108,i=105

      i karakteri için: [**105**, 63, 63, 0, 55, 18, 24, 45,**105**]
      n karakteri için: [**110**, 63, 63, 0, 55, 18, 24, 45,**110**]
      c karakteri için: [**99**, 63, 63, 0, 55, 18, 24, 45,**99**]
      i karakteri için: [*105*, 63, 63, 0, 55, 18, 24, 45,*105*]
      l karakteri için: [*108*, 63, 63, 0, 55, 18, 24, 45,*108*]
      i karakteri için: [*105*, 63, 63, 0, 55, 18, 24, 45,*105*]
      
````

**6)** Her karakter için oluşturulmuş bu listelerden 3x3'lük matrisler oluşturulur.Bu matrislerin determinantı hesaplanır.
Her bir determinant değeri girdi karakterlerinin ascii karşılığı ile sırasıyla xor işlemine sokulur ve her xor işleminden
sonra bulunmuş olan determinant değerinin üzerine eklenir.Daha sonra bu değer bir listeye atanır.Bu işlem tüm matrisler
için ayrı ayrı uygulanır.Kısaca açıklamak gerekirse
```
      girdi="incili"   
      Karakterlerin ascii karşılıkları: i=105,n=110,c=99,i=105,l=108,i=105

      i karakterinin matrisi: [[105, 63, 63],
                               [ 0,  55, 18],   ==> i matrisinin determinantı=465381    
                               [24,  45, 105]]
                          
       for i in girdi:
            det+=det^ord(i)
       list.append(det)     
      
````
  Yukarıdaki bu işlem adım beşte yer alan tüm listelere için uygulanır.
  
 **7)** 6.adımdaki işlemler sonucunda bir özet listesi oluşur.Bu özet listesindeki elemanlar toplanır.Çıkan değerin bit
 uzuluğuna bakılır ve gerekiyorsa değer 32 bit haline getirilir.Son olarak bu değer hexadecimale çevirilir.
 ````
    oluşan özet listesi:[29781109, 23845771, 18205579, 9284491, 3212171, 4191349]
    listenin toplamı: 88520470
    88520470 sayısı 27 bittir.
    32 bit olacak şekilde kaydırıldığında yeni değer:2832655040 olur
 
    32 bitlik yeni değerin hexadecimal karşılığı:a8d6e2c0 olur

      
````
 Bu işlemden sonra ozet değeri elde edilmiş olur ve golge.txt'ye yazılır.
 

## Özet Doğrulama İşlemi
  golge.txt dosyasından ozet değeri alınır.Kullanıcının belirttiği dosya açılır ve 6 karakter olan tüm veriler alınır.
  Tüm veriler teker teker özet değeri ile karşılaştırılır.Bulunan eşleşmeler yazdırılır.Eşleşme yoksa bu kullanıcıya 
  bir mesajla iletilir ve program sonlanır.
