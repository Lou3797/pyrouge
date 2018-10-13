from ecs.component import *
from ecs.entities.death_functions import on_death


class Hitpoints(Component):
    def __init__(self, hp=10, death_function=on_death):
        super().__init__(Components.HITPOINTS)
        self.cur_hp = hp
        self.max_hp = hp
        self.temp_hp = 0
        self.on_death = death_function
