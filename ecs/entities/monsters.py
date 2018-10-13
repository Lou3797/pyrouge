from enum import Enum

import libtcodpy as tcod
from ecs.component import Components
from ecs.components.ability_scores import Ability_Scores
from ecs.components.ai import AI
from ecs.components.icon import Icon
from ecs.components.fighter import Fighter
from ecs.components.fov import FOV
from ecs.components.hitpoints import Hitpoints
from ecs.components.movable import Movable
from ecs.components.position import Position
from ecs.components.reads_input import ReadsInput
from ecs.entities.render_order import Render_Order
from ecs.entity import Entity


class Monsters(Enum):
    PLAYER = 0
    KOBOLD = 1


def generate_monster(map, x, y, id):
    if id is Monsters.PLAYER:
        return Entity("player", {Components.READS_INPUT: ReadsInput(),
                                 Components.POSITION: Position(x, y, True),
                                 Components.ICON: Icon('@', render_order=Render_Order.ACTOR),
                                 Components.MOVABLE: Movable(),
                                 Components.FOV: FOV(map, 8, True, 1),
                                 Components.ABILITY_SCORES: Ability_Scores(),
                                 Components.FIGHTER: Fighter(),
                                 Components.HITPOINTS: Hitpoints(10)})

    if id is Monsters.KOBOLD:
        return Entity("kobold", {Components.POSITION: Position(x, y, True),
                                 Components.ICON: Icon('k', tcod.orange, Render_Order.ACTOR),
                                 Components.MOVABLE: Movable(),
                                 Components.FOV: FOV(map, 10, algorithm=1),
                                 Components.ABILITY_SCORES: Ability_Scores(),
                                 Components.FIGHTER: Fighter(),
                                 Components.HITPOINTS: Hitpoints(8),
                                 Components.AI: AI()})
