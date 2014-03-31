from chess_color2 import Color
from chess_square import Square


class Piece(object):
    symbol = u'?'
    simple_simbol = u'?'  # Used in JSON representation
    color = None
    # A numerical limit to the number of squares this piece can move in
    # If none then it can move an unlimted amount in a direction
    limit = None
    value = None  # Tradional chess values - used to determince some statemate
    has_moved = False

    def __str__(self):
        u"""Return a utf-8 encoded string representation of this chess piece."""
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        u"""Return the unicode string representation of this chess piece."""
        return self.symbol

    def move(self, location):
        u"""Move a piece to the location specified. Does not check if this is a legal chess move. """
        self.has_moved = True
        self.location = location

    def get_limit(self):
        return self.limit

    @classmethod
    def get_piece_class(cls, symbol):
        u"""Returns class the piece identified by its unicode symbol
           Raises a ValueError if the code is invalid.
        """
        for cls in Piece.__subclasses__():
            if cls.symbol == symbol:
                return cls

        raise ValueError()


class King(object):
    u"""The King chess piece.

    This should not be created directly, instead a BlackKing or WhiteKing
    should be instanciated.
    """
    attacks = frozenset([(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)])  # x,y
    limit = 1  # The King may only move one place via his move vectors
    has_moved = False
    value = 0

    def __new__(cls, *args, **kwargs):
        if cls is King:
            raise TypeError(u"King class may not be instantiated.")
        return object.__new__(cls, *args, **kwargs)


class WhiteKing(King, Piece):
    u"""The White King chess piece."""
    symbol = u'\u2654'
    simple_simbol = u'WK'
    name = u'white_king'
    color = Color.white

    def __init__(self, has_moved=False):
        self.has_moved = has_moved


class BlackKing(King, Piece):
    u"""The Black King chess piece."""
    symbol = u'\u265a'
    simple_simbol = u'BK'
    name = u'black_king'
    color = Color.black

    def __init__(self, has_moved=False):
        self.has_moved = has_moved


class Queen(object):
    u"""The Queen chess piece.

    This should not be created directly, instead a BlackQueen or WhiteQueen
    should be instanciated.
    """
    attacks = frozenset([(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)])  # x,y
    value = 9

    def __new__(cls, *args, **kwargs):
        if cls is Queen:
            raise TypeError(u"Queen class may not be instantiated.")
        return object.__new__(cls, *args, **kwargs)


class WhiteQueen(Queen, Piece):
    u"""The White Queen chess piece."""
    symbol = u'\u2655'
    simple_simbol = u'WQ'
    name = u'white_queen'
    color = Color.white


class BlackQueen(Queen, Piece):
    u"""The Black Queen chess piece."""
    symbol = u'\u265b'
    simple_simbol = u'BQ'
    name = u'black_queen'
    color = Color.black


class Rook(object):
    u"""The Rook (castle) chess piece.

    This should not be created directly, instead a BlackRook or WhiteRook
    should be instanciated.
    """
    attacks = frozenset([(1, 0), (0, 1), (-1, 0), (0, -1)])
    has_moved = False
    value = 5

    def __new__(cls, *args, **kwargs):
        if cls is Rook:
            raise TypeError(u"Rook class may not be instantiated.")
        return object.__new__(cls, *args, **kwargs)


class WhiteRook(Rook, Piece):
    u"""The White Rook chess piece."""
    symbol = u'\u2656'
    simple_simbol = u'WR'
    name = u'white_rook'
    color = Color.white

    def __init__(self, has_moved=False):
        self.has_moved = has_moved


class BlackRook(Rook, Piece):
    u"""The Black Rook chess piece."""
    symbol = u'\u265c'
    simple_simbol = u'BR'
    name = u'black_rook'
    color = Color.black

    def __init__(self, has_moved=False):
        self.has_moved = has_moved


class Bishop(object):
    u"""The Bishop chess piece.

    This should not be created directly, instead a BlackBishop or WhiteBishop
    should be instanciated.
    """
    attacks = frozenset([(1, 1), (-1, 1), (-1, -1), (1, -1)])  # x,y
    value = 3

    def __new__(cls, *args, **kwargs):
        if cls is Bishop:
            raise TypeError("Bishop class may not be instantiated.")
        return object.__new__(cls, *args, **kwargs)


class WhiteBishop(Bishop, Piece):
    u"""The White Bishop chess piece."""
    symbol = u'\u2657'
    simple_simbol = u'WB'
    name = u'white_bishop'
    color = Color.white


class BlackBishop(Bishop, Piece):
    """The Black Bishop chess piece."""
    symbol = u'\u265d'
    simple_simbol = u'BB'
    name = u'black_bishop'
    color = Color.black


