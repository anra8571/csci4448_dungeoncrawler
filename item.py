# https://sourcemaking.com/design_patterns/object_pool/python/1
import random
import os
import pygame
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

POOL_SIZE = 10

class Item():
    def __init__(self, in_attribute, in_effect = 3):
        super(Item, self).__init__()
        self.attribute = in_attribute
        self.effect = in_effect

class Spell(Item):
    def __init__(self):
        super().__init__("heal", random.randint(1, 10))
        self.effect = random.randint(1, 5)

    def cast(self, stat):
        return stat + self.effect

class Healing(Spell):
    def __init__(self):
        super().__init__()
        self.effect = random.randint(2, 4)
        self.type = "Healing"

class AttackBuff(Spell):
    def __init__(self):
        super().__init__()
        self.effect = random.randint(1, 5)
        self.type = "Attack Buff"

class DefenseBuff(Spell):
    def __init__(self):
        super().__init__()
        self.effect = random.randint(2, 3)
        self.type = "Defense Buff"

class Weapon(Item):
    def __init__(self):
        super().__init__("weapon", random.randint(2, 5))

    def attack():
        print("Attack")

class RustySword(Weapon):
    def __init__(self):
        super().__init__()
        self.damage = random.randint(1, 2)
        self.type = "Rusty Sword"

class Axe(Weapon):
    def __init__(self):
        super().__init__()
        self.damage = random.randint(2, 4)
        self.type = "Axe"

class Bow(Weapon):
    def __init__(self):
        super().__init__()
        self.damage = random.randint(1, 3)
        self.type = "Bow"

class Pool:
    def __init__(self, size=10):
        self.objs = []

        rand_int = 0
        for i in range(size):
            rand_int = random.randint(0, 5)
            if (rand_int == 0):
                self.objs.append(Healing())
            elif (rand_int == 1):
                self.objs.append(AttackBuff())
            elif (rand_int == 2):
                self.objs.append(DefenseBuff())
            elif (rand_int == 3):
                self.objs.append(RustySword())
            elif (rand_int == 4):
                self.objs.append(Axe())
            else:
                self.objs.append(Bow())
    
    def return_items(self):
        return self.objs
    
    def acquire(self):
        return self.objs.pop()
    
    def release(self, item):
        return self.objs.append(item)
    
    def print_pool(self):
        obj_array = pool.return_items()
        for i in range(POOL_SIZE):
            print(f"{i}: {obj_array[i]}, attribute {obj_array[i].attribute}, effect {obj_array[i].effect}")
    
pool = Pool(POOL_SIZE)