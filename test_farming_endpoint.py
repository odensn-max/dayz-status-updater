"""
test_farming_endpoint.py — script temporaire pour verifier si l'endpoint
stats XML/JSON de Farming Simulator est accessible sans authentification
et voir son contenu.
"""

import requests

IP = "82.66.186.234"
PORT = 8080

URLS_A_TESTER = [
    f"http://{IP}:{PORT}/feed/dedicated-server-stats.xml",
    f"http://{IP}:{PORT}/feed/dedicated-server-stats.xml?dsstype=json",
    f"http://{IP}:{PORT}/feed/dedicated-server-savegame.html",
]

for url in URLS_A_TESTER:
    try:
        resp = requests.get(url, timeout=5)
        print(f"[OK] {url}")
        print(f"     status={resp.status_code}")
        print(f"     body={resp.text[:500]}")
        print()
    except Exception as e:
        print(f"[echec] {url}: {e}")
        print()
