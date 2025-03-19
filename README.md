## Metro Rota Simulasyonu
---
Proje
---
Bu proje, bir metro ağı üzerinde istasyonlar arasındaki en hızlı ve en az aktarmalı rotayı bulmaya yönelik bir rota planlayıcıdır. Kullanıcılar, bir başlangıç ve hedef istasyonu belirleyerek, metro hattındaki en uygun rotayı hesaplayabilirler. Hem en hızlı rota hem de en az aktarmalı rota seçenekleri sunulmaktadır.

Proje, BFS (Breadth-First Search) ve A* algoritmalarını kullanarak bu hesaplamaları yapar ve sonuçları görsel bir şekilde sunar.

![](https://komarev.com/ghpvc/?username=MahmutFurkanYildirim)
---
## Kullanılan Teknolojiler ve Kütüphaneler

- **NetworkX**: Metro ağının grafiksel olarak görselleştirilmesi için kullanılan bir kütüphanedir. Metro istasyonları ve bağlantıları bir grafik yapısına dönüştürülerek görselleştirilir.
- **Matplotlib**: NetworkX tarafından üretilen grafikleri görsel olarak sunmak için kullanılan bir kütüphanedir.
- **Collections**: Python'un deque yapısı, BFS algoritmasında kuyruğun verimli şekilde kullanılmasını sağlar.
- **Heapq**: A* algoritmasında öncelik kuyruğu (min-heap) oluşturmak için kullanılır, bu da en düşük toplam süreyi bulmamıza yardımcı olur.
- **Dict, List, Tuple, Optional**: Pythondaki çeşitli veri yapılarıdır.
    ```
    Dict: Dict genel olarak anahtar (key) ve değer (value) çiftlerini tutar.
    Örnek:
    my_dict: Dict[str, int] = {'a': 1, 'b': 2}

    List: Bir dizi elemanı tutan veri yapısını belirtir.
    Örnek:
    my_list: List[int] = [1, 2, 3, 4]

    Tuple: Sıralı ve değiştirilemez bir koleksiyon tutar. Bu koleksiyonun elemanlarının tipleri de belirtilebilir. Birden fazla veri tipi içerebilir.
    Örnek:
    my_tuple: Tuple[int, str, float] = (1, "hello", 3.14)

    Optional: Genellikle fonksiyon parametrelerinde veya dönüş değerlerinde bir değerin isteğe bağlı olduğunu belirtmek için kullanılır. Bu, değerin ya belirtilen tipte olabileceğini ya da None olabileceğini ifade eder. Optional aslında Union[X, None] şeklinde bir eşdeğeri ifade eder.
    Örnek:
    def ornek_optional(x: Optional[int]) -> None:
    if x is not None:
        print(f"Verilen değer: {x}")
    else:
        print("Değer sağlanmadı")
    ```
---