import random

class Room():
    def __init__(self, coords):
        # room type, chest, coordinates, monster
        num = random.randint(1, 10)
        if num <= 8: # 80% chance of monster room
            self.roomType = "monster"
        else: # 20% chance of safe room
            self.roomType = "safe"

        if self.roomType == "monster": 
            # self.monster = Monster()
            print("Init monster for this room")
        else:
            # self.chest = Chest()
            print("Init chest for this room")

        self.x = coords[0] # pass in the x and y coordinates when initialized, based on player's location and which arrow is clicked
        self.y = coords[1]

    def __init__(self, coords, roomType): # for initial safe room, 
        # room type, chest, coordinates, monster
        self.roomType = roomType

        # self.chest = Chest() # init chest for this room

        self.x = coords[0] # pass in the x and y coordinates when initialized, based on player's location and which arrow is clicked
        self.y = coords[1]