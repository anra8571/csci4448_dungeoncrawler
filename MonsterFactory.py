from Monster import Monster
from Monster import Goblin
from Monster import Cheeseman
from Monster import Boss
from Monster import Slime
from Monster import Monkey
class MonsterFactory:

    def createMonster(self):
        pass

class GoblinFactory:

    def createMonster(self):
        bob = Goblin()
        return bob

class CheesemanFactory:

    def createMonster(self):
        cheese = Cheeseman()
        return cheese
    
class BossFactory:
    def createMonster(self):
        chad = Boss()
        return chad
    
class SlimeFactory:
    def createMonster(self):
        slime = Slime()
        return slime
    
class MonkeyFactory:
    def createMonster(self):
        monkey = Monkey()
        return monkey