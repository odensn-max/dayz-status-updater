"""
update_status.py — execute une seule fois puis s'arrete.
Concu pour etre lance par GitHub Actions toutes les 5 minutes.

Ecrit dans la table site_data (cle "site:servers"), le meme
emplacement que celui gere par le panel admin du site — index.html
lit deja cette cle directement, aucune modification du site necessaire.
"""

import os
import json
import a2s
from supabase import create_client

# ─── CONFIG ─────────────────────────────────────────────────────────────

SUPABASE_URL = "https://qhnsizbrnwclsdebpbor.supabase.co"
# Lu depuis un secret GitHub (Settings > Secrets and variables > Actions)
SUPABASE_SERVICE_KEY = os.environ["SUPABASE_SERVICE_KEY"]

DAYZ_SERVERS = [
    {"name": "Chernarus - Vanilla", "ip": "82.66.186.234", "query_port": 2403, "game_port": 2402},
    {"name": "Takistan",            "ip": "82.66.186.234", "query_port": 2503, "game_port": 2502},
    {"name": "Namalsk",             "ip": "82.66.186.234", "query_port": 2603, "game_port": 2602},
    {"name": "Deerisle v6 No Mods", "ip": "82.66.186.234", "query_port": 2703, "game_port": 2702},
]

# ─── SUPABASE ───────────────────────────────────────────────────────────

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


def query_dayz(server):
    """Renvoie un objet au format attendu par la fonction card() de index.html :
       { name, game, ip, port, status, map }"""
    try:
        info = a2s.info((server["ip"], server["query_port"]), timeout=5)
        return {
            "name": server["name"],
            "game": "dayz",
            "ip": server["ip"],
            "port": server["game_port"],
            "status": "online",
            "map": info.map_name,
        }
    except Exception:
        return {
            "name": server["name"],
            "game": "dayz",
            "ip": server["ip"],
            "port": server["game_port"],
            "status": "offline",
            "map": None,
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
            print(f"     - {s['name']}: {s['status']} ({s['map']})")
    except Exception as e:
        print(f"[erreur supabase] {e}")
        raise


if __name__ == "__main__":
    main()
