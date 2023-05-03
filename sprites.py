# Fire Art: https://www.pinterest.co.kr/pin/361836151308159504/

import pygame
import os
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

class FireSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(FireSprite, self).__init__()
        char_path = os.path.join("graphics", "campfire.gif")
        self.surf = pygame.image.load(char_path).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()

class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(PlayerSprite, self).__init__()
        char_path = os.path.join("graphics", "char1.png")
        self.surf = pygame.image.load(char_path).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()

class MonsterSprite(pygame.sprite.Sprite):
    def __init__(self, image_name):
        super(MonsterSprite, self).__init__()
        char_path = os.path.join("graphics", image_name)
        self.surf = pygame.image.load(char_path).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()

class ArrowSprite(pygame.sprite.Sprite):
    def __init__(self, direction):
        super(ArrowSprite, self).__init__()
        self.direction = direction
        if direction == "North":
            char_path = os.path.join("graphics", "arrow_up.png")
            #self.surf = pygame.image.load(char_path).convert()
            #self.surf.set_colorkey((0, 0, 0), RLEACCEL)
            #self.rect = self.surf.get_rect()
        elif direction == "East":
            char_path = os.path.join("graphics", "arrow_right.png")
        elif direction == "South":
            char_path = os.path.join("graphics", "arrow_down.png")
        else:
            char_path = os.path.join("graphics", "arrow_left.png")
        self.surf = pygame.image.load(char_path).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()

    def Clicked(self):
        print("clicked the " + self.direction + " arrow")

class XSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(XSprite, self).__init__()
        char_path = os.path.join("graphics", "x.png")
        self.surf = pygame.image.load(char_path).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()

class HealingSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(HealingSprite, self).__init__()
        char_path = os.path.join("graphics", "healing.png")
        self.surf = pygame.image.load(char_path).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()

class AttackSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(AttackSprite, self).__init__()
        char_path = os.path.join("graphics", "attack.png")
        self.surf = pygame.image.load(char_path).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()

class DefenseSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(DefenseSprite, self).__init__()
        char_path = os.path.join("graphics", "defense.png")
        self.surf = pygame.image.load(char_path).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()

class RustySwordSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(RustySwordSprite, self).__init__()
        char_path = os.path.join("graphics", "rustysword.png")
        self.surf = pygame.image.load(char_path).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

class AxeSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(AxeSprite, self).__init__()
        char_path = os.path.join("graphics", "axe.png")
        self.surf = pygame.image.load(char_path).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

class BowSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(BowSprite, self).__init__()
        char_path = os.path.join("graphics", "bow.png")
        self.surf = pygame.image.load(char_path).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()