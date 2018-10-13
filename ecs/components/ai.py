from enum import Enum

from ecs.component import *


class AI_Types(Enum):
    RANDOM = 0
    CHASE_TARGET = 1


class AI(Component):
    def __init__(self):
        super().__init__(Components.AI)


class Specific_AI(AI):
    def __init__(self, ai_type):
        super().__init__()
        self.ai_type = ai_type


class Random_AI(Specific_AI):
    def __init__(self):
        super().__init__(AI_Types.RANDOM)


class Chase_Target_AI(Specific_AI):
    def __init__(self, target):
        super().__init__(AI_Types.CHASE_TARGET)
        self.target = target