import libtcodpy as tcod
from ecs.components.component import Components
from ecs.entities.render_order import Render_Order
from ui.messages import Message


def on_death(entity, char='%', color=tcod.red, src=None, visible=True):
    if entity.get_component(Components.CHAR):
        chara = entity.get_component(Components.CHAR)
        chara.char = char
        chara.color = color
        chara.visible = visible
    if entity.get_component(Components.POSITION):
        entity.get_component(Components.POSITION).solid = False

    entity.remove_component(Components.FIGHTER)
    entity.remove_component(Components.AI)
    entity.remove_component(Components.FOV)
    if src:
        return Message("{0} has killed {1}!".format(src.name.capitalize(), entity.name))
    else:
        return Message("{0} has died!".format(entity.name.capitalize()))
