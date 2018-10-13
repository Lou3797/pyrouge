from ecs.entity import Entity
from ecs.component import Components, Component
from ecs.system import System, ObserverSystem
from ecs.components.position import Position
from ecs.components.icon import Icon
from ecs.components.movable import Movable


class TestObersverSystem(ObserverSystem):
    def __init__(self):
        super().__init__(Components.POSITION, Components.MOVABLE)

    def process(self):
        return


char1 = Entity("test1", {
    Components.POSITION: Position(0, 0),
    Components.MOVABLE: Movable()
})
char2 = Entity("test2", {
    Components.POSITION: Position(0, 0),
    # Components.MOVABLE: Movable()
})
char3 = Entity("test3", {
    # Components.POSITION: Position(0, 0),
    # Components.MOVABLE: Movable()
})
chars = [char1, char2, char3]
sys = TestObersverSystem()
def report(text):
    print("=========", text, "=========")
    print("System Subjects:", sys.subjects)
    for char in chars:
        print("Observers for", char.name, ":", char.observers)

report("START")

sys.attach_multiple(chars)
report("ATTACH MULTIPLE")

sys.attach_one(char2)
report("ATTEMPT TO ADD MANUALLY IMPROPER ENTITY")

char2.add_component(Components.MOVABLE, Movable())
sys.attach_one(char2)
report("CHAR2 GIVEN MOVABLE")

sys.attach_multiple(chars)
report("ATTEMPT TO ADD ALL AGAIN")

char1.remove_component(Components.POSITION)
report("AFTER REMOVING POSITION FROM CHAR1")