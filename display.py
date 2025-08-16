import sys
import pygame
from classes.constant import WIDTH, HEIGHT, FPS, WHITE, RED, BLACK, YELLOW  # Game constants
from classes.enemy import Enemy  # Enemy class
from classes.health_bar import HealthBar  # Health bar UI
from classes.player import Player  # Player character
from game_logic import combat, get_username  # Game logic functions
from save_load import fetch_all_players, save_game, load_game  # Save/load functions

# Initialize pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Crystal of Eldoria")
FONT = pygame.font.SysFont("arial", 24)  # Font for UI text

# -----------------------------
# Load game assets (images)
# -----------------------------
background_img = pygame.image.load("assets/img/Background/background.png").convert_alpha()
victory_img = pygame.image.load("assets/img/Icons/victory.png").convert_alpha()
defeat_img = pygame.image.load("assets/img/Icons/defeat.png").convert_alpha()

# Game logo
logo_img = pygame.image.load("assets/img/Logo/game_logo.png").convert_alpha()
logo_img = pygame.transform.scale(logo_img, (250, 150))
logo_x = (WIDTH - logo_img.get_width()) // 2  # Center horizontally
logo_y = 50  # Top padding

# Main menu background
mainmenu_img = pygame.image.load("assets/img/Background/home_page_background.jpg").convert_alpha()
mainmenu_img = pygame.transform.scale(mainmenu_img, (WIDTH, HEIGHT))

# -----------------------------
# Enemy instances
# -----------------------------
bandit = Enemy(550, 380, "Bandit")
bandit2 = Enemy(550, 380, "Bandit2")
wizard = Enemy(500, 248, "Wizard")
bringer = Enemy(500, 248, "Bringer")
huntress = Enemy(500, 248, "Huntress")

# -----------------------------
# Health bar instances
# -----------------------------
bringer_health_bar = HealthBar(550, 50, "Bringer", bringer.health, 80)
huntress_health_bar = HealthBar(550, 50, "Huntress", huntress.health, 70)
bandit_health_bar = HealthBar(550, 50, "Bandit", bandit.health, 50)
bandit2_health_bar = HealthBar(550, 50, "Bandit2", bandit2.health, 60)
wizard_health_bar = HealthBar(550, 50, "Wizard", wizard.health, 100)

