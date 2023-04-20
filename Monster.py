import sys
import os
import random
import pygame

from attackStrat import (
    Balanced,
    Defensive,
    Offensive,
)

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    MOUSEBUTTONDOWN,
)

class Monster():
    health = 0
    damage = 0
    defense = 0
    healing = 0

    def __init__(self, image_name, type):
        super(Monster, self).__init__()
        char_path = os.path.join("graphics", image_name)
        self.surf = pygame.image.load(char_path).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()

        if type=="Offensive":
            self.strat = Offensive()
        elif type == "Defensive":
            self.strat = Defensive()
        elif type == "Balanced":
            self.strat = Balanced()
        else:
            print("Please give a correct type")
        print(self.image_name)
            

    def pickAction(self):
        choice = self.strat.getAttack()
        if choice == "attack":
            damage = self.attack()
            return ["attack", damage]
        elif choice == 'defend':
            self.health = self.defend()
            return ["defend", self.health]


    def attack(self):
        if self.crit():
            return self.damage * 1.5
        else:
            return self.damage

    def defend(self):
        return self.health + self.healing


    def crit(self):
        choice = self.strat.getCrit()
        if choice:
            return True
        else:
            return False
        
    def printStats(self):
        print(self.health, self.damage, self.defense)

    def checkAlive(self):
        if self.health <= 0:
            return True
        else:
            return False
    
    def getAttack(self):
        return self.damage
    
    def takeDamage(self, damage):
        if damage > self.defense:
            self.health = self.health - damage + self.defense

class Goblin(Monster):
    def __init__(self):
        self.image_name = "goblin.png"
        Monster.__init__(self, "goblin.png", "Offensive")
        self.health = 10
        self.damage = 5
        self.defense = 2
        self.healing = 1

class Cheeseman(Monster):
    def __init__(self):
        self.image_name =  "funnyRockGuy.png"
        Monster.__init__(self, "funnyRockGuy.png", "Defensive")
        self.health = 20
        self.damage = 2
        self.defense = 2
        self.healing = 1
