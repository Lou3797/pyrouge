import libtcodpy as tcod


# ######################################################################
# User Input
# ######################################################################
def handle_keys():
    key = tcod.console_wait_for_keypress(True)

    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle fullscreen
        tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

    elif key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}  # exit game

    # movement keys
    if key.vk == tcod.KEY_UP or key.vk == tcod.KEY_KP8:
        return {'move': (0, -1)}
    elif key.vk == tcod.KEY_DOWN or key.vk == tcod.KEY_KP2:
        return {'move': (0, 1)}
    elif key.vk == tcod.KEY_LEFT or key.vk == tcod.KEY_KP4:
        return {'move': (-1, 0)}
    elif key.vk == tcod.KEY_RIGHT or key.vk == tcod.KEY_KP6:
        return {'move': (1, 0)}
    elif key.vk == tcod.KEY_KP7:
        return {'move': (-1, -1)}
    elif key.vk == tcod.KEY_KP9:
        return {'move': (1, -1)}
    elif key.vk == tcod.KEY_KP1:
        return {'move': (-1, 1)}
    elif key.vk == tcod.KEY_KP3:
        return {'move': (1, 1)}
    elif key.vk == tcod.KEY_KP5:
        return {'wait': True}

    return {}
