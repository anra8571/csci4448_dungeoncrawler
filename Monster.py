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
        # super(Monster, self).__init__()
        # char_path = os.path.join("graphics", image_name)
        # self.surf = pygame.image.load(char_path).convert()
        # self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # self.rect = self.surf.get_rect()

        if type=="Offensive":
            self.strat = Offensive()
        elif type == "Defensive":
            self.strat = Defensive()
        elif type == "Balanced":
            self.strat = Balanced()
        else:
            print("Please give a correct type")
        print(self.image_name)
            
    #When it is the monster's turn, call this function and it will decide what it does
    def pickAction(self):
        #The strategy will return a option
        choice = self.strat.getAttack()
        #if it is attacking
        if choice == "attack":
            damage = self.attack()
            return ["attack", damage]
        elif choice == 'defend':
            return ["defend", self.health]

    #Will return the damage done by the monster
    def attack(self):
        if self.crit():
            return self.damage * 1.5
        else:
            return self.damage

    #If the monster chose to defend itself, it will heal
    def defend(self):
        self.health + self.healing

    #Gets the chance of a critical hit and returns whether or not it was
    def crit(self):
        choice = self.strat.getCrit()
        if choice:
            return True
        else:
            return False
        
    #Debugging purposes
    def printStats(self):
        print(self.health, self.damage, self.defense)

    #Checks to see if the monster is alove
    def checkAlive(self):
        if self.health <= 0:
            return True
        else:
            return False
    
    #For debugging purposes
    def getAttack(self):
        return self.damage
    
    #Call this function when the player does damage. It will take the damage given
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

#Cheeseman my beloved
class Cheeseman(Monster):
    def __init__(self):
        self.image_name =  "funnyRockGuy.png"
        Monster.__init__(self, "funnyRockGuy.png", "Defensive")
        self.health = 20
        self.damage = 2
        self.defense = 2
        self.healing = 1

#Cool chad boss guy
class Boss(Monster):
    def __init__(self):
        self.image_name =  "MediumFinalBoss.png"
        Monster.__init__(self, "MediumFinalBoss.png", "Balanced")
        self.health = 40
        self.damage = 6
        self.defense = 5
        self.healing = 3