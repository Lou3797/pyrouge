import libtcodpy as tcod
from enum import Enum
import math


class RenderOrder(Enum):
    DECAL = 0
    CORPSE = 1
    OBJECT = 2
    ITEM = 3
    ACTOR = 4


class Entity:
    # this is a generic object: the player, a monster, an item, the stairs...
    # it's always represented by a character on screen.
    def __init__(self, x, y, char, name, color, solid=False, render_order=RenderOrder.DECAL, *components):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.solid = solid
        self.render_order = render_order
        self.components = []
        self.components.extend(components)
        self.set_components_owner()

    def move(self, dx, dy, dest_map=None):
        # move by the given amount

        if dest_map:
            if dest_map.is_blocked_at(self.x + dx, self.y + dy):
                return False

        self.x += dx
        self.y += dy
        return True

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def move_towards(self, target_x, target_y, map):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not map.is_blocked_at(self.x + dx, self.y + dy):
            self.move(dx, dy)

    def move_astar(self, target, map):
        # Create a FOV map that has the dimensions of the map
        fov = tcod.map_new(map.width, map.height)

        # Scan the current map each turn and set all the walls as unwalkable
        for y1 in range(map.height):
            for x1 in range(map.width):
                tcod.map_set_properties(fov, x1, y1, not map.tiles[x1][y1].opaque, not map.tiles[x1][y1].solid)

        # Scan all the objects to see if there are objects that must be navigated around
        # Check also that the object isn't self or the target (so that the start and the end points are free)
        # The AI class handles the situation if self is next to the target so it will not use this A* function anyway
        for entity in map.entities:
            if entity.solid and entity != self and entity != target:
                # Set the tile as a wall so it must be navigated around
                tcod.map_set_properties(fov, entity.x, entity.y, True, False)

        # Allocate a A* path
        # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
        my_path = tcod.path_new_using_map(fov, 1.41)

        # Compute the path between self's coordinates and the target's coordinates
        tcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # Check if the path exists, and in this case, also the path is shorter than 25 tiles
        # The path size matters if you want the monster to use alternative longer paths (for example through other rooms) if for example the player is in a corridor
        # It makes sense to keep path size relatively low to keep the monsters from running around the map if there's an alternative path really far away
        if not tcod.path_is_empty(my_path) and tcod.path_size(my_path) < 25:
            # Find the next coordinates in the computed full path
            x, y = tcod.path_walk(my_path, True)
            if x or y:
                # Set self's coordinates to the next path tile
                self.x = x
                self.y = y
        else:
            # Keep the old move function as a backup so that if there are no paths (for example another monster blocks a corridor)
            # it will still try to move towards the player (closer to the corridor opening)
            self.move_towards(target.x, target.y, map)

            # Delete the path to free memory
            tcod.path_delete(my_path)

    def draw(self, con):
        # set the color and then draw the character that represents this object at its position
        tcod.console_set_default_foreground(con, self.color)
        tcod.console_put_char(con, self.x, self.y, self.char, tcod.BKGND_NONE)

    def clear(self, con):
        # erase the character that represents this object
        tcod.console_put_char(con, self.x, self.y, ' ', tcod.BKGND_NONE)

    def get_component(self, component_id):
        for comp in self.components:
            if comp.id == component_id:
                return comp
        return None

    def remove_component(self, component_id):
        # print("Looking for", component_id, "to remove it")
        for comp in self.components:
            if comp.id == component_id:
                # print("Removing", component_id)
                self.components.remove(comp)

    def print_all_components(self):
        for comp in self.components:
            print(comp.id)

    def set_components_owner(self):
        for comp in self.components:
            comp.owner = self
