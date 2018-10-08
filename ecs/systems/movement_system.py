import libtcodpy as tcod
import math
from ecs.systems.system import System
from ecs.components.component import Components
from ecs.systems.collision_system import Collision_System


class Basic_Movement_System(System):
    def __init__(self):
        super().__init__(Components.POSITION, Components.MOVABLE)
        self.collision_system = Collision_System()

    def move(self, entity, dx, dy, map=None):
        if self.has_required_components(entity):
            pos = entity.get_component(Components.POSITION)
            if map:
                if self.collision_system.is_blocked_at(map, pos.x + dx, pos.y + dy):
                    return False
            pos.x += dx
            pos.y += dy
            return True
        return False

    def distance_to(self, source, target):
        if self.has_required_components(source) and self.has_required_components(target):
            src = source.get_component(Components.POSITION)
            trg = target.get_component(Components.POSITION)
            dx = trg.x - src.x
            dy = trg.y - src.y
            return math.sqrt(dx ** 2 + dy ** 2)
        return None

    def move_towards(self, source, target, map):
        if self.has_required_components(source) and self.has_required_components(target):
            src = source.get_component(Components.POSITION)
            trg = target.get_component(Components.POSITION)
            dx = trg.x - src.x
            dy = trg.y - src.y
            distance = self.distance_to(source, target)

            dx = int(round(dx / distance))
            dy = int(round(dy / distance))

            if not self.collision_system.is_blocked_at(map, src.x + dx, src.y + dy):
                return self.move(source, dx, dy, map)
        return False


class FOV_Movement_System(System):
    def __init__(self):
        super().__init__(Components.POSITION, Components.MOVABLE, Components.FOV)
        self.basic_movement = Basic_Movement_System()

    def move_astar(self, source, target, map):
        if self.has_required_components(source) and self.has_required_components(target):
            src = source.get_component(Components.POSITION)
            fov = source.get_component(Components.FOV)
            trg = target.get_component(Components.POSITION)
            # # Create a FOV map that has the dimensions of the map
            # fov = tcod.map_new(map.width, map.height)
            # # Scan the current map each turn and set all the walls as unwalkable
            # for y1 in range(map.height):
            #     for x1 in range(map.width):
            #         tcod.map_set_properties(fov, x1, y1, not map.tiles[x1][y1].opaque, not map.tiles[x1][y1].solid)
            # Scan all the objects to see if there are objects that must be navigated around
            # Check also that the object isn't self or the target (so that the start and the end points are free)
            # The AI class handles the situation if self is next to the target so it will not use this A* function anyway
            for entity in map.entities:
                if self.has_required_components(entity):
                    pos = entity.get_component(Components.POSITION)
                    if pos.solid and entity != source and entity != target:
                        # Set the tile as a wall so it must be navigated around
                        tcod.map_set_properties(fov.fov, pos.x, pos.y, True, False)
            # Allocate a A* path
            # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
            my_path = tcod.path_new_using_map(fov.fov, 1.41)
            # Compute the path between self's coordinates and the target's coordinates
            tcod.path_compute(my_path, src.x, src.y, trg.x, trg.y)
            # Check if the path exists, and in this case, also the path is shorter than 25 tiles
            # The path size matters if you want the monster to use alternative longer paths (for example through other rooms) if for example the player is in a corridor
            # It makes sense to keep path size relatively low to keep the monsters from running around the map if there's an alternative path really far away
            if not tcod.path_is_empty(my_path) and tcod.path_size(my_path) < 25:
                # Find the next coordinates in the computed full path
                x, y = tcod.path_walk(my_path, True)
                if x or y:
                    # Set self's coordinates to the next path tile
                    src.x = x
                    src.y = y
            else:
                # Keep the old move function as a backup so that if there are no paths (for example another monster blocks a corridor)
                # it will still try to move towards the player (closer to the corridor opening)
                self.basic_movement.move_towards(trg.x, trg.y, map)
                # Delete the path to free memory
                tcod.path_delete(my_path)
