# game_logic.py

import time
import pygame

def combat(player, enemy, keys):
    action = None
    if keys == 1:  # Attack
        action = 1
    elif keys == 2:  # Heal
        action = 2
    elif keys == 3:  # Flee
        action = 3

    if action == 1:
        print("You chose to attack!")
        result, damage = player.use_skill("Basic Attack", enemy)
        if damage == 0:
            print("You missed!")
        else:
            print(result)

    elif action == 2:
        result, _ = player.use_skill("Heal")
        print(result)

    elif action == 3:
        print("You fled the battle!")
        return "fled"

    # Check if enemy is dead
    if enemy.health <= 0:
        enemy.death()
        print(f"{enemy.name} defeated!")
        leveled_up = player.gain_xp(50)
        if leveled_up:
            print(f"{player.name} leveled up to level {player.level}! Heal skill upgraded.")
        if enemy.name == "Wolf":
            new_weapon = {"name": "Sword", "bonus": 0}
            player.add_item(new_weapon)
            player.equip_weapon("Sword")
            print("You obtained a sword from the enemy!")
        return "victory"

    # Enemy attacks after player’s turn
    pygame.time.delay(500)
    damage = enemy.attack_player(player)
    if damage == 0:
        print(f"{enemy.name} missed!")
    else:
        print(f"{enemy.name} deals {damage} damage to you!")

    if player.health <= 0:
        player.death()
        print("You were defeated...")
        return "defeat"

    return None
