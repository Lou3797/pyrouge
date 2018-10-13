from enum import Enum


class Gamestates(Enum):
    MAIN_MENU = 0
    PLAYER_ROUND = 1
    OTHER_ROUND = 2
    PLAYER_DEAD = 3
    INVENTORY = 4
    SHOP = 5
    LOOTING = 6
    TARGETING = 7

