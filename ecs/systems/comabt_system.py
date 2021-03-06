import libtcodpy as tcod
from ecs.component import Components
from ecs.system import System
from ui.message import Message


class Combat_System(System):
    def __init__(self):
        super().__init__(Components.FIGHTER)
        self.health_system = Health_System()

    def attack(self, attacker, target):
        logs = []
        if self.has_required_components(attacker) and self.health_system.has_required_components(target):
            if not self.health_system.is_dead(target):
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

    def heal(self, entity, hp):
        if self.has_required_components(Components.HITPOINTS):
            health = entity.get_component(Components.HITPOINTS)
            if self.is_dead(entity):
                return Message("{0} cannot be healed.".format(entity.name.capitalize()))
            else:
                health.cur_hp += hp
                if health.cur_hp > health.max_hp:
                    health.cur_hp = health.max_hp
                return Message("{0} regains {1} HP!".format(entity.name.capitalize(), str(hp)))

    def temp_health(self, entity, hp, max=None):
        if self.has_required_components(Components.HITPOINTS):
            health = entity.get_component(Components.HITPOINTS)
            if max:
                if health.temp_hp >= max:
                    return
                else:
                    health.temp_hp += hp
                    if health.temp_hp >= max:
                        health.temp_hp = max
            else:
                health.temp_hp += hp

    def is_dead(self, entity):
        if self.has_required_components(entity):
            return entity.get_component(Components.HITPOINTS).cur_hp <= 0
