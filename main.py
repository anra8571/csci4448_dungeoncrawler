# Citations and Helpful Links
# https://realpython.com/pygame-a-primer/: Setup, adding sprites
# https://stackoverflow.com/questions/28005641/how-to-add-a-background-image-into-pygame: Adding background images
# https://www.pygame.org/docs/ref/cursors.html: Cursors
# Music for battle rooms: Hitman by Kevin MacLeod | https://incompetech.com/ Music promoted by https://www.chosic.com/free-music/all/ Creative Commons CC BY 3.0 https://creativecommons.org/licenses/by/3.0/
 # Music for normal and chest rooms: My Dark Passenger by Darren Curtis | https://www.darrencurtismusic.com/ Music promoted by https://www.chosic.com/free-music/all/ Creative Commons CC BY 3.0 https://creativecommons.org/licenses/by/3.0/
import item
import room
import chest
import pygame
import MonsterFactory
import sys

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

MONSTER_IMAGES = ["goblin.png"]


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

class Player():
    def __init__(self):
        self.inventory = []
        self.health = 15
        self.damage = 15
        self.defense = 9

def PrintMap(map, currentRoom, screen):
    pygame.draw.rect(screen, (0,0,0), [300, 40, 135, 135]) # mini-map backdrop
    for i in range(5):
        for j in range(5):
            x = i - 2 # the room coordinates are centered on (0,0), top left is (-2,-2)
            y = j - 2
            if (x,y) in map: # if we have been to the room before and know its type
                room = map[(x,y)]
                if room.roomType == "safe" and room.chest.opened == False:
                    color = (0, 50, 255) # blue-ish
                elif room.roomType == "safe":
                    color = (50, 50, 50) # brown-ish
                else:
                    color = (255, 50, 0) # red-ish
            else:
                color = (100,100,100) # grey-ish

            pygame.draw.rect(screen, color, [300 + i*27, 40 + j*27, 25, 25]) # Inventory
    text = smallfont.render("P", True, (255, 255, 255))
    screen.blit(text, (362 + (currentRoom.x)*27, 99 + (currentRoom.y)*27))

# Setup
WIDTH = 500
HEIGHT = 500
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
bg_looted_path = os.path.join("graphics", "arena.png")
bg_looted = pygame.image.load(bg_looted_path)
bg_monster_path = os.path.join("graphics", "bg_monster.png")
bg_monster = pygame.image.load(bg_monster_path)
bg_safe_path = os.path.join("graphics", "bg_safe.png")
bg_safe = pygame.image.load(bg_safe_path)
smallfont = pygame.font.SysFont('Corbel', 16)
show_inventory = False
monst_factory = MonsterFactory.MonsterFactory()
monster = monst_factory.createMonster()
pygame.mixer.music.load("My-Dark-Passenger.mp3")
pygame.mixer.music.play()

# pygame.cursors.Cursor()

# Instanciate starting objects
player_sprite = PlayerSprite()
player = Player()
monster = MonsterSprite(MONSTER_IMAGES[0])
inventory = InventorySprite()

northArrow = ArrowSprite("North")
eastArrow = ArrowSprite("East")
southArrow = ArrowSprite("South")
westArrow = ArrowSprite("West")

map = {} # empty dictionary that will contain all the rooms - coordinate tuple is the key, room object value
currentRoom = room.Room((0,0), "safe") # create initial room at (0,0) and it is a safe room
map[(0,0)] = currentRoom

numDefeated = 0 # number of enemies defeated

