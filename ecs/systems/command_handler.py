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
    FULLSCREEN = 8


class CommandHandler:
    def __init__(self, game_controller):
        self.gc = game_controller
        pass

    def execute_command(self, dict):
        if dict.get(Commands.MOVE):
            entity, dx, dy = dict.get(Commands.MOVE)
            return self.gc.movement.move(entity, dx, dy, self.gc.map)
