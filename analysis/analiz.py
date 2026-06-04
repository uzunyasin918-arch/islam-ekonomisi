#!/usr/bin/env python3
"""
İslam İktisadı Araştırma ve Veri Projesi - Analiz Aracı
Tüm veri dosyalarını okuyup özet istatistikler ve raporlar üretir.
"""

import json
import os
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

def json_oku(dosya_yolu):
    with open(dosya_yolu, 'r', encoding='utf-8') as f:
        return json.load(f)

def kurum_analizi():
    """Kurum verilerini analiz eder"""
    dosya = DATA_DIR / "kurumlar" / "islami-finans-kurumlari.json"
    veri = json_oku(dosya)
    
    kurumlar = veri["kurumlar"]
    
    print("=" * 60)
    print("🏛️  İSLAMİ FİNANS KURUMLARI ANALİZİ")
    print("=" * 60)
    print(f"\nToplam Kurum: {len(kurumlar)}")
    
    tur_dagilimi = {}
    ulke_dagilimi = {}
    aktif_sayisi = 0
    
    for k in kurumlar:
        tur = k.get("tur", "Bilinmeyen")
        tur_dagilimi[tur] = tur_dagilimi.get(tur, 0) + 1
        
        for ulke in k.get("ulkeler", []):
            ulke_dagilimi[ulke] = ulke_dagilimi.get(ulke, 0) + 1
        
        if k.get("guncel_durum") == "Aktif":
            aktif_sayisi += 1
    
    print(f"Aktif Kurum: {aktif_sayisi}")
    print(f"\n📊 Tür Dağılımı:")
    for tur, sayi in sorted(tur_dagilimi.items(), key=lambda x: -x[1]):
        print(f"   {tur}: {sayi}")
    
    print(f"\n🌍 Ülke Dağılımı:")
    for ulke, sayi in sorted(ulke_dagilimi.items(), key=lambda x: -x[1]):
        print(f"   {ulke}: {sayi}")
    
    return veri

def zekat_analizi():
    """Zekat kurumları analizi"""
    dosya = DATA_DIR / "kurumlar" / "zekat-kurumlari.json"
    veri = json_oku(dosya)
    
    kurumlar = veri["kurumlar"]
    
    print("\n" + "=" * 60)
    print("💰 ZEKAT KURUMLARI ANALİZİ")
    print("=" * 60)
    print(f"\nToplam Zekat Kuruluşu: {len(kurumlar)}")
    print(f"   Türkiye merkezli: {veri['istatistikler']['turkiye_merkezli']}")
    print(f"   Dijital platform: {veri['istatistikler']['dijital_platform']}")
    print(f"   Küresel kuruluş: {veri['istatistikler']['kuresel_kurulus']}")
    print(f"\n💰 Potansiyel Zekat Piyasası: {veri['istatistikler']['yillik_zekat_potansiyeli_tahmini']}")
    print(f"💵 Toplanan Zekat: {veri['istatistikler']['gunumuzde_toplanan_zekat']}")
    
    return veri

def yatirim_analizi():
    """Helal yatırım araçları analizi"""
    dosya = DATA_DIR / "veriler" / "helal-yatirim-araclari.json"
    veri = json_oku(dosya)
    
    araclar = veri["yatirim_araclari"]
    
    print("\n" + "=" * 60)
    print("📈 HELAL YATIRIM ARAÇLARI ANALİZİ")
    print("=" * 60)
    print(f"\nToplam Yatırım Aracı: {len(araclar)}")
    
    kategori_dagilimi = {}
    risk_dagilimi = {}
    
    for a in araclar:
        kat = a.get("kategori", "Bilinmeyen")
        kategori_dagilimi[kat] = kategori_dagilimi.get(kat, 0) + 1
        
        risk = a.get("risk_seviyesi", "Bilinmeyen")
        risk_dagilimi[risk] = risk_dagilimi.get(risk, 0) + 1
    
    print(f"\n📊 Kategori Dağılımı:")
    for kat, sayi in sorted(kategori_dagilimi.items(), key=lambda x: -x[1]):
        print(f"   {kat}: {sayi}")
    
    print(f"\n⚠️  Risk Seviyesi Dağılımı:")
    for risk, sayi in sorted(risk_dagilimi.items(), key=lambda x: -x[1]):
        print(f"   {risk}: {sayi}")
    
    print(f"\n🌍 Küresel İstatistikler:")
    istatistikler = veri.get("istatistikler", {})
    for key, val in istatistikler.items():
        print(f"   {key}: {val}")
    
    print(f"\n📋 Servet Koruma Stratejileri:")
    for s in veri.get("servet_koruma_stratejileri", []):
        print(f"   🟢 {s['strateji']}: {s['aciklama'][:100]}...")
    
    return veri

