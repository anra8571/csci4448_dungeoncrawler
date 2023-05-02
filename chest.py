import pygame
import os
import item

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

class ChestSprite(pygame.sprite.Sprite):
    def __init__(self, image_name):
        super(ChestSprite, self).__init__()
        char_path = os.path.join("graphics", image_name)
        self.surf = pygame.image.load(char_path).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.opened = False
        
    def open(self):
        if not self.opened: # can only loot once
            self.opened = True
            char_path = os.path.join("graphics", "chest_open.png")
            self.surf = pygame.image.load(char_path).convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
            self.rect = self.surf.get_rect()
            acquired_item = item.pool.acquire()
            return acquired_item