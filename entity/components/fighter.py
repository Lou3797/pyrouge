from entity.components.components import *


class Fighter(Component):
    def __init__(self, hostile=True):
        super().__init__(Components.FIGHTER)
        self.hostile = hostile

    def attack(self):
        return 4