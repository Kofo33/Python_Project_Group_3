import pygame
from classes.constant import WIDTH, HEIGHT, FPS, SHOOT_DELAY
from display import display_menu


def main():
    pygame.init()
    display_menu()
    pygame.quit()

if __name__ == "__main__":
    main()

