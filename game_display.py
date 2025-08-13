import pygame
import time  # For brief delays in displaying results
from game_logic import Player, Enemy  # Import classes, but not combat (we'll recreate the loop here)

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Crystal of Eldoria")
FONT = pygame.font.SysFont("arial", 24)
SMALL_FONT = pygame.font.SysFont("arial", 18)

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Load assets (update paths; use different enemy sprites if available)
background_img = pygame.image.load("assets/forest.png")
player_img = pygame.image.load("assets/player.png")

# Enemy sprites (load specific ones based on enemy name)
enemy_sprites = {
    "Goblin": pygame.image.load("assets/goblin.png"),
    "Wolf": pygame.image.load("assets/wolf.png"),
    "Shadow Knight": pygame.image.load("assets/knight.png")
}

def draw_health_bar(x, y, current, max_health, color):
    bar_width = 200
    bar_height = 20
    fill = (current / max_health) * bar_width
    pygame.draw.rect(screen, color, (x, y, fill, bar_height))
    pygame.draw.rect(screen, WHITE, (x, y, bar_width, bar_height), 2)  # Border

def display_text(text, x, y, font=FONT, color=WHITE):
    rendered = font.render(text, True, color)
    screen.blit(rendered, (x, y))

def show_result(message, color=YELLOW, duration=2):
    display_text(message, 300, 450, SMALL_FONT, color)
    pygame.display.flip()
    time.sleep(duration)  # Brief pause to show result

def display_combat(player, enemy):
    # Get enemy sprite
    enemy_img = enemy_sprites.get(enemy.name, pygame.image.load("assets/goblin.png"))  # Fallback to goblin

    running = True
    result = None
    while running and player.health > 0 and enemy.health > 0:
        screen.blit(background_img, (0, 0))
        screen.blit(player_img, (100, 300))
        screen.blit(enemy_img, (600, 300))

        # Health bars and labels
        display_text(f"{player.name}: {player.health}/{player.max_health()} HP", 100, 50)
        draw_health_bar(100, 80, player.health, player.max_health(), GREEN)
        display_text(f"{enemy.name}: {enemy.health}/{enemy.max_health} HP", 600, 50)
        draw_health_bar(600, 80, enemy.health, enemy.max_health, RED)

        # Action prompt
        display_text("Actions: 1. Basic Attack  2. Heal  3. Run", 200, 500)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Basic Attack
                    res, damage = player.use_skill("Basic Attack", enemy)
                    if damage == 0:
                        show_result("You missed!", RED)
                    else:
                        show_result(res, GREEN)
                elif event.key == pygame.K_2:  # Heal
                    res, _ = player.use_skill("Heal")
                    show_result(res, GREEN)
                elif event.key == pygame.K_3:  # Run
                    show_result("You fled the battle!", YELLOW)
                    result = False
                    running = False

                # Check if enemy defeated after player action
                if enemy.health <= 0:
                    show_result(f"{enemy.name} defeated!", GREEN)
                    leveled_up = player.gain_xp(50)
                    if leveled_up:
                        show_result(f"{player.name} leveled up to level {player.level}!", YELLOW)
                    if enemy.name == "Wolf":
                        new_weapon = {"name": "Sword", "bonus": 0}
                        player.add_item(new_weapon)
                        player.equip_weapon("Sword")
                        show_result("You obtained a sword from the enemy!", YELLOW)
                    result = True
                    running = False
                    break  # Exit event loop

                # Enemy's turn if still alive
                if enemy.health > 0:
                    enemy_res, value = enemy.perform_action(player)
                    show_result(enemy_res, RED)

                # Check if player defeated after enemy action
                if player.health <= 0:
                    show_result("You were defeated...", RED)
                    result = False
                    running = False

    return result

# Note: Call this from main.py like: result = display_combat(player, enemy)