import libtcodpy as tcod
from ecs.systems.system import System
from ecs.components.component import Components


class FOV_System(System):
    def __init__(self):
        super().__init__(Components.FOV, Components.POSITION)

    def recompute_all_entity_fovs(self, map):
        for entity in map.entities:
            self.recompute_single_entity_fov(entity)
        return None

    def recompute_single_entity_fov(self, entity):
        if self.has_required_components(entity):
            fov = entity.get_component(Components.FOV)
            pos = entity.get_component(Components.POSITION)
            tcod.map_compute_fov(fov.fov, pos.x, pos.y, fov.radius, fov.light_walls, fov.algorithm)

    def can_see(self, entity):
        if self.has_required_components(entity):
            fov = entity.get_component(Components.FOV)
            pos = entity.get_component(Components.POSITION)
            return tcod.map_is_in_fov(fov.fov, pos.x, pos.y)
