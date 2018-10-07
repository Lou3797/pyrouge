from entity.components.components import Components
from ui.messages import Message


def on_death(entity, src=None):
    entity.char = '%'
    entity.solid = False
    entity.remove_component(Components.FIGHTER)
    if src:
        return Message('{0} has killed {1}!'.format(src.name, entity.name))
    else:
        return Message('{0} has died!'.format(entity.name))
