import libtcodpy as tcod
from entity.components.components import *
from entity.death_functions import on_death
from ui.messages import Message


class Hitpoints(Component):
    def __init__(self, hp=10, death_function=None):
        super().__init__(Components.HITPOINTS)
        self.cur_hp = hp
        self.max_hp = hp
        self.temp_hp = 0
        self.on_death = death_function

    def take_damage(self, dmg, src=None):
        logs = []
        self.cur_hp -= dmg
        logs.append(Message('{0} attacks {1} for {2} hit points!'.format(
            src.name, self.owner.name, str(dmg)), tcod.red))
        if self.cur_hp <= 0:
            self.cur_hp = 0
            if self.on_death:
                logs.append(self.on_death(self.owner, src))
            else:
                logs.append(on_death(self.owner, src))
        return logs
        # return Message('{0} attacks {1} for {2} hit points.'.format(src.name, self.owner.name, str(dmg)), tcod.red)

    def heal(self, hp):
        self.cur_hp += hp
        if self.cur_hp > self.max_hp:
            self.cur_hp = self.max_hp

    def temp_health(self, hp, max=None):
        if max:
            if self.temp_hp >= max:
                return
            else:
                self.temp_hp += hp
                if self.temp_hp >= max:
                    self.temp_hp = max
        else:
            self.temp_hp += hp

    def is_dead(self):
        return self.cur_hp <= 0