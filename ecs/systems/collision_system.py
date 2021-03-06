# from ecs.systems.system import System
# from ecs.components.component import Components
#
#
# class Collision_System(System):
#     def __init__(self):
#         super().__init__(Components.POSITION)
#
#     def is_blocked_at_entity_projection(self, map, entity, dx, dy):
#         if self.has_required_components(entity):
#             pos = entity.get_component(Components.POSITION)
#             return self.is_blocked_at(map, pos.x + dx, pos.y + dy)
#         return False
#
#     def is_blocked_at(self, map, x, y):
#         # first test the map tile
#         if map.tiles[x][y].solid:
#             return True
#         # now check for any blocking objects
#         for entity in map.entities:
#             if self.has_required_components(entity):
#                 pos = entity.get_component(Components.POSITION)
#                 if pos.solid and pos.x == x and pos.y == y:
#                     return True
#         return False
#
#     def entities_at_projection(self, map, entity, dx, dy):
#         if self.has_required_components(entity):
#             pos = entity.get_component(Components.POSITION)
#             return self.entities_at(map, pos.x + dx, pos.y + dy)
#         return []
#
#     def entities_at(self, map, x, y):
#         entities = []
#         for entity in map.entities:
#             if self.has_required_components(entity):
#                 pos = entity.get_component(Components.POSITION)
#                 if pos.x == x and pos.y == y:
#                     entities.append(entity)
#         return entities
