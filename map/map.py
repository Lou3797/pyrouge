import libtcodpy as tcod
from map.tile import Tile
from map.shapes import Rectangle
from colors import COLORS


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.entities = []

    def initialize_tiles(self):
        return [[Tile(True) for y in range(self.height)] for x in range(self.width)]

    def create_map(self):
        # Create two rooms for demonstration purposes
        room1 = Rectangle(20, 15, 10, 15)
        room2 = Rectangle(35, 15, 10, 15)

        self.create_room(room1)
        self.create_room(room2)
        self.create_h_tunnel(25, 40, 23)

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].solid = False
            self.tiles[x][y].opaque = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].solid = False
            self.tiles[x][y].opaque = False

    def create_room(self, room):
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].solid = False
                self.tiles[x][y].opaque = False

    def add(self, *args):
        for entity in args:
            self.entities.append(entity)

    def draw(self, con):
        # Draw all the tiles in the game map
        for y in range(self.height):
            for x in range(self.width):
                wall = self.tiles[x][y].opaque

                if wall:
                    tcod.console_set_char_background(con, x, y, COLORS.get('dark_wall'), tcod.BKGND_SET)
                else:
                    tcod.console_set_char_background(con, x, y, COLORS.get('dark_ground'), tcod.BKGND_SET)

        for entity in self.entities:
            entity.draw(con)

    def clear(self, con):
        for entity in self.entities:
            entity.clear(con)
