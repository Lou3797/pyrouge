from entity.components.components import *


class Hitpoints(Component):
    def __init__(self, hp=10):
        super().__init__(Components.HITPOINTS)
        self.cur_hp = hp
        self.max_hp = hp
        self.temp_hp = 0
