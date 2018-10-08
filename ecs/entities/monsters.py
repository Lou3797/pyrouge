from enum import Enum

import libtcodpy as tcod
from ecs.components.component import Components
from ecs.components.ai import BasicMonster
from ecs.components.fov import FOV
from ecs.components.hitpoints import Hitpoints
from ecs.components.fighter import Fighter
from ecs.components.ability_scores import Ability_Scores
from ecs.components.movable import Movable
from ecs.components.char import Char
from ecs.components.position import Position
from ecs.entities.entity import Entity
from ecs.entities.render_order import Render_Order
from ecs.systems.death_functions import on_death


class Monsters(Enum):
    PLAYER = 0
    KOBOLD = 1


def generate_monster(map, x, y, id):
    if id is Monsters.PLAYER:
        return Entity("player", {Components.POSITION: Position(x, y, True),
                                 Components.CHAR: Char('@', render_order=Render_Order.ACTOR),
                                 Components.MOVABLE: Movable(),
                                 Components.FOV: FOV(map, 8, True, 2),
                                 Components.ABILITY_SCORES: Ability_Scores(),
                                 Components.FIGHTER: Fighter(),
                                 Components.HITPOINTS: Hitpoints(10)})

    if id is Monsters.KOBOLD:
        return Entity("kobold", {Components.POSITION: Position(x, y, True),
                                 Components.CHAR: Char('k', tcod.orange, Render_Order.ACTOR),
                                 Components.MOVABLE: Movable(),
                                 Components.FOV: FOV(map, 10, algorithm=2),
                                 Components.ABILITY_SCORES: Ability_Scores(),
                                 Components.FIGHTER: Fighter(),
                                 Components.HITPOINTS: Hitpoints(8),
                                 Components.AI: BasicMonster()})
