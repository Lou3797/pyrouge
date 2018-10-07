#!/usr/bin/env python
import libtcodpy as tcod
from entity.components.ability_scores import Ability_Scores
from entity.components.components import Components
from entity.components.fighter import Fighter
from entity.components.hitpoints import Hitpoints
from entity.entity import Entity, RenderOrder
from gamestates import Gamestates
from input import handle_keys
from map.map import Map
from ui.messages import Message, MessageLog
from ui.bar import draw_bar


def main():
    FULLSCREEN = False
    SCREEN_WIDTH = 96  # characters wide
    SCREEN_HEIGHT = 54  # characters tall
    CAMERA_WIDTH, CAMERA_HEIGHT = 70, 36
    CAMERA_BUFFER = 2

    FOV_ALGO = 0  # default FOV algorithm
    FOV_LIGHT_WALLS = True
    LIGHT_RADIUS = 8

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

    tcod.console_print_frame(status_con, 0, 0, SCREEN_WIDTH - CAMERA_WIDTH, SCREEN_HEIGHT // 2, True, tcod.BKGND_NONE,
                             'STATUS')
    tcod.console_print_frame(equip_con, 0, 0, SCREEN_WIDTH - CAMERA_WIDTH, SCREEN_HEIGHT // 2, True, tcod.BKGND_NONE,
                             'EQUIPMENT')

    current_map = Map(SCREEN_WIDTH, SCREEN_HEIGHT)
    xo, yo = current_map.generate_map(SCREEN_WIDTH, SCREEN_HEIGHT, 6, 10, 30)
    camera_x, camera_y = xo - (CAMERA_WIDTH // 2), yo - (CAMERA_HEIGHT // 2)

    player = Entity(xo, yo, '@', "player", tcod.white, True, RenderOrder.ACTOR, Ability_Scores(dex=14), Hitpoints(30), Fighter())
    current_map.add(player)
    current_map.recompute_fov(map_con, player.x, player.y, LIGHT_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)

    msg_log = MessageLog(1, CAMERA_WIDTH - 2, SCREEN_HEIGHT - CAMERA_HEIGHT - 2)

    gamestate = Gamestates.PLAYER_ROUND

    ###################################################################################
    # Main Game Loop
    ###################################################################################
    while not tcod.console_is_window_closed():
        logs = []

        tcod.console_set_default_foreground(map_con, tcod.white)
        current_map.draw(map_con)
        msg_log.draw(log_con)
        # draw_bar(status_con, 1, 1, 20, "HP", player.get_component(Components.HITPOINTS).cur_hp,
        #          player.get_component(Components.HITPOINTS).max_hp, tcod.dark_green, tcod.dark_red)
        tcod.console_blit(map_con, camera_x, camera_y, CAMERA_WIDTH, CAMERA_HEIGHT, 0, 0, 0)
        tcod.console_blit(log_con, 0, 0, CAMERA_WIDTH, SCREEN_HEIGHT - CAMERA_HEIGHT, 0, 0, CAMERA_HEIGHT)
        tcod.console_blit(status_con, 0, 0, SCREEN_WIDTH - CAMERA_WIDTH, SCREEN_HEIGHT // 2, 0, CAMERA_WIDTH, 0)
        tcod.console_blit(equip_con, 0, 0, SCREEN_WIDTH - CAMERA_WIDTH, SCREEN_HEIGHT // 2, 0, CAMERA_WIDTH, SCREEN_HEIGHT // 2)
        tcod.console_flush()
        # tcod.console_clear(map_con)
        current_map.clear(map_con)
        tcod.console_clear(log_con)
        # tcod.console_clear(status_con)

        userInput = handle_keys()

        if gamestate is Gamestates.PLAYER_ROUND and userInput.get('move'):
            dx, dy, = userInput.get('move')
            moved = player.move(dx, dy, current_map)
            if moved:
                if player.x < camera_x + (CAMERA_WIDTH // 2) - CAMERA_BUFFER or player.x > camera_x + (CAMERA_WIDTH // 2) + CAMERA_BUFFER:
                    camera_x += dx
                if player.y < camera_y + (CAMERA_HEIGHT // 2) - CAMERA_BUFFER or player.y > camera_y + (CAMERA_HEIGHT // 2) + CAMERA_BUFFER:
                    camera_y += dy
                current_map.recompute_fov(map_con, player.x, player.y, LIGHT_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)
                gamestate = Gamestates.OTHER_ROUND
                current_map.sort_entities_by_render_order()

            else:
                entity = current_map.entity_at(player.x + dx, player.y + dy)
                if entity and entity.get_component(Components.HITPOINTS):
                    logs.extend(player.get_component(Components.FIGHTER).attack(entity))
                    gamestate = Gamestates.OTHER_ROUND
                    current_map.sort_entities_by_render_order()

        if player.get_component(Components.HITPOINTS).is_dead():
            gamestate = Gamestates.PLAYER_DEAD

        if gamestate is Gamestates.OTHER_ROUND:
            for entity in current_map.entities:
                if entity.get_component(Components.AI):
                    entity.get_component(Components.AI).take_turn()
            gamestate = Gamestates.PLAYER_ROUND
            current_map.sort_entities_by_render_order()

        if gamestate is Gamestates.PLAYER_DEAD:
            logs.append(Message("You have died!", tcod.red))

        if userInput.get('exit'):
            return True

        msg_log.add_message_log(logs)


if __name__ == '__main__':
    main()
