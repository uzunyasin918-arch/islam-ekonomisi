#!/usr/bin/env python3
"""Tek sayfalık İslam İktisadı proje görüntüleyici - Tüm veri gömülü"""
import json, os, sys

PROJE = "/home/engine/islam-ekonomisi"

def load_json(path):
    with open(os.path.join(PROJE, path)) as f:
        return json.load(f)

# Tüm veriyi yükle
kurumlar = load_json("data/kurumlar/islami-finans-kurumlari.json")
zekat = load_json("data/kurumlar/zekat-kurumlari.json")
yatirim = load_json("data/veriler/helal-yatirim-araclari.json")
surdurulebilirlik = load_json("data/veriler/surdurulebilirlik-projeleri.json")
arastirmacilar = load_json("data/arastirmacilar/arastirmacilar.json")
terminoloji = load_json("data/terminoloji/islam-iktisadi-terimleri.json")

def badge(txt, cls):
    return f'<span class="badge {cls}">{txt}</span>'

def make_kurum_card(k):
    ulkeler = ' '.join(badge(u, 'b-ulke') for u in k.get("ulkeler",[]))
    faaliyet = ' '.join(badge(f, 'b-tur') for f in k.get("faaliyet_alanlari",[])[:5])
    durum = badge("✅ Aktif", "b-aktif") if k.get("guncel_durum")=="Aktif" else ""
    extra = ""
    for key, label in [("sube_sayisi","🏢 Şube"),("uye_sayisi","👥 Üye"),("yayin_sayisi","📄 Yayın")]:
        if key in k: extra += f'<p class="meta">{label}: <strong>{k[key]}</strong></p>'
    if k.get("web"): extra += f'<p class="meta">🔗 {k["web"]}</p>'
    if k.get("not"): extra += f'<p class="meta">⭐ {k["not"]}</p>'
    return f'<div class="card"><h3>{k["ad"]}</h3><p class="meta">{k["tur"]} {durum}</p><p class="meta">{ulkeler}</p><p class="desc">{k["aciklama"][:200]}</p>{faaliyet}{extra}</div>'

def make_zekat_card(z):
    return f'<div class="card"><h3>{z["ad"]}</h3><p class="meta">{z["tur"]} {badge(z["ulkeler"][0] if z.get("ulkeler") else "Küresel", "b-ulke")}</p><p class="desc">{z["aciklama"][:200]}</p>{badge("✅ Aktif","b-aktif")}{(" 🔗 "+z["web"]) if z.get("web") else ""}</div>'

def make_yatirim_card(a):
    return f'<div class="card"><h3>{a["ad"]}</h3><p class="meta">{a["kategori"]} {badge(a["risk_seviyesi"],"b-risk")} {badge(a["helal_uyum"][:20],"b-helal")}</p><p class="desc">{a["aciklama"][:200]}</p><p class="meta">📍 {a.get("kullanim_alanlari","")[:100]}</p></div>'

def make_sur_card(p):
    return f'<div class="card"><h3>{p["ad"]}</h3><p class="meta">{p["tur"]} {badge(p.get("ulke","Küresel"),"b-ulke")}</p><p class="desc">{p["aciklama"][:200]}</p><p class="meta">📌 {p.get("kapsam","")[:120]}</p></div>'

def make_arastirmaci_card(a):
    eserler = ""
    if a.get("onemli_eserler"):
        eserler = '<ul class="strategy-list">'+''.join(f'<li>📖 {e}</li>' for e in a["onemli_eserler"][:3])+'</ul>'
    return f'<div class="card"><h3>{a["ad"]}</h3><p class="meta">🏛️ {a["kurum"]} {badge(a["ulke"],"b-ulke")}</p><p class="meta">📌 {a["alan"]}</p><p class="desc">{a.get("katki","")[:200]}</p>{eserler}</div>'

def make_term_card(t):
    return f'<div class="card"><h3>{t["terim"]} <span style="color:#818cf8;font-size:0.7em">{t.get("arapca","")}</span></h3><p class="meta">{t.get("ingilizce","")} {badge(t.get("turu",""),"b-tur")}</p><p class="desc">{t["anlami"][:200]}</p>{("<p class=\"meta\">📚 Kaynak: "+t["kaynak"]+"</p>") if t.get("kaynak") else ""}</div>'

