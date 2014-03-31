class Move(object):
    u"""Represents a move in a chess game."""
    from_ = None
    to_ = None
    piece = None
    is_double_move = False  # Did the the pawn moved two squares? Only relevant for pawns
    is_capture = False  # TODO: Set this property as it affects the display string

    def __init__(self, piece, from_, to_, is_double_move=False):
        """Initialize a new Move.

        piece -- A chess piece
        from_ -- The location the piece moved from
        to_   -- The location the piece moved to
        is_double_move -- True if a pawn has moved two squares in one turn
        """
        assert(from_.x)
        assert(from_.y)
        assert(from_.name)
        assert(to_.x)
        assert(to_.y)
        assert(to_.name)
        self.piece = piece
        self.from_ = from_
        self.to_ = to_
        self.is_double_move = is_double_move

    def display(self):
        """Returns the display string for the move in ??? notation."""
        if self.is_capture:
            operator = "x"
        else:
            operator = " "
        return self.from_.name + operator + self.to_.name
