
import random

class Enemy:
    def __init__(self, name="Goblin", health=50, attack=5):
        self.name = name
        self.health = health
        self.attack = attack

    def attack_player(self, player):
        damage = self.attack + random.randint(-1, 1)
        player.health -= max(0, damage)
        return damage
