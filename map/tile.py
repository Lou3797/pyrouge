class Tile:
    """
    A tile on a map. It may or may not be solid, and may or may not block sight.
    """
    def __init__(self, solid, opaque=None):
        self.solid = solid
        # An opaque tile is solid and a transparent one is not solid by default
        if opaque is None:
            self.opaque = solid
        else:
            self.opaque = opaque
        self.explored = False
