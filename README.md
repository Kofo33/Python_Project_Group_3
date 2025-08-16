Python_Project_Group_3
The Crystal of Eldoria
The Crystal of Eldoria is a turn-based 2D RPG developed in Python using Pygame and SQLite. Players take on the role of a Knight battling through a mystical forest to defeat enemies (Bandit I, Bandit II, Wizard, and Bringer of Death) and recover the stolen Crystal of Light. The game features four levels, a main menu with save/load functionality, and immersive combat visuals with health bars, sprites, and victory/defeat screens. This project was created by a four-person team for a one-week development cycle, completed by August 16, 2025.
Table of Contents

Features
Gameplay
Installation
Running the Game
File Structure
Dependencies
Team Roles
Assets
Contributors

Features
Four Levels:

Level 1 (Bandit I): Fight a Bandit (Health: 50, Attack: 5) to earn a Dagger (+5 attack bonus) and level up to Level 2.

Level 2 (Bandit II): Battle a stronger Bandit (Health: 50, Attack: variable) to earn a Sword (+15 attack bonus).

Level 3 (Wizard): Face a Wizard (Health: TBD, Attack: TBD) to earn a new reward (TBD).

Level 4 (Bringer of Death): Confront the final boss, Bringer of Death (Health: TBD, Attack: TBD), to complete the quest for the Crystal of Light.

Turn-Based Combat: Choose actions (Attack, Heal, Flee) using keys A, H, or ESC, with dynamic health bars and combat messages.

Main Menu: Options for "New Game" (prompts for username), "Load" (via SQLite), and "Exit".

Pygame Visuals: Displays sprites, health bars, victory/defeat screens, and a username input screen with a custom background.

SQLite Persistence: Saves player progress (Name, Health, Attack, Level, XP, Skills, Weapon) after each battle.


Gameplay
Main Menu:

Select "New Game" to enter a username and start as a Level 1 Knight (Health: 100, Attack: 30, Fists).
Choose "Load" to resume from a saved game.
Select "Exit" to quit.

Combat:

Level 1: Face the Bandit I. Use A (Attack), H (Heal), or ESC (Flee). Defeating the Bandit grants a Dagger and levels up the Knight (Health: 120, Attack: 45).
Level 2: Face the Bandit II. Defeating it grants a Sword. Health bars show real-time health for the Knight and enemy.
Level 3: Face the Wizard. Defeating it grants an Axe. Health bars show real-time health for the Knight and enemy.
Level 4: Face the Bringer of Death. Defeating it grants a Sword. Health bars show real-time health for the Knight and enemy.
Victory shows a "Victory" image with "Next Level" or "End Game" buttons; defeat shows a "Defeat" image with "Restart" or "End Game" buttons.

Progression:
Player stats and weapons are saved after each battle using SQLite, allowing continuation via the "Load" option.
Installation

Clone the Repository:
git clone <repository-url>
cd rpg_game


Install Dependencies: Ensure Python 3.8+ is installed, then install Pygame and SQLite:
pip install pygame

SQLite is included in Python’s standard library.

Download Assets: Place the required image assets in the assets/img/ folder (see Assets).


Running the Game

Navigate to the project directory:
cd rpg_game


Run the main script:
python main.py


Use the main menu to start a new game (enter a username), load a saved game, or exit.

In combat, press:

A: Attack the enemy.
H: Heal yourself.
ESC: Flee the battle.


After victory/defeat, use arrow keys and Enter to select "Next Level", "Restart", or "End Game".


File Structure
rpg_game/
├── assets/
│   ├── img/
│   │   ├── Background/
│   │   │   ├── background.png        # Combat background
│   │   │   ├── bg_username.png       # Username input background
│   │   │   ├── home_page_background.jpg  # Main menu background
│   │   ├── Icons/
│   │   │   ├── victory.png           # Victory screen image
│   │   │   ├── defeat.png            # Defeat screen image
│   │   ├── Logo/
│   │   │   ├── game_logo.png         # Main menu logo
│   │   ├── Knight/
│   │   │   ├── Attack/
│   │   │   │   ├── 0.png            # Knight sprite
│   │   ├── Bandit/
│   │   │   ├── Idle/
│   │   │   │   ├── 0.png            # Bandit sprite
│   │   ├── BanditII/
│   │   │   ├── Idle/
│   │   │   │   ├── 0.png            # BanditII sprite (placeholder)
│   │   ├── Wizard/
│   │   │   ├── Idle/
│   │   │   │   ├── 0.png            # Wizard sprite (placeholder)
│   │   ├── BringerOfDeath/
│   │   │   ├── Idle/
│   │   │   │   ├── 0.png            # Bringer of Death sprite (placeholder)
├── classes/
│   ├── constant.py                   # Game constants (WIDTH, HEIGHT, FPS, colors)
│   ├── enemy.py                     # Enemy class (Bandit, Wizard, Bandit II, Bringer of Death)
│   ├── health_bar.py                # HealthBar class for rendering health
│   ├── player.py                    # Player class (Knight)
├── save_load.py                      # SQLite database for saving/loading player
├── display.py                       # Pygame menu and combat visuals
├── game_logic.py                    # Combat logic and username input
├── main.py                          # Main game loop
├── game_database.db                 # SQLite database file
├── README.md                        # This file

Dependencies

Python: 3.12 or higher
Pygame: pip install pygame
SQLite: Included in Python’s standard library
Assets: Image files from OpenGameArt or similar (see Assets)

Assets
Assets are stored in assets/img/. Download or create the following:

Backgrounds: background.png, bg_username.png, home_page_background.jpg (e.g., from OpenGameArt).
Sprites: Knight/Attack/0.png, Bandit/Idle/0.png, Wizard/Idle/0.png (placeholder for Wizard; use Kenney or OpenGameArt).
Icons: victory.png, defeat.png (e.g., from OpenGameArt).
Logo: game_logo.png (custom or from free resources). Ensure all images are PNG with transparency or JPG as specified and match the folder structure.

Contributors

Ozuzu Angel Edwin Iruoma
Michael Orinya
Idowu Kofoworola
Osundeyi Emmanuel Bamidele
