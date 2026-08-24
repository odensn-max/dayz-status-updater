"""
update_status.py — execute une seule fois puis s'arrete.
Concu pour etre lance par GitHub Actions toutes les 5 minutes.
"""

import os
import a2s
from supabase import create_client

# ─── CONFIG ─────────────────────────────────────────────────────────────

SUPABASE_URL = "https://qhnsizbrnwclsdebpbor.supabase.co"
# La cle est lue depuis une variable d'environnement (secret GitHub),
# jamais ecrite en clair dans ce fichier.
SUPABASE_SERVICE_KEY = os.environ["SUPABASE_SERVICE_KEY"]

DAYZ_SERVERS = [
    {"name": "Chernarus - Vanilla", "ip": "82.66.186.234", "query_port": 2403, "game_port": 2402, "max": 60},
    {"name": "Takistan",            "ip": "82.66.186.234", "query_port": 2503, "game_port": 2502, "max": 60},
    {"name": "Namalsk",             "ip": "82.66.186.234", "query_port": 2603, "game_port": 2602, "max": 60},
    {"name": "Deerisle v6 No Mods", "ip": "82.66.186.234", "query_port": 2703, "game_port": 2702, "max": 60},
]

# ─── SUPABASE ───────────────────────────────────────────────────────────

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


def query_dayz(server):
    try:
        info = a2s.info((server["ip"], server["query_port"]), timeout=5)
        return {
            "name": server["name"],
            "game": "DayZ",
            "online": True,
            "players": info.player_count,
            "max_players": info.max_players,
            "map": info.map_name,
            "address": f"{server['ip']}:{server['game_port']}",
        }
    except Exception:
        return {
            "name": server["name"],
            "game": "DayZ",
            "online": False,
            "players": 0,
            "max_players": server["max"],
            "map": None,
            "address": f"{server['ip']}:{server['game_port']}",
        }


def main():
    for srv in DAYZ_SERVERS:
        data = query_dayz(srv)
        try:
            supabase.table("server_status").upsert(data).execute()
            print(f"[ok] {data['name']} -> online={data['online']} players={data['players']}")
        except Exception as e:
            print(f"[erreur supabase] {data['name']}: {e}")


if __name__ == "__main__":
    main()
