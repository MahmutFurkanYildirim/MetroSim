## Metro Rota Simulasyonu
---
Proje
---
Bu proje, bir metro ağı üzerinde istasyonlar arasındaki en hızlı ve en az aktarmalı rotayı bulmaya yönelik bir rota planlayıcıdır. Kullanıcılar, bir başlangıç ve hedef istasyonu belirleyerek, metro hattındaki en uygun rotayı hesaplayabilirler. Hem en hızlı rota hem de en az aktarmalı rota seçenekleri sunulmaktadır.

Proje, BFS (Breadth-First Search) ve A* algoritmalarını kullanarak bu hesaplamaları yapar ve sonuçları görsel bir şekilde sunar.

![](https://komarev.com/ghpvc/?username=MahmutFurkanYildirim)
---
## Kullanılan Teknolojiler ve Kütüphaneler

- Python: Proje, Python 3.x kullanılarak geliştirilmiştir.
- NetworkX: Metro ağının grafiksel olarak görselleştirilmesi için kullanılan bir kütüphanedir. Metro istasyonları ve bağlantıları bir grafik yapısına dönüştürülerek görselleştirilir.
- Matplotlib: NetworkX tarafından üretilen grafikleri görsel olarak sunmak için kullanılan bir kütüphanedir.
- Collections: Python'un deque yapısı, BFS algoritmasında kuyruğun verimli şekilde kullanılmasını sağlar.
- Heapq: A* algoritmasında öncelik kuyruğu (min-heap) oluşturmak için kullanılır, bu da en düşük toplam süreyi bulmamıza yardımcı olur.
---