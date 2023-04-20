import random

class attackStrat():
    attackProb = 0
    defenseProb = 0
    critPower = 0
    
    def getAttack():
        pass

    def getCrit():
        pass



class Defensive(attackStrat):
    
    def __init__(self):
        self.attackProb = 0.3
        self.defenseProb = 0.7
        self.critPower = 0.2

    def getAttack(self):
        choice = random.uniform(0,1)
        if choice < self.attacProb:
            return "attack"
        else:
            return "defend"
        
    def getCrit(self):
        choice = random.uniform(0,1)
        if choice < self.critPower:
            return True
        
class Offensive(attackStrat):
    
    def __init__(self):
        self.attackProb = 0.7
        self.defenseProb = 0.3
        self.critPower = 0.4

    def getAttack(self):
        choice = random.uniform(0,1)
        if choice < self.attacProb:
            return "attack"
        else:
            return "defend"
        
    def getCrit(self):
        choice = random.uniform(0,1)
        if choice < self.critPower:
            return True

class Balanced(attackStrat):
    def __init__(self):
        self.attackProb = 0.7
        self.defenseProb = 0.3
        self.critPower = 0.4

    def getAttack(self):
        choice = random.uniform(0,1)
        if choice < self.attacProb:
            return "attack"
        else:
            return "defend"
        
    def getCrit(self):
        choice = random.uniform(0,1)
        if choice < self.critPower:
            return True