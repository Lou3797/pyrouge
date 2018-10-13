from ecs.component import *


class Position(Component):
    def __init__(self, x, y, solid=False):
        super().__init__(Components.POSITION)
        self.x = x
        self.y = y
        self.solid = solid
