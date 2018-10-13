from ecs.component import Components
from ecs.system import System


class CameraSystem(System):
    def __init__(self, x, y, width, height, buffer=0):
        super().__init__(Components.POSITION)
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.buffer = buffer
        self.center_on_coordinates(x, y)

    def follow(self, entity, dx, dy):
        if self.has_required_components(entity):
            pos = entity.get_component(Components.POSITION)
            if pos.x < self.x + (self.width // 2) - self.buffer or pos.x > self.x + (self.width // 2) + self.buffer:
                self.x += dx
            if pos.y < self.y + (self.height // 2) - self.buffer or pos.y > self.y + (self.height // 2) + self.buffer:
                self.y += dy

    def center_on_coordinates(self, x, y):
        self.x, self.y = x - (self.width // 2), y - (self.height // 2)

    def center_on_entity(self, entity):
        if self.has_required_components(entity):
            pos = entity.get_component(Components.POSITION)
            self.x, self.y = pos.x - (self.width // 2), pos.y - (self.height // 2)
