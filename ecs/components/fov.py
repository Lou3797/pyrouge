import libtcodpy as tcod
from ecs.component import *


class FOV(Component):
    def __init__(self, map, radius, light_walls=True, algorithm=0):
        super().__init__(Components.FOV)
        self.fov = None
        self.radius = radius
        self.algorithm = algorithm
        self.light_walls = light_walls
        self.set_fov(map)

    def initialize_fov(self, map):
        fov = tcod.map_new(map.width, map.height)
        for y in range(map.height):
            for x in range(map.width):
                tcod.map_set_properties(fov, x, y, not map.tiles[x][y].opaque, not map.tiles[x][y].solid)
        return fov

    def set_fov(self, map):
        self.fov = self.initialize_fov(map)
