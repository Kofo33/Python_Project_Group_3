import sys
import pygame
import random
from classes.constant import WIDTH, HEIGHT, FPS, WHITE, RED, BLACK,YELLOW
from classes.enemy import Enemy
from classes.health_bar import HealthBar
from classes.player import Player
from game_logic import combat


pygame.init()
SCREEN_WIDTH = WIDTH
SCREEN_HEIGHT = HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Crystal of Eldoria")
FONT = pygame.font.SysFont("arial", 24)

# Load assets (replace with your sprite paths)
# player_img = pygame.image.load("assets/img/Knight/Attack/0.png").convert_alpha()
# enemy_img = pygame.image.load("assets/img/Bandit/Idle/0.png").convert_alpha()
background_img = pygame.image.load("assets/img/Background/background.png").convert_alpha()

#load victory and defeat images
victory_img = pygame.image.load('assets/img/Icons/victory.png').convert_alpha()
defeat_img = pygame.image.load('assets/img/Icons/defeat.png').convert_alpha()

logo_img = pygame.image.load("assets/img/Logo/game_logo.png").convert_alpha()
logo_img = pygame.transform.scale(logo_img, (250, 150))
logo_x = (SCREEN_WIDTH - logo_img.get_width()) // 2
logo_y = 50

mainmenu_img = pygame.image.load('assets/img/Background/home_page_background.jpg').convert_alpha()
mainmenu_img = pygame.transform.scale(mainmenu_img, (WIDTH, HEIGHT))

play_button_rect = pygame.Rect(WIDTH // 2 - 76, HEIGHT // 2 - 60, 150, 50)
load_button_rect = pygame.Rect(WIDTH // 2 - 76, HEIGHT // 2 + 5, 150, 50)
quit_button_rect = pygame.Rect(WIDTH // 2 - 76, HEIGHT // 2 + 70, 150, 50)

restart_button_rect = pygame.Rect(WIDTH // 2 - 76, HEIGHT // 2 + 5, 150, 50)
next_level_button_rect = pygame.Rect(WIDTH // 2 - 76, HEIGHT // 2 + 5, 150, 50)
end_game_button_rect = pygame.Rect(WIDTH // 2 - 76, HEIGHT // 2 + 70, 150, 50)


knight = Player(250, 370,"Knight")
bandit = Enemy(550, 380,"Bandit")


knight_health_bar = HealthBar(100,50 ,"Knight", knight.health, 100)
bandit1_health_bar = HealthBar(550,50 ,"Bandit", bandit.health, 50)


def animate_screen():
    screen.blit(mainmenu_img, (0, 0))
   

def display_menu():
    running = True
    selected_button = 0
    buttons = [
        ("Play", play_button_rect, YELLOW),
        ("Load", load_button_rect, YELLOW),
        ("Exit", quit_button_rect, RED)
    ]
    font = pygame.font.SysFont('Comic Sans MS', 25)

    while running:
        animate_screen()  # Background animation
        screen.blit(logo_img, (logo_x, logo_y))  # Logo

        mouse_pos = pygame.mouse.get_pos()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0][1].collidepoint(mouse_pos):
                    display_combat()
                elif buttons[1][1].collidepoint(mouse_pos):
                    print("Load clicked")
                elif buttons[2][1].collidepoint(mouse_pos):
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
                       display_combat()  # Replace with actual combat function
                    elif selected_button == 1:
                        print("Load selected")
                    elif selected_button == 2:
                        pygame.quit()
                        sys.exit()

        # Draw buttons
        for i, (label, rect, highlight_color) in enumerate(buttons):

            # Always fill button background first
            pygame.draw.rect(screen, BLACK, rect, border_radius=10)
            # Hover or keyboard selection effect
            if rect.collidepoint(mouse_pos) or selected_button == i:
                pygame.draw.rect(screen, highlight_color, rect, border_radius=10, width=4)
            else:
                pygame.draw.rect(screen, BLACK, rect, border_radius=10)

            # Draw text
            text_surf = font.render(label, True, WHITE)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

        pygame.display.flip()

    return None


def display_combat():
    running = True
    clock = pygame.time.Clock()
    end_state = None

    selected_button = 0
    buttons_of_victory = [
        ("Next Level", next_level_button_rect, YELLOW),
        ("End Game", end_game_button_rect, RED)
    ]

    buttons_of_defeat = [
        ("Restart", restart_button_rect, YELLOW),
        ("End Game", end_game_button_rect, RED)
    ]

    font = pygame.font.SysFont('Comic Sans MS', 25)

    while running:

        screen.blit(background_img, (0, -50))

        knight.update()
        knight.draw()
        bandit.update()
        bandit.draw()

        knight_health_bar.draw(knight.health)
        bandit1_health_bar.draw(bandit.health)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if end_state:
                # Keyboard navigation
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_button = (selected_button - 1) % len(buttons_of_victory)
                    elif event.key == pygame.K_DOWN:
                        selected_button = (selected_button + 1) % len(buttons_of_victory)
                    elif event.key == pygame.K_RETURN:
                        if selected_button == 0:
                            knight.restart()
                            bandit.restart()
                            end_state = None
                            selected_button = 0  
                        elif selected_button == 1:
                            knight.restart()
                            bandit.restart()
                            running = False
                        
        
            # Handle combat actions
            elif event.type == pygame.KEYDOWN:
                # Press ESC to return to main menu
                if event.key == pygame.K_ESCAPE:
                    running = False
                 # Handle combat actions only on key press
                elif event.key == pygame.K_a:
                    result = combat(knight, bandit, keys = 1)
                    if result in ("victory", "defeat"):
                        end_state = result
                elif event.key == pygame.K_h:
                    result = combat(knight, bandit, keys = 2)
                    if result == "victory" or result == "defeat" or result == "fled":
                        running = False
                elif event.key == pygame.K_ESCAPE:
                    running = False

        if end_state == "victory":
            screen.blit(victory_img, (260, 200))
            # Draw buttons
            for i, (label, rect, highlight_color) in enumerate(buttons_of_victory):

                # Always fill button background first
                pygame.draw.rect(screen, BLACK, rect, border_radius=10)
                # Hover or keyboard selection effect
                if selected_button == i:
                    pygame.draw.rect(screen, highlight_color, rect, border_radius=10, width=4)
                else:
                    pygame.draw.rect(screen, BLACK, rect, border_radius=10)

                # Draw text
                text_surf = font.render(label, True, WHITE)
                text_rect = text_surf.get_rect(center=rect.center)
                screen.blit(text_surf, text_rect)
        elif end_state == "defeat":
            screen.blit(defeat_img, (285, 200))
            # Draw buttons
            for i, (label, rect, highlight_color) in enumerate(buttons_of_defeat):

                # Always fill button background first
                pygame.draw.rect(screen, BLACK, rect, border_radius=10)
                # Hover or keyboard selection effect
                if selected_button == i:
                    pygame.draw.rect(screen, highlight_color, rect, border_radius=10, width=4)
                else:
                    pygame.draw.rect(screen, BLACK, rect, border_radius=10)

                # Draw text
                text_surf = font.render(label, True, WHITE)
                text_rect = text_surf.get_rect(center=rect.center)
                screen.blit(text_surf, text_rect)
                    

        pygame.display.flip()
        clock.tick(FPS)


