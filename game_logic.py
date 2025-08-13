
import random

class Player:
    def __init__(self, name, health=100, attack=30, level=1, xp=0):
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

    def attack_enemy(self, enemy):
        if random.randint(1, 100) > self.skill:
            return 0
        damage = self.attack + self.equipped_weapon["bonus"] + random.randint(-2, 2)
        enemy.health -= max(0, damage)
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

    def add_item(self, item):
        self.inventory.append(item)


class Enemy:
    def __init__(self, name="Goblin", health=50, attack=5):
        self.name = name
        self.health = health
        self.attack = attack
        # Increasing skill (hit chance) for enemies
        if name == "Goblin":
            self.skill = 40
        elif name == "Wolf":
            self.skill = 50
        else:  # e.g., Shadow Knight
            self.skill = 60

    def attack_player(self, player):
        if random.randint(1, 100) > self.skill:
            return 0  # Miss
        damage = self.attack + random.randint(-1, 1)
        player.health -= max(0, damage)
        return damage

def combat(player, enemy):
    while player.health > 0 and enemy.health > 0:
        print(f"\n{player.name}: {player.health}/{player.max_health()} HP | {enemy.name}: {enemy.health} HP")
        print("Actions: 1. Basic Attack  2. Heal  3. Run")
        action = input("Choose an action: ")
        if action == "1":
            result, damage = player.use_skill("Basic Attack", enemy)
            if damage == 0:
                print("You missed!")
            else:
                print(result)
        elif action == "2":
            result, _ = player.use_skill("Heal")
            print(result)
        elif action == "3":
            print("You fled the battle!")
            return False
        else:
            print("Invalid choice.")
            continue

        if enemy.health <= 0:
            print(f"{enemy.name} defeated!")
            leveled_up = player.gain_xp(50)
            if leveled_up:
                print(f"{player.name} leveled up to level {player.level}! Heal skill upgraded.")
            # Obtain sword from specific enemy (e.g., Wolf) at level 3 transition
            if enemy.name == "Wolf":
                new_weapon = {"name": "Sword", "bonus": 0}  # Bonus 0 to keep attack exactly 60; adjust if needed
                player.add_item(new_weapon)
                player.equip_weapon("Sword")
                print("You obtained a sword from the enemy!")
            return True

        damage = enemy.attack_player(player)
        if damage == 0:
            print(f"{enemy.name} missed!")
        else:
            print(f"{enemy.name} deals {damage} damage to you!")

    print("You were defeated...")
    return False
