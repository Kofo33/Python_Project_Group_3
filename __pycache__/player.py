
import random

class Player:
    def __init__(self, name, health=100, attack=10, level=1, xp=0):
        self.name = name
        self.health = health
        self.attack = attack
        self.level = level
        self.xp = xp
        self.inventory = [{"name": "Fists", "bonus": 0}]
        self.equipped_weapon = self.inventory[0]

    def attack_enemy(self, enemy):
        damage = self.attack + self.equipped_weapon["bonus"] + random.randint(-2, 2)
        enemy.health -= max(0, damage)
        return damage

    def gain_xp(self, amount):
        self.xp += amount
        if self.xp >= 100:
            self.level += 1
            self.health += 20
            self.attack += 5
            self.xp = 0
            return True
        return False

    def equip_weapon(self, weapon_name):
        for weapon in self.inventory:
            if weapon["name"] == weapon_name:
                self.equipped_weapon = weapon
                return True
        return False
