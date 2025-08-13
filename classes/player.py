import pygame
import random
from classes.constant import WIDTH, HEIGHT, FPS, BLACK, WHITE, RED, GREEN

SCREEN_WIDTH = WIDTH
SCREEN_HEIGHT = HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Player:
    def __init__(self,x,y, name, health=100, attack=30, level=1, xp=0):
        self.name = name
        self.health = health
        self.attack = attack
        self.level = level
        self.xp = xp
        self.inventory = [{"name": "Fists", "bonus": 0}]
        self.equipped_weapon = self.inventory[0]
        self.skills = {
            "Basic Attack": {"damage": 0, "level": 1},
            "Heal": {"heal_amount": 20, "level": 1}
        }
        self.skill = 50
        self.update_stats()
        self.update_time = pygame.time.get_ticks()
        self.action = 0  # 0: Idle, 1: Attack, 2: Hurt, 3: Death
        self.frame_index = 0
        self.animation_list = []
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
            img = pygame.transform.scale(img, (img.get_width() * 5
            , img.get_height() * 5
            ))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load death images
        temp_list = []
        for i in range(10):
            img = pygame.image.load(f'assets/img/{self.name}/Death/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 5
            , img.get_height() * 5
            ))
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


	
    def idle(self):
        #set variables to idle animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def attack_enemy(self, enemy):
        if random.randint(1, 100) > self.skill:
            return 0
        damage = self.attack + self.equipped_weapon["bonus"] + random.randint(-2, 2)
        print(f"{self.name} attacks {enemy.name} for {damage} damage!")
        enemy.health -= max(0, damage)
        enemy.hurt()
        # if enemy.health <= 0:
        #     enemy.death()
        #     print(f"{enemy.name} has been defeated!")
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        return damage

    def use_skill(self, skill_name, enemy=None):
        if skill_name not in self.skills:
            return "Invalid skill", 0
        skill = self.skills[skill_name]
        if skill_name == "Basic Attack":
            damage = self.attack_enemy(enemy)
            return f"Attacked for {damage} damage", damage
        elif skill_name == "Heal":
            heal = skill["heal_amount"] + (skill["level"] - 1) * 5
            self.health = min(self.health + heal, self.max_health())
            return f"Healed for {heal} HP", heal
        return "Skill used", 0

    def max_health(self):
        return 100

    def gain_xp(self, amount):
        self.xp += amount
        xp_needed = 50
        leveled_up = False
        while self.xp >= xp_needed:
            self.xp -= xp_needed
            self.level += 1
            self.skills["Heal"]["level"] += 1
            self.update_stats()
            self.health = self.max_health()
            leveled_up = True

            # Equip weapon based on level
            if self.level == 2:
                sword = {"name": "Sword", "bonus": 15}
                self.add_item(sword)
                self.equip_weapon("Sword")
                print("You equipped a Sword!")
            elif self.level == 3:
                axe = {"name": "Axe", "bonus": 30}
                self.add_item(axe)
                self.equip_weapon("Axe")
                print("You equipped an Axe!")

        return leveled_up

    def update_stats(self):
        if self.level == 1:
            self.attack = 30
            self.skill = 50
        elif self.level == 2:
            self.attack = 45
            self.skill = 60
        elif self.level == 3:
            self.attack = 60
            self.skill = 70

    def equip_weapon(self, weapon_name):
        for weapon in self.inventory:
            if weapon["name"] == weapon_name:
                self.equipped_weapon = weapon
                return True
        return False
    
    def restart(self):
        self.health = self.max_health()
        self.xp = 0
        self.level = 1
        self.update_stats()
        self.equipped_weapon = self.inventory[0]
        self.idle()
        print(f"{self.name} has been restarted.")


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

    def add_item(self, item):
        self.inventory.append(item)

    def draw(self):
        screen.blit(self.image, self.rect)