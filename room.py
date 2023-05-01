import random
import chest
import MonsterFactory

goblin_factory = MonsterFactory.GoblinFactory()
cheeseman_factory = MonsterFactory.CheesemanFactory()

class Room():

    def __init__(self, coords, roomType): # for initial safe room, 
        
        self.chest = None
        if roomType == "random":
            # room type, chest, coordinates, monster
            num = random.randint(1, 10)
            if num <= 8: # 80% chance of monster room
                self.roomType = "monster"
                # self.monster = Monster()
                print("Init monster for this room")
            else: # 20% chance of safe room
                self.roomType = "safe"
                self.chest = chest.ChestSprite("closed_chest.png")
                print("Init chest for this room")     

            num = random.randint(1, 2)
            if num == 1:
                self.monster = goblin_factory.createMonster()     
            else:
                self.monster = cheeseman_factory.createMonster()

            self.x = coords[0] # pass in the x and y coordinates when initialized, based on player's location and which arrow is clicked
            self.y = coords[1]
        else: # if we need to specifically define the saferoom or boss room
            # room type, chest, coordinates, monster
            self.roomType = roomType

            if roomType == "safe":
                self.chest = chest.ChestSprite("closed_chest.png") # init chest for this room
            if roomType == "boss":
                print("boss room")
                # different background, and will lead to end of game

            self.x = coords[0] # pass in the x and y coordinates when initialized, based on player's location and which arrow is clicked
            self.y = coords[1]


    def SpawnRoom(map, currentRoom, coord, numDefeated, direction):
        if direction == "north":
            new_coord = (coord[0], coord[1]-1)
        elif direction == "east":
            new_coord = (coord[0]+1, coord[1])
        elif direction == "south":
            new_coord = (coord[0], coord[1]+1)
        else: # west
            new_coord = (coord[0]-1, coord[1])
        if new_coord not in map: # generate room
                if numDefeated == 3:
                    print("spawn boss")
                else:
                    new_room = Room(new_coord, "random")
                    map[new_coord] = new_room # add to map
                    return new_room
        return map[new_coord] # this exists in the map already

    def DefeatedRoom(self):
        self.roomType = "safe"
        self.chest = chest.ChestSprite("closed_chest.png") # init chest for this room

