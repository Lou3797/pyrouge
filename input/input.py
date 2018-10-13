import libtcodpy as tcod
from enum import Enum


class Commands(Enum):
    EXIT = 0
    MOVE = 1
    WAIT = 2
    ATTACK = 3
    OPEN = 4
    CLOSE = 5
    LOOK = 6
    SEARCH = 7
    # OR DO A PROPER COMMAND CLASS? COMMAND PATTERN, ALL COMMANDS EXTEND COMMAND
    # MOVE_COMMAND()


class Input():
    def __init__(self):
        pass

    def get_input(self):
        pass


class Keyboard(Input):
    def __init__(self):
        super().__init__()

    def get_input(self):
        key = tcod.console_wait_for_keypress(False)

        if key.vk == tcod.KEY_ENTER and key.lalt:
            # Alt+Enter: toggle fullscreen
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        elif key.vk == tcod.KEY_ESCAPE:
            return {Commands.EXIT: True}  # exit game

        # movement keys
        if key.vk == tcod.KEY_UP or key.vk == tcod.KEY_KP8:
            return {Commands.MOVE: (0, -1)}
        elif key.vk == tcod.KEY_DOWN or key.vk == tcod.KEY_KP2:
            return {Commands.MOVE: (0, 1)}
        elif key.vk == tcod.KEY_LEFT or key.vk == tcod.KEY_KP4:
            return {Commands.MOVE: (-1, 0)}
        elif key.vk == tcod.KEY_RIGHT or key.vk == tcod.KEY_KP6:
            return {Commands.MOVE: (1, 0)}
        elif key.vk == tcod.KEY_KP7:
            return {Commands.MOVE: (-1, -1)}
        elif key.vk == tcod.KEY_KP9:
            return {Commands.MOVE: (1, -1)}
        elif key.vk == tcod.KEY_KP1:
            return {Commands.MOVE: (-1, 1)}
        elif key.vk == tcod.KEY_KP3:
            return {Commands.MOVE: (1, 1)}
        elif key.vk == tcod.KEY_KP5:
            return {Commands.WAIT: True}

        return {}


class Gamepad(Input):
    def __init__(self):
        super().__init__()

    def get_input(self):
        return {}
