import collections


class Square(collections.namedtuple('Square', ['x', 'y'])):
    u"""Represents the coordinates of any square on the chess board."""
    @property
    def name(self):
        u"""Returns the letter and number notation of the square, like E4 for Square(4,5)."""
        return chr(ord(u'A') + self.x - 1) + str(self.y)

    @classmethod
    def fromName(cls, name):
        u"""Instanciates a new Square from letter and number notation.

        name -- A string ranging from A1 to H8
        returns -- A new instance of a square instance representing this board position.
        """
        x = ord(name[0].upper()) - ord(u'A') + 1
        y = int(name[1])
        return Square(x, y)
