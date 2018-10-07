from entity.components.components import *


class Corpse(Component):
    def __init__(self, char='%'):
        super().__init__(Components.CORPSE)
        self.char = char
