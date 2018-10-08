import libtcodpy as tcod
from ecs.components.ability_scores import Ability_Scores
from ecs.components.component import Components
from ecs.components.fighter import Fighter
from ecs.components.fov import FOV
from ecs.components.hitpoints import Hitpoints
from ecs.components.movable import Movable
from ecs.entities.monsters import generate_monster, Monsters
from ecs.entities.entity import Entity
from ecs.systems.camera_system import Camera_System
from ecs.systems.render_system import Render_System
from ecs.systems.fov_system import FOV_System
from ecs.systems.movement_system import Basic_Movement_System, FOV_Movement_System
from gamestates import Gamestates
from input import handle_keys
from map.map import Map
from ui.messages import Message, MessageLog


def main():
    FULLSCREEN = False
    SCREEN_WIDTH = 96  # characters wide
    SCREEN_HEIGHT = 54  # characters tall
    CAMERA_WIDTH, CAMERA_HEIGHT = 70, 36
    CAMERA_BUFFER = 2

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
    # camera_x, camera_y = xo - (CAMERA_WIDTH // 2), yo - (CAMERA_HEIGHT // 2)
    camera = Camera_System(xo, yo, CAMERA_WIDTH, CAMERA_HEIGHT, CAMERA_BUFFER)

    player = generate_monster(current_map, xo, yo, Monsters.PLAYER)
    current_map.add(player)

    msg_log = MessageLog(1, CAMERA_WIDTH - 2, SCREEN_HEIGHT - CAMERA_HEIGHT - 2)

    map_renderer = Render_System(map_con)
    fov_renderer = FOV_System()
    fov_renderer.recompute_single_entity_fov(player)
    basic_movement = Basic_Movement_System()

    gamestate = Gamestates.PLAYER_ROUND

    ###################################################################################
    # Main Game Loop
    ###################################################################################
    while not tcod.console_is_window_closed():
        logs = []

        tcod.console_set_default_foreground(map_con, tcod.white)
        map_renderer.render_map(current_map, player.get_component(Components.FOV).fov)
        msg_log.draw(log_con)
        tcod.console_blit(map_con, camera.x, camera.y, CAMERA_WIDTH, CAMERA_HEIGHT, 0, 0, 0)
        tcod.console_blit(log_con, 0, 0, CAMERA_WIDTH, SCREEN_HEIGHT - CAMERA_HEIGHT, 0, 0, CAMERA_HEIGHT)
        tcod.console_blit(status_con, 0, 0, SCREEN_WIDTH - CAMERA_WIDTH, SCREEN_HEIGHT // 2, 0, CAMERA_WIDTH, 0)
        tcod.console_blit(equip_con, 0, 0, SCREEN_WIDTH - CAMERA_WIDTH, SCREEN_HEIGHT // 2, 0, CAMERA_WIDTH, SCREEN_HEIGHT // 2)
        tcod.console_flush()
        map_renderer.clear_entities(current_map)
        tcod.console_clear(log_con)

        userInput = handle_keys()

        if gamestate is Gamestates.PLAYER_ROUND and userInput.get('move'):
            dx, dy, = userInput.get('move')
            moved = basic_movement.move(player, dx, dy, current_map)
            if moved:
                camera.follow(player, dx, dy)
                fov_renderer.recompute_single_entity_fov(player)

                # if player.get_component(Components.MOVABLE):
            #     moved = player.get_component(Components.MOVABLE).move(dx, dy, current_map)
            #     if moved:
            #         if player.x < camera_x + (CAMERA_WIDTH // 2) - CAMERA_BUFFER or player.x > camera_x + (
            #             CAMERA_WIDTH // 2) + CAMERA_BUFFER:
            #             camera_x += dx
            #         if player.y < camera_y + (CAMERA_HEIGHT // 2) - CAMERA_BUFFER or player.y > camera_y + (
            #             CAMERA_HEIGHT // 2) + CAMERA_BUFFER:
            #             camera_y += dy
            #         # player.get_component(Components.FOV).recompute_fov()
            #         current_map.recompute_entity_fovs()
            #         gamestate = Gamestates.OTHER_ROUND
            #         # THIS IS NOT EFFICIENT AND SHOULD CHANGE. ONLY A MOVING ENTITY NEEDS TO UPDATE ITS FOV
            #         current_map.sort_entities_by_render_order()
            #
            #     else:
            #         entities = current_map.entities_at(player.x + dx, player.y + dy)
            #         for entity in entities:
            #             if entity.get_component(Components.HITPOINTS):
            #                 if not entity.get_component(Components.HITPOINTS).is_dead():
            #                     logs.extend(player.get_component(Components.FIGHTER).attack(entity))
            #                     gamestate = Gamestates.OTHER_ROUND
            #                     current_map.sort_entities_by_render_order()

        if userInput.get('wait'):
            gamestate = Gamestates.OTHER_ROUND

        # if player.get_component(Components.HITPOINTS).is_dead():
        #     gamestate = Gamestates.PLAYER_DEAD

        if gamestate is Gamestates.OTHER_ROUND:
            # for entity in current_map.entities:
            #     if entity.get_component(Components.AI):
            #         entity.get_component(Components.AI).take_turn(player, current_map)
            # current_map.sort_entities_by_render_order()
            gamestate = Gamestates.PLAYER_ROUND

        if gamestate is Gamestates.PLAYER_DEAD:
            logs.append(Message("You have died!", tcod.red))

        if userInput.get('exit'):
            return True

        msg_log.add_message_log(logs)


if __name__ == '__main__':
    main()
