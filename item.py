import random

POOL_SIZE = 10

class Item():
    def __init__(self, in_attribute, in_effect):
        self.attribute = in_attribute
        self.effect = in_effect

class Spell(Item):
    def __init__(self):
        super().__init__("heal", random.randint(1, 10))

    def cast():
        print("cast")

class Weapon(Item):
    def __init__(self):
        super().__init__("weapon", random.randint(2, 5))

    def attack():
        print("Attack")

class Pool:
    def __init__(self, size=10):
        self.objs = []

        rand_int = 0
        for i in range(size):
            rand_int = random.randint(0, 1)
            if (rand_int == 0):
                self.objs.append(Spell())
            elif (rand_int == 1):
                self.objs.append(Weapon())
    
    def return_items(self):
        return self.objs
    
    def acquire(self):
        return self.objs.pop()
    
    def release(self, item):
        return self.objs.append(item)
    
pool = Pool(POOL_SIZE)
obj_array = pool.return_items()

for i in range(POOL_SIZE):
    print(f"{i}: {obj_array[i]}, attribute {obj_array[i].attribute}, effect {obj_array[i].effect}")