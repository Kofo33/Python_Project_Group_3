import sqlite3
import json
from classes.player import Player
from classes.constant import WIDTH, HEIGHT


DB_FILE = "game_database.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS player (
            name TEXT PRIMARY KEY,
            level INTEGER,
            health INTEGER,
            attack_power INTEGER,
            xp INTEGER,
            inventory TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_game(player, level_count):
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    inventory_json = json.dumps(player.inventory)

    cursor.execute("""
        INSERT OR REPLACE INTO player (
            name, level, health, attack_power, xp, inventory
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        player.name,
        player.level,
        player.health,
        player.attack,
        player.xp,
        inventory_json
    ))

    conn.commit()
    conn.close()
    print("💾 Game saved to database.")


def load_game(name):
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM player WHERE name = ?", (name,))
    row = cursor.fetchone()
    conn.close()

    if row:
        player = Player(250, 370, name=row[0], health=row[2], attack=row[3], level=row[1], xp=row[4])
        player.inventory = json.loads(row[5])
        print(f"✅ Game loaded for {name}.")
        return player, player.level
    else:
        print(f"⚠️ No saved game found for {name}.")
        return None, 1

