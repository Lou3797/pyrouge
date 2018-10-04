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
    if tcod.console_is_key_pressed(tcod.KEY_UP):
        return {'move': (0, -1)}

    elif tcod.console_is_key_pressed(tcod.KEY_DOWN):
        return {'move': (0, 1)}

    elif tcod.console_is_key_pressed(tcod.KEY_LEFT):
        return {'move': (-1, 0)}

    elif tcod.console_is_key_pressed(tcod.KEY_RIGHT):
        return {'move': (1, 0)}

    return {}
