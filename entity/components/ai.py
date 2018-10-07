from entity.components.components import *


class Ai:
    def __init__(self):
        pass

    def take_turn(self):
        # do some stuff
        return


class BasicMonster(Component, Ai):
    def __init__(self):
        Component.__init__(self, Components.AI)
        Ai.__init__(self)

    def take_turn(self):
        # placeholder
        return
