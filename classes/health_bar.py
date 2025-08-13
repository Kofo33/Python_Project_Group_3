import pygame
import sys
from classes.constant import WIDTH, HEIGHT, FPS, BLACK, WHITE, RED, GREEN

SCREEN_WIDTH = WIDTH
SCREEN_HEIGHT = HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



class HealthBar():
	def __init__(self, x, y, name, hp, max_hp):
		self.x = x
		self.y = y
		self.name = name
		self.hp = hp
		self.max_hp = max_hp
		self.font = pygame.font.SysFont('Comic Sans MS', 15)
		self.life_bar = pygame.image.load('assets/img/life_bar.png')
		self.life_bar = pygame.transform.scale(self.life_bar, (30, 30))
		

	def draw(self, hp):
		#update with new health
		self.hp = hp
		#calculate health ratio
		ratio = self.hp / self.max_hp
		health_name = self.font.render(f"{self.name} Health", True, WHITE)
		screen.blit(health_name, (self.x, self.y - 30))
		screen.blit(self.life_bar, (self.x-40, self.y-8))
        #draw health bar
		pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
		pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))