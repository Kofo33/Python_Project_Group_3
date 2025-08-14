# game_logic.py

import time
import pygame
import sys
from classes.constant import WIDTH, HEIGHT, FPS, WHITE, RED, BLACK,YELLOW

SCREEN_WIDTH = WIDTH
SCREEN_HEIGHT = HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

input_bg = pygame.image.load("assets/img/Background/bg_username.png").convert_alpha()
# input_bg = pygame.transform.scale(input_bg, (WIDTH, HEIGHT))


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
        if enemy.name == "Wizard":
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

def get_username():
    """Prompt player to enter a username before the game starts."""
    username = ""
    font = pygame.font.SysFont('Comic Sans MS', 25)
    input_active = True

    while input_active:
        screen.fill(BLACK)
        screen.blit(input_bg,(10,-50))
        prompt_text = font.render("Enter your username:", True, YELLOW)
        screen.blit(prompt_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))

        # Draw input box
        input_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 40)
        pygame.draw.rect(screen, YELLOW, input_rect, 2)

        # Render current text
        text_surface = font.render(username, True, WHITE)
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username.strip() != "":
                    input_active = False  # Exit loop when username entered
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    if len(username) < 15:  # limit name length
                        username += event.unicode

    return username

