from enum import Enum

from ecs.component import *


class Attack_Modes(Enum):
    ALL = 0
    HOSTILES = 1
    MANUAL = 2


class Fighter(Component):
    def __init__(self, attack_mode=Attack_Modes.ALL):
        super().__init__(Components.FIGHTER)
        self.attack_mode = attack_mode
