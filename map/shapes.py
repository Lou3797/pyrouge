class Rectangle:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return (center_x, center_y)

    def intersect(self, other):
        # returns true if this rectangle intersects with another shape
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)


class Ellipse:
    def __init__(self, x, y, r1, r2=None):
        self.x = x
        self.y = y
        self.r1 = r1
        if r2:
            self.r2 = r2
        else:
            self.r2 = r1


    def center(self):
        return (self.x, self.y)

    def intersect(self, other):
        return True
