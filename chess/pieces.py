from color import Color


class InvlaidPieceException(Exception):
    u"""Returned if a chess piece is not a legal chess piece."""
    pass


class Piece(object):
    symbol = u'?'
    simple_simbol = u'?'  # Used in JSON representation
    color = None
    # A numerical limit to the number of squares this piece can move in
    # If none then it can move an unlimted amount in a direction
    limit = None
    value = None  # Tradional chess values - used to determince some statemate

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
    value = 0
    has_moved = False

    def __new__(cls, *args, **kwargs):
        if cls is King:
            raise TypeError(u"King class may not be instantiated.")
        return object.__new__(cls, *args, **kwargs)


class WhiteKing(King, Piece):
    u"""The White King chess piece."""
    symbol = u'\u2654'
    simple_simbol = u'WK'
    name = u'WhiteKing'
    color = Color.WHITE

    def __init__(self, has_moved=False):
        self.has_moved = has_moved


class BlackKing(King, Piece):
    u"""The Black King chess piece."""
    symbol = u'\u265a'
    simple_simbol = u'BK'
    name = u'BlackKing'
    color = Color.BLACK

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
    name = u'WhiteQueen'
    color = Color.WHITE


class BlackQueen(Queen, Piece):
    u"""The Black Queen chess piece."""
    symbol = u'\u265b'
    simple_simbol = u'BQ'
    name = u'BlackQueen'
    color = Color.BLACK


class Rook(object):
    u"""The Rook (castle) chess piece.

    This should not be created directly, instead a BlackRook or WhiteRook
    should be instanciated.
    """
    attacks = frozenset([(1, 0), (0, 1), (-1, 0), (0, -1)])
    value = 5
    has_moved = False

    def __new__(cls, *args, **kwargs):
        if cls is Rook:
            raise TypeError(u"Rook class may not be instantiated.")
        return object.__new__(cls, *args, **kwargs)


class WhiteRook(Rook, Piece):
    u"""The White Rook chess piece."""
    symbol = u'\u2656'
    simple_simbol = u'WR'
    name = u'WhiteRook'
    color = Color.WHITE

    def __init__(self, has_moved=False):
        self.has_moved = has_moved


class BlackRook(Rook, Piece):
    u"""The Black Rook chess piece."""
    symbol = u'\u265c'
    simple_simbol = u'BR'
    name = u'BlackRook'
    color = Color.BLACK

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
    name = u'WhiteBishop'
    color = Color.WHITE


class BlackBishop(Bishop, Piece):
    """The Black Bishop chess piece."""
    symbol = u'\u265d'
    simple_simbol = u'BB'
    name = u'BlackBishop'
    color = Color.BLACK


class Knight(object):
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
    name = u'WhiteKnight'
    color = Color.WHITE


class BlackKnight(Knight, Piece):
    u"""The Black Knight chess piece."""
    symbol = u'\u265e'
    simple_simbol = u'BN'
    name = u'BlackKnight'
    color = Color.BLACK


class Pawn(object):
    u"""The Pawn chess piece.

    This should not be called directly, instead a  BlackPawn or WhitePawn
    should be instanciated.
    """
    limit = 1  # Pawns can only attack/move 1 space (double move is treated special)
    value = 1
    forward = None  # Either 1 or -1 depending on subclass

    def __new__(cls, *args, **kwargs):
        if cls is Pawn:
            raise TypeError(u"Pawn class may not be instantiated.")
        return object.__new__(cls, *args, **kwargs)

    @property
    def attacks(self):
        u"""Returns the vectors of the directions a pawn can attack in."""
        return frozenset([(-1, self.forward), (1, self.forward)])

    @staticmethod
    def en_passant():
        u"""Returns the vectors of the directions a pawn can attack via en_passant in."""
        return frozenset([(-1, 0), (1, 0)])

    @property
    def moves(self):
        u"""Returns the direction the pawn can move in in the form of an (x,y) move vector."""
        frozenset([(self.forward, 0)])


class WhitePawn(Pawn, Piece):
    u"""A White Pawn chess piece."""
    symbol = u'\u2659'
    simple_simbol = u'WP'
    name = u'WhitePawn'
    color = Color.WHITE
    forward = 1  # Based off White starting at rows 1,2


class BlackPawn(Pawn, Piece):
    u"""A Black Pawn chess piece."""
    symbol = u'\u265f'
    simple_simbol = u'BP'
    name = u'BlackPawn'
    color = Color.BLACK
    forward = -1  # Based off Black starting at rows 7,8


class PieceFactory(object):
    u"""The peice factory allows the generic creation of chess pieces based on their name."""

    @staticmethod
    def create(name, has_moved=False):
        u""" Creates a new piece of the type equal to name.

        name -- The name of the chess piece, one of: WhiteKing, WhiteQueen, WhiteRook, WhiteBishop, WhiteKnight,
               WhitePawn, BlackKing, BlackQueen, BlackRook, BlackBishop, BlackKnight, or BlackPawn
        has_moved -- Boolean, marks whether the chess piece has previously moved or not.

        returns -- A piece of the class which is the same as the name specified
        raises  -- InvlaidPieceException is the name is an invalid value.
        """
        types = Piece.__subclasses__()
        piece_names = [(type.__name__, type) for type in types]
        d = dict(piece_names)
        try:
            piece = d[name]
        except KeyError:
            raise InvlaidPieceException("The chess piece {piece} does not exist.".format(piece=name))

        if hasattr(piece, 'has_moved'):
            return piece(has_moved)
        else:
            return piece()

    @staticmethod
    def createFromSymbol(symbol, has_moved):
        types = Piece.__subclasses__()
        symbols = [(type.symbol, type) for type in types]
        d = dict(symbols)
        try:
            piece = d[symbol]
        except KeyError:
            raise InvlaidPieceException("The chess piece {symbol} does not exist.".format(symbol=symbol))

        if hasattr(piece, 'has_moved'):
            return piece(has_moved)
        else:
            return piece()
