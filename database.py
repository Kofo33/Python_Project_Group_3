import sqlite3
from game_logic import Player

def init_db():
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS player (
            name TEXT PRIMARY KEY,
            health INTEGER,
            attack INTEGER,
            level INTEGER,
            xp INTEGER,
            weapon TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_player(player):
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO player VALUES (?, ?, ?, ?, ?, ?)
    """, (player.name, player.health, player.attack, player.level, player.xp, player.equipped_weapon["name"]))
    conn.commit()
    conn.close()

def load_player(name):
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM player WHERE name = ?", (name,))
    data = cursor.fetchone()
    conn.close()
    if data:
        player = Player(data[0], data[1], data[2], data[3], data[4])
        player.equip_weapon(data[5])
        return player
    return None