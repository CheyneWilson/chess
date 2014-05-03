class Move(object):
    u"""Represents a move in a chess game."""
    from_ = None
    to_ = None
    piece = None
    is_double_move = False  # Did the the pawn moved two squares? Only relevant for pawns
    is_capture = False  # TODO: Set this property as it affects the display string

    def __init__(self, piece, from_, to_, is_double_move=False, is_capture=False, is_castle=False):
        """Initialize a new Move.

        piece -- A chess piece
        from_ -- The location the piece moved from
        to_   -- The location the piece moved to
        is_double_move -- True if a pawn has moved two squares in one turn
        """
        self.piece = piece
        self.from_ = from_
        self.to_ = to_
        self.is_double_move = is_double_move
        self.is_capture = is_capture
        self.is_castle = is_castle

    def display(self):
        """Returns the display string for the move in ??? notation."""
        # TODO: Add logic to display castling better
        if self.is_capture:
            operator = "x"
        else:
            operator = " "
        return self.from_ + operator + self.to_

    def algebraic_notation(self):
        """Returns the move in Algebraic Chess Notation

            http://en.wikipedia.org/wiki/Algebraic_chess_notation
        """
        # TODO: This is kinda tricky, as we need to minimize the notations, therefore must check more about the board
        pass
