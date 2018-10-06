import libtcodpy as tcod


class Entity:
    # this is a generic object: the player, a monster, an item, the stairs...
    # it's always represented by a character on screen.
    def __init__(self, x, y, char, name, color, solid=False, *components):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.solid = solid
        # A dictionary of components ex. {'fighter': Fighter(10, 5, 2), 'inventory': Inventory(26)}
        self.components = components
        self.set_components_owner()

    def move(self, dx, dy, dest_map=None):
        # move by the given amount

        if dest_map:
            if dest_map.is_blocked(self.x + dx, self.y + dy):
                return False

        self.x += dx
        self.y += dy
        return True

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

    def set_components_owner(self):
        for comp in self.components:
            comp.owner = self
