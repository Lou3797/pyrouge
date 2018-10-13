import libtcodpy as tcod
from ecs.systems.game_controller import GameController
from ecs.systems.gamestates import Gamestates
from ui.message import MessageLog


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

    # current_map = Map(SCREEN_WIDTH, SCREEN_HEIGHT)
    # xo, yo = current_map.generate_map(SCREEN_WIDTH, SCREEN_HEIGHT, 6, 10, 30)
    # camera = Camera_System(xo, yo, CAMERA_WIDTH, CAMERA_HEIGHT, CAMERA_BUFFER)
    # player = generate_monster(current_map, xo, yo, Monsters.PLAYER)
    # p1_input = Input_Handler(player)
    # current_map.add(player)

    gc = GameController()

    # msg_log = MessageLog(1, CAMERA_WIDTH - 2, SCREEN_HEIGHT - CAMERA_HEIGHT - 2)

    # map_renderer = Render_System(map_con)
    # fov_renderer = FOV_System()
    # # fov_renderer.recompute_all_entity_fovs(current_map)
    # basic_movement = Basic_Movement_System()
    # combat_system = Combat_System()
    # ai_controller = Base_AI_System()

    ###################################################################################
    # Main Game Loop
    ###################################################################################
    x,y, = 0,0
    while not tcod.console_is_window_closed():
        # logs = []

        # map_renderer.render_map(current_map, player.get_component(Components.FOV).fov)
        # msg_log.draw(log_con)
        # tcod.console_blit(map_con, camera.x, camera.y, camera.width, camera.height, 0, 0, 0)
        # tcod.console_blit(log_con, 0, 0, CAMERA_WIDTH, SCREEN_HEIGHT - CAMERA_HEIGHT, 0, 0, CAMERA_HEIGHT)
        # tcod.console_blit(status_con, 0, 0, SCREEN_WIDTH - CAMERA_WIDTH, SCREEN_HEIGHT // 2, 0, CAMERA_WIDTH, 0)
        # tcod.console_blit(equip_con, 0, 0, SCREEN_WIDTH - CAMERA_WIDTH, SCREEN_HEIGHT // 2, 0, CAMERA_WIDTH, SCREEN_HEIGHT // 2)
        # tcod.console_flush()
        # map_renderer.clear_entities(current_map)
        # tcod.console_clear(log_con)

        gc.update()

        # tcod.console_put_char(0, x, y, '@', tcod.BKGND_NONE)
        # tcod.console_flush()
        # x+=1
        # y+=1




        # input = p1_input.handle_input()
        #
        # if gamestate is Gamestates.PLAYER_ROUND and input.get(Commands.MOVE):
        #     dx, dy = input.get(Commands.MOVE)
        #     moved = basic_movement.move(player, dx, dy, current_map)
        #     if moved:
        #         camera.follow(player, dx, dy)
        #         fov_renderer.recompute_all_entity_fovs(current_map)
        #         gamestate = Gamestates.OTHER_ROUND
        #     else:
        #         entities = basic_movement.collision_system.entities_at_projection(current_map, player, dx, dy)
        #         for entity in entities:
        #             logs.extend(combat_system.attack(player, entity))
        #
        #             gamestate = Gamestates.OTHER_ROUND
        # if input.get(Commands.WAIT):
        #     gamestate = Gamestates.OTHER_ROUND
        # if combat_system.health_system.is_dead(player):
        #     gamestate = Gamestates.PLAYER_DEAD





        # if input.get(Commands.EXIT):
        #     return True

        # msg_log.add_message_log(logs)

        key = tcod.console_check_for_keypress()
        if key.vk == tcod.KEY_ESCAPE:
            return True


if __name__ == '__main__':
    main()
