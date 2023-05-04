import random

# Strategy Pattern: Determines what type of battle style a monster has
class attackStrat():
    attackProb = 0
    defenseProb = 0
    critPower = 0
    
    def getAttack():
        pass

    def getCrit():
        pass

# Most likely to heal
class Defensive(attackStrat):
    
    def __init__(self):
        self.attackProb = 0.3
        self.defenseProb = 0.7
        self.critPower = 0.2

    def getAttack(self):
        choice = random.uniform(0,1)
        if choice < self.attackProb:
            return "attack"
        else:
            return "defend"
        
    def getCrit(self):
        choice = random.uniform(0,1)
        if choice < self.critPower:
            return True
        
# Most likely to attack
class Offensive(attackStrat):
    
    def __init__(self):
        self.attackProb = 0.7
        self.defenseProb = 0.3
        self.critPower = 0.4

    def getAttack(self):
        choice = random.uniform(0,1)
        if choice < self.attackProb:
            return "attack"
        else:
            return "defend"
        
    def getCrit(self):
        choice = random.uniform(0,1)
        if choice < self.critPower:
            return True

# Equal probability of attacking and defending
class Balanced(attackStrat):
    def __init__(self):
        self.attackProb = 0.7
        self.defenseProb = 0.3
        self.critPower = 0.4

    def getAttack(self):
        choice = random.uniform(0,1)
        if choice < self.attackProb:
            return "attack"
        else:
            return "defend"
        
    def getCrit(self):
        choice = random.uniform(0,1)
        if choice < self.critPower:
            return True