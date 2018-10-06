from entity.components.components import *


class Ability_Scores(Component):
    def __init__(self, str=10, dex=10, con=10, int=10, wis=10, cha=10):
        super().__init__(Components.ABILITY_SCORES)
        self.str = str # Damage dealt using weapons, ability to break things
        self.dex = dex # Damage dealt using weapons, ability to use hands
        self.con = con # Ability to take and recover from damage
        self.int = int # Arcane spellcasting capacity, worldly knowledge
        self.wis = wis # Divine spellcasting capacity, meta-knowledge
        self.cha = cha # Ability to talk to friends and foes
