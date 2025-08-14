import pygame

from classes.player import Player
from classes.enemy import Enemy
from classes.constant import WIDTH, HEIGHT, FPS, SHOOT_DELAY
from display import display_menu
# from database import init_db, save_player, load_player


def main():
    pygame.init()

    display_menu()
   

   
    pygame.quit()

if __name__ == "__main__":
    main()