def arastirmaci_analizi():
    """Araştırmacı verilerini analiz eder"""
    dosya = DATA_DIR / "arastirmacilar" / "arastirmacilar.json"
    veri = json_oku(dosya)
    
    arastirmacilar = veri["arastirmacilar"]
    
    print("\n" + "=" * 60)
    print("👨‍🔬 ARAŞTIRMACI ANALİZİ")
    print("=" * 60)
    print(f"\nToplam Araştırmacı: {len(arastirmacilar)}")
    print(f"   Türkiyeli: {veri['istatistikler']['turkiyeli']}")
    print(f"   Küresel: {veri['istatistikler']['kuresel']}")
    print(f"   Aktif: {veri['istatistikler']['aktif_calisan']}")
    
    print(f"\n📚 Öne Çıkan Araştırmacılar:")
    for a in arastirmacilar[:5]:
        eser = a.get("onemli_eserler", [])
        eser_str = eser[0] if eser else "-"
        print(f"   👤 {a['ad']} ({a['ulke']})")
        print(f"      📌 {a['alan']}")
        print(f"      📖 Önemli Eser: {eser_str}")
    
    return veri

def surdurulebilirlik_analizi():
    """Sürdürülebilirlik projeleri analizi"""
    dosya = DATA_DIR / "veriler" / "surdurulebilirlik-projeleri.json"
    veri = json_oku(dosya)
    
    projeler = veri["projeler"]
    
    print("\n" + "=" * 60)
    print("🌱 SÜRDÜRÜLEBİLİRLİK PROJELERİ ANALİZİ")
    print("=" * 60)
    print(f"\nToplam Proje: {len(projeler)}")
    print(f"   Türkiye: {veri['istatistikler']['turkiye_projeleri']}")
    print(f"   Küresel: {veri['istatistikler']['kuresel_projeler']}")
    
    tur_dagilimi = {}
    for p in projeler:
        tur = p.get("tur", "Bilinmeyen")
        tur_dagilimi[tur] = tur_dagilimi.get(tur, 0) + 1
    
    print(f"\n📊 Proje Türleri:")
    for tur, sayi in sorted(tur_dagilimi.items(), key=lambda x: -x[1]):
        print(f"   {tur}: {sayi}")
    
    return veri

def terminoloji_ozeti():
    """Terminoloji özeti"""
    dosya = DATA_DIR / "terminoloji" / "islam-iktisadi-terimleri.json"
    veri = json_oku(dosya)
    
    terimler = veri["terimler"]
    kategoriler = veri["kategori_index"]
    
    print("\n" + "=" * 60)
    print("📖 İSLAM İKTİSADI TERMİNOLOJİ ÖZETİ")
    print("=" * 60)
    print(f"\nToplam Terim: {len(terimler)}")
    
    print(f"\n📂 Kategoriler:")
    for kat, liste in kategoriler.items():
        print(f"   {kat}: {', '.join(liste[:5])}")
    
    return veri

def tum_rapor():
    """Tüm veri setlerini analiz edip kapsamlı rapor üretir"""
    print("=" * 60)
    print("📊 İSLAM İKTİSADI VERİ PROJESİ - KAPSAMLI ANALİZ RAPORU")
    print(f"📅 Rapor Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    kurum_veri = kurum_analizi()
    zekat_veri = zekat_analizi()
    yatirim_veri = yatirim_analizi()
    arastirmaci_veri = arastirmaci_analizi()
    surdurulebilirlik_veri = surdurulebilirlik_analizi()
    
    print("\n" + "=" * 60)
    print("📋 GENEL ÖZET")
    print("=" * 60)
    
    toplam_kurum = len(kurum_veri["kurumlar"]) + len(zekat_veri["kurumlar"])
    toplam_arastirmaci = len(arastirmaci_veri["arastirmacilar"])
    toplam_yatirim_araci = len(yatirim_veri["yatirim_araclari"])
    dosya_terminoloji = DATA_DIR / "terminoloji" / "islam-iktisadi-terimleri.json"
    term_veri = json_oku(dosya_terminoloji)
    toplam_terim = len(term_veri["terimler"])
    
    toplam_proje = len(surdurulebilirlik_veri["projeler"])
    
    print(f"""
📊 PROJE İSTATİSTİKLERİ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏛️  Kurum Sayısı          : {toplam_kurum}
💰 Zekat Kuruluşu        : {len(zekat_veri["kurumlar"])}
👨‍🔬 Araştırmacı Sayısı   : {toplam_arastirmaci}
📈 Yatırım Aracı Sayısı  : {toplam_yatirim_araci}
🌱 Sürdürülebilirlik Proje: {toplam_proje}
📖 Terminoloji Sayısı    : {toplam_terim}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌍 Küresel İslami Finans : {yatirim_veri.get("istatistikler", {}).get("kuresel_islami_finans_varliklari", "Veri yok")}
🇹🇷 Türkiye Payı          : ~%15-20 (katılım bankacılığı mevduat payı)
💎 Potansiyel Zekat      : {zekat_veri.get("istatistikler", {}).get("yillik_zekat_potansiyeli_tahmini", "Veri yok")}
    """)
    
    print("✅ Analiz tamamlandı.")

if __name__ == "__main__":
    tum_rapor()