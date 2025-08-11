import sys
import pygame
import random
from classes.constant import WIDTH, HEIGHT, FPS, WHITE, RED, BLACK,YELLOW
# from game_logic import Player, Enemy, combat

pygame.init()
SCREEN_WIDTH = WIDTH
SCREEN_HEIGHT = HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Crystal of Eldoria")
FONT = pygame.font.SysFont("arial", 24)

# Load assets (replace with your sprite paths)
player_img = pygame.image.load("assets/img/Knight/Attack/0.png")
enemy_img = pygame.image.load("assets/img/Bandit/Idle/0.png")
background_img = pygame.image.load("assets/img/Background/background.png").convert_alpha()

logo_img = pygame.image.load("assets/img/Logo/game_logo.png")
logo_img = pygame.transform.scale(logo_img, (250, 150))
logo_x = (SCREEN_WIDTH - logo_img.get_width()) // 2
logo_y = 50

mainmenu_img = pygame.image.load('assets/img/Background/home_page_background.jpg').convert()
mainmenu_img = pygame.transform.scale(mainmenu_img, (WIDTH, HEIGHT))

play_button_rect = pygame.Rect(WIDTH // 2 - 76, HEIGHT // 2 - 60, 150, 50)
load_button_rect = pygame.Rect(WIDTH // 2 - 76, HEIGHT // 2 + 5, 150, 50)
quit_button_rect = pygame.Rect(WIDTH // 2 - 76, HEIGHT // 2 + 70, 150, 50)



def animate_screen():
    screen.blit(mainmenu_img, (0, 0))
    # for i in range(0, 20):
    #     screen.blit(mainmenu_img, (0, 0))
    #     pygame.display.flip()
    #     pygame.time.wait(10)
    #     screen.blit(mainmenu_img, (random.randint(-5, 5), random.randint(-5, 5)))
    #     pygame.display.flip()
    #     pygame.time.wait(10)



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
                    display_combat_bg()
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
                       display_combat_bg()  # Replace with actual combat function
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


def display_combat_bg():
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Press ESC to return to main menu
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Draw combat background
        screen.blit(background_img, (0, -50))

        pygame.display.flip()
        clock.tick(FPS)


def main():
    # player = Player(input("Enter your name: "))
    # enemy = Enemy()
    # display_combat(player, enemy)
    display_menu()
    pygame.quit()

if __name__ == "__main__":
    main()