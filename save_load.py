import sqlite3
import json
from classes.player import Player
from classes.constant import WIDTH, HEIGHT

DB_FILE = "game_database.db"

def init_db():
    """
    Initializes the SQLite database by creating the 'player' table if it doesn't exist.
    """
    try:
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
    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")
    finally:
        if conn:
            conn.close()

def save_game(player, level_count):
    """
    Saves the current game state of a player to the database.

    Args:
        player (Player): The player object containing game state.
        level_count (int): The current level count (not stored but may be used elsewhere).
    """
    init_db()
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Convert inventory list to JSON string
        try:
            inventory_json = json.dumps(player.inventory)
        except (TypeError, ValueError) as e:
            print(f"Error serializing inventory: {e}")
            inventory_json = "[]"

        # Insert or update player data
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
        print("Game saved to database.")
    except sqlite3.Error as e:
        print(f"Error saving game: {e}")
    finally:
        if conn:
            conn.close()

def fetch_all_players():
    """
    Fetches all saved player data from the database.

    Returns:
        list: A list of dictionaries containing player data.
    """
    init_db()
    players = []

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM player")
        rows = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error fetching players: {e}")
        return players
    finally:
        if conn:
            conn.close()

    # Convert each row into a dictionary
    for row in rows:
        try:
            inventory = json.loads(row[5]) if row[5] else []
        except (TypeError, ValueError) as e:
            print(f"Error deserializing inventory for {row[0]}: {e}")
            inventory = []

        player_data = {
            "name": row[0],
            "level": row[1],
            "health": row[2],
            "attack": row[3],
            "xp": row[4],
            "inventory": inventory
        }
        players.append(player_data)

    return players

def load_game(name):
    """
    Loads a saved game state for a player from the database.

    Args:
        name (str): The name of the player to load.

    Returns:
        Player or tuple: The Player object if found, otherwise (None, 1).
    """
    init_db()
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM player WHERE name = ?", (name,))
        row = cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Error loading game: {e}")
        return None, 1
    finally:
        if conn:
            conn.close()

    if row:
        try:
            inventory = json.loads(row[5])
        except (TypeError, ValueError) as e:
            print(f"Error deserializing inventory for {name}: {e}")
            inventory = []

        # Create Player object with loaded data
        player = Player(250, 370, name=row[0], health=row[2], attack=row[3], level=row[1], xp=row[4])
        player.inventory = inventory
        print(f"Game loaded for {name}.")
        return player
    else:
        print(f"No saved game found for {name}.")
        return None, 1
