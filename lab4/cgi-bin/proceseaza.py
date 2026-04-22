#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lab 4 – Script CGI Python
Preia datele din formularul HTML, le salvează într-un fișier
și generează un răspuns HTML formatat.
"""

import sys
import os
import json
import urllib.parse
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

# Calea absolută spre folderul lab4/
LAB4_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
DATA_FILE = os.path.join(LAB4_DIR, 'data', 'date_auto.json')

# ============================================
#  HELPER: citire date POST
# ============================================
def get_post_data():
    try:
        length = int(os.environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        length = 0
    raw = sys.stdin.read(length) if length > 0 else ""
    return urllib.parse.parse_qs(raw, keep_blank_values=True)

def val(data, key, default=""):
    return data.get(key, [default])[0].strip()

# ============================================
#  CLASIFICĂRI
# ============================================
def cls_viteza(v):
    if v < 150:  return ("Oraș",             "badge-green")
    if v < 200:  return ("Sport",            "badge-yellow")
    if v < 250:  return ("High Performance", "badge-gold")
    return              ("Supercar",         "badge-red")

def cls_consum(c):
    if c <= 5:   return ("Eco",      "badge-green")
    if c <= 9:   return ("Normal",   "badge-yellow")
    if c <= 14:  return ("Sportiv",  "badge-gold")
    return              ("Extrem",   "badge-red")

def cls_putere(cp):
    if cp < 100: return ("Economic", "badge-green")
    if cp < 250: return ("Standard", "badge-yellow")
    if cp < 450: return ("Sport",    "badge-gold")
    return              ("Supercar", "badge-red")

CULORI_HEX = {
    "negru":"#1a1a1a", "alb":"#f5f5f5", "rosu":"#cc2200",
    "albastru":"#1a4a99", "gri":"#888888", "portocaliu":"#e05a00"
}
CULORI_LABEL = {
    "negru":"Negru", "alb":"Alb", "rosu":"Roșu",
    "albastru":"Albastru", "gri":"Gri", "portocaliu":"Portocaliu"
}

# ============================================
#  SALVARE ÎN JSON
# ============================================
def salveaza(d):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    toate = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                toate = json.load(f)
        except:
            toate = []
    toate.append(d)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(toate, f, ensure_ascii=False, indent=2)
    return len(toate)

# ============================================
#  CSS COMUN (inline pentru portabilitate)
# ============================================
COMMON_CSS = """
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Exo+2:wght@300;400;600&display=swap');
    :root{--bg-dark:#0a0a0f;--bg-card:#111118;--bg-input:#0d0d14;--accent-gold:#c9a84c;
          --text-primary:#f0f0f0;--text-secondary:#999;--border-color:#2a2a35;--transition:.3s ease}
    *{margin:0;padding:0;box-sizing:border-box}
    body{font-family:'Exo 2',sans-serif;background:#0a0a0f;color:#f0f0f0;min-height:100vh}
    header{background:linear-gradient(135deg,#0a0a0f,#1a1a2e);border-bottom:1px solid #c9a84c;padding:20px 40px;position:sticky;top:0;z-index:100}
    header h1{font-family:'Rajdhani',sans-serif;font-size:2rem;font-weight:700;color:#c9a84c;letter-spacing:4px;text-transform:uppercase}
    nav{background:#111118;padding:12px 40px;border-bottom:1px solid #2a2a35}
    nav ul{list-style:none;display:flex;gap:8px}
    nav ul li a{display:inline-block;padding:8px 22px;color:#999;text-decoration:none;font-family:'Rajdhani',sans-serif;font-size:.95rem;letter-spacing:2px;text-transform:uppercase;border:1px solid transparent;border-radius:2px;transition:.3s}
    nav ul li a:hover,nav ul li a.active{color:#c9a84c;border-color:#c9a84c;background:rgba(201,168,76,.08)}
    .container{max-width:1000px;margin:0 auto;padding:50px 20px}
    .page-title{font-family:'Rajdhani',sans-serif;font-size:2.2rem;font-weight:700;color:#c9a84c;letter-spacing:4px;text-transform:uppercase;text-align:center;margin-bottom:8px}
    .page-subtitle{text-align:center;color:#999;font-size:.95rem;letter-spacing:1px;margin-bottom:40px}
    .card{background:#111118;border:1px solid #2a2a35;border-radius:6px;padding:36px;position:relative;overflow:hidden}
    .card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#c9a84c,transparent)}
    .sec-title{font-family:'Rajdhani',sans-serif;font-size:1rem;font-weight:600;color:#c9a84c;letter-spacing:3px;text-transform:uppercase;margin-bottom:20px;padding-bottom:10px;border-bottom:1px solid #2a2a35}
    .stats-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:24px}
    .stat-box{background:#0d0d14;border:1px solid #2a2a35;border-radius:4px;padding:16px;text-align:center;transition:.3s}
    .stat-box:hover{border-color:#c9a84c}
    .stat-value{font-family:'Rajdhani',sans-serif;font-size:1.6rem;font-weight:700;color:#c9a84c;display:block}
    .stat-label{font-size:.7rem;letter-spacing:2px;text-transform:uppercase;color:#999;margin-top:4px;display:block}
    .badge{display:inline-block;padding:5px 14px;border-radius:2px;font-family:'Rajdhani',sans-serif;font-size:.85rem;font-weight:600;letter-spacing:2px;text-transform:uppercase}
    .badge-green{background:rgba(76,175,130,.15);border:1px solid #4caf82;color:#4caf82}
    .badge-yellow{background:rgba(232,160,32,.15);border:1px solid #e8a020;color:#e8a020}
    .badge-gold{background:rgba(201,168,76,.15);border:1px solid #c9a84c;color:#c9a84c}
    .badge-red{background:rgba(224,80,80,.15);border:1px solid #e05050;color:#e05050}
    .badge-row{display:flex;gap:10px;flex-wrap:wrap;margin:10px 0 22px}
    .analiza{background:#0d0d14;border-left:3px solid #c9a84c;padding:16px 20px;border-radius:0 4px 4px 0;font-size:.95rem;line-height:1.7;color:#999}
    .analiza strong{color:#f0f0f0}
    .back-link{display:inline-flex;align-items:center;gap:8px;margin-top:20px;padding:10px 24px;color:#999;text-decoration:none;border:1px solid #2a2a35;border-radius:2px;font-family:'Rajdhani',sans-serif;letter-spacing:2px;font-size:.9rem;text-transform:uppercase;transition:.3s;margin-right:10px}
    .back-link:hover{color:#c9a84c;border-color:#c9a84c;background:rgba(201,168,76,.06)}
    .cgi-tag{font-family:'Rajdhani',sans-serif;font-size:.75rem;letter-spacing:2px;color:#c9a84c;text-transform:uppercase;background:rgba(201,168,76,.08);border:1px solid rgba(201,168,76,.3);padding:6px 14px;border-radius:2px;display:inline-block;margin-bottom:20px}
    .cdot{width:14px;height:14px;border-radius:50%;display:inline-block;vertical-align:middle;margin-right:5px;border:1px solid rgba(255,255,255,.15)}
    footer{background:#111118;border-top:1px solid #2a2a35;padding:24px 40px;text-align:center;margin-top:60px}
    footer p{font-size:.8rem;color:#666;letter-spacing:1px}
  </style>
"""

# ============================================
#  PAGINA EROARE
# ============================================
def pagina_eroare(mesaje):
    items = "".join(f"<li style='margin-bottom:8px'>{m}</li>" for m in mesaje)
    return f"""<!DOCTYPE html>
<html lang="ro"><head><meta charset="UTF-8"><title>Eroare</title>{COMMON_CSS}</head>
<body>
<header><h1>Automobile de Lux</h1></header>
<nav><ul>
  <li><a href="../index.html">Acasă</a></li>
  <li><a href="../bmw.html">BMW</a></li>
  <li><a href="../mclaren.html">McLaren</a></li>
  <li><a href="../porsche.html">Porsche</a></li>
  <li><a href="../formular.html" class="active">Formular</a></li>
</ul></nav>
<div class="container">
  <h2 class="page-title" style="color:#e05050">Erori de validare</h2>
  <div class="card">
    <ul style="color:#e05050;line-height:2;padding-left:20px">{items}</ul>
    <a href="../formular.html" class="back-link" style="margin-top:24px">&#8592; Înapoi la formular</a>
  </div>
</div>
<footer><p>Lucrare de Laborator Nr. 4 — CGI</p></footer>
</body></html>"""

# ============================================
#  PAGINA REZULTAT
# ============================================
def pagina_rezultat(d, nr):
    hex_c  = CULORI_HEX.get(d['culoare'], '#888')
    lbl_c  = CULORI_LABEL.get(d['culoare'], d['culoare'])
    pg     = round(d['cp'] / d['greutate'] * 1000, 2)
    cv,ccv = cls_viteza(d['viteza'])
    cc,ccc = cls_consum(d['consum'])
    cpt,cpc= cls_putere(d['cp'])
    model  = f" {d['model']}" if d.get('model') else ""

    if d['cp'] >= 450:   intro = "spectaculoasă pentru pasionații de performanță extremă."
    elif d['cp'] >= 250: intro = "excelentă pentru cei care caută echilibrul dintre lux și dinamism."
    else:                intro = "inteligentă pentru uz cotidian și eficiență."

    if d['viteza'] >= 250:   dv = "intră în categoria supercarurilor — puțini o pot egaliza pe circuit."
    elif d['viteza'] >= 200: dv = "oferă performanțe de înaltă clasă, potrivite pentru circuit și autostradă."
    else:                    dv = "este ideală pentru condus urban și interurban."

    if d['consum'] <= 5:    dc = "Consumul este remarcabil de eficient — ideal pentru cei preocupați de mediu."
    elif d['consum'] <= 9:  dc = "Consumul este rezonabil — un bun compromis între performanță și economie."
    elif d['consum'] <= 14: dc = "Consumul este specific unui automobil sportiv — performanța are un preț."
    else:                   dc = "Consumul este ridicat, caracteristic unui motor de înaltă performanță."

    if pg > 400:    dpg = "plasează această mașină printre cele mai agile din categorie."
    elif pg > 200:  dpg = "oferă o accelerație plăcută și răspuns prompt al motorului."
    else:           dpg = "asigură un condus liniștit și controlat."

    return f"""<!DOCTYPE html>
<html lang="ro"><head><meta charset="UTF-8"><title>Rezultat – {d['marca']}{model}</title>{COMMON_CSS}</head>
<body>
<header><h1>Automobile de Lux</h1></header>
<nav><ul>
  <li><a href="../index.html">Acasă</a></li>
  <li><a href="../bmw.html">BMW</a></li>
  <li><a href="../mclaren.html">McLaren</a></li>
  <li><a href="../porsche.html">Porsche</a></li>
  <li><a href="../formular.html" class="active">Formular</a></li>
</ul></nav>
<div class="container">
  <h2 class="page-title">Analiză Completă</h2>
  <p class="page-subtitle">Datele au fost procesate și salvate pe server</p>
  <div class="card">
    <span class="cgi-tag">✓ Procesat CGI · {d['timestamp']} · Înregistrarea #{nr}</span>

    <p class="sec-title">
      {d['marca']}{model}
      <span class="cdot" style="background:{hex_c}"></span>
      <span style="font-size:.9rem;color:#c9a84c">{lbl_c}</span>
    </p>

    <div class="stats-grid">
      <div class="stat-box"><span class="stat-value">{d['viteza']} km/h</span><span class="stat-label">Viteză Maximă</span></div>
      <div class="stat-box"><span class="stat-value">{d['cp']} CP</span><span class="stat-label">Putere Motor</span></div>
      <div class="stat-box"><span class="stat-value">{pg} CP/t</span><span class="stat-label">Raport P/G</span></div>
      <div class="stat-box"><span class="stat-value">{d['greutate']} kg</span><span class="stat-label">Greutate</span></div>
      <div class="stat-box"><span class="stat-value">{d['consum']} L/100</span><span class="stat-label">Consum</span></div>
      <div class="stat-box">
        <span class="stat-value"><span class="cdot" style="background:{hex_c}"></span>{lbl_c}</span>
        <span class="stat-label">Culoare</span>
      </div>
    </div>

    <p class="sec-title">Clasificare</p>
    <div class="badge-row">
      <span class="badge {ccv}">{cv}</span>
      <span class="badge {cpc}">{cpt}</span>
      <span class="badge {ccc}">{cc}</span>
    </div>

    <div class="analiza">
      <strong>{d['marca']}{model}</strong> în
      <span class="cdot" style="background:{hex_c}"></span>
      <strong>{lbl_c}</strong> — o alegere {intro}
      <br><br>
      Cu o viteză maximă de <strong>{d['viteza']} km/h</strong>, mașina {dv}
      Cei <strong>{d['cp']} CP</strong> la un raport putere/greutate de <strong>{pg} CP/tonă</strong> {dpg}
      <br><br>
      {dc}
    </div>

    <div style="display:flex;gap:10px;flex-wrap:wrap">
      <a href="../formular.html" class="back-link">&#8592; Înapoi la formular</a>
      <a href="lista_date.py" class="back-link">&#9776; Toate înregistrările</a>
    </div>
  </div>
</div>
<footer><p>Lucrare de Laborator Nr. 4 — CGI</p></footer>
</body></html>"""

# ============================================
#  MAIN
# ============================================
print("Content-Type: text/html; charset=utf-8")
print()

try:
    data     = get_post_data()
    marca    = val(data, "marca")
    model    = val(data, "model")
    culoare  = val(data, "culoare", "negru")

    try:    viteza   = float(val(data, "viteza",   "0"))
    except: viteza   = 0
    try:    cp       = float(val(data, "cp",       "0"))
    except: cp       = 0
    try:    greutate = float(val(data, "greutate", "0"))
    except: greutate = 0
    try:    consum   = float(val(data, "consum",   "0"))
    except: consum   = 0

    erori = []
    if not marca:      erori.append("Marca este obligatorie.")
    if viteza < 50:    erori.append("Viteza trebuie să fie minim 50 km/h.")
    if cp < 50:        erori.append("Cai putere trebuie să fie minim 50.")
    if greutate < 500: erori.append("Greutatea trebuie să fie minim 500 kg.")
    if consum < 1:     erori.append("Consumul trebuie să fie minim 1 L/100km.")

    if erori:
        print(pagina_eroare(erori))
    else:
        d = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "marca":    marca,
            "model":    model,
            "viteza":   viteza,
            "cp":       cp,
            "greutate": greutate,
            "consum":   consum,
            "culoare":  culoare
        }
        nr = salveaza(d)
        print(pagina_rezultat(d, nr))

except Exception as e:
    import traceback
    print(f"<pre style='color:red;padding:20px'>{traceback.format_exc()}</pre>")
    print("<a href='../formular.html'>Înapoi</a>")
