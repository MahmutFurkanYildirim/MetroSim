from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional
import networkx as nx
import matplotlib.pyplot as plt

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))

    def __lt__(self, other):
        # İstasyonları sıralamak için bir kriter belirledik. idx'yi baz aldik
        return self.idx < other.idx

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if id not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)

    def metro_grafik(self, rota=None):
        # Burada 'self' kullanarak metro nesnesine erişebilirsiniz
        G = nx.Graph()
        
        # Metro'yu ve bağlantılarını ekle
        for istasyon in self.istasyonlar.values():
            for komsu, _ in istasyon.komsular:
                G.add_edge(istasyon.ad, komsu.ad)
        
        pos = nx.kamada_kawai_layout(G)
        plt.figure(figsize=(10, 6))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
        
        if rota:
            rota_edges = [(rota[i].ad, rota[i+1].ad) for i in range(len(rota)-1)]
            nx.draw_networkx_edges(G, pos, edgelist=rota_edges, edge_color='red', width=2)
        
        plt.show()
    
    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        # Başlangıç ve hedef istasyonların varlığını kontrol et
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
        
        # İstasyon nesnelerini al
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        # Başlangıç istasyonu hedef istasyonsa, döndür
        if baslangic == hedef:
            return [baslangic]
        
        # BFS kuyruk yapısını oluştur
        kuyruk = deque([(baslangic, [baslangic])])

        # Ziyaret edilen istasyonları takip et
        ziyaret_edildi = {baslangic}   

        # BFS algoritmasi ile en az aktarmali rotayı bul
        while kuyruk:

            # Kuyruğun başındaki istasyonu ve rotayı al
            aktif_istasyon, rota = kuyruk.popleft()

            # Mevcut istasyonun tüm komşularını incele
            for komsu_istasyon, _ in aktif_istasyon.komsular:

                # Eğer komşu daha önce ziyaret edilmediyse
                if komsu_istasyon not in ziyaret_edildi:

                    # Komşu hedef istasyonsa, rotayı tamamla ve döndür
                    if komsu_istasyon == hedef:
                        return rota + [komsu_istasyon]
                    
                    # Değilse, komşuyu ziyaret edildi olarak işaretle ve kuyruğa ekle
                    ziyaret_edildi.add(komsu_istasyon)
                    kuyruk.append((komsu_istasyon, rota + [komsu_istasyon]))
        return None

             


    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        # Başlangıç ve hedef istasyonların varlığını kontrol et
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        # İstasyon nesnelerini al
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        # Başlangıç istasyonu hedef istasyonsa, hemen döndür
        if baslangic == hedef:
            return ([baslangic],0)
        
        # A* için öncelik kuyruğu: (toplam_tahmini_sure, unique_id, istasyon, rota, toplam_sure)
        # unique_id: Aynı tahmini süreye sahip istasyonları ayırt etmek için
        oncelik_kuyrugu = [(0, id(baslangic), baslangic, [baslangic],0)]

        # Ziyaret edilen istasyonlar ve en kısa süreleri
        ziyaret_edildi = {}

        # Öncelik kuyruğu boş olana kadar devam et
        while oncelik_kuyrugu:
            # En düşük tahmini süreye sahip elemanı kuyruktan çıkar
            toplam_sure, id_istasyon, aktif_istasyon, rota, toplam_tahmini_sure = heapq.heappop(oncelik_kuyrugu)

            # Eğer hedefe ulaştıysak, rotayı ve toplam süreyi döndür
            if aktif_istasyon == hedef:
                return(rota, toplam_sure)
            
            # Eğer bu istasyona daha önce daha kısa bir sürede ulaştıysak, bu yolu atla
            if aktif_istasyon in ziyaret_edildi and ziyaret_edildi[aktif_istasyon] <= toplam_sure:
                continue
            # İstasyonu ziyaret edildi olarak işaretle ve süresini kaydet
            ziyaret_edildi[aktif_istasyon] = toplam_sure

            # Aktif istasyonun tüm komşularını kontrol et
            for id_istasyon, gecis_suresi in aktif_istasyon.komsular:
                # Komşuya ulaşma süresini hesapla
                toplam_tahmini_sure = toplam_sure + gecis_suresi

                # Eğer komşuya daha önce daha kısa bir sürede ulaştıysak, bu yolu atla
                if id_istasyon in ziyaret_edildi and ziyaret_edildi[id_istasyon] <= toplam_tahmini_sure:
                    continue

                # Hedefe olan tahmini kalan süreyi hesapla (heuristik)
                tahmini_kalan = 0  #Şu an için basit bir değer, iyileştirilebilir

                # Toplam tahmini süreyi hesapla (şimdiye kadarki süre + tahmini kalan süre)
                toplam_tahmini = toplam_tahmini_sure + tahmini_kalan

                 # Yeni rotayı oluştur (mevcut rota + komşu istasyon)
                yeni_rota = rota + [id_istasyon]

                # Yeni durumu öncelik kuyruğuna ekle
                heapq.heappush(oncelik_kuyrugu, (toplam_tahmini, id(id_istasyon), id_istasyon, yeni_rota, toplam_tahmini_sure))
        # Eğer hedef istasyona ulaşan bir rota bulunamazsa None döndür
        return None
                



# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    metro.istasyon_ekle("K5", "TCDD", "Kırmızı Hat")
    metro.istasyon_ekle("K6", "Sincan", "Kırmızı Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    metro.istasyon_ekle("M5", "Demirlibahçe", "Mavi Hat")
    metro.istasyon_ekle("M6", "Tandoğan", "Mavi Hat")
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    metro.istasyon_ekle("T5", "Bağlum", "Turuncu Hat")
    metro.istasyon_ekle("T6", "Şehitler", "Turuncu Hat")
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    metro.baglanti_ekle("K4", "K5", 10)  # OSB -> TCDD
    metro.baglanti_ekle("K5", "K6", 12)  # TCDD -> Sincan
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    metro.baglanti_ekle("M4", "M5", 8)  # Gar -> Demirlibahçe
    metro.baglanti_ekle("M5", "M6", 6)  # Demirlibahçe -> Tandoğan
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    metro.baglanti_ekle("T4", "T5", 9)  # Keçiören -> Bağlum
    metro.baglanti_ekle("T5", "T6", 7)  # Bağlum -> Şehitler
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma
    metro.baglanti_ekle("M1", "M5", 3)  # AŞTİ -> Demirlibahçe
    metro.baglanti_ekle("T3", "M6", 4)  # Gar -> Tandoğan
    metro.baglanti_ekle("K2", "M3", 4)  # Ulus -> Sıhhiye
    metro.baglanti_ekle("M5", "T4", 5)  # Demirlibahçe -> Keçiören
    metro.baglanti_ekle("T1", "M6", 6)  # Batıkent -> Tandoğan
    metro.baglanti_ekle("T5", "K4", 3)  # Bağlum -> OSB
    metro.baglanti_ekle("M2", "T6", 7)  # Kızılay -> Şehitler
    
    # Test senaryoları
    print("\n=== Test Senaryoları ===")
    
    # Senaryo 1: AŞTİ'den Sincan'a
    print("\n1. AŞTİ'den Sincan'a:")
    rota = metro.en_az_aktarma_bul("M1", "K6")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
        metro.metro_grafik(rota)
    
    sonuc = metro.en_hizli_rota_bul("M1", "K6")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
        metro.metro_grafik(rota)
    
    # Senaryo 2: Batıkent'ten Şehitler'e
    print("\n2. Batıkent'ten Şehitler'e:")
    rota = metro.en_az_aktarma_bul("T1", "T6")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
        metro.metro_grafik(rota)
    
    sonuc = metro.en_hizli_rota_bul("T1", "T6")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
        metro.metro_grafik(rota)
    
    # Senaryo 3: Şehitler'den Tandoğan'a
    print("\n3. Şehitler'den Tandoğan'a:")
    rota = metro.en_az_aktarma_bul("T6", "M6")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
        metro.metro_grafik(rota)
    
    sonuc = metro.en_hizli_rota_bul("T6", "M6")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
        metro.metro_grafik(rota)

    
  