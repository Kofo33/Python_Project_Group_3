# Python_Project_Group_3
# The Crystal of Eldoria

The Crystal of Eldoria is a turn-based 2D RPG developed in Python using Pygame and SQLite. Players take on the role of a Knight battling through a mystical forest to defeat enemies (Bandit I, Bandit II, Wizard, and Bringer of Death) and recover the stolen Crystal of Light. The game features four levels, a main menu with save/load functionality, and immersive combat visuals with health bars, sprites, and victory/defeat screens. This project was created by a four-person team for a one-week development cycle, completed by August 16, 2025.

## Table of Contents
- [Features](#features)
- [Gameplay](#gameplay)
- [Installation](#installation)
- [Running the Game](#running-the-game)
- [File Structure](#file-structure)
- [Dependencies](#dependencies)
- [Assets](#assets)
- [Contributors](#contributors)

## Features
**Four Levels:**
- **Level 1 (Bandit I):** Fight a Bandit (Health: 50, Attack: 5) to earn a Dagger (+5 attack bonus) and level up to Level 2.  
- **Level 2 (Bandit II):** Battle a stronger Bandit (Health: 50, Attack: variable) to earn a Sword (+15 attack bonus).  
- **Level 3 (Wizard):** Face a Wizard (Health: TBD, Attack: TBD) to earn a new reward (TBD).  
- **Level 4 (Bringer of Death):** Confront the final boss, Bringer of Death (Health: TBD, Attack: TBD), to complete the quest for the Crystal of Light.  

**Turn-Based Combat:** Choose actions (Attack, Heal, Flee) using keys A, H, or ESC, with dynamic health bars and combat messages.  

**Main Menu:** Options for "New Game" (prompts for username), "Load" (via SQLite), and "Exit".  

**Pygame Visuals:** Displays sprites, health bars, victory/defeat screens, and a username input screen with a custom background.  

**SQLite Persistence:** Saves player progress (Name, Health, Attack, Level, XP, Skills, Weapon) after each battle.  

## Gameplay
**Main Menu:**
- Select "New Game" to enter a username and start as a Level 1 Knight (Health: 100, Attack: 30, Fists).  
- Choose "Load" to resume from a saved game.  
- Select "Exit" to quit.  

**Combat:**
- Level 1: Face Bandit I. Defeating the Bandit grants a Dagger and levels up the Knight (Health: 120, Attack: 45).  
- Level 2: Face Bandit II. Defeating it grants a Sword.  
- Level 3: Face the Wizard. Defeating it grants an Axe.  
- Level 4: Face the Bringer of Death. Defeating it completes the quest.  

Victory shows a "Victory" screen with "Next Level" or "End Game" buttons; defeat shows a "Defeat" screen with "Restart" or "End Game" buttons.  

**Progression:** Player stats and weapons are saved after each battle using SQLite, allowing continuation via the "Load" option.  

## Installation
Clone the Repository:
```bash
git clone <repository-url>
cd rpg_game
```

Install Dependencies (Python 3.8+ required):
```bash
pip install pygame
```
SQLite is included in Python’s standard library.  

Download Assets: Place the required image assets in the `assets/img/` folder (see [Assets](#assets)).  

## Running the Game
Navigate to the project directory:
```bash
cd rpg_game
```

Run the main script:
```bash
python main.py
```

**Combat Controls:**
- `A`: Attack  
- `H`: Heal  
- `ESC`: Flee  

After victory/defeat, use arrow keys and Enter to select "Next Level", "Restart", or "End Game".  

## File Structure
```plaintext
rpg_game/
├── assets/
│   ├── img/
│   │   ├── Background/
│   │   │   ├── background.png
│   │   │   ├── bg_username.png
│   │   │   ├── home_page_background.jpg
│   │   ├── Icons/
│   │   │   ├── victory.png
│   │   │   ├── defeat.png
│   │   ├── Logo/
│   │   │   ├── game_logo.png
│   │   ├── Knight/Attack/0.png
│   │   ├── Bandit/Idle/0.png
│   │   ├── BanditII/Idle/0.png
│   │   ├── Wizard/Idle/0.png
│   │   ├── BringerOfDeath/Idle/0.png
├── classes/
│   ├── constant.py
│   ├── enemy.py
│   ├── health_bar.py
│   ├── player.py
├── save_load.py
├── display.py
├── game_logic.py
├── main.py
├── game_database.db
├── README.md
```

## Dependencies
- Python: 3.12 or higher  
- Pygame: `pip install pygame`  
- SQLite: Included in Python’s standard library  
- Assets: Image files from OpenGameArt or similar sources  

## Assets
Assets are stored in `assets/img/`. Required:  
- **Backgrounds:** `background.png`, `bg_username.png`, `home_page_background.jpg`  
- **Sprites:** Knight, Bandit, Wizard, Bringer of Death  
- **Icons:** `victory.png`, `defeat.png`  
- **Logo:** `game_logo.png`  

## Contributors
- Ozuzu Angel Edwin Iruoma  
- Michael Orinya  
- Idowu Kofoworola  
- Osundeyi Emmanuel Bamidele  
