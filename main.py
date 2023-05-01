# Citations and Helpful Links
# https://realpython.com/pygame-a-primer/: Setup, adding sprites
# https://stackoverflow.com/questions/28005641/how-to-add-a-background-image-into-pygame: Adding background images
# https://www.pygame.org/docs/ref/cursors.html: Cursors
# Music for battle rooms: Hitman by Kevin MacLeod | https://incompetech.com/ Music promoted by https://www.chosic.com/free-music/all/ Creative Commons CC BY 3.0 https://creativecommons.org/licenses/by/3.0/
 # Music for normal and chest rooms: My Dark Passenger by Darren Curtis | https://www.darrencurtismusic.com/ Music promoted by https://www.chosic.com/free-music/all/ Creative Commons CC BY 3.0 https://creativecommons.org/licenses/by/3.0/
import item
import room
import chest
import sprites
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

MONSTER_IMAGES = ["goblin.png"]
INVENTORY_WIDTH = 5
INVENTORY_HEIGHT = 2

def get_item_type(curr_item):
    if isinstance(curr_item, item.Healing):
        return "healing"
    elif isinstance(curr_item, item.DefenseBuff):
        return "defense"
    elif isinstance(curr_item, item.AttackBuff):
        return "attack"
    elif isinstance(curr_item, item.Axe):
        return "axe"
    elif isinstance(curr_item, item.RustySword):
        return "sword"
    elif isinstance(curr_item, item.Bow):
        return "bow"
    else:
        return "none"
    
def return_sprite(curr_item):
    if get_item_type(curr_item) == "healing":
        return sprites.HealingSprite()
    elif get_item_type(curr_item) == "defense":
        return sprites.DefenseSprite()
    elif get_item_type(curr_item) == "attack":
        return sprites.AttackSprite()
    elif get_item_type(curr_item) == "axe":
        return sprites.AxeSprite()
    elif get_item_type(curr_item) == "sword":
        return sprites.RustySwordSprite()
    elif get_item_type(curr_item) == "bow":
        return sprites.BowSprite()
    else:
        return "none"
    
class Player():
    def __init__(self):
        self.inventory = []
        self.sprites_list = []
        for i in range(INVENTORY_HEIGHT):
            self.inventory.append([])
            self.sprites_list.append([])
        for i in range(INVENTORY_HEIGHT):
            for j in range(INVENTORY_WIDTH):
                self.inventory[i].append(None)
                self.sprites_list[i].append(None)
        self.health = 15
        self.damage = 15
        self.defense = 9

    def add_inventory(self, item):
        # Maximum of 10 items in inventory - otherwise, the first one is automatically overwritten
        for i in range(INVENTORY_HEIGHT):
            for j in range(INVENTORY_WIDTH):
                if self.inventory[i][j] is None:
                    self.inventory[i][j] = item
                    self.sprites_list[i][j] = return_sprite(item)
                    return
        self.inventory[0][0] = item
        self.sprites_list[0][0] = return_sprite(item)

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

def printInventory(screen, sprite, player):
    pygame.draw.rect(screen, (100,100,100), [0, 0, 500, 500]) # background
    screen.blit(sprites.XSprite().surf, (WIDTH/10 * 9, HEIGHT/40))

    # Draws the inventory rectangles
    for i in range(5):
        for j in range(2):
            color = (200, 200, 200)
            pygame.draw.rect(screen, color, [50 + i*60, 50 + j*60, 50, 50])
            if player.inventory[j][i] is not None:
                screen.blit(player.sprites_list[j][i].surf, [50 + i*60, 50 + j*60, 50, 50])
    screen.blit(player_sprite.surf, (WIDTH/10 * 8, HEIGHT/4))
    text = smallfont.render(f"Health: {player.health}   Damage: {player.damage}   Defense: {player.defense}", True, (255, 255, 255))
    screen.blit(text, (WIDTH/4, 200))

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
bigfont = pygame.font.SysFont('Corbel', 34)
show_inventory = False

# pygame.cursors.Cursor()

