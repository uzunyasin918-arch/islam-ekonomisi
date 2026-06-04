#!/bin/bash
# İslam İktisadı Veri Projesi - Güncelleme Scripti
echo "🔄 İslam İktisadı Veri Projesi Güncelleme Başlatılıyor..."
echo "=========================================="

TARIH=$(date +%Y-%m-%d)
PROJE_DIR="/home/engine/islam-ekonomisi"

echo "📂 Proje dizini: $PROJE_DIR"
echo "📅 Tarih: $TARIH"
echo ""

# 1. Veri dosyalarını kontrol et
echo "📋 Veri dosyaları kontrol ediliyor..."
for dosya in data/kurumlar/islami-finans-kurumlari.json data/kurumlar/zekat-kurumlari.json data/veriler/helal-yatirim-araclari.json data/veriler/surdurulebilirlik-projeleri.json data/arastirmacilar/arastirmacilar.json data/terminoloji/islam-iktisadi-terimleri.json data/konferanslar/konferanslar.json; do
    if [ -f "$PROJE_DIR/$dosya" ]; then
        BOYUT=$(stat --format=%s "$PROJE_DIR/$dosya" 2>/dev/null || stat -f%z "$PROJE_DIR/$dosya" 2>/dev/null)
        echo "   ✅ $dosya ($BOYUT bytes)"
    else
        echo "   ❌ $dosya BULUNAMADI!"
    fi
done

echo ""

# 2. Analiz çalıştır
echo "📊 Veri analizi çalıştırılıyor..."
cd "$PROJE_DIR" && python3 analysis/analiz.py 2>/dev/null || python3 analysis/analiz.py
echo ""

# 3. JSON dosyalarını doğrula
echo "✅ JSON doğrulama..."
for dosya in data/kurumlar/islami-finans-kurumlari.json data/kurumlar/zekat-kurumlari.json data/veriler/helal-yatirim-araclari.json data/veriler/surdurulebilirlik-projeleri.json data/arastirmacilar/arastirmacilar.json data/terminoloji/islam-iktisadi-terimleri.json data/konferanslar/konferanslar.json; do
    python3 -c "import json; json.load(open('$PROJE_DIR/$dosya')); print('   ✅ $dosya - Geçerli')" 2>&1 || echo "   ❌ $dosya - GEÇERSİZ!"
done

echo ""
echo "=========================================="
echo "✅ Güncelleme tamamlandı!"
echo "📅 $TARIH"