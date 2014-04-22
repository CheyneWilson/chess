class InvalidSquareException(Exception):
    pass


class Square(object):
    u"""Represents the coordinates of any square on the chess board."""
    def __init__(self, name):
        self.name = name.upper()
        self.x, self.y = Square.coordsFromName(self.name)
        self.piece = None
        if Square._isValidSquare(self.x, self.y):
            pass
        else:
            raise InvalidSquareException(
                u"Square ({name}) is not within 8 x 8 board, it must be between A1 and H8".format(name=name)
            )

    @staticmethod
    def nameFromCoords(x, y):
        u"""Maps x,y coordinates like A4 to x,y coordinates like (1, 4).

        The white player starts on rows with y values 1, and 2, while the black players pieces start on rows 7 and 8.
        x coordinates increment left to right.

        x  --  The square from left to right
        y  --  The square from bottom to top, starting from white players side

        Returns  -- The name of the square
        Raises   -- InvalidSquareException if the square is not on the chess board

        """
        if 1 <= x <= 8 and 1 <= y <= 8:
            name = chr(ord(u'A') + x - 1) + str(y)
            return name
        else:
            raise InvalidSquareException(
                "The square ({x}, {y}), does not exist on a chess board. X and Y must be between 1 and 8 (inclusive).".
                format(x=x, y=y)
            )

    @staticmethod
    def coordsFromName(name):
        u"""Maps square names like H6 to x,y coordinates like (8, 6)

        The white player starts on rows with y values 1, and 2, while the black players pieces start on rows 7 and 8.
        x coordinates increment left to right.

        name    -- The name of the Square
        Returns -- x, y coordinates of this square
        Raises  -- InvalidSquareException if the square is not on the chess board

        """
        x = ord(name[0].upper()) - ord(u'A') + 1
        y = int(name[1])

        if 1 <= x <= 8 and 1 <= y <= 8:
            return x, y
        else:
            raise InvalidSquareException(
                "The square {name}, does not exist on a chess board. ".format(name=name)
            )

    def pop(self):
        u"""Removes the current peice from this square and returns it"""
        piece = self.piece
        self.piece = None
        return piece

    @staticmethod
    def _isValidSquare(x, y):
        U"""Returns true if the x, and y coordinates are within a chess board (both between 1 and 8)."""
        if 0 < x <= 8 and 0 < y <= 8:
            return True
        else:
            return False

    def isAdjacent(self, square_name):
        u"""Returns True if two squares are horizontally, vertically or diagonally adjacent (side by side)."""
        if self.name != square_name:
            x, y = self.coordsFromName(square_name)
            if abs(self.x - x) <= 1:
                if abs(self.y - y) <= 1:
                    return True
        return False

    def direction(self, to_):
        u"""The direction from this square to to_ is normalized to have x and y components of 0 or 1.

        Normalization involves keeping the ratio of x and y components the same (so the direction is the same,
        but reducing the magnitured of the x and y components to either 1 or 0 each.

        to_     -- The name of another Square
        returns -- One of (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (1,-1)
                   or if the vector cannot be reduced to one of these None
        """
        to_square = Square(to_)
        x = to_square.x - self.x
        y = to_square.y - self.y

        if x == 0:
            y = y / abs(y)
        elif y == 0:
            x = x / abs(x)
        elif abs(x) == abs(y):
            x = x / abs(x)
            y = y / abs(y)
        else:
            # Can't be normalized (ratio)
            return None
        return (x, y)
