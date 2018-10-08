from ecs.systems.system import System
from ecs.components.component import Components


class Render_System(System):
    def __init__(self):
        super().__init__(Components.POSITION, Components.MOVABLE)
