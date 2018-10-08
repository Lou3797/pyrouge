from entity.components.components import Components
from ui.messages import Message
from entity.entity import RenderOrder


def on_death(entity, char='%', src=None):
    entity.char = char
    entity.solid = False
    entity.render_order = RenderOrder.CORPSE
    entity.remove_component(Components.FIGHTER)
    entity.remove_component(Components.AI)
    entity.remove_component(Components.FOV)
    if src:
        return Message("{0} has killed {1}!".format(src.name.capitalize(), entity.name))
    else:
        return Message("{0} has died!".format(entity.name.capitalize()))
