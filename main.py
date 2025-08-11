import pygame
from game_logic import Player, Enemy, combat
from database import init_db, save_player, load_player

def main():
    pygame.init()
    init_db()

    print("🌟 The Crystal of Eldoria 🌟")
    print("The Crystal of Light has been stolen by Malakar, plunging Eldoria into chaos.")
    print("You are chosen to retrieve it. Battle through the forest to face the Shadow Knight!")

    choice = input("1. New Game\n2. Load Game\n3. Quit\nChoose: ")
    if choice == "1":
        name = input("Enter your hero’s name: ")
        player = Player(name)
    elif choice == "2":
        name = input("Enter your hero’s name: ")
        player = load_player(name)
        if not player:
            print("No saved game found. Starting new game.")
            player = Player(name)
    else:
        print("Goodbye.")
        return

    # Initial weapon setup (Fists already equipped at level 1)
    print(f"{player.name} begins their journey with Fists.")

    # Define enemies with appropriate stats
    enemies = [
        Enemy("Goblin", health=50, attack=5),
        Enemy("Wolf", health=70, attack=7),
        Enemy("Shadow Knight", health=100, attack=10)
    ]

    for enemy in enemies:
        print(f"\n⚔️ A wild {enemy.name} appears!")
        result = combat(player, enemy)
        if not result:
            print("Game Over.")
            break
        save_player(player)
    else:
        print("\n🏆 You defeated the Shadow Knight and retrieved the Crystal of Light!")
        print("✨ Eldoria is saved!")

    pygame.quit()

if __name__ == "__main__":
    main()
