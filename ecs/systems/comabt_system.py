from ecs.systems.system import System
from ecs.components.component import Components


class Combat_System(System):
    def __init__(self):
        super().__init__(Components.FIGHTER, Components.HITPOINTS)
