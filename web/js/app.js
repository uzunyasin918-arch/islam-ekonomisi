// İslam İktisadı Veri Projesi - Web Uygulaması

// JSON verilerini yükle
async function yukleJSON(dosya) {
    try {
        const res = await fetch(`../data/${dosya}`);
        return await res.json();
    } catch(e) {
        console.error(`${dosya} yüklenemedi:`, e);
        return null;
    }
}

// Kart oluşturma yardımcıları
function badgeMetin(metin, cssClass) {
    return `<span class="badge ${cssClass}">${metin}</span>`;
}

function kartOlustur(baslik, icerik) {
    return `<div class="card">
        <h3>${baslik}</h3>
        ${icerik}
    </div>`;
}

// ==================== KURUMLAR ====================
function kurumKarti(k) {
    const ulkeler = (k.ulkeler || []).map(u => badgeMetin(u, 'badge-ulke')).join(' ');
    const faaliyet = (k.faaliyet_alanlari || []).map(f => badgeMetin(f, 'badge-tur')).join(' ');
    const durum = k.guncel_durum === 'Aktif' ? badgeMetin('✅ Aktif', 'badge-aktif') : '';
    
    let ekstra = '';
    if (k.sube_sayisi) ekstra += `<p>🏢 Şube: <span class="detail">${k.sube_sayisi}</span></p>`;
    if (k.uye_sayisi) ekstra += `<p>👥 Üye: <span class="detail">${k.uye_sayisi}</span></p>`;
    if (k.yayin_sayisi) ekstra += `<p>📄 Yayın: <span class="detail">${k.yayin_sayisi}</span></p>`;
    if (k.web) ekstra += `<p>🔗 <a href="${k.web}" target="_blank" style="color:#60a5fa">${k.web}</a></p>`;
    if (k.not) ekstra += `<p class="detail">⭐ ${k.not}</p>`;
    
    return kartOlustur(`${k.ad}`, `
        <p>🎯 ${k.tur} ${durum}</p>
        <p>${ulkeler}</p>
        <p>${k.aciklama}</p>
        ${faaliyet ? `<p>📌 ${faaliyet}</p>` : ''}
        ${ekstra}
    `);
}

// ==================== ZEKAT ====================
function zekatKarti(z) {
    return kartOlustur(`${z.ad}`, `
        <p>🎯 ${z.tur} ${badgeMetin(z.ulkeler.join(', '), 'badge-ulke')}</p>
        <p>${z.aciklama}</p>
        ${z.faaliyet_alanlari ? `<p>📌 ${z.faaliyet_alanlari.map(f => badgeMetin(f, 'badge-tur')).join(' ')}</p>` : ''}
        ${z.web ? `<p>🔗 <a href="${z.web}" target="_blank" style="color:#60a5fa">${z.web}</a></p>` : ''}
        ${z.yillik_toplam || z.yillik_gelir || z.yillik_butce ? `<p>💰 ${z.yillik_toplam || z.yillik_gelir || z.yillik_butce}</p>` : ''}
        <p>${badgeMetin('✅ Aktif', 'badge-aktif')}</p>
    `);
}

// ==================== YATIRIM ====================
function yatirimKarti(a) {
    return kartOlustur(`${a.ad}`, `
        <p>🎯 ${a.kategori} ${badgeMetin(a.risk_seviyesi, 'badge-risk')} ${badgeMetin(a.helal_uyum, 'badge-helal')}</p>
        <p>${a.aciklama}</p>
        <p>📍 Kullanım: ${a.kullanim_alanlari}</p>
        ${a.turkiye_ornekler ? `<p>🇹🇷 ${a.turkiye_ornekler.join(', ')}</p>` : ''}
        ${a.kuresel_ornekler ? `<p>🌍 ${a.kuresel_ornekler.join(', ')}</p>` : ''}
        ${a.kuresel_hacim ? `<p>💰 <span class="detail">${a.kuresel_hacim}</span></p>` : ''}
    `);
}

