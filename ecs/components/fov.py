import libtcodpy as tcod
from ecs.components.component import *


class FOV(Component):
    def __init__(self, map, radius, light_walls=True, algorithm=0):
        super().__init__(Components.FOV)
        self.fov = self.initialize_fov(map)
        self.radius = radius
        self.algorithm = algorithm
        self.light_walls = light_walls

    def initialize_fov(self, map):
        fov = tcod.map_new(map.width, map.height)
        for y in range(map.height):
            for x in range(map.width):
                tcod.map_set_properties(fov, x, y, not map.tiles[x][y].opaque, not map.tiles[x][y].solid)
        return fov
    #
    # def can_see(self, entity):
    #     return tcod.map_is_in_fov(self.fov, entity.x, entity.y)
    #
    # def recompute_fov(self):
    #     tcod.map_compute_fov(self.fov, self.owner.x, self.owner.y, self.radius, self.light_walls, self.algorithm)
    #
    # def change_fov(self, map=None, radius=None, light_walls=None, algorithm=None):
    #     if map:
    #         self.fov = map.initialize_fov()
    #     if radius:
    #         self.radius = radius
    #     if light_walls:
    #         self.light_walls = light_walls
    #     if algorithm:
    #         self.algorithm = algorithm
