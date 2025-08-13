import pygame
from game_logic import Player, Enemy
from game_display import display_combat
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

    # Story prompts for each enemy
    story_prompts = {
        "Goblin": (
            "\n🌲 You step into the shadowy Eldorian forest, the air thick with mist.\n"
            "A rustling in the bushes reveals a snarling Goblin, clutching a crude dagger.\n"
            "It lunges, eager to protect its master’s dark plans!"
        ),
        "Wolf": (
            "\n🐺 Deeper in the forest, the trees grow denser, and a chilling howl echoes.\n"
            "A massive Wolf emerges, its eyes glowing with Malakar’s corruption.\n"
            "It bares its fangs, ready to tear you apart!"
        ),
        "Shadow Knight": (
            "\n⚔️ At the heart of the forest, a dark clearing pulses with evil energy.\n"
            "The Shadow Knight, Malakar’s fiercest lieutenant, stands before the stolen Crystal.\n"
            "Its blade gleams as it vows to crush you!"
        )
    }

    for enemy in enemies:
        print(story_prompts[enemy.name])  # Display story prompt in console
        result = display_combat(player, enemy)  # Use Pygame combat
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