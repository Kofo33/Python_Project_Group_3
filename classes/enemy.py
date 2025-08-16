import random
import pygame
from classes.constant import WIDTH, HEIGHT

# Screen setup
SCREEN_WIDTH = WIDTH
SCREEN_HEIGHT = HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Enemy:
    def __init__(self, x, y, name="Bandit", health=50, attack=70, level=1):
        self.name = name
        self.max_health = health
        self.health = health
        self.attack = attack
        self.level = level

        # Skill represents hit chance (%) — varies by enemy type
        if name == "Bandit":
            self.skill = 40
        elif name == "Bandit2":
            self.skill = 50
        elif name == "Huntress":
            self.skill = 60
        elif name == "Bringer":  
            self.skill = 60
        elif name == "Wizard":  
            self.skill = 70

        # Animation control variables
        self.action = 0  # 0: Idle, 1: Attack, 2: Hurt, 3: Death
        self.frame_index = 0
        self.animation_list = []  # Stores lists of frames for each action
        self.update_time = pygame.time.get_ticks()

        # -------------------
        # Load enemy animations
        # -------------------

        # Idle animation
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'assets/img/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 5, img.get_height() * 5))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Attack animation
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'assets/img/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 5, img.get_height() * 5))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Hurt animation
        temp_list = []
        for i in range(3):
            img = pygame.image.load(f'assets/img/{self.name}/Hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 5, img.get_height() * 5))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Death animation
        temp_list = []
        for i in range(10):
            img = pygame.image.load(f'assets/img/{self.name}/Death/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 5, img.get_height() * 5))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Set starting image and position
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        """
        Updates the enemy's animation frames based on the current action.
        """
        animation_cooldown = 100  # Time (ms) between frames

        # Update current frame
        self.image = self.animation_list[self.action][self.frame_index]

        # Check if it's time to go to the next frame
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # Loop or stop animation when it ends
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:  # Death animation stops on last frame
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()

    def update_stats(self):
        """
        Scales enemy stats based on its level.
        """
        # Increase health every new level
        base_health = 60
        if self.name == "Bandit":
            self.health = base_health + (self.level - 1) * 10
            self.attack = 70 + (self.level - 1) * 5
            self.skill = 40 + (self.level - 1) * 2
        elif self.name == "Bandit2":
            self.max_health = 60
            self.health = 60 + (self.level - 1) * 10
            self.attack = 80 + (self.level - 1) * 5
            self.skill = 50 + (self.level - 1) * 2
        elif self.name == "Huntress":
            self.max_health = 70
            self.health = 70 + (self.level - 1) * 10
            self.attack = 80 + (self.level - 1) * 5
            self.skill = 60 + (self.level - 1) * 2
        elif self.name == "Bringer":
            self.max_health = 80
            self.health = 80 + (self.level - 1) * 10
            self.attack = 85 + (self.level - 1) * 5
            self.skill = 70 + (self.level - 1) * 2
        elif self.name == "Wizard":
            self.max_health = 100
            self.health = 100 + (self.level - 1) * 15
            self.attack = 90 + (self.level - 1) * 5
            self.skill = 90 + (self.level - 1) * 2
        print(f"{self.name} stats updated:Max-Health={self.max_health} Health={self.health}, Attack={self.attack}, Skill={self.skill}")

    def idle(self):
        """Switch enemy to idle animation."""
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack_player(self, player):
        """
        Attempts to attack the player.

        Returns:
            int: Damage dealt (0 if missed)
        """
        # Hit chance check
        if random.randint(1, 100) > self.skill:
            return 0  # Miss

        # Calculate damage with small variation
        damage = self.attack + random.randint(-2, 2)
        player.health -= max(0, damage)  # Reduce player's health
        player.hurt()  # Trigger player's hurt animation

        # Switch to attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        return damage

    def hurt(self):
        """Switch enemy to hurt animation."""
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        """Switch enemy to death animation."""
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def restart(self, health):
        """Resets enemy stats and animations (used when reusing enemy objects)."""
        self.health = health
        self.idle()

    def draw(self):
        """Draws the enemy on the screen."""
        screen.blit(self.image, self.rect)
