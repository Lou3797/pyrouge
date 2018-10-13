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


class Input_Handler:
    def __init__(self):
        pass