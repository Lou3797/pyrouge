import libtcodpy as tcod


class Entity:
    # this is a generic object: the player, a monster, an item, the stairs...
    # it's always represented by a character on screen.
    def __init__(self, x, y, char, color, components=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        # A dictionary of components ex. {'fighter': Fighter(10, 5, 2), 'inventory': Inventory(26)}
        self.components = components

    def move(self, dx, dy):
        # move by the given amount
        self.x += dx
        self.y += dy

    def draw(self, con):
        # set the color and then draw the character that represents this object at its position
        tcod.console_set_default_foreground(con, self.color)
        tcod.console_put_char(con, self.x, self.y, self.char, tcod.BKGND_NONE)

    def clear(self, con):
        # erase the character that represents this object
        tcod.console_put_char(con, self.x, self.y, ' ', tcod.BKGND_NONE)
