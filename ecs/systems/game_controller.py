import libtcodpy as tcod
from enum import Enum
from map.map import Map
from ecs.component import Components
from ecs.systems.ai_system import RandomAI
from ecs.systems.command_handler import CommandHandler
from ecs.systems.input_handler import InputHandler
from ecs.systems.movement_system import BasicMovementSystem
from ecs.systems.render_system import RenderSystem
from ecs.systems.camera_system import CameraSystem
from ecs.systems.fov_system import FOVSystem
from ui.game_window import GameWindow
from ecs.systems.command_handler import Commands


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
        SCREEN_WIDTH, SCREEN_HEIGHT  = 96, 54
        VIEW_WIDTH, VIEW_HEIGHT = 70, 36

        self.gamestate = Gamestates.PLAYER_ROUND
        self.map = Map(96, 54)
        xo, yo = self.map.generate_map(6, 10, 30)
        # Systems
        self.input = InputHandler()
        self.camera = CameraSystem(xo, yo, VIEW_WIDTH, VIEW_HEIGHT, 2)
        self.window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, VIEW_WIDTH, VIEW_HEIGHT)
        self.render = RenderSystem(self.window.map_con)
        self.ai = RandomAI()
        self.fov = FOVSystem()
        self.movement = BasicMovementSystem()
        self.cmd = CommandHandler(self)
        self.update_observers()
        self.current_control_index = 0

    def update(self):
        input = self.input.capture_input(self.get_control())

        if input and self.gamestate is Gamestates.PLAYER_ROUND:
            if self.get_control():
                print(input)
                valid_command = self.cmd.execute_command(input)
                if valid_command:
                    print("ASS")
                    self.fov.recompute_all_entity_fovs()
                    self.increment_control()
                    self.camera.center_on_entity(self.get_control())
                    self.draw(self.get_control())

        if self.gamestate is Gamestates.OTHER_ROUND:
        # TODO: make it so enemies must take a valid command in order to proceed
            command_list = self.ai.process()
            for cmd in command_list:
                self.cmd.execute_command(cmd)
            self.gamestate = Gamestates.PLAYER_ROUND

        # if self.gamestate is Gamestates.PLAYER_ROUND:
        #     for subject in self.input.subjects:
        #
        #         self.draw(subject)
        #
        #         valid_command = False
        #         while not valid_command:
        #             valid_command = self.cmd.execute_command(self.input.capture_input(subject))
        #         self.camera.center_on_entity(subject)
        #     self.gamestate = Gamestates.OTHER_ROUND
        #
        # self.fov.recompute_all_entity_fovs()

        return input

    def get_control(self):
        if len(self.input.subjects) > 0:
            return self.input.subjects[self.current_control_index]
        else:
            return None

    def increment_control(self):
        self.current_control_index+=1
        if self.current_control_index >= len(self.input.subjects):
            self.current_control_index = 0
            self.gamestate = Gamestates.OTHER_ROUND

    def update_observers(self):
        self.ai.attach_multiple(self.map.entities)
        self.input.attach_multiple(self.map.entities)
        self.fov.attach_multiple(self.map.entities)

    def draw(self, subject):
        self.render.render_map(self.map, subject.get_component(Components.FOV).fov)
        self.window.draw(self.camera)
        self.render.clear_entities(self.map.entities)