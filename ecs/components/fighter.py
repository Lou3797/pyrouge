from ecs.components.component import *


class Fighter(Component):
    def __init__(self, hostile=True):
        super().__init__(Components.FIGHTER)
        self.hostile = hostile

    # def attack(self, target):
    #     logs = []
    #     logs.extend(target.get_component(Components.HITPOINTS).take_damage(self.roll_damage(), self.owner))
    #     return logs
    #
    # def roll_damage(self):
    #     return 3