# Instanciate starting objects
player_sprite = sprites.PlayerSprite()
player = Player()
test_item = item.pool.acquire()
test_item2 = item.pool.acquire()
player.add_inventory(test_item)
player.add_inventory(test_item2)
print(player.inventory)
print(player.sprites_list)
monster = sprites.MonsterSprite(MONSTER_IMAGES[0])
inventory = sprites.InventorySprite()

northArrow = sprites.ArrowSprite("North")
eastArrow = sprites.ArrowSprite("East")
southArrow = sprites.ArrowSprite("South")
westArrow = sprites.ArrowSprite("West")

map = {} # empty dictionary that will contain all the rooms - coordinate tuple is the key, room object value
currentRoom = room.Room((0,0), "safe") # create initial room at (0,0) and it is a safe room
map[(0,0)] = currentRoom

numDefeated = 0 # number of enemies defeated

run = True
while run:
    if curr_music != currentRoom.roomType:
        if curr_music == 'safe':
            pygame.mixer.music.load("Hitman.mp3")
            pygame.mixer.music.play()
            curr_music = 'monster'
        else:
            pygame.mixer.music.load("My-Dark-Passenger.mp3")
            pygame.mixer.music.play()
            curr_music = 'safe'
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

    screen.blit(player_sprite.surf, (WIDTH/4, HEIGHT/2))

    if (show_inventory):
        printInventory(screen, player_sprite, player)

    # Gets the mouse position
    mouse = pygame.mouse.get_pos()

    # Event Handler
    # Check if the user closed the window or pressed escape
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == MOUSEBUTTONDOWN:
            print(mouse)
            # If not in the inventory (so in the main game)
            if not show_inventory:
                # clicking on arrow
                if 235 <= mouse[0] < 270 and 25 <= mouse[1] <= 70 and "North" in validMoves: # northArrow.rect.collidepoint(mouse)
                    sprites.ArrowSprite.Clicked(northArrow)
                    currentRoom = room.Room.SpawnRoom(map, currentRoom, (currentRoom.x, currentRoom.y), numDefeated, "north")
                    print("current room coordinates are (" + str(currentRoom.x) + "," + str(currentRoom.y) + ")")
                elif 430 <= mouse[0] < 475 and 205 <= mouse[1] <= 240 and "East" in validMoves:
                    sprites.ArrowSprite.Clicked(eastArrow)
                    currentRoom = room.Room.SpawnRoom(map, currentRoom, (currentRoom.x, currentRoom.y), numDefeated, "east")
                    print("current room coordinates are (" + str(currentRoom.x) + "," + str(currentRoom.y) + ")")
                elif 235 <= mouse[0] < 270 and 400 <= mouse[1] <= 445 and "South" in validMoves:
                    sprites.ArrowSprite.Clicked(southArrow)
                    currentRoom = room.Room.SpawnRoom(map, currentRoom, (currentRoom.x, currentRoom.y), numDefeated, "south")
                    print("current room coordinates are (" + str(currentRoom.x) + "," + str(currentRoom.y) + ")")
                elif 30 <= mouse[0] < 75 and 205 <= mouse[1] <= 240 and "West" in validMoves:
                    sprites.ArrowSprite.Clicked(westArrow)
                    currentRoom = room.Room.SpawnRoom(map, currentRoom, (currentRoom.x, currentRoom.y), numDefeated, "west")
                    print("current room coordinates are (" + str(currentRoom.x) + "," + str(currentRoom.y) + ")")
                
                # clicking on chest
                if currentRoom.chest != None:
                    # Clicked chest
                    if ((3 * WIDTH)/4) <= mouse[0] < ((3 * WIDTH)/4) + 100 and HEIGHT/2 <= mouse[1] <= HEIGHT/2 + 100:
                        print("clicked chest")
                        acquired_item = currentRoom.chest.open()
                        if acquired_item != None:
                            player.add_inventory(acquired_item)
                        print(f"Inventory: {player.inventory}")
                # Clicked inventory button
                if 375 <= mouse[0] <= 465 and 450 <= mouse[1] <= 475:
                    print("clicked inventory")
                    show_inventory = True
            # If currently in the inventory
            else:
                # Clicked the X button to exit inventory
                if 456 <= mouse[0] <= 490 and 16 <= mouse[1] <= 53:
                    show_inventory = False

    pygame.display.update()

pygame.quit()
