import os

# Observer Pattern: Prints important events to log.txt
# Publisher
class ConcreteEventManager():
    def __init__(self):
        self.observers = []

    def registerObserver(self, observer):
        self.observers.append(observer)

    def removeObserver(self, observer):
        self.observers.remove(observer)

    def notifyObservers(self, note):
        for obs in self.observers:
            obs.update(note)

    def acquireItem(self):
        self.notifyObservers("Player acquired an item!\n")

    def update(self, note):
        self.notifyObservers(note)

# Subscriber
class Logger():
    def __init__(self):
        filepath = "log.txt"
        self.file = open(filepath, 'w')

        self.file.write("Game starting...\n")

    def update(self, note):
        self.file.write(note)