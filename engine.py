#!/usr/bin/env python
import libtcodpy as tcod
from input import handle_keys
from map.map import Map
from entity.entity import Entity
from gamestates import Gamestates


def main():
    FULLSCREEN = False
    SCREEN_WIDTH = 96  # characters wide
    SCREEN_HEIGHT = 54  # characters tall
    CAMERA_WIDTH, CAMERA_HEIGHT = 64, 36
    CAMERA_BUFFER = 2

    FOV_ALGO = 0  # default FOV algorithm
    FOV_LIGHT_WALLS = True
    LIGHT_RADIUS = 10

    # Setup Font
    font_filename = 'res/arial12x12.png'
    tcod.console_set_custom_font(font_filename, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    # Initialize screen
    title = 'Pyrouge'
    map_con = tcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT) # This needs to only be as big as the map can be
    log_con = tcod.console_new(CAMERA_WIDTH, SCREEN_HEIGHT - CAMERA_HEIGHT)
    status_con = tcod.console_new(SCREEN_WIDTH - CAMERA_WIDTH , SCREEN_HEIGHT // 2)
    equip_con = tcod.console_new(SCREEN_WIDTH - CAMERA_WIDTH, SCREEN_HEIGHT // 2)
    tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, title, FULLSCREEN)

    tcod.console_print_frame(log_con, 0, 0, CAMERA_WIDTH, SCREEN_HEIGHT - CAMERA_HEIGHT, True, tcod.BKGND_NONE,
                             'MESSAGE LOG')
    tcod.console_print_frame(status_con, 0, 0, SCREEN_WIDTH - CAMERA_WIDTH, SCREEN_HEIGHT // 2, True, tcod.BKGND_NONE,
                             'STATUS')
    tcod.console_print_frame(equip_con, 0, 0, SCREEN_WIDTH - CAMERA_WIDTH, SCREEN_HEIGHT // 2, True, tcod.BKGND_NONE,
                             'EQUIPMENT')

    current_map = Map(SCREEN_WIDTH, SCREEN_HEIGHT)
    xo, yo = current_map.generate_map(SCREEN_WIDTH, SCREEN_HEIGHT, 6, 10, 30)
    camera_x, camera_y = xo - (CAMERA_WIDTH // 2), yo - (CAMERA_HEIGHT // 2)
    player = Entity(xo, yo, '@', "Player", tcod.white, True)
    current_map.add(player)
    current_map.recompute_fov(map_con, player.x, player.y, 10)

    gamestate = Gamestates.PLAYER_ROUND

    while not tcod.console_is_window_closed():
        tcod.console_set_default_foreground(map_con, tcod.white)
        current_map.draw(map_con)
        tcod.console_blit(map_con, camera_x, camera_y, CAMERA_WIDTH, CAMERA_HEIGHT, 0, 0, 0)
        tcod.console_blit(log_con, 0, 0, CAMERA_WIDTH, SCREEN_HEIGHT - CAMERA_HEIGHT, 0, 0, CAMERA_HEIGHT)
        tcod.console_blit(status_con, 0, 0, SCREEN_WIDTH - CAMERA_WIDTH, SCREEN_HEIGHT // 2, 0, CAMERA_WIDTH, 0)
        tcod.console_blit(equip_con, 0, 0, SCREEN_WIDTH - CAMERA_WIDTH, SCREEN_HEIGHT // 2, 0, CAMERA_WIDTH, SCREEN_HEIGHT // 2)
        tcod.console_flush()
        current_map.clear(map_con)

        userInput = handle_keys()

        if gamestate is Gamestates.PLAYER_ROUND and userInput.get('move'):
            dx, dy, = userInput.get('move')
            # if not map.is_blocked(player.x + dx, player.y + dy):
            #     player.move(dx, dy)
            #     if player.x < camera_x + (CAMERA_WIDTH // 2) - CAMERA_BUFFER or player.x > camera_x + (CAMERA_WIDTH // 2) + CAMERA_BUFFER:
            #         camera_x += dx
            #     if player.y < camera_y + (CAMERA_HEIGHT // 2) - CAMERA_BUFFER or player.y > camera_y + (CAMERA_HEIGHT // 2) + CAMERA_BUFFER:
            #         camera_y += dy
            #     map.recompute_fov(map_con, player.x, player.y, 10)
            #     gamestate = Gamestates.OTHER_ROUND
            moved = player.move(dx, dy, current_map)
            if moved:
                if player.x < camera_x + (CAMERA_WIDTH // 2) - CAMERA_BUFFER or player.x > camera_x + (CAMERA_WIDTH // 2) + CAMERA_BUFFER:
                    camera_x += dx
                if player.y < camera_y + (CAMERA_HEIGHT // 2) - CAMERA_BUFFER or player.y > camera_y + (CAMERA_HEIGHT // 2) + CAMERA_BUFFER:
                    camera_y += dy
                current_map.recompute_fov(map_con, player.x, player.y, 10)
                gamestate = Gamestates.OTHER_ROUND

        if userInput.get('exit'):
            return True

        if gamestate is Gamestates.OTHER_ROUND:
            print("Enemies take a turn")
            gamestate = Gamestates.PLAYER_ROUND


if __name__ == '__main__':
    main()
