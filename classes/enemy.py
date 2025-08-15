import random
import pygame
import random
from classes.constant import WIDTH, HEIGHT, FPS, BLACK, WHITE, RED, GREEN

SCREEN_WIDTH = WIDTH
SCREEN_HEIGHT = HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Enemy:
    def __init__(self,x,y, name="Bandit", health=50, attack=70, level=1):
        self.name = name
        self.health = health
        self.attack = attack
        self.level = level
        # Increasing skill (hit chance) for enemies
        if name == "Bandit":
            self.skill = 40
        elif name == "Bandit2":
            self.skill = 50
        elif name == "Bringer":  # e.g., Shadow Knight
            self.skill = 60
        elif name == "Wizard":
            self.skill = 70
        self.action = 0 # 0: Idle, 1: Attack, 2: Hurt, 3: Death
        self.frame_index = 0
        self.animation_list = []
        self.update_time = pygame.time.get_ticks()


        #load idle images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'assets/img/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 5, img.get_height() * 5))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load attack images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'assets/img/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 5, img.get_height() * 5))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load hurt images
        temp_list = []
        for i in range(3):
            img = pygame.image.load(f'assets/img/{self.name}/Hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 5, img.get_height() * 5))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load death images
        temp_list = []
        for i in range(10):
            img = pygame.image.load(f'assets/img/{self.name}/Death/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 5, img.get_height() * 5))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def update(self):
            animation_cooldown = 100
            #handle animation
            #update image
            self.image = self.animation_list[self.action][self.frame_index]
            #check if enough time has passed since the last update
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            #if the animation has run out then reset back to the start
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 3:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.idle()

    def update_stats(self):
        # Update stats based on level
        self.health = 50 + (self.level - 1) * 10
        self.attack = 70 + (self.level - 1) * 5
        if self.name == "Bandit":
            self.skill = 40 + (self.level - 1) * 2
        elif self.name == "Bandit2":
            self.skill = 50 + (self.level - 1) * 2
        elif self.name == "Bringer":
            self.skill = 60 + (self.level - 1) * 2
        elif self.name == "Wizard":
            self.skill = 70 + (self.level - 1) * 2
        elif self.name == "Overlord":
            self.skill = 90 + (self.level - 1) * 2
        
       
	
    def idle(self):
        #set variables to idle animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack_player(self, player):
        if random.randint(1, 100) > self.skill:
            return 0  # Miss
        damage = self.attack + random.randint(-2, 2)
        player.health -= max(0, damage)
        player.hurt()
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        return damage


    def hurt(self):
        #set variables to hurt animation
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        #set variables to death animation
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def restart(self):
        self.health = 50
        self.idle()
    
    def draw(self):
        screen.blit(self.image, self.rect)