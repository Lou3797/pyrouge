from enum import Enum
import libtcodpy as tcod
from map.map import Map
from ecs.component import Components
from ecs.components.ai import AI
from ecs.components.icon import Icon
from ecs.components.movable import Movable
from ecs.components.position import Position
from ecs.components.reads_input import ReadsInput
from ecs.entity import Entity
from ecs.systems.ai_system import RandomAI
from ecs.systems.command_handler import CommandHandler
from ecs.systems.input_handler import InputHandler
from ecs.systems.movement_system import BasicMovementSystem
from ecs.systems.render_system import RenderSystem
from ui.game_window import GameWindow


class Gamestates(Enum):
    MAIN_MENU = 0
    PLAYER_ROUND = 1
    OTHER_ROUND = 2
    PLAYER_DEAD = 3
    INVENTORY = 4
    SHOP = 5
    LOOTING = 6
    TARGETING = 7


class GameController:
    def __init__(self):
        self.gamestate = Gamestates.PLAYER_ROUND
        self.map = Map(96, 54)
        # Systems
        self.input = InputHandler()
        self.window = GameWindow()
        self.render = RenderSystem(self.window.map_con)
        self.ai = RandomAI()
        self.movement = BasicMovementSystem()
        self.cmd = CommandHandler(self)
        self.add_test_entities()
        self.ai.attach_multiple(self.map.entities)
        self.input.attach_multiple(self.map.entities)

    def update(self):
        self.render.start()
        self.render.render_entities(self.map.entities)
        self.render.exit()
        self.render.clear_entities(self.map.entities)

        if self.gamestate is Gamestates.PLAYER_ROUND:
            for subject in self.input.subjects:
                valid_command = False
                while not valid_command:
                    valid_command = self.cmd.execute_command(self.input.capture_input(subject))
        self.gamestate = Gamestates.OTHER_ROUND

        if self.gamestate is Gamestates.OTHER_ROUND:
            # TODO: make it so enemies must take a valid command in order to proceed
            command_list = self.ai.process()
            for cmd in command_list:
                self.cmd.execute_command(cmd)
            self.gamestate = Gamestates.PLAYER_ROUND

    def add_test_entities(self):
        self.map.entities.extend([
            Entity("player", {
                Components.POSITION: Position(2, 2, True),
                Components.ICON: Icon('@'),
                Components.MOVABLE: Movable(),
                Components.READS_INPUT: ReadsInput()
            }),
            Entity("kobold", {
                Components.POSITION: Position(5, 5, True),
                Components.ICON: Icon('k'),
                Components.MOVABLE: Movable(),
                Components.AI: AI()
            }),
            Entity("kobold", {
                Components.POSITION: Position(6, 8, True),
                Components.ICON: Icon('k'),
                Components.MOVABLE: Movable(),
                Components.AI: AI()
            }),
            Entity("wall", {
                Components.POSITION: Position(3, 3, True),
                Components.ICON: Icon('#')
            })
        ])
