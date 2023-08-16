import numpy as np

class ControlPoint:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def from_text(cls, text):
        return cls(int(text.split(":")[0]),int(text.split(":")[1]))

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Can only access (0:x) and (1:y)")

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def lengthSquared(self):
        """
        Treat this control point as a vector and get it's length squared
        """
        return self.x ** 2 + self.y ** 2

    def as_ndarray(self):
        return np.array([self.x, self.y])