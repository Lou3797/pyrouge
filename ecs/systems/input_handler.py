import libtcodpy as tcod
from input.commands import Commands
from ecs.component import Components
from ecs.system import ObserverSystem

class InputHandler(ObserverSystem):
    def __init__(self):
        super().__init__(Components.READS_INPUT)

    def capture_input(self, entity):
        key = tcod.console_wait_for_keypress(True)

        if key.vk == tcod.KEY_UP or key.vk == tcod.KEY_KP8:
            return {Commands.MOVE: (entity, 0, -1)}
        elif key.vk == tcod.KEY_DOWN or key.vk == tcod.KEY_KP2:
            return {Commands.MOVE: (entity, 0, 1)}
        elif key.vk == tcod.KEY_LEFT or key.vk == tcod.KEY_KP4:
            return {Commands.MOVE: (entity, -1, 0)}
        elif key.vk == tcod.KEY_RIGHT or key.vk == tcod.KEY_KP6:
            return {Commands.MOVE: (entity, 1, 0)}

        return {}