# HTML oluştur
html = '''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>İslam İktisadı Veri Projesi</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0f172a;color:#e2e8f0;line-height:1.6}
.container{max-width:1200px;margin:0 auto;padding:16px}
header{text-align:center;padding:28px 16px;background:linear-gradient(135deg,#1e3a5f,#1a237e);border-radius:12px;margin-bottom:16px}
header h1{font-size:2em;color:#ffd700;margin-bottom:6px}
.subtitle{color:#94a3b8;font-size:0.9em}
.tagline{font-style:italic;color:#818cf8;margin-top:4px;font-size:0.85em}
.tabs{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:16px;justify-content:center}
.tab-btn{padding:8px 14px;border:2px solid #334155;background:#1e293b;color:#94a3b8;border-radius:8px;cursor:pointer;font-size:0.8em;transition:.2s}
.tab-btn:hover,.tab-btn.active{background:#ffd700;color:#0f172a;font-weight:bold;border-color:#ffd700}
.tab{display:none}
.tab.active{display:block}
h2{font-size:1.3em;margin-bottom:12px;color:#ffd700;border-bottom:2px solid #334155;padding-bottom:6px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:10px}
.card{background:#1e293b;border:1px solid #334155;border-radius:10px;padding:14px}
.card h3{color:#ffd700;font-size:1em;margin-bottom:5px}
.meta{color:#94a3b8;font-size:0.8em;margin:3px 0}
.desc{color:#cbd5e1;font-size:0.85em;margin:5px 0}
.badge{display:inline-block;padding:1px 7px;border-radius:8px;font-size:0.7em;font-weight:600;margin:1px}
.b-tur{background:#1a3a5c;color:#60a5fa}
.b-ulke{background:#3b1a5c;color:#c084fc}
.b-aktif{background:#14532d;color:#4ade80}
.b-risk{background:#5c1a1a;color:#f87171}
.b-helal{background:#1a5c3a;color:#34d399}
.summary{background:#1e293b;border:2px solid #ffd700;border-radius:12px;padding:20px;margin-bottom:16px}
.summary h3{color:#ffd700;text-align:center;font-size:1.2em;margin-bottom:8px}
.s-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:6px}
.s-box{background:#0f172a;border-radius:8px;padding:10px;text-align:center}
.s-box .num{color:#ffd700;font-size:1.3em;font-weight:bold}
.s-box .lbl{color:#94a3b8;font-size:0.75em}
.str-list{list-style:none;margin-top:6px}
.str-list li{background:#0f172a;border-radius:6px;padding:6px 10px;margin:3px 0;font-size:0.8em;border-left:3px solid #ffd700;color:#cbd5e1}
footer{text-align:center;padding:16px;color:#64748b;font-size:0.8em;margin-top:24px;border-top:1px solid #334155}
@media(max-width:640px){header h1{font-size:1.4em}.grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="container">

<header>
<h1>📊 İslam İktisadı Projesi</h1>
<p class="subtitle">İslam Ekonomisi · Helal Yatırım · Zekat · Sürdürülebilirlik</p>
<p class="tagline">"Helal yoldan kazan, koru ve yatırım yap"</p>
</header>

<nav class="tabs" id="tabs">
<button class="tab-btn active" data-tab="tab-summary">📊 Genel</button>
<button class="tab-btn" data-tab="tab-kurumlar">🏛️ Kurumlar</button>
<button class="tab-btn" data-tab="tab-zekat">💰 Zekat</button>
<button class="tab-btn" data-tab="tab-yatirim">📈 Yatırım</button>
<button class="tab-btn" data-tab="tab-sur">🌱 Sürdürülebilirlik</button>
<button class="tab-btn" data-tab="tab-ara">👨‍🔬 Araştırmacılar</button>
<button class="tab-btn" data-tab="tab-term">📖 Sözlük</button>
</nav>

<!-- GENEL -->
<div class="tab active" id="tab-summary">
<div class="summary">
<h3>📊 Proje Özeti</h3>
<div class="s-grid">
<div class="s-box"><span class="num">''' + str(len(kurumlar["kurumlar"])+len(zekat["kurumlar"])) + '''</span><span class="lbl">🏛️ Kurum</span></div>
<div class="s-box"><span class="num">''' + str(len(arastirmacilar["arastirmacilar"])) + '''</span><span class="lbl">👨‍🔬 Araştırmacı</span></div>
<div class="s-box"><span class="num">''' + str(len(yatirim["yatirim_araclari"])) + '''</span><span class="lbl">📈 Yatırım Aracı</span></div>
<div class="s-box"><span class="num">''' + str(len(surdurulebilirlik["projeler"])) + '''</span><span class="lbl">🌱 Proje</span></div>
<div class="s-box"><span class="num">''' + str(len(terminoloji["terimler"])) + '''</span><span class="lbl">📖 Terim</span></div>
<div class="s-box"><span class="num" style="font-size:1em">$4-5T</span><span class="lbl">🌍 Küresel İslami Finans</span></div>
</div>
</div>

<h2>📋 Servet Koruma Stratejileri</h2>
<ul class="str-list">
'''

for s in yatirim.get("servet_koruma_stratejileri", []):
    html += f'<li><strong>{s["strateji"]}:</strong> {s["aciklama"][:150]}</li>\n'

html += '''</ul>

<h2 style="margin-top:16px">🏛️ Öne Çıkan Kurumlar</h2>
<div class="grid">
'''

