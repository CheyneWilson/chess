from enum import Enum


class Winner(Enum):
    UNDECIDED = 1
    DRAW = 2
    WHITE = 3
    BLACK = 4

    @staticmethod
    def from_color(color):
        """
        Coverts from the Color enum to Winner Enum
        """
        try:
            return Winner._member_map_[color.name]
        except KeyError:
            raise KeyError("Color {color} in not valid, expected name property to equal BLACK or WHITE.")
