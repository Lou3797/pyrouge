import libtcodpy as tcod


def draw_bar(con, x, y, width, name, value, max, bar_color, back_color):
    bar_width = (value // max) * width

    tcod.console_set_default_background(con, back_color)
    tcod.console_rect(con, x, y, width, 1, False, tcod.BKGND_ADD)

    tcod.console_set_default_background(con, bar_color)
    if bar_width > 0:
        tcod.console_rect(con, x, y, bar_width, 1, False, tcod.BKGND_SCREEN)

    tcod.console_set_default_foreground(con, tcod.white)
    tcod.console_print_ex(con, int(x + width / 2), y, tcod.BKGND_NONE, tcod.CENTER, '{0}: {1}/{2}'.format(name, value, max))
