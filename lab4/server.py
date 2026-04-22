#!/usr/bin/env python3
"""
Lab 4 – Server CGI local
Pornește un server HTTP cu suport CGI pe portul 8080.

Rulați din folderul lab4/:
    python server.py

Apoi deschideți în browser:
    http://localhost:8080/formular.html
"""

import http.server
import os

PORT = 8080
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Asigură permisiuni de execuție pe scripturile CGI
for f in ['cgi-bin/proceseaza.py', 'cgi-bin/lista_date.py']:
    if os.path.exists(f):
        os.chmod(f, 0o755)

# Asigură că folderul data există
os.makedirs('data', exist_ok=True)

Handler = http.server.CGIHTTPRequestHandler
Handler.cgi_directories = ['/cgi-bin']

print(f"╔══════════════════════════════════════╗")
print(f"║  Lab 4 – Server CGI pornit           ║")
print(f"║  http://localhost:{PORT}/formular.html  ║")
print(f"║  Apăsați Ctrl+C pentru a opri        ║")
print(f"╚══════════════════════════════════════╝")

with http.server.HTTPServer(('', PORT), Handler) as httpd:
    httpd.serve_forever()
