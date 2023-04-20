from Monster import Monster
from Monster import Goblin
from Monster import Cheeseman
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