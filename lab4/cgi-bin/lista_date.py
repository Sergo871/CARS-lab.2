#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lab 4 – Script CGI: Afișare toate înregistrările salvate din data/date_auto.json
"""

import sys
import os
import json

sys.stdout.reconfigure(encoding='utf-8')

# Calea absolută spre folderul lab4/
LAB4_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
DATA_FILE = os.path.join(LAB4_DIR, 'data', 'date_auto.json')

CULORI_HEX = {
    "negru":"#1a1a1a", "alb":"#f5f5f5", "rosu":"#cc2200",
    "albastru":"#1a4a99", "gri":"#888888", "portocaliu":"#e05a00"
}
CULORI_LABEL = {
    "negru":"Negru", "alb":"Alb", "rosu":"Roșu",
    "albastru":"Albastru", "gri":"Gri", "portocaliu":"Portocaliu"
}

COMMON_CSS = """
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Exo+2:wght@300;400;600&display=swap');
    *{margin:0;padding:0;box-sizing:border-box}
    body{font-family:'Exo 2',sans-serif;background:#0a0a0f;color:#f0f0f0;min-height:100vh}
    header{background:linear-gradient(135deg,#0a0a0f,#1a1a2e);border-bottom:1px solid #c9a84c;padding:20px 40px;position:sticky;top:0;z-index:100}
    header h1{font-family:'Rajdhani',sans-serif;font-size:2rem;font-weight:700;color:#c9a84c;letter-spacing:4px;text-transform:uppercase}
    nav{background:#111118;padding:12px 40px;border-bottom:1px solid #2a2a35}
    nav ul{list-style:none;display:flex;gap:8px}
    nav ul li a{display:inline-block;padding:8px 22px;color:#999;text-decoration:none;font-family:'Rajdhani',sans-serif;font-size:.95rem;letter-spacing:2px;text-transform:uppercase;border:1px solid transparent;border-radius:2px;transition:.3s}
    nav ul li a:hover,nav ul li a.active{color:#c9a84c;border-color:#c9a84c;background:rgba(201,168,76,.08)}
    .container{max-width:1100px;margin:0 auto;padding:50px 20px}
    .page-title{font-family:'Rajdhani',sans-serif;font-size:2.2rem;font-weight:700;color:#c9a84c;letter-spacing:4px;text-transform:uppercase;text-align:center;margin-bottom:8px}
    .page-subtitle{text-align:center;color:#999;font-size:.95rem;letter-spacing:1px;margin-bottom:40px}
    .card{background:#111118;border:1px solid #2a2a35;border-radius:6px;padding:36px;position:relative;overflow:hidden}
    .card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#c9a84c,transparent)}
    .count-tag{font-family:'Rajdhani',sans-serif;font-size:.8rem;letter-spacing:2px;color:#c9a84c;text-transform:uppercase;background:rgba(201,168,76,.08);border:1px solid rgba(201,168,76,.3);padding:6px 16px;border-radius:2px;display:inline-block;margin-bottom:24px}
    .tbl-wrap{overflow-x:auto}
    table{width:100%;border-collapse:collapse}
    th{font-family:'Rajdhani',sans-serif;letter-spacing:2px;text-transform:uppercase;font-size:.75rem;color:#c9a84c;padding:12px 14px;border-bottom:2px solid #c9a84c;text-align:left;background:#0d0d14;white-space:nowrap}
    td{padding:12px 14px;border-bottom:1px solid #1e1e28;font-size:.9rem;color:#ccc;vertical-align:middle}
    tr:hover td{background:rgba(201,168,76,.04)}
    .marca-cell{color:#c9a84c;font-family:'Rajdhani',sans-serif;font-weight:600;letter-spacing:1px}
    .cdot{width:12px;height:12px;border-radius:50%;display:inline-block;vertical-align:middle;margin-right:6px;border:1px solid rgba(255,255,255,.15)}
    .empty-msg{text-align:center;color:#555;padding:50px 20px;font-size:1rem;letter-spacing:1px}
    .back-link{display:inline-flex;align-items:center;gap:8px;margin-top:24px;padding:10px 24px;color:#999;text-decoration:none;border:1px solid #2a2a35;border-radius:2px;font-family:'Rajdhani',sans-serif;letter-spacing:2px;font-size:.9rem;text-transform:uppercase;transition:.3s}
    .back-link:hover{color:#c9a84c;border-color:#c9a84c;background:rgba(201,168,76,.06)}
    footer{background:#111118;border-top:1px solid #2a2a35;padding:24px 40px;text-align:center;margin-top:60px}
    footer p{font-size:.8rem;color:#666;letter-spacing:1px}
    .nr-cell{color:#555;font-size:.85rem}
    .ts-cell{color:#555;font-size:.8rem;font-family:monospace}
  </style>
"""

print("Content-Type: text/html; charset=utf-8")
print()

try:
    # Citire date din JSON
    toate = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                toate = json.load(f)
        except Exception as e:
            toate = []

    # Construire rânduri tabel (cele mai noi primele)
    if toate:
        randuri = ""
        for i, d in enumerate(reversed(toate)):
            nr_real = len(toate) - i
            hex_c = CULORI_HEX.get(d.get('culoare',''), '#888')
            lbl_c = CULORI_LABEL.get(d.get('culoare',''), d.get('culoare','—'))
            model_text = f" {d.get('model','')}" if d.get('model') else ""
            try:    v = f"{float(d.get('viteza',0)):.0f} km/h"
            except: v = "—"
            try:    c = f"{float(d.get('cp',0)):.0f} CP"
            except: c = "—"
            try:    g = f"{float(d.get('greutate',0)):.0f} kg"
            except: g = "—"
            try:    con = f"{float(d.get('consum',0)):.1f} L/100"
            except: con = "—"

            randuri += f"""
            <tr>
              <td class="nr-cell">{nr_real}</td>
              <td class="marca-cell">{d.get('marca','—')}{model_text}</td>
              <td>{v}</td>
              <td>{c}</td>
              <td>{g}</td>
              <td>{con}</td>
              <td><span class="cdot" style="background:{hex_c}"></span>{lbl_c}</td>
              <td class="ts-cell">{d.get('timestamp','—')}</td>
            </tr>"""

        body = f"""
        <div class="tbl-wrap">
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>Marcă / Model</th>
                <th>Viteză</th>
                <th>Putere</th>
                <th>Greutate</th>
                <th>Consum</th>
                <th>Culoare</th>
                <th>Timestamp</th>
              </tr>
            </thead>
            <tbody>{randuri}</tbody>
          </table>
        </div>"""
    else:
        body = '<p class="empty-msg">Nu există înregistrări salvate încă.<br>Trimite primul formular!</p>'

    print(f"""<!DOCTYPE html>
<html lang="ro"><head><meta charset="UTF-8"><title>Înregistrări – Lab 4</title>{COMMON_CSS}</head>
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
  <h2 class="page-title">Înregistrări Salvate</h2>
  <p class="page-subtitle">Toate datele trimise prin formular și stocate în <code style="color:#c9a84c">data/date_auto.json</code></p>
  <div class="card">
    <span class="count-tag">Total: {len(toate)} înregistrări</span>
    {body}
    <a href="../formular.html" class="back-link">&#8592; Înapoi la formular</a>
  </div>
</div>
<footer><p>Lucrare de Laborator Nr. 4 — CGI</p></footer>
</body></html>""")

except Exception as e:
    import traceback
    print(f"<pre style='color:red;padding:20px'>{traceback.format_exc()}</pre>")
