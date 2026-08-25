"""
test_acevo_port_v2.py — deuxieme passe de test pour trouver le port
HTTP d'Assetto Corsa EVO, en testant des ports proches de ceux deja
connus (Farming: 8080/8443, DayZ: 2302-2803) et quelques valeurs
standards pour les serveurs de jeu avec API HTTP.
"""

import requests

IP = "82.66.186.234"
PORTS_A_TESTER = [
    8443,  # port HTTPS habituel a cote du 8080 (vu dans la doc Farming)
    9701, 9702, 9703,  # variantes autour du port de jeu 9700
    9600, 9800,
    8181, 8280,
    18080,
    7700, 7701,
]

for port in PORTS_A_TESTER:
    for scheme in ["http", "https"]:
        url = f"{scheme}://{IP}:{port}/"
        try:
            resp = requests.get(url, timeout=4, verify=False)
            print(f"[OK] {url}: status={resp.status_code} body={resp.text[:150]}")
        except Exception as e:
            print(f"[echec] {url}: {type(e).__name__}")
