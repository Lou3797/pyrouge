import libtcodpy as tcod
from map.tile import Tile
from map.shapes import Rectangle
from colors import COLORS


class Map:
    def __init__(self, width, height, fov_mod=0):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.entities = []
        self.fov_mod = fov_mod # apply this onto fov, for different lighting scenarios
        self.fov = None # fov can't be generated until the map is

    def initialize_tiles(self):
        return [[Tile(True) for y in range(self.height)] for x in range(self.width)]

    def initialize_map(self):
        # Create two rooms for demonstration purposes
        room1 = Rectangle(20, 15, 10, 15)
        room2 = Rectangle(35, 15, 10, 15)

        self.create_room(room1)
        self.create_room(room2)
        self.create_h_tunnel(25, 40, 23)

    def initialize_fov(self):
        fov = tcod.map_new(self.width, self.height)

        for y in range(self.height):
            for x in range(self.width):
                tcod.map_set_properties(fov, x, y, not self.tiles[x][y].opaque, not self.tiles[x][y].solid)
        return fov

    def recompute_fov(self, con, x, y, radius, light_walls=True, algorithm=0):
        tcod.map_compute_fov(self.fov, x, y, radius, light_walls, algorithm)

    def create_room(self, room):
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].solid = False
                self.tiles[x][y].opaque = False


    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].solid = False
            self.tiles[x][y].opaque = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].solid = False
            self.tiles[x][y].opaque = False

    def add(self, *args):
        for entity in args:
            self.entities.append(entity)

    def draw(self, con, draw_all=False):
        # Draw all the tiles in the game map
        if draw_all:
            for y in range(self.height):
                for x in range(self.width):
                    wall = self.tiles[x][y].opaque
                    if wall:
                        tcod.console_set_char_background(con, x, y, COLORS.get('dark_wall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(con, x, y, COLORS.get('dark_ground'), tcod.BKGND_SET)

        else:
            for y in range(self.height):
                for x in range(self.width):
                    visible = tcod.map_is_in_fov(self.fov, x, y)
                    wall = self.tiles[x][y].opaque
                    if visible:
                        if wall:
                            tcod.console_set_char_background(con, x, y, COLORS.get('light_wall'), tcod.BKGND_SET)
                        else:
                            tcod.console_set_char_background(con, x, y, COLORS.get('light_ground'), tcod.BKGND_SET)
                        self.tiles[x][y].explored = True
                    elif self.tiles[x][y].explored:
                        if wall:
                            tcod.console_set_char_background(con, x, y, COLORS.get('dark_wall'), tcod.BKGND_SET)
                        else:
                            tcod.console_set_char_background(con, x, y, COLORS.get('dark_ground'), tcod.BKGND_SET)

        for entity in self.entities:
            if tcod.map_is_in_fov(self.fov, entity.x, entity.y):
                entity.draw(con)

    def clear(self, con):
        for entity in self.entities:
            entity.clear(con)

    def is_blocked(self, x, y):
        # first test the map tile
        if self.tiles[x][y].solid:
            return True

        # now check for any blocking objects
        for entity in self.entities:
            if entity.solid and entity.x == x and entity.y == y:
                return True

        return False

    def generate_map(self, map_width, map_height, min_room_size, max_room_size, max_rooms):
        rooms = []
        num_rooms = 0
        xo = 0
        yo = 0

        for r in range(max_rooms):
            # random width and height
            w = tcod.random_get_int(0, min_room_size, max_room_size)
            h = tcod.random_get_int(0, min_room_size, max_room_size)
            # random position without going out of the boundaries of the map
            x = tcod.random_get_int(0, 0, map_width - w - 1)
            y = tcod.random_get_int(0, 0, map_height - h - 1)

            # "Rect" class makes rectangles easier to work with
            new_room = Rectangle(x, y, w, h)

            # run through the other rooms and see if they intersect with this one
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # this means there are no intersections, so this room is valid

                # "paint" it to the map's tiles
                self.create_room(new_room)

                # center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    # this is the first room, where the player starts at
                    xo = new_x
                    yo = new_y
                else:
                    # all rooms after the first:
                    # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # flip a coin (random number that is either 0 or 1)
                    if tcod.random_get_int(0, 0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                # finally, append the new room to the list
                #self.place_entities(new_room, entities, max_monsters_per_room, max_items_per_room)
                rooms.append(new_room)
                num_rooms += 1

        self.fov = self.initialize_fov()
        return (xo, yo)

