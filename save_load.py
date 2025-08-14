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


def load_game():
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM player LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if row:
        player = Player(x=WIDTH//2, y=HEIGHT//2, name=row[0], level=row[1])
        player.health = row[2]
        player.attack = row[3]
        player.xp = row[4]
        player.inventory = json.loads(row[5])
        print("✅ Game loaded from database.")
        return player, player.level
    else:
        print("⚠️ No saved game found.")
        return None, 1
