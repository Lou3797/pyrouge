import libtcodpy as tcod
from ecs.systems.system import System
from ecs.components.component import Components
from ui.messages import Message


class Combat_System(System):
    def __init__(self):
        super().__init__(Components.FIGHTER)
        self.health_system = Health_System()

    def attack(self, attacker, target):
        logs = []
        if self.has_required_components(attacker) and self.health_system.has_required_components(target):
            logs.extend(self.health_system.take_damage(attacker, target, self.roll_damage(attacker)))
        return logs

    def roll_damage(self, attacker):
        return 3


class Health_System(System):
    def __init__(self):
        super().__init__(Components.HITPOINTS)

    def take_damage(self, attacker, target, damage):
        logs = []
        if self.has_required_components(target):
            hp = target.get_component(Components.HITPOINTS)
            if hp.temp_hp > 0:
                hp.temp_hp -= damage
                if hp.temp_hp < 0:
                    hp.cur_hp += hp.temp_hp
                    hp.temp_hp = 0
            else:
                hp.cur_hp -= damage
            logs.append(Message("{0} attacks {1} for {2} HP!".format(
                attacker.name.capitalize(), target.name, str(damage)), tcod.red))
            if hp.cur_hp <= 0:
                hp.cur_hp = 0
                if hp.on_death:
                    logs.append(hp.on_death(target, src=attacker))
                else:
                    logs.append(hp.on_death(target, src=attacker))
        return logs

    # def heal(self, hp):
    #     if self.is_dead():
    #         return Message("{0} cannot be healed.".format(self.owner.name.capitalize()))
    #     else:
    #         self.cur_hp += hp
    #         if self.cur_hp > self.max_hp:
    #             self.cur_hp = self.max_hp
    #         # return Message("{0} heals {1} for {2} HP!".format())
    #         return Message("{0} regains {1} HP!".format(self.owner.name.capitalize(), str(hp)))
    #
    # def temp_health(self, hp, max=None):
    #     if max:
    #         if self.temp_hp >= max:
    #             return
    #         else:
    #             self.temp_hp += hp
    #             if self.temp_hp >= max:
    #                 self.temp_hp = max
    #     else:
    #         self.temp_hp += hp
    #
    # def is_dead(self):
    #     return self.cur_hp <= 0
