import libtcodpy as tcod
from ecs.component import Components
from ecs.components.ai import AI_Types
from ecs.system import System, ObserverSystem
from ecs.systems.command_handler import Commands


class Base_AI_System(System):
    def __init__(self):
        super().__init__(Components.AI, Components.MOVABLE, Components.POSITION)

    def map_entities_take_turn(self, map):
        for entity in map.entities:
            self.entity_take_turn(entity, map)

    def entity_take_turn(self, actor, map):
        if self.has_required_components(actor):

            if self.get_ai_type(actor) is AI_Types.RANDOM:
                # actor.get_component(Components.MOVABLE).move(tcod.random_get_int(0, -1, 1),
                #                                                    tcod.random_get_int(0, -1, 1), map)
                # This needs to return an input type that can be recognized by the game
                return
            # actor.get_component(Components.AI).take_turn(actor, map)

    def get_ai_type(self, entity):
        if self.has_required_components(entity):
            return entity.get_component(Components.AI).ai_type


class Target_Based_AI_System(System):
    def __init__(self):
        super().__init__(Components.FOV, Components.AI, Components.MOVABLE, Components.POSITION)
        self.ai_system = Base_AI_System()

    def take_turn(self):
        return


class RandomAI(ObserverSystem):
    def __init__(self):
        super().__init__(Components.AI)

    def process(self):
        commands = []
        for entity in self.subjects:
            dx, dy = tcod.random_get_int(0, -1, 1), tcod.random_get_int(0, -1, 1)
            commands.append({Commands.MOVE: (entity, dx, dy)})
        return commands