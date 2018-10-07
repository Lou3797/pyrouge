import libtcodpy as tcod
import textwrap


class Message:
    def __init__(self, text, color=tcod.white):
        self.text = text
        self.color = color


class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    def add_message_log(self, message_log):
        for msg in message_log:
            self.add_message(msg)

    def add_message(self, message):
        # Split the message if necessary, among multiple lines
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            # If the buffer is full, remove the first line to make room for the new one
            if len(self.messages) == self.height:
                del self.messages[0]

            # Add the new line as a Message object, with the text and the color
            self.messages.append(Message(line, message.color))

    def draw(self, con, border=True):
        if border:
            tcod.console_set_default_foreground(con, tcod.white)
            tcod.console_print_frame(con, 0, 0, self.width + 2, self.height + 2, True, tcod.BKGND_NONE, 'MESSAGE LOG')
        y = 1
        for message in self.messages:
            tcod.console_set_default_foreground(con, message.color)
            tcod.console_print_ex(con, self.x, y, tcod.BKGND_NONE, tcod.LEFT, message.text)
            y += 1
