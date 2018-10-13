from enum import Enum

import libtcodpy as tcod
from cmd.command import Commands
from cmd.invoker import Invoker
from ecs.component import Components
from ecs.components.icon import Icon
from ecs.components.position import Position
from ecs.entity import Entity
from ecs.system import ObserverSystem
from ecs.systems.render_system import RenderSystem
from ui.game_window import GameWindow
from ecs.components.movable import Movable
from ecs.components.ai import AI
from ecs.systems.movement_system import BasicMovementSystem


class Gamestates(Enum):
    MAIN_MENU = 0
    PLAYER_ROUND = 1
    OTHER_ROUND = 2
    PLAYER_DEAD = 3
    INVENTORY = 4
    SHOP = 5
    LOOTING = 6
    TARGETING = 7


class SampleInputHandler:
    def __init__(self):
        pass

    def capture_input(self):
        key = tcod.console_wait_for_keypress(True)

        if key.vk == tcod.KEY_UP or key.vk == tcod.KEY_KP8:
            return {Commands.MOVE: (0, -1)}
        elif key.vk == tcod.KEY_DOWN or key.vk == tcod.KEY_KP2:
            return {Commands.MOVE: (0, 1)}
        elif key.vk == tcod.KEY_LEFT or key.vk == tcod.KEY_KP4:
            return {Commands.MOVE: (-1, 0)}
        elif key.vk == tcod.KEY_RIGHT or key.vk == tcod.KEY_KP6:
            return {Commands.MOVE: (1, 0)}

        return {}


class SampleCommandHandler:
    def __init__(self):
        pass

    def get_command(self, dict):
        for k, v in dict.items():
            entity = k
            if v.get(Commands.MOVE):
                dx, dy = v.get(Commands.MOVE)
                temp = BasicMovementSystem()
                # print("GOT:", entity, dx, dy)
                temp.move(entity, dx, dy)



class SampleAI(ObserverSystem):
    def __init__(self):
        super().__init__(Components.AI)

    def process(self):
        commands = []
        for entity in self.subjects:
            commands.append({entity: {Commands.MOVE: (1, 0)}})

        return commands


class GameController:
    def __init__(self):
        self.invoker = Invoker()
        self.gamestate = Gamestates.PLAYER_ROUND
        self.io = SampleInputHandler()
        self.cmd = SampleCommandHandler()
        self.window = GameWindow()
        self.render = RenderSystem(self.window.map_con)
        self.entities = []
        self.entities.append(Entity("player", {Components.POSITION: Position(0, 0),
                                               Components.ICON: Icon('@')}))
        self.entities.append(Entity("kobold1", {Components.POSITION: Position(3, 1),
                                                Components.ICON: Icon('1'),
                                                Components.AI: AI(),
                                                Components.MOVABLE: Movable()
                                                }))
        self.entities.append(Entity("kobold2", {Components.POSITION: Position(5, 5),
                                                Components.ICON: Icon('2'),
                                                Components.AI: AI(),
                                                Components.MOVABLE: Movable()
                                                }))
        self.ai = SampleAI()
        self.ai.attach_multiple(self.entities)
        self.movement = BasicMovementSystem()

    def update(self):
        self.render.start()
        self.render.render_entities(self.entities)
        self.render.exit()
        self.render.clear_entities(self.entities)

        if self.gamestate is Gamestates.PLAYER_ROUND:
            tcod.console_wait_for_keypress(True)
            self.gamestate = Gamestates.OTHER_ROUND
            # logs.extend(gc.handle_input())
            # ---
            # cmd = self.cmd.get_command(self.io.capture_input())
            # change to add controllable entity that called it
            # cmd = self.cmd.get_command( {entity: self.io.capture_input()} )
            # if cmd:
            #     self.invoker.execute(cmd)
            #     self.gamestate = Gamestates.OTHER_ROUND
            # ---
            #print(self.io.capture_input())
        if self.gamestate is Gamestates.OTHER_ROUND:
            # logs.extend(gc.execute_ai())
            # self.invoker.execute(self.ai.process())
            command_list = self.ai.process()
            print("Command list", command_list)
            for cmd in command_list:
                self.cmd.get_command(cmd)

            self.gamestate = Gamestates.PLAYER_ROUND
