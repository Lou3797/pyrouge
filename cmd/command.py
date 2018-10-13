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


class Command:
    def __init__(self):
        pass

    def execute(self):
        print("A vague action cannot be done")
        return False