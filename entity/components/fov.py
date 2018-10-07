import libtcodpy as tcod
from entity.components.components import *


class FOV(Component):
    def __init__(self, map_fov, radius, light_walls=True, algorithm=0):
        super().__init__(Components.FOV)
        self.fov = map_fov
        self.radius = radius
        self.algorithm = algorithm
        self.light_walls = light_walls

    def can_see(self, entity):
        if tcod.map_is_in_fov(self.fov, entity.x, entity.y):
            return True
        return False

    def recompute_fov(self):
        tcod.map_compute_fov(self.fov, self.owner.x, self.owner.y, self.radius, self.light_walls, self.algorithm)

    def update_fov(self, map_fov=None, radius=None, light_walls=None, algorithm=None):
        if map_fov:
            self.fov = map_fov
        if radius:
            self.radius = radius
        if light_walls:
            self.light_walls = light_walls
        if algorithm:
            self.algorithm = algorithm
