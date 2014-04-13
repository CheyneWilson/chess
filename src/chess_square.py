class InvalidSquareException(Exception):
    pass


class Square(object):
    u"""Represents the coordinates of any square on the chess board."""
    def __init__(self, name):
        self.x = ord(name[0].upper()) - ord(u'A') + 1
        self.y = int(name[1])
        self.name = name.upper()
        if Square._isValidSquare(self.x, self.y):
            pass
        else:
            raise InvalidSquareException(
                u"Square ({name}) is not within 8 x 8 board, it must be between A1 and H8".format(name=name)
            )

    @staticmethod
    def createFromCoords(x, y):
        u"""Instanciates a new Square from x, y notation

        returns -- A new instance of a square instance representing this board position.
        """
        if Square._isValidSquare(x, y):
            name = chr(ord(u'A') + x - 1) + str(y)
            return Square(name)
        else:
            raise InvalidSquareException(u"Square coordinates ({x}, {y}) must be between (1, 1) and (8, 8)".format(
                x=x, y=y)
            )

    @staticmethod
    def resetAllSquares():
        u"""Clears all of the pieces in all squares (sets to None)."""
        Square.all_squares = {}

    @property
    def piece(self):
        u"""Returns the piece in this square or None if there is no piece"""
        # TODO: Raise custom exception if _board is none, explaining how to init.
        return Square.all_squares.get(self, None)

    @piece.setter
    def piece(self, value):
        Square.all_squares[self] = value

    def pop(self):
        u"""Removes the current peice from this square and returns it"""
        piece = self.piece
        del Square.all_squares[self]
        return piece

    @staticmethod
    def _isValidSquare(x, y):
        U"""Returns true if the x, and y coordinates are within a chess board (both between 1 and 8)."""
        if 0 < x <= 8 and 0 < y <= 8:
            return True
        else:
            return False

    def isAdjacent(self, square):
        u"""Returns True if two squares are horizontally, vertically or diagonally adjacent (side by side)."""
        if abs(self.x - square.x) <= 1:
            if abs(self.y - square.y) <= 1:
                if self != square:
                    return True
        return False

    def direction(self, to_):
        u"""The direction from this square to to_ is normalized to have x and y components of 0 or 1.

        Normalization involves keeping the ratio of x and y components the same (so the direction is the same,
        but reducing the magnitured of the x and y components to either 1 or 0 each.

        to_     -- Another Square
        returns -- One of (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (1,-1)
                   or if the vector cannot be reduced to one of these None
        """
        x = to_.x - self.x
        y = to_.y - self.y

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

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __ne__(self, other):
        return (self.x, self.y) != (other.x, other.y)

    def __iter__(self):
        return iter([self.x, self.y])

    def __str__(self):
        return self.name

    def __repr__(self):
        return str((self.x, self.y))
