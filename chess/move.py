class Move(object):
    """
    Represents a move in a chess game.
    """

    def __init__(self, piece, from_, to_, double_move=False, capture=False, king_side_castle=False,
                 queen_side_castle=False, check=False, checkmate=False, stalemate=False, promotion=None,
                 display_value=None):
        """
        Initialize a new Move.

        piece -- A chess piece
        from_ -- The location the piece moved from
        to_   -- The location the piece moved to
        double_move -- True if a pawn has moved two squares in one turn
        """
        self.piece = piece
        self.from_loc = from_
        self.to_loc = to_
        self.double_move = double_move
        self.capture = capture
        self.king_side_castle = king_side_castle
        self.queen_side_castle = queen_side_castle
        self.check = check
        self.checkmate = checkmate
        self.stalemate = stalemate
        self.promotion = promotion
        self.display_value = display_value

    # def display(self):
    #     """Returns the display string for the move in ??? notation."""
    #     # TODO: Add logic to display castling better
    #     if self.is_capture:
    #         operator = "x"
    #     else:
    #         operator = " "
    #     return self.from_ + operator + self.to_

    # def algebraic_notation(self):
    #     """Returns the move in Algebraic Chess Notation

    #         http://en.wikipedia.org/wiki/Algebraic_chess_notation
    #     """
    #     # TODO: This is kinda tricky, as we need to minimize the notations, therefore must check more about the board
    #     pass
