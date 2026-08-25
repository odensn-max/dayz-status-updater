"""
test_bitteroot_port.py — script temporaire, a lancer UNE FOIS via
GitHub Actions (workflow_dispatch) pour trouver le bon port de requete
du serveur Bitteroot. A supprimer une fois le port trouve.
"""

import a2s

IP = "82.66.186.234"
PORTS_A_TESTER = [2302, 2303, 2402, 2403, 27015, 27016, 27017, 2802, 2803]

for port in PORTS_A_TESTER:
    try:
        info = a2s.info((IP, port), timeout=5)
        print(f"[OK] port {port}: {info.server_name} | map={info.map_name} | {info.player_count}/{info.max_players}")
    except Exception as e:
        print(f"[echec] port {port}: {e}")
