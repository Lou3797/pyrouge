import libtcodpy as tcod
from enum import Enum
from entity.entity import Entity, RenderOrder
from entity.components.ability_scores import Ability_Scores
from entity.components.ai import BasicMonster
from entity.components.fighter import Fighter
from entity.components.fov import FOV
from entity.components.hitpoints import Hitpoints
from entity.components.inventory import Inventroy
from entity.components.item import Item
from entity.components.movable import Movable

class Monsters(Enum):
    KOBOLD = 0


def generate_monster(map, x, y, id):
     if id is Monsters.KOBOLD:
         return Entity(x, y, "k", "kobold", tcod.dark_orange, True,
                       RenderOrder.ACTOR, Hitpoints(8), BasicMonster(), FOV(map, 10), Movable())
