# Lab 4 – CGI

## Cum pornești serverul

1. Deschide Command Prompt (cmd) în folderul `lab4/`
2. Rulează:
   ```
   python server.py
   ```
3. Deschide în browser:
   ```
   http://localhost:8080/formular.html
   ```

## Structura proiectului

```
lab4/
├── index.html          ← Pagina principală
├── bmw.html
├── mclaren.html
├── porsche.html
├── formular.html       ← Formularul (trimite date la server)
├── server.py           ← Server CGI local (pornit cu python server.py)
├── css/
│   └── style.css
├── js/
│   ├── validare.js     ← Validare JS înainte de submit (sarcina suplimentară)
│   └── efecte.js       ← Efecte vizuale
├── images/
├── cgi-bin/
│   ├── proceseaza.py   ← Script CGI: procesează și salvează datele
│   └── lista_date.py   ← Script CGI: afișează toate înregistrările
└── data/
    └── date_auto.json  ← Fișier JSON cu datele salvate (creat automat)
```

## Ce face Lab 4

- **Formularul** trimite date prin `POST` la `cgi-bin/proceseaza.py`
- **proceseaza.py** validează datele pe server, le salvează în `data/date_auto.json` și generează un răspuns HTML
- **lista_date.py** afișează toate înregistrările din JSON
- **validare.js** validează datele în browser înainte de trimitere (sarcina suplimentară)
