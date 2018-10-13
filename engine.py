import libtcodpy as tcod
from ecs.systems.game_controller import GameController


def main():
    gc = GameController()
    ###################################################################################
    # Main Game Loop
    ###################################################################################
    while not tcod.console_is_window_closed():
        gc.update()
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

        # key = tcod.console_check_for_keypress()
        # if key.vk == tcod.KEY_ESCAPE:
        #     return True


if __name__ == '__main__':
    main()
