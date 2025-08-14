import sys
import pygame
from classes.constant import WIDTH, HEIGHT, FPS, WHITE, RED, BLACK, YELLOW
from classes.enemy import Enemy
from classes.health_bar import HealthBar
from classes.player import Player
from game_logic import combat, get_username
from save_load import save_game, load_game

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Crystal of Eldoria")
FONT = pygame.font.SysFont("arial", 24)

# Load assets
background_img = pygame.image.load("assets/img/Background/background.png").convert_alpha()
victory_img = pygame.image.load("assets/img/Icons/victory.png").convert_alpha()
defeat_img = pygame.image.load("assets/img/Icons/defeat.png").convert_alpha()
logo_img = pygame.image.load("assets/img/Logo/game_logo.png").convert_alpha()
logo_img = pygame.transform.scale(logo_img, (250, 150))
logo_x = (WIDTH - logo_img.get_width()) // 2
logo_y = 50
mainmenu_img = pygame.image.load("assets/img/Background/home_page_background.jpg").convert_alpha()
mainmenu_img = pygame.transform.scale(mainmenu_img, (WIDTH, HEIGHT))

# Enemy setup
bandit = Enemy(550, 380, "Bandit")
wizard = Enemy(500, 248, "Wizard")
bandit_health_bar = HealthBar(550, 50, "Bandit", bandit.health, 50)
wizard_health_bar = HealthBar(550, 50, "Wizard", wizard.health, 50)

# Button setup
play_button_rect = pygame.Rect(WIDTH // 2 - 76, HEIGHT // 2 - 60, 150, 50)
load_button_rect = pygame.Rect(WIDTH // 2 - 76, HEIGHT // 2 + 5, 150, 50)
quit_button_rect = pygame.Rect(WIDTH // 2 - 76, HEIGHT // 2 + 70, 150, 50)
restart_button_rect = pygame.Rect(WIDTH // 2 - 76, HEIGHT // 2 + 5, 150, 50)
next_level_button_rect = pygame.Rect(WIDTH // 2 - 76, HEIGHT // 2 + 5, 150, 50)
end_game_button_rect = pygame.Rect(WIDTH // 2 - 76, HEIGHT // 2 + 70, 150, 50)

def animate_screen():
    screen.blit(mainmenu_img, (0, 0))

def display_menu():
    running = True
    selected_button = 0
    buttons = [
        ("New Game", play_button_rect, YELLOW),
        ("Load", load_button_rect, YELLOW),
        ("Exit", quit_button_rect, RED)
    ]
    font = pygame.font.SysFont('Comic Sans MS', 25)

    while running:
        animate_screen()
        screen.blit(logo_img, (logo_x, logo_y))
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0][1].collidepoint(mouse_pos):
                    username = get_username()
                    player = Player(250, 370, username, character_type="Knight")
                    display_combat(player)
                elif buttons[1][1].collidepoint(mouse_pos):
                    username = get_username()  # Ask which name to load
                    loaded_player, level = load_game(username)
                    if loaded_player:
                        display_combat(loaded_player)

                elif buttons[2][1].collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

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
                        username = get_username()
                        loaded_player, level = load_game(username)
                        if loaded_player:
                            display_combat(loaded_player)

                    elif selected_button == 2:
                        pygame.quit()
                        sys.exit()

        for i, (label, rect, highlight_color) in enumerate(buttons):
            pygame.draw.rect(screen, BLACK, rect, border_radius=10)
            if rect.collidepoint(mouse_pos) or selected_button == i:
                pygame.draw.rect(screen, highlight_color, rect, border_radius=10, width=4)
            text_surf = font.render(label, True, WHITE)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

        pygame.display.flip()

def display_combat(player):
    knight = player
    knight_health_bar = HealthBar(100, 50, knight.name, knight.health, knight.max_health())
    current_enemy = bandit
    running = True
    clock = pygame.time.Clock()
    end_state = None
    selected_button = 0

    buttons_of_victory = [("Next Level", next_level_button_rect, YELLOW), ("End Game", end_game_button_rect, RED)]
    buttons_of_defeat = [("Restart", restart_button_rect, YELLOW), ("End Game", end_game_button_rect, RED)]
    font = pygame.font.SysFont('Comic Sans MS', 25)

    while running:
        screen.blit(background_img, (0, -50))
        knight.update()
        knight.draw()
        current_enemy.update()
        current_enemy.draw()
        knight_health_bar.draw(knight.health)

        if current_enemy.name == "Bandit":
            bandit_health_bar.draw(current_enemy.health)
        elif current_enemy.name == "Wizard":
            wizard_health_bar.draw(current_enemy.health)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if end_state:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_button = (selected_button - 1) % len(buttons_of_victory)
                    elif event.key == pygame.K_DOWN:
                        selected_button = (selected_button + 1) % len(buttons_of_victory)
                    elif event.key == pygame.K_RETURN:
                        if end_state == "victory":
                            if selected_button == 0:
                                if knight.level == 2:
                                    current_enemy = wizard
                                knight.next()
                                save_game(knight, knight.level)
                                end_state = None
                                selected_button = 0
                            elif selected_button == 1:
                                running = False
                        elif end_state == "defeat":
                            if selected_button == 0:
                                knight.restart()
                                save_game(knight, knight.level)
                                end_state = None
                                selected_button = 0
                            elif selected_button == 1:
                                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_a:
                    result = combat(knight, current_enemy, keys=1)
                    if result in ("victory", "defeat"):
                        end_state = result
                elif event.key == pygame.K_h:
                    result = combat(knight, current_enemy, keys=2)
                    if result in ("victory", "defeat", "fled"):
                        running = False

        if end_state == "victory":
            screen.blit(victory_img, (260, 200))
            for i, (label, rect, highlight_color) in enumerate(buttons_of_victory):
                pygame.draw.rect(screen, BLACK, rect, border_radius=10)
                if selected_button == i:
                    pygame.draw.rect(screen, highlight_color, rect, border_radius=10, width=4)
                text_surf = font.render(label, True, WHITE)
                text_rect = text_surf.get_rect(center=rect.center)
                screen.blit(text_surf, text_rect)
        elif end_state == "defeat":
            screen.blit(defeat_img, (285, 200))
            for i, (label, rect, highlight_color) in enumerate(buttons_of_defeat):
                pygame.draw.rect(screen, BLACK, rect, border_radius=10)
                if selected_button == i:
                    pygame.draw.rect(screen, highlight_color, rect, border_radius=10, width=4)
                text_surf = font.render(label, True, WHITE)
                text_rect = text_surf.get_rect(center=rect.center)
                screen.blit(text_surf, text_rect)

        pygame.display.flip()
        clock.tick(FPS)
