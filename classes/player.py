import pygame
import random
from classes.constant import WIDTH, HEIGHT, FPS, BLACK, WHITE, RED, GREEN

# Setup screen dimensions
SCREEN_WIDTH = WIDTH
SCREEN_HEIGHT = HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Player:
    def __init__(self, x, y, name, character_type="Knight", health=100, attack=30, level=1, xp=0):
        """
        Initialize the player character with stats, inventory, skills, and animations.
        """
        self.name = name
        self.character_type = character_type  # Used for loading character-specific assets
        self.health = health
        self.attack = attack
        self.level = level
        self.xp = xp

        # Player starts with fists (no bonus damage)
        self.inventory = [{"name": "Fists", "bonus": 0}]
        self.equipped_weapon = self.inventory[0]

        # Basic skill set (more can be added later)
        self.skills = {
            "Basic Attack": {"damage": 0, "level": 1},
            "Heal": {"heal_amount": 20, "level": 1}
        }

        self.skill = 50  # Accuracy percentage
        self.update_stats()  # Set stats based on level

        # Animation variables
        self.update_time = pygame.time.get_ticks()
        self.action = 0  # 0: Idle, 1: Attack, 2: Hurt, 3: Death
        self.frame_index = 0
        self.animation_list = []

        # Load idle animation frames
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'assets/img/{self.character_type}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 5, img.get_height() * 5))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Load attack animation frames
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'assets/img/{self.character_type}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 5, img.get_height() * 5))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Load hurt animation frames
        temp_list = []
        for i in range(3):
            img = pygame.image.load(f'assets/img/{self.character_type}/Hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 5, img.get_height() * 5))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Load death animation frames
        temp_list = []
        for i in range(10):
            img = pygame.image.load(f'assets/img/{self.character_type}/Death/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 5, img.get_height() * 5))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Set initial image and position
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        """
        Update the animation frames based on cooldown timing.
        """
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]

        # Check if enough time passed to move to the next frame
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # Loop animation or stop at last frame (death animation stays)
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()

    def idle(self):
        """
        Switch player state to idle animation.
        """
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack_enemy(self, enemy):
        """
        Perform an attack on an enemy, dealing damage if it hits.
        """
        if random.randint(1, 100) > self.skill:
            return 0  # Attack missed
        damage = self.attack + self.equipped_weapon["bonus"] + random.randint(-2, 2)
        print(f"{self.name} attacks {enemy.name} for {damage} damage!")
        enemy.health -= max(0, damage)
        enemy.hurt()  # Trigger enemy hurt animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        return damage

    def use_skill(self, skill_name, enemy=None):
        """
        Use a skill (e.g., basic attack or heal).
        """
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
        """
        Return player's maximum health.
        """
        return 100

    def gain_xp(self, amount):
        """
        Gain experience points and handle leveling up.
        """
        self.xp += amount
        xp_needed = 50
        leveled_up = False

        # Level up until XP is below threshold
        while self.xp >= xp_needed:
            self.xp -= xp_needed

            if self.level < 5:  # Max level is 5
                self.level += 1
                
            self.skills["Heal"]["level"] += 1
            self.update_stats()
            self.health = self.max_health()
            leveled_up = True

            # Grant new weapons at specific levels
            if self.level == 2:
                sword = {"name": "Sword", "bonus": 10}
                self.add_item(sword)
                self.equip_weapon("Sword")
                print("You equipped a Sword!")
            elif self.level == 3:
                axe = {"name": "Axe", "bonus": 15}
                self.add_item(axe)
                self.equip_weapon("Axe")
                print("You equipped an Axe!")
            elif self.level == 4:
                bow = {"name": "Bow", "bonus": 20}
                self.add_item(bow)
                self.equip_weapon("Bow")
                print("You equipped a Bow!")
            elif self.level == 5:
                staff = {"name": "Staff", "bonus": 25}
                self.add_item(staff)
                self.equip_weapon("Staff")
                print("You equipped a Staff!")

        return leveled_up

    def update_stats(self):
        """
        Update attack power and accuracy based on level.
        """
        if self.level == 1:
            self.attack = 30
            self.skill = 50
        elif self.level == 2:
            self.attack = 40
            self.skill = 60
        elif self.level == 3:
            self.attack = 45
            self.skill = 65
        elif self.level == 4:
            self.attack = 50
            self.skill = 70
        elif self.level == 5:
            self.attack = 55
            self.skill = 80

    def equip_weapon(self, weapon_name):
        """
        Equip a weapon if it exists in the player's inventory.
        """
        for weapon in self.inventory:
            if weapon["name"] == weapon_name:
                self.equipped_weapon = weapon
                return True
        return False

    def restart(self, level):
        """
        Reset player stats for a restart.
        """
        self.health = self.max_health()
        self.xp = 0
        self.level = level
        self.update_stats()
        self.equipped_weapon = self.inventory[0]
        self.idle()
        print(f"{self.name} has been restarted.")

    def next(self):
        """
        Reset health and XP for moving to the next stage/level.
        """
        self.health = self.max_health()
        self.xp = 0
        self.update_stats()
        self.equipped_weapon = self.inventory[0]
        self.idle()
        print(f"{self.name} has moved to the next level.")

    def hurt(self):
        """
        Trigger hurt animation.
        """
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        """
        Trigger death animation.
        """
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def add_item(self, item):
        """
        Add an item to inventory.
        """
        self.inventory.append(item)

    def draw(self):
        """
        Draw the player on screen.
        """
        screen.blit(self.image, self.rect)
