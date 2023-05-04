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
import eventManager
import pygame
import MonsterFactory
import random
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

MONSTER_IMAGES = ["goblin.png", "funnyRockGuy.png"]
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
        self.equipped_item = item.RustySword() # start off with this, and have as current equipped. Damage based on this
        self.equipped_sprite = sprites.RustySwordSprite()
        self.sprites_list = []
        for i in range(INVENTORY_HEIGHT):
            self.inventory.append([])
            self.sprites_list.append([])
        for i in range(INVENTORY_HEIGHT):
            for j in range(INVENTORY_WIDTH):
                self.inventory[i].append(None)
                self.sprites_list[i].append(None)
        self.max_health = 20
        self.health = 20
        self.base_damage = 6
        self.buff_damage = 0
        self.weapon_damage = self.equipped_item.damage
        self.base_defense = 3
        self.buff_defense = 0

    def CalcDamage(self):
        return self.base_damage + self.buff_damage + self.weapon_damage
    
    def CalcDefense(self):
        return self.base_defense + self.buff_defense

    def checkPlayerAlive(self):
        if self.health <= 0:
            return False
        return True
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
    screen.blit(player_sprite.surf, (WIDTH/10 * 8 - 8, HEIGHT/4 + 5))
    text = smallfont.render(f"Health: {player.health}   Damage: {player.CalcDamage()}   Defense: {player.CalcDefense()}", True, (255, 255, 255))
    screen.blit(text, (WIDTH/4, 200))

    # currently equipped item sprite and text 
    text = smallfont.render("Equipped", True, (255,255,255))
    screen.blit(text, (375, 30))
    screen.blit(player.equipped_sprite.surf, (380, 50))
    text = smallfont.render("Damage: " + str(player.equipped_item.damage), True, (255,255,255))
    screen.blit(text, (370, 105))

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
bg_boss_path = os.path.join("graphics", "bossBackground.png")
bg_boss = pygame.image.load(bg_boss_path)
bg_tempW_path = os.path.join("graphics", "tempWinBackground.png")
bg_tempW = pygame.image.load(bg_tempW_path)
bg_tempStart_path = os.path.join("graphics", "tempStart.png")
bg_tempStart = pygame.image.load(bg_tempStart_path)
bg_death_path = os.path.join("graphics", "tempDeath.png")
bg_death = pygame.image.load(bg_death_path)
smallfont = pygame.font.SysFont('Corbel', 16)
bigfont = pygame.font.SysFont('Corbel', 34)
show_inventory = False
pygame.mixer.music.load("My-Dark-Passenger.mp3")
pygame.mixer.music.play()
curr_music = 'safe'
gameOver = False
gameStart = True
instructions = False
playerDead = False

# inventory variables of if they have an item selected
selected_item = None
show_prompt = False
inventory_coords = [0,0]

# Instanciate starting objects
player_sprite = sprites.PlayerSprite()
player = Player()
test_item = item.pool.acquire()
test_item2 = item.pool.acquire()
player.add_inventory(test_item)
player.add_inventory(test_item2)
print(player.inventory)
print(player.sprites_list)
inventory = sprites.InventorySprite()

