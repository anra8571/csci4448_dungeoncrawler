# Citations and Helpful Links
# https://realpython.com/pygame-a-primer/: Setup, adding sprites
# https://stackoverflow.com/questions/28005641/how-to-add-a-background-image-into-pygame: Adding background images
# https://www.pygame.org/docs/ref/cursors.html: Cursors

import item
import room
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

class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(PlayerSprite, self).__init__()
        char_path = os.path.join("graphics", "char1.png")
        self.surf = pygame.image.load(char_path).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()

MONSTER_IMAGES = ["monster1.png"]

class MonsterSprite(pygame.sprite.Sprite):
    def __init__(self, image_name):
        super(MonsterSprite, self).__init__()
        char_path = os.path.join("graphics", image_name)
        self.surf = pygame.image.load(char_path).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()

class InventorySprite(pygame.sprite.Sprite):
    def __init__(self):
        super(InventorySprite, self).__init__()
        char_path = os.path.join("graphics", "inventory.png")
        self.surf = pygame.image.load(char_path).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()

class ChestSprite(pygame.sprite.Sprite):
    def __init__(self, image_name):
        super(ChestSprite, self).__init__()
        char_path = os.path.join("graphics", image_name)
        self.surf = pygame.image.load(char_path).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
    def open(self):
        char_path = os.path.join("graphics", "chest_open.png")
        self.surf = pygame.image.load(char_path).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        acquired_item = item.pool.acquire()
        return acquired_item

class ArrowSprite(pygame.sprite.Sprite):
    def __init__(self, direction):
        super(ArrowSprite, self).__init__()
        if direction == "North":
            char_path = os.path.join("graphics", "arrow_up.png")
        elif direction == "East":
            char_path = os.path.join("graphics", "arrow_right.png")
        elif direction == "South":
            char_path = os.path.join("graphics", "arrow_down.png")
        else:
            char_path = os.path.join("graphics", "arrow_left.png")
        self.surf = pygame.image.load(char_path).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()

class Player():
    def __init__(self):
        self.inventory = []

# Setup
WIDTH = 500
HEIGHT = 500
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
bg_path = os.path.join("graphics", "arena.png")
bg_image = pygame.image.load(bg_path)
bg_monster_path = os.path.join("graphics", "bg_monster.png")
bg_monster = pygame.image.load(bg_monster_path)
smallfont = pygame.font.SysFont('Corbel', 16)
show_inventory = False
pygame.cursors.Cursor()

# Instanciate starting objects
player_sprite = PlayerSprite()
player = Player()
monster = MonsterSprite(MONSTER_IMAGES[0])
inventory = InventorySprite()
chest = ChestSprite("closed_chest.png")
chest_opened = False
northArrow = ArrowSprite("North")
eastArrow = ArrowSprite("East")
southArrow = ArrowSprite("South")
westArrow = ArrowSprite("West")

map = {} # empty dictionary that will contain all the rooms - coordinate tuple is the key, room object value
currentRoom = room.Room((0,0), "safe") # create initial room at (0,0) and it is a safe room

run = True
while run:
    # Draws the background and inventory buttons
    if currentRoom.roomType == "safe":
        screen.blit(bg_image, (0, 0)) # safe room background
    else:
        screen.blit(bg_monster, (0,0)) # monster background
    pygame.draw.rect(screen, (100, 100, 100), [375, 450, 90, 25]) # Inventory
    text = smallfont.render("Inventory", True, (255, 255, 255))
    screen.blit(text, (389, 457))
    pygame.draw.rect(screen, (100, 100, 100), [25, 450, 50, 25]) # Run away
    text = smallfont.render("Run", True, (255, 255, 255))
    screen.blit(text, (32, 457))
    pygame.draw.rect(screen, (100, 100, 100), [100, 450, 90, 25]) # Use Item in fight
    text = smallfont.render("Use Item", True, (255, 255, 255))
    screen.blit(text, (117, 457))
    pygame.draw.rect(screen, (100, 100, 100), [200, 450, 90, 25]) # Attack in fight
    text = smallfont.render("Attack", True, (255, 255, 255))
    screen.blit(text, (220, 457))

    # pygame.draw.rect(screen, (100, 100, 100), [100, 450, 300, 25]) # Use Item in fight
    # text = smallfont.render("Use Item", True, (255, 255, 255))
    # screen.blit(text, (135, 457))
    if (show_inventory):
        screen.blit((inventory.surf), ((WIDTH)/8, HEIGHT/8))
        continue
    else:
        screen.blit(player_sprite.surf, (WIDTH/4, HEIGHT/2))
        screen.blit((chest.surf), ((3 * WIDTH)/4, HEIGHT/2))
    screen.blit((northArrow.surf), (WIDTH/2, 20))

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
            # Clicked chest
            if ((3 * WIDTH)/4) <= mouse[0] < ((3 * WIDTH)/4) + 100 and HEIGHT/2 <= mouse[1] <= HEIGHT/2 + 100:
                print("chest opened")
                acquired_item = chest.open()
                player.inventory.append(acquired_item)
                print(f"Inventory: {player.inventory}")
    
    # screen.blit(player.surf, (WIDTH/4, HEIGHT/2))
    # screen.blit((chest.surf), ((3 * WIDTH)/4, HEIGHT/2))

    pygame.display.update()

pygame.quit()