from cmd.command import Command


class MoveCommand(Command):
    def __init__(self, entity, dx, dy):
        super().__init__()
        self.entity = entity
        self.dx = dx
        self.dy = dy

    def execute(self):
        print("move the character " + str(self.dx) + ", " + str(self.dy))
        return True
