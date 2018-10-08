from ecs.components.component import *


class Fighter(Component):
    def __init__(self, hostile=True):
        super().__init__(Components.FIGHTER)
        self.hostile = hostile
