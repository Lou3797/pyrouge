from entity.components.components import *


class Ai:
    def __init__(self):
        pass

    def take_turn(self):
        # do some stuff
        return


class BasicMonster(Component):
    def __init__(self):
        # Component.__init__(self, Components.AI)
        # Ai.__init__(self)
        super().__init__(Components.AI)

    def take_turn(self):
        # print(self.owner.name, "took a turn")
        return