# Observer Pattern
events = eventManager.ConcreteEventManager()
logger = eventManager.Logger()
events.registerObserver(logger)

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
    if gameStart and not instructions:
        screen.blit(bg_tempStart, (0, 0))
        pygame.draw.rect(screen, (100, 100, 100), [210, 450, 90, 25]) # Inventory
        text = smallfont.render("Start Game", True, (255, 255, 255))
        screen.blit(text, (224, 457))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 210 <= mouse[0] <= 290 and 450 <= mouse[1] <= 475:
                        print("clicked inventory")
                        gameStart = False
    elif gameOver:
        if playerDead:
            screen.blit(bg_death, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == MOUSEBUTTONDOWN:
                    print(mouse)
        else:
            screen.blit(bg_tempW, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == MOUSEBUTTONDOWN:
                    print(mouse)
    else:

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
            pygame.draw.rect(screen, (100, 100, 100), [210, 450, 90, 25]) # Inventory
            text = smallfont.render("Inventory", True, (255, 255, 255))
            screen.blit(text, (224, 457))
        elif currentRoom.roomType == "safe":
            screen.blit(bg_looted, (0, 0)) # safe room background
            screen.blit((currentRoom.chest.surf), ((3 * WIDTH)/4, HEIGHT/2))
            pygame.draw.rect(screen, (100, 100, 100), [210, 450, 90, 25]) # Inventory
            text = smallfont.render("Inventory", True, (255, 255, 255))
            screen.blit(text, (224, 457))
        else:
            if currentRoom.roomType == "boss":
                screen.blit(bg_boss, (0,0))
                screen.blit((currentRoom.monster.image.surf), ((1 * WIDTH)/3, HEIGHT/3))
            else:
                screen.blit(bg_monster, (0,0)) # monster background
                screen.blit((currentRoom.monster.image.surf), ((3 * WIDTH)/4, HEIGHT/2))
            
            pygame.draw.rect(screen, (100, 100, 100), [25, 450, 50, 25]) # Run away
            text = smallfont.render("Run", True, (255, 255, 255))
            screen.blit(text, (32, 457))
            pygame.draw.rect(screen, (100, 100, 100), [200, 450, 90, 25]) # Attack in fight
            text = smallfont.render("Attack", True, (255, 255, 255))
            screen.blit(text, (220, 457))
            pygame.draw.rect(screen, (100, 100, 100), [100, 450, 90, 25]) # Use Item in fight
            text = smallfont.render("Use Item", True, (255, 255, 255))
            screen.blit(text, (117, 457))
            pygame.draw.rect(screen, (100, 100, 100), [375, 450, 90, 25]) # Inventory
            text = smallfont.render("Inventory", True, (255, 255, 255))
            screen.blit(text, (389, 457))

        PrintMap(map, currentRoom, screen)

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

        if show_prompt: # the item use prompt and change equipment prompt
        
            # background rectangle
            item_text = ""
            item_type = get_item_type(selected_item)
            if item_type == "axe" or item_type == "sword" or item_type == "bow":
                item_text = "Would you like to swap weapons?"
            else:
                item_text = "Would you like to use this item?"
            pygame.draw.rect(screen, (200, 200, 200), [100, 300, 300, 80])
            text = smallfont.render(item_text, True, (0,0,0))
            screen.blit(text, (150, 315))

            # yes and no buttons
            pygame.draw.rect(screen, (100,100,100), [150, 350, 90, 25])
            text = smallfont.render("Yes", True, (250, 250, 250))
            screen.blit(text, (180, 355))
            pygame.draw.rect(screen, (100,100,100), [270, 350, 90, 25])
            text = smallfont.render("No", True, (250, 250, 250))
            screen.blit(text, (300, 355))

            # Currently selected item details - show sprite, item name, damage / spell effect amount
            pygame.draw.rect(screen, (200, 200, 200), [100, 400, 300, 80])
            screen.blit(return_sprite(selected_item).surf, (120, 415))
            text = smallfont.render(selected_item.type, True, (0,0,0))
            screen.blit(text, (200, 420))
            if item_type == "axe" or item_type == "sword" or item_type == "bow": 
                text = smallfont.render("Damage: " + str(selected_item.damage), True, (0,0,0))
                screen.blit(text, (200, 440))
            else:
                text = smallfont.render("Effect Amount: " + str(selected_item.effect), True, (0,0,0))
                screen.blit(text, (200, 440))

        # Gets the mouse position
        mouse = pygame.mouse.get_pos()

        # Event Handler
        # Check if the user closed the window or pressed escape
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == MOUSEBUTTONDOWN:
                print(mouse)
                if (not show_inventory) and (currentRoom.roomType == "safe"): # can't change rooms accidentally when inventory is open
                    # clicking on arrow
                    if 235 <= mouse[0] < 270 and 25 <= mouse[1] <= 70 and "North" in validMoves: # northArrow.rect.collidepoint(mouse)
                        player.buff_damage = 0
                        player.buff_defense = 0 # remove buffs on room change
                        sprites.ArrowSprite.Clicked(northArrow)
                        currentRoom = room.Room.SpawnRoom(map, currentRoom, (currentRoom.x, currentRoom.y), numDefeated, "north")
                        print("current room coordinates are (" + str(currentRoom.x) + "," + str(currentRoom.y) + ")")
                    elif 430 <= mouse[0] < 475 and 205 <= mouse[1] <= 240 and "East" in validMoves:
                        player.buff_damage = 0
                        player.buff_defense = 0 # remove buffs on room change
                        sprites.ArrowSprite.Clicked(eastArrow)
                        currentRoom = room.Room.SpawnRoom(map, currentRoom, (currentRoom.x, currentRoom.y), numDefeated, "east")
                        print("current room coordinates are (" + str(currentRoom.x) + "," + str(currentRoom.y) + ")")
                    elif 235 <= mouse[0] < 270 and 400 <= mouse[1] <= 445 and "South" in validMoves:
                        player.buff_damage = 0
                        player.buff_defense = 0 # remove buffs on room change
                        sprites.ArrowSprite.Clicked(southArrow)
                        currentRoom = room.Room.SpawnRoom(map, currentRoom, (currentRoom.x, currentRoom.y), numDefeated, "south")
                        print("current room coordinates are (" + str(currentRoom.x) + "," + str(currentRoom.y) + ")")
                    elif 30 <= mouse[0] < 75 and 205 <= mouse[1] <= 240 and "West" in validMoves:
                        player.buff_damage = 0
                        player.buff_defense = 0 # remove buffs on room change
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
                                events.acquireItem()
                            print(f"Inventory: {player.inventory}")
            

                # using items, and changing weapons in the inventory
                if show_inventory: 
                    # check which slot they clicked on if inventory is open
                    if 50 <= mouse[0] <= 100 and 50 <= mouse[1] <= 100: # first inventory slot clicked
                        if player.inventory[0][0] != None:
                            show_prompt = True
                            inventory_coords[0] = 0
                            inventory_coords[1] = 0
                            selected_item = player.inventory[0][0]
                    elif 110 <= mouse[0] <= 160 and 50 <= mouse[1] <= 100:
                        if player.inventory[0][1] != None:
                            show_prompt = True
                            inventory_coords[0] = 0
                            inventory_coords[1] = 1
                            selected_item = player.inventory[0][1]
                    elif 170 <= mouse[0] <= 220 and 50 <= mouse[1] <= 100:
                        if player.inventory[0][2] != None:
                            show_prompt = True
                            inventory_coords[0] = 0
                            inventory_coords[1] = 2
                            selected_item = player.inventory[0][2]
                    elif 230 <= mouse[0] <= 280 and 50 <= mouse[1] <= 100:
                        if player.inventory[0][3] != None:
                            show_prompt = True
                            inventory_coords[0] = 0
                            inventory_coords[1] = 3
                            selected_item = player.inventory[0][3]
                    elif 290 <= mouse[0] <= 340 and 50 <= mouse[1] <= 100:
                        if player.inventory[0][4] != None:
                            show_prompt = True
                            inventory_coords[0] = 0
                            inventory_coords[1] = 4
                            selected_item = player.inventory[0][4]
                    elif 50 <= mouse[0] <= 100 and 110 <= mouse[1] <= 160:
                        if player.inventory[1][0] != None:
                            show_prompt = True
                            inventory_coords[0] = 1
                            inventory_coords[1] = 0
                            selected_item = player.inventory[1][0]
                    elif 110 <= mouse[0] <= 160 and 110 <= mouse[1] <= 160:
                        if player.inventory[1][1] != None:
                            show_prompt = True
                            inventory_coords[0] = 1
                            inventory_coords[1] = 1
                            selected_item = player.inventory[1][1]
                    elif 170 <= mouse[0] <= 220 and 110 <= mouse[1] <= 160:
                        if player.inventory[1][2] != None:
                            show_prompt = True
                            inventory_coords[0] = 1
                            inventory_coords[1] = 2
                            selected_item = player.inventory[1][2]
                    elif 230 <= mouse[0] <= 280 and 110 <= mouse[1] <= 160:
                        if player.inventory[1][3] != None:
                            show_prompt = True
                            inventory_coords[0] = 1
                            inventory_coords[1] = 3
                            selected_item = player.inventory[1][3]
                    elif 290 <= mouse[0] <= 340 and 110 <= mouse[1] <= 160:
                        if player.inventory[1][4] != None:
                            show_prompt = True
                            inventory_coords[0] = 1
                            inventory_coords[1] = 4
                            selected_item = player.inventory[1][4]

                    # When a player has selected an item, a prompt will display for whether or not to use the item / switch weapon 
                    if show_prompt:
                        if 150 <= mouse[0] <= 240 and 350 <= mouse[1] <= 375: # clicked "yes" for use item
                            print("yes clicked")
                            show_prompt = False
                            item_type = selected_item.type
                            if item_type == "Axe" or item_type == "Rusty Sword" or item_type == "Bow": # player is swapping weapons
                                print("swap weapon")
                                player.inventory[inventory_coords[0]][inventory_coords[1]] = player.equipped_item # place equipped weapon into inventory, then put inventory weapon selected to equipped
                                player.equipped_item = selected_item
                                player.weapon_damage = player.equipped_item.damage
                                player.sprites_list[inventory_coords[0]][inventory_coords[1]] = player.equipped_sprite
                                player.equipped_sprite = return_sprite(selected_item)
                            else: # player is using a spell
                                print("spell selected")
                                if item_type == "Healing":
                                    player.health += selected_item.effect 
                                    if player.health > player.max_health:
                                        player.health = player.max_health # can't heal above max
                                    print("healing")
                                elif item_type == "Attack Buff":
                                    print("attack buff")
                                    player.buff_damage = selected_item.effect
                                else: # defense buff
                                    print("defense buff")
                                    player.buff_defense = selected_item.effect 
                                # remove spell from inventory and sprites list (one time use)
                                player.inventory[inventory_coords[0]][inventory_coords[1]] = None
                                player.sprites_list[inventory_coords[0]][inventory_coords[1]] = None

                        elif 270 <= mouse[0] <= 360 and 350 <= mouse[1] <= 375:
                            print("no clicked")
                            show_prompt = False
                            selected_item = None

                if currentRoom.roomType == "safe":
                    # Clicked inventory button
                    if 210 <= mouse[0] <= 290 and 450 <= mouse[1] <= 475:
                        print("clicked inventory")
                        show_inventory = True

                    # Clicked inventory exit
                    if 456 <= mouse[0] <= 490 and 16 <= mouse[1] <= 53:
                        show_inventory = False
                        show_prompt = False
                else:
                    # Clicked inventory button
                    if 375 <= mouse[0] <= 465 and 450 <= mouse[1] <= 475:
                        print("clicked inventory")
                        show_inventory = True

                    # Clicked inventory exit
                    if 456 <= mouse[0] <= 490 and 16 <= mouse[1] <= 53:
                        show_inventory = False
                        show_prompt = False # exit out of item use prompt as well if exit inventory

                    # Clicked Attack button
                    if 200 <= mouse[0] <= 290 and 450 <= mouse[1] <= 475:
                        print(f"Attack: player health {player.health} and monster health {currentRoom.monster.health}")
                        currentRoom.monster.takeDamage(player.CalcDamage())
                        if (currentRoom.monster.checkAlive()):
                            print("The monster has died")
                            if currentRoom.roomType == 'boss':
                                print("You've won")
                                gameOver = True

                            else:
                                currentRoom.DefeatedRoom()
                                numDefeated += 1
                        
                        else:
                            action = currentRoom.monster.pickAction()
                            print(f"Monster Action: {action}")
                            if action[0] == "attack":
                                if action[1] > player.CalcDefense():
                                    player.health -= action[1] - player.CalcDefense()
                            print(f"End Attack: player health {player.health} and monster health {currentRoom.monster.health}")
                            if player.health <= 0:
                                playerDead = True
                                gameOver = True

                    #Clicked the run away button
                    if 25 <= mouse[0] <= 115 and 450 <= mouse[1] <= 475:
                        print("Tried to run away")
                        chance = random.random()
                        print(chance)
                        if chance < 0.3:
                            print("run away successfully")
                            #TODO lose an item in inventory
                            player.buff_damage = 0
                            player.buff_defense = 0 # spell buffs are removed upon room change 
                            newRoom = random.choice(validMoves)
                            print(newRoom)
                            if newRoom == "North": # northArrow.rect.collidepoint(mouse)
                                sprites.ArrowSprite.Clicked(northArrow)
                                currentRoom = room.Room.SpawnRoom(map, currentRoom, (currentRoom.x, currentRoom.y), numDefeated, "north")
                                print("current room coordinates are (" + str(currentRoom.x) + "," + str(currentRoom.y) + ")")
                            elif newRoom == "East":
                                sprites.ArrowSprite.Clicked(eastArrow)
                                currentRoom = room.Room.SpawnRoom(map, currentRoom, (currentRoom.x, currentRoom.y), numDefeated, "east")
                                print("current room coordinates are (" + str(currentRoom.x) + "," + str(currentRoom.y) + ")")
                            elif newRoom == "South":
                                sprites.ArrowSprite.Clicked(southArrow)
                                currentRoom = room.Room.SpawnRoom(map, currentRoom, (currentRoom.x, currentRoom.y), numDefeated, "south")
                                print("current room coordinates are (" + str(currentRoom.x) + "," + str(currentRoom.y) + ")")
                            elif newRoom == "West":
                                sprites.ArrowSprite.Clicked(westArrow)
                                currentRoom = room.Room.SpawnRoom(map, currentRoom, (currentRoom.x, currentRoom.y), numDefeated, "west")
                                print("current room coordinates are (" + str(currentRoom.x) + "," + str(currentRoom.y) + ")")                
                        else:
                            print("Did not run away")
                            action = currentRoom.monster.pickAction()
                            print(f"Monster Action: {action}")
                            if action[0] == "attack":
                                if action[1] > player.CalcDefense():
                                    player.health -= action[1] - player.CalcDefense()
                                if player.checkPlayerAlive() == False:
                                    print("Player has died")
                            print(f"End Attack: player health {player.health} and monster health {currentRoom.monster.health}")
                            if player.health <= 0:
                                playerDead = True
                                gameOver = True

                    if 100 <= mouse[0] <= 190 and 450 <= mouse[1] <= 475:
                        print("Use item")
                        show_inventory = True

    pygame.display.update()

pygame.quit()
