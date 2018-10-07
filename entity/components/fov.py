import libtcodpy as tcod
from entity.components.components import *


class FOV(Component):
    def __init__(self, radius, map):
        super().__init__(Components.FOV)
        self.radius = radius
        self.fov = self.initialize_fov(map)

    def initialize_fov(self, map):
        for y in range(map.height):
            for x in range(map.width):
                tcod.map_set_properties(self.fov, x, y, not map.tiles[x][y].opaque, not map.tiles[x][y].solid)

    def can_see(self, entity):
        if tcod.map_is_in_fov(self.fov, entity.x, entity.y):
            return True
        return False
