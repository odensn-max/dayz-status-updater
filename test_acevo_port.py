"""
test_acevo_port.py — script temporaire, a lancer UNE FOIS via
GitHub Actions pour trouver le bon port HTTP du serveur Assetto Corsa
EVO. A supprimer une fois le port trouve.
"""

import requests

IP = "82.66.186.234"
PORTS_A_TESTER = [8080, 9700, 8081, 8082, 80, 8090, 8000, 9701, 9702, 3000]

for port in PORTS_A_TESTER:
    url = f"http://{IP}:{port}/"
    try:
        resp = requests.get(url, timeout=5)
        print(f"[OK] port {port}: status={resp.status_code} body={resp.text[:200]}")
    except Exception as e:
        print(f"[echec] port {port}: {e}")
