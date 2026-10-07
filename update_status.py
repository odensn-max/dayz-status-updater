"""
update_status.py — execute une seule fois puis s'arrete.
Lance par GitHub Actions (cron toutes les 5 min + declenchement manuel).

Interroge chaque serveur DayZ (protocole A2S) puis envoie la liste a
https://nikolezin.fr/api/servers_push.php, qui l'ecrit dans la table MySQL
site_data (cle "site:servers"). index.html lit deja cette cle.
"""

import os
import sys
import a2s
import requests

# ─── CONFIG ─────────────────────────────────────────────────────────────

# URL de l'endpoint du site (modifiable via le secret/variable SERVERS_PUSH_URL)
PUSH_URL = os.environ.get("SERVERS_PUSH_URL", "https://nikolezin.fr/api/servers_push.php")
# Meme valeur que SERVERS_TOKEN dans api/config.php
PUSH_TOKEN = os.environ["SERVERS_TOKEN"]

DAYZ_SERVERS = [
    {"name": "1363 | EUROPE - FR | CHERNARUS - VANILLA", "ip": "82.66.186.234", "query_port": 2403, "game_port": 2402},
    {"name": "1363 | EUROPE - FR | TAKISTAN",            "ip": "82.66.186.234", "query_port": 2503, "game_port": 2502},
    {"name": "1363 | EUROPE - FR | NAMALSK",             "ip": "82.66.186.234", "query_port": 2603, "game_port": 2602},
    {"name": "1363 | EUROPE - FR | DEERISLE v6 - VANILLA - No Mods", "ip": "82.66.186.234", "query_port": 2703, "game_port": 2702},
    {"name": "1363 | EUROPE - FR | BITTERROOT - VANILLA", "ip": "82.66.186.234", "query_port": 2303, "game_port": 2302},
]

# ────────────────────────────────────────────────────────────────────────


def query_dayz(server):
    """Format attendu par card() dans index.html :
       { name, game, ip, port, status, map, players, maxPlayers }"""
    base = {
        "name": server["name"],
        "game": "dayz",
        "ip": server["ip"],
        "port": server["game_port"],
    }
    try:
        info = a2s.info((server["ip"], server["query_port"]), timeout=5)
        return {**base, "status": "online", "map": info.map_name,
                "players": info.player_count, "maxPlayers": info.max_players}
    except Exception:
        return {**base, "status": "offline", "map": None,
                "players": 0, "maxPlayers": None}


def main():
    servers = [query_dayz(s) for s in DAYZ_SERVERS]

    try:
        r = requests.post(
            PUSH_URL,
            json=servers,
            headers={"X-Token": PUSH_TOKEN},
            timeout=20,
        )
        r.raise_for_status()
    except Exception as e:
        print(f"[erreur site] {e}")
        sys.exit(1)

    print(f"[ok] site:servers mis a jour avec {len(servers)} serveurs")
    for s in servers:
        print(f"     - {s['name']}: {s['status']} ({s['players']}/{s['maxPlayers']} joueurs, {s['map']})")


if __name__ == "__main__":
    main()
