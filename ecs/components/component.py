from enum import Enum


class Components(Enum):
    ABILITY_SCORES = 0
    HITPOINTS = 1
    INVENTORY = 2
    ITEM = 3
    AI = 4
    FIGHTER = 5
    CORPSE = 6
    FOV = 7
    MOVABLE = 8
    READS_INPUT = 9
    POSITION = 10
    CHAR = 11


class Component:
    def __init__(self, id):
        self.id = id
        self.owner = None
