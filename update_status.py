"""
update_status.py — execute une seule fois puis s'arrete.
Concu pour etre lance par GitHub Actions (declenche par cron-job.org
toutes les minutes via workflow_dispatch, et par le cron GitHub natif
toutes les 5 minutes en filet de securite).

Ecrit dans la table site_data (cle "site:servers"), le meme
emplacement que celui gere par le panel admin du site — index.html
lit deja cette cle directement, aucune modification du site necessaire.
"""

import os
import a2s
import requests
from supabase import create_client

# ─── CONFIG ─────────────────────────────────────────────────────────────

SUPABASE_URL = "https://qhnsizbrnwclsdebpbor.supabase.co"
SUPABASE_SERVICE_KEY = os.environ["SUPABASE_SERVICE_KEY"]

DAYZ_SERVERS = [
    {"name": "1363 | EUROPE - FR | CHERNARUS - VANILLA", "ip": "82.66.186.234", "query_port": 2403, "game_port": 2402},
    {"name": "1363 | EUROPE - FR | TAKISTAN",            "ip": "82.66.186.234", "query_port": 2503, "game_port": 2502},
    {"name": "1363 | EUROPE - FR | NAMALSK",             "ip": "82.66.186.234", "query_port": 2603, "game_port": 2602},
    {"name": "1363 | EUROPE - FR | DEERISLE v6 - VANILLA - No Mods", "ip": "82.66.186.234", "query_port": 2703, "game_port": 2702},
    {"name": "Bitteroot - Vanilla", "ip": "82.66.186.234", "query_port": 2303, "game_port": 2302},
]

# ─── SUPABASE ───────────────────────────────────────────────────────────

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


def query_dayz(server):
    """Renvoie un objet au format attendu par la fonction card() de index.html :
       { name, game, ip, port, status, map, players, maxPlayers }"""
    try:
        info = a2s.info((server["ip"], server["query_port"]), timeout=5)
        return {
            "name": server["name"],
            "game": "dayz",
            "ip": server["ip"],
            "port": server["game_port"],
            "status": "online",
            "map": info.map_name,
            "players": info.player_count,
            "maxPlayers": info.max_players,
        }
    except Exception:
        return {
            "name": server["name"],
            "game": "dayz",
            "ip": server["ip"],
            "port": server["game_port"],
            "status": "offline",
            "map": None,
            "players": 0,
            "maxPlayers": None,
        }


def main():
    servers = [query_dayz(s) for s in DAYZ_SERVERS]

    try:
        supabase.table("site_data").upsert({
            "key": "site:servers",
            "value": servers,
        }).execute()
        print(f"[ok] site:servers mis a jour avec {len(servers)} serveurs")
        for s in servers:
            print(f"     - {s['name']}: {s['status']} ({s['players']}/{s['maxPlayers']} joueurs, {s['map']})")
    except Exception as e:
        print(f"[erreur supabase] {e}")
        raise


if __name__ == "__main__":
    main()
