#!/usr/bin/env python
import libtcodpy as tcod
from input import handle_keys
from map.map import Map
from entity.entity import Entity


def main():
    FULLSCREEN = False
    SCREEN_WIDTH = 80  # characters wide
    SCREEN_HEIGHT = 50  # characters tall

    # Setup player
    player_x = SCREEN_WIDTH // 2
    player_y = SCREEN_HEIGHT // 2

    # Setup Font
    font_filename = 'res/arial12x12.png'
    tcod.console_set_custom_font(font_filename, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    # Initialize screen
    title = 'Python 3 + Libtcod tutorial'
    mainCon = tcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
    tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, title, FULLSCREEN)

    map = Map(SCREEN_WIDTH, SCREEN_HEIGHT)
    map.create_map()
    player = Entity(player_x, player_y, '@', tcod.white)
    map.add(player)


    while not tcod.console_is_window_closed():
        tcod.console_set_default_foreground(mainCon, tcod.white)
        # tcod.console_put_char(0, player_x, player_y, ' ', tcod.BKGND_NONE)
        # tcod.console_put_char(mainCon, player_x, player_y, '@', tcod.BKGND_NONE)

        map.draw(mainCon)
        tcod.console_blit(mainCon, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
        tcod.console_flush()
        map.clear(mainCon)
        # map.clear

        userInput = handle_keys()

        if userInput.get('move'):
            dx, dy, = userInput.get('move')
            if not map.tiles[player.x + dx][player.y + dy].solid:
                player.move(dx, dy)

        if userInput.get('exit'):
            return True


if __name__ == '__main__':
    main()
