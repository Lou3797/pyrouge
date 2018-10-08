import libtcodpy as tcod
from ecs.components.component import *


class BasicMonster(Component):
    def __init__(self):
        super().__init__(Components.AI)

    # def take_turn(self, target, map):
    #     if self.owner.get_component(Components.FOV):
    #         if self.owner.get_component(Components.FOV).can_see(target) and self.owner.get_component(Components.MOVABLE):
    #             if self.owner.get_component(Components.MOVABLE).distance_to(target) >= 2:
    #                 self.owner.get_component(Components.MOVABLE).move_astar(target, map)
    #         else:
    #             self.owner.get_component(Components.MOVABLE).move(tcod.random_get_int(0, -1, 1), tcod.random_get_int(0, -1, 1), map)
