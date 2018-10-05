#!/usr/bin/env python
import libtcodpy as tcod
from input import handle_keys
from map.map import Map
from entity.entity import Entity


def main():
    FULLSCREEN = False
    SCREEN_WIDTH = 80  # characters wide
    SCREEN_HEIGHT = 50  # characters tall

    FOV_ALGO = 0  # default FOV algorithm
    FOV_LIGHT_WALLS = True
    LIGHT_RADIUS = 10

    # Setup Font
    font_filename = 'res/arial12x12.png'
    tcod.console_set_custom_font(font_filename, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    # Initialize screen
    title = 'Python 3 + Libtcod tutorial'
    main_con = tcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
    tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, title, FULLSCREEN)

    map = Map(SCREEN_WIDTH, SCREEN_HEIGHT)
    xo, yo = map.generate_map(SCREEN_WIDTH, SCREEN_HEIGHT, 6, 10, 30)
    player = Entity(xo, yo, '@', tcod.white)
    map.add(player)
    map.recompute_fov(main_con, player.x, player.y, 10)


    while not tcod.console_is_window_closed():
        tcod.console_set_default_foreground(main_con, tcod.white)

        map.draw(main_con)
        tcod.console_blit(main_con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
        tcod.console_flush()
        map.clear(main_con)

        userInput = handle_keys()

        if userInput.get('move'):
            dx, dy, = userInput.get('move')
            if not map.tiles[player.x + dx][player.y + dy].solid:
                player.move(dx, dy)
                map.recompute_fov(main_con, player.x, player.y, 10)

        if userInput.get('exit'):
            return True


if __name__ == '__main__':
    main()
