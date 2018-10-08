import libtcodpy as tcod
from ecs.entities.render_order import Render_Order
from ecs.components.component import *


class Char(Component):
    def __init__(self, char, color=tcod.white, render_order=Render_Order.DECAL, visible=True):
        super().__init__(Components.CHAR)
        self.char = char
        self.color = color
        self.render_order = render_order
        self.visible = visible