// ==================== SÜRDÜRÜLEBİLİRLİK ====================
function surdurulebilirlikKarti(p) {
    return kartOlustur(`${p.ad}`, `
        <p>🎯 ${p.tur} ${badgeMetin(p.ulke || 'Küresel', 'badge-ulke')}</p>
        <p>${p.aciklama}</p>
        <p>📌 Kapsam: ${p.kapsam}</p>
        ${p.baslangic ? `<p>📅 Başlangıç: ${p.baslangic}</p>` : ''}
        ${p.hacim ? `<p>💰 <span class="detail">${p.hacim}</span></p>` : ''}
        ${p.yararlanan ? `<p>👥 Yararlanan: <span class="detail">${p.yararlanan}</span></p>` : ''}
        ${p.web ? `<p>🔗 <a href="${p.web}" target="_blank" style="color:#60a5fa">${p.web}</a></p>` : ''}
        <p>${badgeMetin(p.guncel_durum, 'badge-aktif')}</p>
    `);
}

// ==================== ARAŞTIRMACILAR ====================
function arastirmaciKarti(a) {
    const eserler = a.onemli_eserler ? 
        `<ul>${a.onemli_eserler.map(e => `<li>${e}</li>`).join('')}</ul>` : '';
    
    return kartOlustur(`${a.ad}`, `
        <p>🏛️ ${a.kurum} ${badgeMetin(a.ulke, 'badge-ulke')}</p>
        <p>📌 ${a.alan}</p>
        <p>💡 ${a.katki}</p>
        ${eserler ? `<p><strong>📖 Önemli Eserler:</strong></p>${eserler}` : ''}
        <p>${badgeMetin(a.guncel_durum, a.guncel_durum === 'Aktif' ? 'badge-aktif' : '')}</p>
    `);
}

// ==================== TERMİNOLOJİ ====================
function terminolojiKarti(t) {
    return kartOlustur(`${t.terim} (${t.arapca})`, `
        <p>📖 ${t.ingilizce} ${badgeMetin(t.turu, 'badge-tur')}</p>
        <p>${t.anlami}</p>
        ${t.kullanim ? `<p>📍 ${t.kullanim}</p>` : ''}
        ${t.kaynak ? `<p>📚 Kaynak: <span class="detail">${t.kaynak}</span></p>` : ''}
        ${t.oran ? `<p>📊 Oran: <span class="detail">${t.oran}</span></p>` : ''}
    `);
}

// ==================== SEKMELER ====================
function initSekmeler() {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(btn.dataset.tab).classList.add('active');
        });
    });
}

// ==================== TERMİNOLOJİ ARAMA ====================
function initArama() {
    const input = document.getElementById('terminoloji-search');
    if (!input) return;
    
    input.addEventListener('input', () => {
        const query = input.value.toLowerCase();
        document.querySelectorAll('#terminoloji-grid .card').forEach(card => {
            const text = card.textContent.toLowerCase();
            card.style.display = text.includes(query) ? 'block' : 'none';
        });
    });
}

// ==================== ANA YÜKLEME ====================
async function init() {
    initSekmeler();
    
    // Tüm verileri paralel yükle
    const [kurumlar, zekat, yatirim, surdurulebilirlik, arastirmacilar, terminoloji] = await Promise.all([
        yukleJSON('kurumlar/islami-finans-kurumlari.json'),
        yukleJSON('kurumlar/zekat-kurumlari.json'),
        yukleJSON('veriler/helal-yatirim-araclari.json'),
        yukleJSON('veriler/surdurulebilirlik-projeleri.json'),
        yukleJSON('arastirmacilar/arastirmacilar.json'),
        yukleJSON('terminoloji/islam-iktisadi-terimleri.json')
    ]);
    
    // Render
    if (kurumlar) {
        document.getElementById('kurumlar-grid').innerHTML = kurumlar.kurumlar.map(kurumKarti).join('');
    }
    
    if (zekat) {
        document.getElementById('zekat-grid').innerHTML = zekat.kurumlar.map(zekatKarti).join('');
    }
    
    if (yatirim) {
        document.getElementById('yatirim-grid').innerHTML = yatirim.yatirim_araclari.map(yatirimKarti).join('');
    }
    
    if (surdurulebilirlik) {
        document.getElementById('surdurulebilirlik-grid').innerHTML = surdurulebilirlik.projeler.map(surdurulebilirlikKarti).join('');
    }
    
    if (arastirmacilar) {
        document.getElementById('arastirmacilar-grid').innerHTML = arastirmacilar.arastirmacilar.map(arastirmaciKarti).join('');
    }
    
    if (terminoloji) {
        document.getElementById('terminoloji-grid').innerHTML = terminoloji.terimler.map(terminolojiKarti).join('');
        initArama();
    }
}

// Başlat
document.addEventListener('DOMContentLoaded', init);