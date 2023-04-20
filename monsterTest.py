
from MonsterFactory import(
    GoblinFactory,
    CheesemanFactory
)


# Citations and Helpful Links
# https://realpython.com/pygame-a-primer/: Setup, adding sprites
# https://stackoverflow.com/questions/28005641/how-to-add-a-background-image-into-pygame: Adding background images
# https://www.pygame.org/docs/ref/cursors.html: Cursors

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

import sys
import os

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        char_path = os.path.join("graphics", "char1.png")
        self.surf = pygame.image.load(char_path).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()

# MONSTER_IMAGES = ["goblin.png"]

# class Monster(pygame.sprite.Sprite):
    

#     def __init__(self, image_name):
#         super(Monster, self).__init__()
#         char_path = os.path.join("graphics", image_name)
#         self.surf = pygame.image.load(char_path).convert()
#         self.surf.set_colorkey((0, 0, 0), RLEACCEL)
#         self.rect = self.surf.get_rect()

# class chadBoss(Monster):
#     health = 40
#     name = "ChadBoss"
#     image = "monster1.png"

#     def __init__(self):
#         char_path = os.path.join("graphics", self.image)
#         self.surf = pygame.image.load(char_path).convert()
#         self.surf.set_colorkey((0, 0, 0), RLEACCEL)
#         self.rect = self.surf.get_rect()




class Inventory(pygame.sprite.Sprite):
    def __init__(self):
        super(Inventory, self).__init__()
        char_path = os.path.join("graphics", "inventory.png")
        self.surf = pygame.image.load(char_path).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()

# Setup
WIDTH = 500
HEIGHT = 500
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
bg_path = os.path.join("graphics", "arena.png")
bg_image = pygame.image.load(bg_path)
smallfont = pygame.font.SysFont('Corbel', 16)
pygame.cursors.Cursor()

# Instanciate starting objects
player = Player()
goblinFactory = GoblinFactory()
cheesemanFactory = CheesemanFactory()
monster = cheesemanFactory.createCheeseman()
# monster = Monster(MONSTER_IMAGES[0])
inventory = Inventory()
show_inventory = False

run = True
while run:
    # Draws the background and inventory buttons
    screen.blit(bg_image, (0, 0))
    pygame.draw.rect(screen, (100, 100, 100), [375, 375, 90, 25])
    text = smallfont.render("Inventory", True, (255, 255, 255))
    screen.blit(text, (387, 380))
    if (show_inventory):
        screen.blit((inventory.surf), ((WIDTH)/8, HEIGHT/8))

    # Gets the mouse position
    mouse = pygame.mouse.get_pos()

    # Event Handler
    # Check if the user closed the window or pressed escape
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == MOUSEBUTTONDOWN:
            print(mouse)
            # Clicked inventory button
            if 375 <= mouse[0] <= 465 and 375 <= mouse[1] <= 400:
                show_inventory = True
            # Clicked inventory exit
            if 420 <= mouse[0] <= 430 and 75 <= mouse[1] <= 95:
                show_inventory = False
    
    screen.blit(player.surf, (WIDTH/4, HEIGHT/2))
    screen.blit((monster.surf), ((3 * WIDTH)/4, HEIGHT/2))

    pygame.display.update()

pygame.quit()