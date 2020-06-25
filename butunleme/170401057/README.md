Kod çalıştırıldığında kullanıcıya özet değerini al (almak için 1'e basılması gerek) ve doğrula(almak için 2'ye basılması gerek) seçenekleri çıkar.

Eğer özet değeri al'ı seçer ise:
girdi olarak alınan değer ozet fonksiyonuna gönderilir ve bir özet değeri return edilerek golge.txt dosyasına yazılır.

Eğer kullanıcı doğrula'yı seçer ise:
girdi olarak gelen dosyanın içerisindeki her satır sırayla özet fonksiyonuna atılır ve her döngüde özet fonksiyonuna atılan girdi golge.txt ile karşılaştırılır.
Eğer aynı ise bulundu yazısı kullanıcıya gösterilip program sonlandırılır.Aksi halde bulunamadı yazısı kullanıcıya gösterilip program sonlandırılır.

# özet fonksiyonu nasıl çalışır?

Özet fonksiyonu öncelikle girdinin her basamağını ascii koduna çevirir ve çevrilen her ascii kodunu asci adında bir değişkene ekler.
Daha sonra oluşan bu asci değişkeni 64 basamağa çıkarılır ve binary'e çevrilip binAsci değişkenine atanır.
Oluşan 64 bitlik binary değeri 32 - 32 bölünür ve öncelikle bölünen iki 32 bitlik binarynin ilk sayıları xorlanıp firstXor'a atılır.
Daha sonra döngü içerisinde 31 defa bölünen 32 bitlik binary sayıların sonraki basamakları(sırayla 2 , 3...) birbirleriyle and'lenip daha sonra firstXorla xorlanır.

binAsci değişkeni ters çevirip aynı döngüye tekrar sokuyoruz ancak burdaki fark bölünen 32 bitlik binary sayıların
sonraki basamakları(sırayla 2 , 3...) birbirleriyle and'lenmez or'lanır.

En son 2  döngüden çıkan değerler birbirleriyle xor'lanır ve oluşan bu değer fonksiyona gelen girdi değerinin özetlenmiş halidir.

