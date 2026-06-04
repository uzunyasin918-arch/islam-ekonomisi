# İslam İktisadı Araştırma ve Veri Projesi

## 📌 Proje Hakkında

Bu proje, **İslam İktisadı (Islamic Economics)** ve **İslami Finans** alanındaki tüm güncel verileri, kurumları, araştırmacıları, yayınları, konferansları ve terminolojiyi kapsamlı şekilde inceleyen bir bilgi ve analiz platformudur.

## 🎯 Amaç

- İslam iktisadı alanındaki akademik çalışmaları derlemek
- Faaliyet gösteren kurumları (bankalar, enstitüler, merkezler) haritalandırmak
- Önde gelen araştırmacıları ve yayınlarını kataloglamak
- Güncel konferans ve etkinlikleri takip etmek
- Temel kavramları ve terminolojiyi açıklamak
- Veri analizi ve görselleştirme yapmak

## 📂 Proje Yapısı

```
islam-ekonomisi/
├── data/                     # Veri dosyaları
│   ├── kurumlar/            # Kurum veritabanı
│   ├── arastirmacilar/      # Araştırmacı profilleri
│   ├── yayinlar/            # Yayın kataloğu
│   ├── konferanslar/        # Konferans ve etkinlikler
│   ├── veriler/             # İstatistiksel veriler
│   └── terminoloji/         # Kavram sözlüğü
├── scraper/                 # Web scraper modülleri
├── analysis/                # Veri analizi araçları
├── scripts/                 # Yardımcı scriptler
├── web/                     # Web arayüzü
│   ├── css/
│   └── js/
├── docs/                    # Dokümantasyon
└── README.md
```

## 🚀 Kullanım

### Web Arayüzü
```bash
cd web && python3 -m http.server 8000
```

### Veri Analizi
```bash
python3 analysis/analiz.py
```

### Scraper Çalıştırma
```bash
python3 scraper/scraper.py
```

## 📊 Veri Kaynakları

- Akademik dergiler (JKAU: Islamic Econ., IJIE, ISRA JIMF, vb.)
- Merkez bankaları ve regülatörler
- İslami finans kuruluşları (AAOIFI, IFSB, CIBAFI)
- Üniversite araştırma merkezleri
- Uluslararası konferans bildirileri

## 🔄 Güncelleme

Proje düzenli olarak güncellenmektedir. Güncel veriler için `scripts/guncelle.sh` scriptini kullanabilirsiniz.

## 📝 Lisans

Akademik araştırma amaçlı kullanım için açık kaynak.