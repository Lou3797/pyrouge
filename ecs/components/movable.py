from ecs.component import *


class Movable(Component):
    def __init__(self):
        super().__init__(Components.MOVABLE)