for k in kurumlar["kurumlar"][:6]:
    html += make_kurum_card(k)

html += '''</div>

<h2 style="margin-top:16px">👨‍🔬 Öne Çıkan Araştırmacılar</h2>
<div class="grid">
'''

for a in arastirmacilar["arastirmacilar"][:4]:
    html += make_arastirmaci_card(a)

html += '''</div>
</div>

<!-- KURUMLAR -->
<div class="tab" id="tab-kurumlar">
<h2>🏛️ İslami Finans Kurumları <span style="font-size:0.6em;color:#94a3b8">(''' + str(len(kurumlar["kurumlar"])) + ''' kayıt)</span></h2>
<div class="grid">
'''

for k in kurumlar["kurumlar"]:
    html += make_kurum_card(k)

html += '''</div></div>

<!-- ZEKAT -->
<div class="tab" id="tab-zekat">
<h2>💰 Zekat Kurum ve Platformları <span style="font-size:0.6em;color:#94a3b8">(''' + str(len(zekat["kurumlar"])) + ''' kayıt)</span></h2>
<div class="grid">
'''

for z in zekat["kurumlar"]:
    html += make_zekat_card(z)

html += '''</div></div>

<!-- YATIRIM -->
<div class="tab" id="tab-yatirim">
<h2>📈 Helal Yatırım Araçları <span style="font-size:0.6em;color:#94a3b8">(''' + str(len(yatirim["yatirim_araclari"])) + ''' araç)</span></h2>
<p style="color:#94a3b8;margin-bottom:12px;font-size:0.85em">Müslümanların helal yoldan para kazanması, biriktirmesi ve yatırım yapması için araçlar</p>
<div class="grid">
'''

for a in yatirim["yatirim_araclari"]:
    html += make_yatirim_card(a)

html += '''</div>

<h2 style="margin-top:16px">📋 Helal Filtreleme Kriterleri</h2>
<ul class="str-list">
'''

for f in yatirim.get("helal_yatirim_filtreleme_kriterleri", {}).get("sektor_filtresi", []):
    html += f'<li>🚫 {f}</li>\n'

html += '</ul></div>\n'

# SÜRDÜRÜLEBİLİRLİK
html += '''<div class="tab" id="tab-sur">
<h2>🌱 Sürdürülebilirlik Projeleri <span style="font-size:0.6em;color:#94a3b8">(''' + str(len(surdurulebilirlik["projeler"])) + ''' proje)</span></h2>
<div class="grid">
'''

for p in surdurulebilirlik["projeler"]:
    html += make_sur_card(p)

html += '''</div></div>

<!-- ARAŞTIRMACILAR -->
<div class="tab" id="tab-ara">
<h2>👨‍🔬 Araştırmacılar <span style="font-size:0.6em;color:#94a3b8">(''' + str(len(arastirmacilar["arastirmacilar"])) + ''' araştırmacı)</span></h2>
<div class="grid">
'''

for a in arastirmacilar["arastirmacilar"]:
    html += make_arastirmaci_card(a)

html += '''</div></div>

<!-- TERMİNOLOJİ -->
<div class="tab" id="tab-term">
<h2>📖 İslam İktisadı Sözlüğü <span style="font-size:0.6em;color:#94a3b8">(''' + str(len(terminoloji["terimler"])) + ''' terim)</span></h2>
<input type="text" id="term-search" placeholder="🔍 Terim ara..." style="width:100%;padding:10px 14px;border:2px solid #334155;background:#1e293b;color:#e2e8f0;border-radius:8px;font-size:0.9em;margin-bottom:12px">
<div class="grid" id="term-grid">
'''

for t in terminoloji["terimler"]:
    html += make_term_card(t)

html += '''</div></div>

<footer>
<p>İslam İktisadı Araştırma ve Veri Projesi · Güncelleme: Haziran 2025</p>
</footer>

</div>

<script>
// Sekme geçişleri
document.querySelectorAll(".tab-btn").forEach(b => {
b.addEventListener("click",()=>{
document.querySelectorAll(".tab-btn").forEach(x=>x.classList.remove("active"))
document.querySelectorAll(".tab").forEach(x=>x.classList.remove("active"))
b.classList.add("active")
document.getElementById(b.dataset.tab).classList.add("active")
})
})

// Terminoloji arama
const search = document.getElementById("term-search")
if(search){
search.addEventListener("input",()=>{
const q = search.value.toLowerCase()
document.querySelectorAll("#term-grid .card").forEach(c=>{
c.style.display = c.textContent.toLowerCase().includes(q)?"block":"none"
})
})
}
</script>
</body>
</html>'''

# Yaz
outpath = os.path.join(PROJE, "web", "index-tek.html")
with open(outpath, "w") as f:
    f.write(html)

print(f"✅ Tek dosya oluşturuldu: {outpath}")
print(f"   Dosya boyutu: {os.path.getsize(outpath)/1024:.0f} KB")