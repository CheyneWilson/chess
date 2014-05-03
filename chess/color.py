from enum import Enum


class Color(Enum):
    WHITE = 1
    BLACK = 2

    @staticmethod
    def decode(code):
        """Creates a new Color instance based off the color code. Used for serialization."""
        if code == 'B':
            return Color.BLACK
        elif code == 'W':
            return Color.WHITE
        raise ValueError("Invalid color code '{0}.".format(code))

    def inverse(self):
        if self is Color.BLACK:
            return Color.WHITE
        elif self is Color.WHITE:
            return Color.BLACK
        assert(False, "Should not be able to end up here")

    def code(self):
        """Retuns the Color mapped to the code. Used with one of the serialaztion methods."""
        if self == Color.BLACK:
            return 'B'
        elif self == Color.WHITE:
            return 'W'
        assert(False, "Should not be able to end up here")
