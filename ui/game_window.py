import libtcodpy as tcod


class GameWindow():
    def __init__(self):
        self.FULLSCREEN = False
        self.SCREEN_WIDTH = 96  # characters wide
        self.SCREEN_HEIGHT = 54  # characters tall

        self.map_con = tcod.console_new(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

    # def render(self):
    #     tcod.console_set_default_foreground(self.map_con, tcod.white)
    #
    #     # tcod.console_put_char(0, x, y, '@', tcod.BKGND_NONE)
    #     tcod.console_flush()