class Knight(Piece):
    u"""The Knight chess piece.

    This should not be called directly, instead a BlackKnight or WhiteKnight
    should be instanciated.
    """
    # All moves a knight may make
    attacks = frozenset([(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)])
    limit = 1  # Knights only move one place via their move vectors
    value = 3

    def __new__(cls, *args, **kwargs):
        if cls is Knight:
            raise TypeError(u"Knight class may not be instantiated.")
        return object.__new__(cls, *args, **kwargs)


class WhiteKnight(Knight, Piece):
    u"""The White Knight chess piece."""
    symbol = u'\u2658'
    simple_simbol = u'WN'
    name = u'white_knight'
    color = Color.white


class BlackKnight(Knight, Piece):
    u"""The Black Knight chess piece."""
    symbol = u'\u265e'
    simple_simbol = u'BN'
    name = u'black_knight'
    color = Color.black


class Pawn(object):
    u"""The Pawn chess piece.

    This should not be called directly, instead a  BlackPawn or WhitePawn
    should be instanciated.
    """
    limit = 1  # Pawns can only attack/move 1 space (double move is treated special)
    has_moved = False
    value = 1

    def __new__(cls, *args, **kwargs):
        if cls is Pawn:
            raise TypeError(u"Pawn class may not be instantiated.")
        return object.__new__(cls, *args, **kwargs)

    @property
    def attacks(self):
        u"""Returns the vectors of the directions a pawn can attack in."""
        return frozenset([(-1, self.forward), (1, self.forward)])

    def en_passant_move(self, dir_):
        x = self.location.x + dir_[0]
        y = self.location.y + self.forward
        return Square(x, y)

    @staticmethod
    def en_passant():
        u"""Returns the vectors of the directions a pawn can attack via en_passant in."""
        return frozenset([(-1, 0), (1, 0)])

    @property
    def moves(self):
        move_1 = Square(self.location.x, self.location.y + self.forward)
        if self.location.y == 8 or self.location.y == 1:
            #Pawn in the last square, cannot move, should be promoted
            return []
        if self.has_moved:
            return [move_1]
        else:
            move_2 = Square(self.location.x, self.location.y + 2 * self.forward)
            return [move_1, move_2]


class WhitePawn(Pawn, Piece):
    u"""A White Pawn chess piece."""
    symbol = u'\u2659'
    simple_simbol = u'WP'
    name = u'white_pawn'
    color = Color.white
    forward = 1  # Based off White starting at rows 1,2

    def __init__(self, loc):
        assert (loc.x)
        assert (loc.y)
        self.location = loc

        # has_moved is used for determining if the pawn can double move
        if loc.y == 2:
            self.has_moved = False
        else:
            self.has_moved = True


class BlackPawn(Pawn, Piece):
    u"""A Black Pawn chess piece."""
    symbol = u'\u265f'
    simple_simbol = u'BP'
    name = u'black_pawn'
    color = Color.black
    forward = -1  # Based off Black starting at rows 7,8

    def __init__(self, loc):
        assert (loc.x)
        assert (loc.y)
        self.location = loc

        # has_moved is used for determining if the pawn can double move
        if loc.y == 7:
            self.has_moved = False
        else:
            self.has_moved = True


class PieceFactory(object):
    """The peice factory allows the generic creation of chess pieces based of their
       color and type.
    """
    # Created primarily for the promote method used to promote pawns
    @staticmethod
    def create(piece, color, loc=None):
        """Create a new peice of the color and type

        color -- The color of the piece to create, e.g  Color.black
        piece -- The type of the piece to create, e.g Rook, or one of its subclasses like WhiteRook

        Returns -- A new piece of the color and type
        Raises -- A value error if the color or type is not valid
        """

        if color is Color.white:
            if issubclass(piece, King):
                return WhiteKing()
            elif issubclass(piece, Queen):
                return WhiteQueen()
            elif issubclass(piece, Rook):
                return WhiteRook(loc)
            elif issubclass(piece, Knight):
                return WhiteKnight()
            elif issubclass(piece, Bishop):
                return WhiteBishop()
            elif issubclass(piece, Pawn):
                return WhitePawn(loc)
            else:
                raise TypeError(u"Invlaid piece {piece}".format(piece=piece))
        elif color is Color.black:
            if issubclass(piece, King):
                return BlackKing()
            elif issubclass(piece, Queen):
                return BlackQueen()
            elif issubclass(piece, Rook):
                return BlackRook(loc)
            elif issubclass(piece, Knight):
                return BlackKnight()
            elif issubclass(piece, Bishop):
                return BlackBishop()
            elif issubclass(piece, Pawn):
                return BlackPawn(loc)
            else:
                raise TypeError(u"Invlaid piece {piece}".format(piece=piece))
        else:
            raise TypeError(u"Invlaid color {color}".format(color=color))
