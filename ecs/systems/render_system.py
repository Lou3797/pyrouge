import libtcodpy as tcod
from colors import COLORS
from ecs.component import Components
from ecs.system import System


class RenderSystem(System):
    def __init__(self, console):
        super().__init__(Components.POSITION, Components.ICON)
        self.console = console

    def start(self):
        tcod.console_set_default_foreground(self.console, tcod.white)

    def render_map(self, map, entity_fov):
        for y in range(map.height):
            for x in range(map.width):
                visible = tcod.map_is_in_fov(entity_fov, x, y)
                wall = map.tiles[x][y].opaque
                if visible:
                    if wall:
                        tcod.console_set_char_background(self.console, x, y, COLORS.get('light_wall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(self.console, x, y, COLORS.get('light_ground'), tcod.BKGND_SET)
                    map.tiles[x][y].explored = True
                elif map.tiles[x][y].explored:
                    if wall:
                        tcod.console_set_char_background(self.console, x, y, COLORS.get('dark_wall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(self.console, x, y, COLORS.get('dark_ground'), tcod.BKGND_SET)

        for entity in map.entities:
            self.render_entity(entity, entity_fov)

    def render_entity(self, entity, fov=None):
        pos = entity.get_component(Components.POSITION)
        char = entity.get_component(Components.ICON)
        x, y = pos.x, pos.y

        if fov and self.has_required_components(entity):
            if not tcod.map_is_in_fov(fov, x, y):
                return

        tcod.console_set_default_foreground(self.console, char.color)
        tcod.console_put_char(self.console, x, y, char.char, tcod.BKGND_NONE)

    def render_entities(self, entities, fov=None):
        for entity in entities:
            self.render_entity(entity, fov)

    def clear_entities(self, entities):
        for entity in entities:
            if self.has_required_components(entity):
                pos = entity.get_component(Components.POSITION)
                x, y = pos.x, pos.y
                tcod.console_put_char(self.console, x, y, ' ', tcod.BKGND_NONE)

    def sort_entities_by_render_order(self, map):
        # This will fail on any entities with no CHAR component
        map.entities = sorted(map.entities, key=lambda x: x.get_component(Components.ICON).render_order.value)

    def exit(self):
        tcod.console_blit(self.console, 0, 0, 96, 54, 0, 0, 0)
        tcod.console_flush()
