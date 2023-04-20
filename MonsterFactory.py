from Monster import Monster
from Monster import Goblin
from Monster import Cheeseman
class MonsterFactory:

    def createMonster(self):
        pass

class GoblinFactory:

    def createGoblin(self):
        bob = Goblin()
        return bob

class CheesemanFactory:

    def createCheeseman(self):
        cheese = Cheeseman()
        return cheese