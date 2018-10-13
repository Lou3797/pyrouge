import libtcodpy as tcod
from ecs.systems.command_handler import Commands
from ecs.component import Components
from ecs.system import ObserverSystem

class InputHandler(ObserverSystem):
    def __init__(self):
        super().__init__(Components.READS_INPUT)

    def capture_input(self, entity):
        key = tcod.console_wait_for_keypress(True)
        # key = tcod.console_check_for_keypress()

        if key.vk == tcod.KEY_UP or key.vk == tcod.KEY_KP8:
            return {Commands.MOVE: (entity, 0, -1)}
        elif key.vk == tcod.KEY_DOWN or key.vk == tcod.KEY_KP2:
            return {Commands.MOVE: (entity, 0, 1)}
        elif key.vk == tcod.KEY_LEFT or key.vk == tcod.KEY_KP4:
            return {Commands.MOVE: (entity, -1, 0)}
        elif key.vk == tcod.KEY_RIGHT or key.vk == tcod.KEY_KP6:
            return {Commands.MOVE: (entity, 1, 0)}

        if key.vk == tcod.KEY_ENTER and key.lalt:
            return {Commands.FULLSCREEN: (not tcod.console_is_fullscreen())}

        elif key.vk == tcod.KEY_ESCAPE:
            return {Commands.EXIT: (True)}

        return {}