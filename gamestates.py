from enum import Enum


class Gamestates(Enum):
    MAIN_MENU = 0
    PLAYER_ROUND = 1
    OTHER_ROUND = 2
    INVENTORY = 3
    SHOP = 4