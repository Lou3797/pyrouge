from entity.components.components import *


class BasicMonster(Component):
    def __init__(self):
        super().__init__(Components.AI)

    def take_turn(self, target, map):
        if self.owner.get_component(Components.FOV):
            if self.owner.get_component(Components.FOV).can_see(target):
                if self.owner.distance_to(target) >= 2:
                    self.owner.move_astar(target, map)
