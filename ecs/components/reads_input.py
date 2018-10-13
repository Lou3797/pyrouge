from ecs.component import *


class Reads_Input(Component):
    def __init__(self, *sources):
        super().__init__(Components.READS_INPUT)
        self.input_sources = []
        self.input_sources.extend(sources)
