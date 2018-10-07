from enum import Enum


class Components(Enum):
    ABILITY_SCORES = 0
    HITPOINTS = 1
    INVENTORY = 2
    ITEM = 3
    AI = 4
    FIGHTER = 5
    CORPSE = 6


class Component:
    def __init__(self, id):
        self.id = id
        self.owner = None