run = True
while run:
    # Draws the background and inventory buttons
    if currentRoom.roomType == "safe" and currentRoom.chest.opened == False:
        screen.blit(bg_safe, (0, 0)) # safe room background
        screen.blit((currentRoom.chest.surf), ((3 * WIDTH)/4, HEIGHT/2))
    elif currentRoom.roomType == "safe":
        screen.blit(bg_looted, (0, 0)) # safe room background
        screen.blit((currentRoom.chest.surf), ((3 * WIDTH)/4, HEIGHT/2))
    else:
        screen.blit(bg_monster, (0,0)) # monster background
        screen.blit((monster.surf), ((3 * WIDTH)/4, HEIGHT/2))

    PrintMap(map, currentRoom, screen)

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

    validMoves = [] # get valid moves so we put arrows in the right spots

    if currentRoom.y > -2:
        screen.blit((northArrow.surf), (225, 20)) 
        validMoves.append("North")
    if currentRoom.x < 2:
        screen.blit((eastArrow.surf), (WIDTH - 75, HEIGHT/2 -50))
        validMoves.append("East")
    if currentRoom.y < 2:
        screen.blit((southArrow.surf), (225, HEIGHT-100))
        validMoves.append("South")
    if currentRoom.x > -2:
        screen.blit((westArrow.surf), (30, HEIGHT/2-50))
        validMoves.append("West")

    if (show_inventory):
        screen.blit(inventory.surf, (WIDTH/8, HEIGHT/8))
    else:
        screen.blit(player_sprite.surf, (WIDTH/4, HEIGHT/2))

    # Gets the mouse position
    mouse = pygame.mouse.get_pos()

    # Event Handler
    # Check if the user closed the window or pressed escape
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == MOUSEBUTTONDOWN:
            print(mouse)
            if not show_inventory:
                # clicking on arrow
                if 235 <= mouse[0] < 270 and 25 <= mouse[1] <= 70 and "North" in validMoves: # northArrow.rect.collidepoint(mouse)
                    ArrowSprite.Clicked(northArrow)
                    currentRoom = room.Room.SpawnRoom(map, currentRoom, (currentRoom.x, currentRoom.y), numDefeated, "north")
                    print("current room coordinates are (" + str(currentRoom.x) + "," + str(currentRoom.y) + ")")
                elif 430 <= mouse[0] < 475 and 205 <= mouse[1] <= 240 and "East" in validMoves:
                    ArrowSprite.Clicked(eastArrow)
                    currentRoom = room.Room.SpawnRoom(map, currentRoom, (currentRoom.x, currentRoom.y), numDefeated, "east")
                    print("current room coordinates are (" + str(currentRoom.x) + "," + str(currentRoom.y) + ")")
                elif 235 <= mouse[0] < 270 and 400 <= mouse[1] <= 445 and "South" in validMoves:
                    ArrowSprite.Clicked(southArrow)
                    currentRoom = room.Room.SpawnRoom(map, currentRoom, (currentRoom.x, currentRoom.y), numDefeated, "south")
                    print("current room coordinates are (" + str(currentRoom.x) + "," + str(currentRoom.y) + ")")
                elif 30 <= mouse[0] < 75 and 205 <= mouse[1] <= 240 and "West" in validMoves:
                    ArrowSprite.Clicked(westArrow)
                    currentRoom = room.Room.SpawnRoom(map, currentRoom, (currentRoom.x, currentRoom.y), numDefeated, "west")
                    print("current room coordinates are (" + str(currentRoom.x) + "," + str(currentRoom.y) + ")")
                
                # clicking on chest
                if currentRoom.chest != None:
                    # Clicked chest
                    if ((3 * WIDTH)/4) <= mouse[0] < ((3 * WIDTH)/4) + 100 and HEIGHT/2 <= mouse[1] <= HEIGHT/2 + 100:
                        print("clicked chest")
                        acquired_item = currentRoom.chest.open()
                        if acquired_item != None:
                            player.inventory.append(acquired_item)
                        print(f"Inventory: {player.inventory}")
            
            # Clicked inventory button
            if 375 <= mouse[0] <= 465 and 450 <= mouse[1] <= 475:
                print("clicked inventory")
                show_inventory = True

            # Clicked inventory exit
            if 420 <= mouse[0] <= 430 and 75 <= mouse[1] <= 95:
                show_inventory = False

            # Clicked Attack button
            if 200 <= mouse[0] <= 290 and 450 <= mouse[1] <= 475:
                print(f"Attack: player health {player.health} and monster health {currentRoom.monster.health}")
                currentRoom.monster.takeDamage(player.damage)
                action = currentRoom.monster.pickAction()
                print(f"Monster Action: {action}")
                # TODO: player should not gain health if the defense is high
                if action[0] == "attack":
                    player.health -= action[1] - player.defense
                print(f"End Attack: player health {player.health} and monster health {currentRoom.monster.health}")
                if (currentRoom.monster.checkAlive()):
                    print("The monster has died")

    pygame.display.update()

pygame.quit()