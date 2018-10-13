from ecs.systems.input_handler import Commands


class CommandHandler:
    def __init__(self, game_controller):
        self.gc = game_controller
        pass

    def execute_command(self, dict):
        if dict.get(Commands.MOVE):
            entity, dx, dy = dict.get(Commands.MOVE)
            return self.gc.movement.move(entity, dx, dy, self.gc.map)