# -----------------------------
# Button positions (menus)
# -----------------------------
play_button_rect = pygame.Rect(WIDTH // 2 - 76, HEIGHT // 2 - 60, 150, 50)
load_button_rect = pygame.Rect(WIDTH // 2 - 76, HEIGHT // 2 + 5, 150, 50)
quit_button_rect = pygame.Rect(WIDTH // 2 - 76, HEIGHT // 2 + 70, 150, 50)
restart_button_rect = pygame.Rect(WIDTH // 2 - 76, HEIGHT // 2 + 5, 150, 50)
next_level_button_rect = pygame.Rect(WIDTH // 2 - 76, HEIGHT // 2 + 5, 150, 50)
end_game_button_rect = pygame.Rect(WIDTH // 2 - 76, HEIGHT // 2 + 70, 150, 50)

# -----------------------------
# Helper function: Draw menu background
# -----------------------------
def animate_screen():
    screen.blit(mainmenu_img, (0, 0))

# -----------------------------
# Main menu screen
# -----------------------------
def display_menu():
    running = True
    selected_button = 0  # Which button is selected (keyboard navigation)
    
    # Button labels, positions, and colors
    buttons = [
        ("New Game", play_button_rect, YELLOW),
        ("Load", load_button_rect, YELLOW),
        ("Exit", quit_button_rect, RED)
    ]
    
    font = pygame.font.SysFont('Comic Sans MS', 25)

    while running:
        animate_screen()  # Draw background
        screen.blit(logo_img, (logo_x, logo_y))  # Draw logo
        mouse_pos = pygame.mouse.get_pos()  # Track mouse position

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Close menu

            # Mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0][1].collidepoint(mouse_pos):  # New Game
                    username = get_username()
                    player = Player(250, 370, username, character_type="Knight")
                    display_combat(player)
                elif buttons[1][1].collidepoint(mouse_pos):  # Load Game
                    loaded_player = load_game_screen()
                    if loaded_player:
                        display_combat(loaded_player)
                elif buttons[2][1].collidepoint(mouse_pos):  # Exit
                    pygame.quit()
                    sys.exit()

            # Keyboard navigation
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_button = (selected_button - 1) % len(buttons)
                elif event.key == pygame.K_DOWN:
                    selected_button = (selected_button + 1) % len(buttons)
                elif event.key == pygame.K_RETURN:
                    if selected_button == 0:
                        username = get_username()
                        player = Player(250, 370, username, character_type="Knight")
                        display_combat(player)
                    elif selected_button == 1:
                        loaded_player = load_game_screen()
                        if loaded_player:
                            display_combat(loaded_player)
                    elif selected_button == 2:
                        pygame.quit()
                        sys.exit()

        # Draw menu buttons
        for i, (label, rect, highlight_color) in enumerate(buttons):
            pygame.draw.rect(screen, BLACK, rect, border_radius=10)  # Button background
            if rect.collidepoint(mouse_pos) or selected_button == i:  # Hover or selected
                pygame.draw.rect(screen, highlight_color, rect, border_radius=10, width=4)
            text_surf = font.render(label, True, WHITE)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

        pygame.display.flip()

# -----------------------------
# Combat screen
# -----------------------------
def display_combat(player):
    knight = player
    knight_health_bar = HealthBar(100, 50, knight.name, knight.health, knight.max_health())
    current_enemy = bandit
    running = True
    clock = pygame.time.Clock()
    end_state = None  # Tracks victory, defeat, or ongoing state
    selected_button = 0  # Menu navigation after combat ends

    # Button configurations for different outcomes
    buttons_of_victory = [("Next Level", next_level_button_rect, YELLOW), ("End Game", end_game_button_rect, RED)]
    buttons_of_defeat = [("Restart", restart_button_rect, YELLOW), ("End Game", end_game_button_rect, RED)]
    buttons_end_only = [("End Game", end_game_button_rect, RED)]
    font = pygame.font.SysFont('Comic Sans MS', 25)

    display_level = knight.level  # Current level of player

    while running:
        screen.blit(background_img, (0, -50))  # Draw combat background

        # Choose current enemy and health bar based on level
        if display_level == 1:
            current_enemy = bandit
        elif display_level == 2:
            current_enemy = bandit2
        elif display_level == 3:
            current_enemy = huntress
        elif display_level == 4:
            current_enemy = bringer
        elif display_level == 5:
            current_enemy = wizard

        # Update and draw characters
        knight.update()
        knight.draw()
        current_enemy.update()
        current_enemy.draw()

        # Draw health bars
        knight_health_bar.draw(knight.health)
        # Always create a fresh health bar for the current enemy with correct max_hp
        enemy_health_bar = HealthBar(550, 50, current_enemy.name, current_enemy.health, current_enemy.health)
        enemy_health_bar.draw(current_enemy.health)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if end_state:  # If combat is over
                if event.type == pygame.KEYDOWN:
                    if display_level == 5:  # Final boss
                        if event.key in [pygame.K_UP, pygame.K_DOWN]:
                            selected_button = 0
                        elif event.key == pygame.K_RETURN:
                            running = False
                    else:  # Other levels
                        if event.key == pygame.K_UP:
                            selected_button = (selected_button - 1) % len(buttons_of_victory)
                        elif event.key == pygame.K_DOWN:
                            selected_button = (selected_button + 1) % len(buttons_of_victory)
                        elif event.key == pygame.K_RETURN:
                            if end_state == "victory":
                                if selected_button == 0:  # Next level
                                    knight.next()
                                    current_enemy.update_stats()
                                    save_game(knight, knight.level)
                                    display_level = knight.level
                                    end_state = None
                                    selected_button = 0
                                elif selected_button == 1:  # End game
                                    running = False
                            elif end_state == "defeat":
                                if selected_button == 0:  # Restart
                                    knight.restart(display_level)
                                    current_enemy.restart()
                                    save_game(knight, knight.level)
                                    end_state = None
                                    selected_button = 0
                                elif selected_button == 1:  # End game
                                    running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_a:  # Attack
                    result = combat(knight, current_enemy, keys=1)
                    if result in ("victory", "defeat"):
                        end_state = result
                elif event.key == pygame.K_h:  # Heal
                    result = combat(knight, current_enemy, keys=2)
                    if result in ("victory", "defeat", "fled"):
                        running = False

        # Post-combat UI
        if end_state == "victory":
            screen.blit(victory_img, (260, 200))
            if display_level == 5:  # Final battle ends game
                buttons_to_display = buttons_end_only
            else:
                buttons_to_display = buttons_of_victory
        elif end_state == "defeat":
            screen.blit(defeat_img, (285, 200))
            buttons_to_display = buttons_of_defeat
        else:
            buttons_to_display = []

        # Draw post-combat buttons
        for i, (label, rect, highlight_color) in enumerate(buttons_to_display):
            pygame.draw.rect(screen, BLACK, rect, border_radius=10)
            if selected_button == i:
                pygame.draw.rect(screen, highlight_color, rect, border_radius=10, width=4)
            text_surf = font.render(label, True, WHITE)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

        pygame.display.flip()
        clock.tick(FPS)

# -----------------------------
# Load game screen
# -----------------------------
def load_game_screen():
    players = fetch_all_players()  # Fetch saved players from database
    clock = pygame.time.Clock()

    # Pre-render player list buttons
    buttons = []
    start_y = 150
    for i, player in enumerate(players):
        label = f"{player['name']} - Lv {player['level']} - HP {player['health']}"
        rect = FONT.render(label, True, (255, 255, 255)).get_rect(center=(400, start_y + i * 60))
        buttons.append((label, rect, player["name"]))

    running = True
    while running:
        screen.fill((30, 30, 30))  # Dark background
        title = FONT.render("Select a Save File", True, (255, 255, 0))
        screen.blit(title, (300, 50))

        mouse_pos = pygame.mouse.get_pos()
        for label, rect, name in buttons:
            color = (255, 255, 255)  # Default color
            if rect.collidepoint(mouse_pos):  # Hover effect
                color = (0, 255, 0)
            text_surface = FONT.render(label, True, color)
            screen.blit(text_surface, rect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for _, rect, name in buttons:
                    if rect.collidepoint(mouse_pos):  # Select player
                        return load_game(name)  # Load selected save

        pygame.display.flip()
        clock.tick(60)
