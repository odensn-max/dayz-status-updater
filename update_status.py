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
    {"name": "Chernarus - Vanilla", "ip": "82.66.186.234", "query_port": 2403, "game_port": 2402},
    {"name": "Takistan",            "ip": "82.66.186.234", "query_port": 2503, "game_port": 2502},
    {"name": "Namalsk",             "ip": "82.66.186.234", "query_port": 2603, "game_port": 2602},
    {"name": "Deerisle v6 No Mods", "ip": "82.66.186.234", "query_port": 2703, "game_port": 2702},
    {"name": "Bitteroot - Vanilla", "ip": "82.66.186.234", "query_port": 2303, "game_port": 2302},
]

ACEVO_SERVER = {
    "name": "ALL CARS - Nurburgring Touristenfahrten - 1363 Community",
    "ip": "82.66.186.234",
    "http_port": 8080,
    "game_port": 9700,
    "max_players": 50,
}

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


def query_acevo(server):
    """Interroge l'API HTTP du serveur Assetto Corsa EVO.
       Renvoie le meme format que query_dayz pour que le front-end
       puisse traiter les deux jeux de facon uniforme."""
    url = f"http://{server['ip']}:{server['http_port']}/"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            player_count = data.get("clients", 0)
            return {
                "name": server["name"],
                "game": "assetto",
                "ip": server["ip"],
                "port": server["game_port"],
                "status": "online",
                "map": None,
                "players": player_count,
                "maxPlayers": server["max_players"],
            }
    except Exception:
        pass
    return {
        "name": server["name"],
        "game": "assetto",
        "ip": server["ip"],
        "port": server["game_port"],
        "status": "offline",
        "map": None,
        "players": 0,
        "maxPlayers": server["max_players"],
    }


def main():
    servers = [query_dayz(s) for s in DAYZ_SERVERS]
    servers.append(query_acevo(ACEVO_SERVER))

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
