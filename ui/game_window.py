import libtcodpy as tcod
from ecs.systems.render_system import RenderSystem
from ui.message import MessageLog


class GameWindow():
    def __init__(self, screen_w, screen_h, view_w, view_h, fullscreen=False):
        self.fullscreen = fullscreen
        self.screen_w, self.screen_h = screen_w, screen_h
        self.view_w, self.view_h = view_w, view_h
        # Setup Font
        font_filename = 'res/arial12x12.png'
        tcod.console_set_custom_font(font_filename, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

        # Initialize screen
        title = 'Pyrouge'
        self.map_con = tcod.console_new(self.screen_w, self.screen_h)  # This needs to only be as big as the map can be
        self.log_con = tcod.console_new(self.view_w, self.screen_h - self.view_h)
        self.status_con = tcod.console_new(self.screen_w - self.view_w, self.screen_h // 2)
        self.equip_con = tcod.console_new(self.screen_w - self.view_w, self.screen_h // 2)
        tcod.console_init_root(self.screen_w, self.screen_h, title, self.fullscreen)

        tcod.console_print_frame(self.status_con, 0, 0, self.screen_w - self.view_w, self.screen_h // 2, True,
                                 tcod.BKGND_NONE, 'STATUS')
        tcod.console_print_frame(self.equip_con, 0, 0, self.screen_w - self.view_w, self.screen_h // 2, True,
                                 tcod.BKGND_NONE, 'EQUIPMENT')

        self.msg_log = MessageLog(1, self.view_w - 2, self.screen_h - self.view_h - 2)

    def draw(self, camera):
        self.msg_log.draw(self.log_con)
        tcod.console_blit(self.map_con, camera.x, camera.y, camera.width, camera.height, 0, 0, 0)
        tcod.console_blit(self.log_con, 0, 0, self.view_w, self.screen_h - self.view_h, 0, 0, self.view_h)
        tcod.console_blit(self.status_con, 0, 0, self.screen_w - self.view_w, self.screen_h // 2, 0, self.view_w, 0)
        tcod.console_blit(self.equip_con, 0, 0, self.screen_w - self.view_w, self.screen_h // 2, 0, self.view_w, self.screen_h // 2)
        tcod.console_flush()
        tcod.console_clear(self.log_con)

    def draw_map_only(self):
        tcod.console_blit(self.map_con, 0, 0, self.screen_w, self.screen_h, 0, 0, 0)
