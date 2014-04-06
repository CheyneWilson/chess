# -*- coding: UTF-8 -*-
# Unit tests for chess. Requires PyHamcrest to be installed.
# This can be easily done using any packaging tool (such as distribute).
# See https://code.google.com/p/hamcrest/ for more details on hamcrest matchers
from board import Board, Color, King, Queen, Bishop, Knight, Rook, Pawn, BlackPawn, WhiteKing, WhiteRook, \
    BlackKing, BlackQueen, BlackRook, BlackBishop, BlackKnight, Square, IllegalMoveException
from hamcrest import is_, assert_that, equal_to, all_of, contains_inanyorder, instance_of
import unittest
import json


class TestBoardFunctions(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_create_new_board(self):
        # Make sure that it is White player's turn to move
        white_player = Color.white
        assert_that(self.board.current_player, equal_to(white_player))

        # Make sure a new board places all the pieces in the correct locations
        # Using 'internal' method get_piece check all of the White pieces
        assert_that(all_of(
            self.board.get_piece((1, 1)), is_(Rook)),
            self.board.get_piece((1, 1)).color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece((2, 1)), is_(Knight)),
            self.board.get_piece((2, 1)).color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece((3, 1)), is_(Bishop)),
            self.board.get_piece((3, 1)).color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece((4, 1)), is_(King)),
            self.board.get_piece((4, 1)).color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece((5, 1)), is_(Queen)),
            self.board.get_piece((5, 1)).color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece((6, 1)), is_(Bishop)),
            self.board.get_piece((6, 1)).color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece((7, 1)), is_(Knight)),
            self.board.get_piece((7, 1)).color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece((8, 1)), is_(Rook)),
            self.board.get_piece((8, 1)).color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece((1, 2)), is_(Pawn)),
            self.board.get_piece((1, 2)).color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece((2, 2)), is_(Pawn)),
            self.board.get_piece((2, 2)).color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece((2, 2)), is_(Pawn)),
            self.board.get_piece((2, 2)).color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece((3, 2)), is_(Pawn)),
            self.board.get_piece((3, 2)).color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece((4, 2)), is_(Pawn)),
            self.board.get_piece((4, 2)).color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece((5, 2)), is_(Pawn)),
            self.board.get_piece((5, 2)).color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece((6, 2)), is_(Pawn)),
            self.board.get_piece((6, 2)).color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece((7, 2)), is_(Pawn)),
            self.board.get_piece((7, 2)).color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece((8, 2)), is_(Pawn)),
            self.board.get_piece((8, 2)).color, is_(Color.white)
        )

        # Using 'internal' method get_piece check all of the Black pieces
        assert_that(all_of(
            self.board.get_piece((1, 8)), is_(Rook)),
            self.board.get_piece((1, 8)).color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece((2, 8)), is_(Knight)),
            self.board.get_piece((2, 8)).color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece((3, 8)), is_(Bishop)),
            self.board.get_piece((3, 8)).color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece((4, 8)), is_(King)),
            self.board.get_piece((4, 8)).color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece((5, 8)), is_(Queen)),
            self.board.get_piece((5, 8)).color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece((6, 8)), is_(Bishop)),
            self.board.get_piece((6, 8)).color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece((7, 8)), is_(Knight)),
            self.board.get_piece((7, 8)).color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece((8, 8)), is_(Rook)),
            self.board.get_piece((8, 8)).color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece((1, 7)), is_(Pawn)),
            self.board.get_piece((1, 7)).color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece((2, 7)), is_(Pawn)),
            self.board.get_piece((2, 7)).color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece((2, 7)), is_(Pawn)),
            self.board.get_piece((2, 7)).color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece((3, 7)), is_(Pawn)),
            self.board.get_piece((3, 7)).color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece((4, 7)), is_(Pawn)),
            self.board.get_piece((4, 7)).color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece((5, 7)), is_(Pawn)),
            self.board.get_piece((5, 7)).color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece((6, 7)), is_(Pawn)),
            self.board.get_piece((6, 7)).color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece((7, 7)), is_(Pawn)),
            self.board.get_piece((7, 7)).color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece((8, 7)), is_(Pawn)),
            self.board.get_piece((8, 7)).color, is_(Color.black)
        )

        # Check all the other squares are empty
        # This will return a horrible error message if it fails,
        # not telling us which square is wrong, but at least we'll
        # know to dig deeper.
        # Using range instead of xrange for if/when we go to python 3
        for x in range(1, 9):
            for y in range(3, 7):
                assert_that(self.board.get_piece((x, y)), is_(None))

    def test_get_moves_opening_white_pawn(self):
        """Check that a white pawn can move from it's starting position as either a single or double move."""
        from_ = Square(1, 2)
        pawn_moves = self.board.get_moves(from_)
        assert_that(pawn_moves, contains_inanyorder((1, 3), (1, 4)))

    def test_get_moves_opening_black_pawn(self):
        """Check that a black pawn can move from it's starting position as either a single or double move."""
        from_ = Square(6, 7)
        pawn_moves = self.board.get_moves(from_)
        assert_that(pawn_moves, contains_inanyorder((6, 6), (6, 5)))

    def test_get_moves_moved_white_pawn(self):
        """Check that a white pawn that has moved can only move one space (when nothing to attack)."""
        pawn_board = Board("♖♘♗♕♔♗♘♖-♙♙_♙♙♙♙♙-__♙_____-________-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        from_ = Square(3, 3)
        pawn_moves = pawn_board.get_moves(from_)
        assert_that(pawn_moves, contains_inanyorder((3, 4)))

    def test_get_moves_white_pawn_attacks_both(self):
        """Check that a white pawn with 3 Black pieces in front can attack the two pieces on the sides only"""
        pawn_board = Board("♖♘♗♕♔♗♘♖-♙♙♙_♙♙♙♙-________-________-________-___♙___-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        from_ = Square(4, 6)
        pawn_moves = pawn_board.get_moves(from_)
        assert_that(pawn_moves, contains_inanyorder((3, 7), (5, 7)))

    def test_get_moves_black_pawn_attack_left(self):
        """Check that a black pawn next to the right board edge blocked by two white pieces can attak diagonally left.

           The board looks like:
              ________________
           8 |♜|♞|♝|♛|♚|♝|♞|♜|
           7 |♟|♟|♟|♟|♟|♟|♟|_|
           6 |_|_|_|_|_|_|_|_|
           5 |_|_|_|_|_|_|_|♟|
           4 |_|_|_|_|_|_|♙|♙|
           3 |_|_|_|_|_|_|_|_|
           2 |♙|♙|♙|♙|♙|♙|_|_|
           1 |♖|♘|♗|♕|♔|♗|♘|♖|
              ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
              A B C D E F G H

        """
        pawn_board = Board("♖♘♗♕♔♗♘♖-♙♙♙♙♙♙__-________-______♙♙-_______♟-________-♟♟♟♟♟♟♟_-♜♞♝♛♚♝♞♜,W,0,0")
        from_ = Square(8, 5)
        pawn_moves = pawn_board.get_moves(from_)
        assert_that(pawn_moves, contains_inanyorder((7, 4)))

    def test_get_moves_black_pawn_cant_attack_black(self):
        """Check that a black pawn can't attack it's own pieces.

           The board looks like:
              ________________
           8 |♜|♞|♝|♛|♚|♝|♞|♜|
           7 |♟|♟|♟|♟|♟|♟|♟|_|
           6 |_|_|_|_|_|_|_|_|
           5 |_|_|_|_|_|_|_|♟|
           4 |_|_|_|_|_|_|♟|♟|
           3 |_|_|_|_|_|_|_|_|
           2 |♙|♙|♙|♙|♙|♙|♙|♙|
           1 |♖|♘|♗|♕|♔|♗|♘|♖|
              ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
              A B C D E F G H
        """
        pawn_board = Board("♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-______♟♟-_______♟-________-♟♟♟♟♟♟♟_-♜♞♝♛♚♝♞♜,W,0,0")
        from_ = Square(8, 5)
        pawn_moves = pawn_board.get_moves(from_)
        assert_that(pawn_moves, is_([]))

    def test_get_moves_black_pawn_can_move_to_end_of_board(self):
        """Check that a black pawn can move into the last square

           This was added because pawns in the last square would throw a key error when get_moves is called.
           These pieces are promoted to the piece a user chooses.

           The board looks like:
              ________________
           8 |♜|♞|♝|♛|♚|♝|♞|♜|
           7 |♟|♟|♟|♟|♟|♟|♟|_|
           6 |_|_|_|_|_|_|_|_|
           5 |_|_|_|_|_|_|_|_|
           4 |_|_|_|_|_|_|_|_|
           3 |_|_|_|_|_|_|_|_|
           2 |♙|♙|♙|♙|♙|♙|♙|♟|
           1 |♖|♘|♗|♕|♔|♗|_|_|
              ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
              A B C D E F G H
        """
        pawn_board = Board("♖♘♗♕♔♗__-♙♙♙♙♙♙♙♟-________-________-________-________-♟♟♟♟♟♟♟_-♜♞♝♛♚♝♞♜,B,0,0")
        from_ = Square(8, 2)
        to_ = Square(8, 1)
        pawn_moves = pawn_board.get_moves(from_)
        assert_that(pawn_moves, contains_inanyorder((8, 1)))

        pawn_moves = pawn_board.move_piece(from_, to_)
        pawn_moves = pawn_board.get_moves(to_)

        # self.assertRaises(IllegalMoveException, pawn_board.get_movesto_, to_)
        assert_that(pawn_moves, is_([]))

    # TODO:
    # Add more tests for the following
    # * Cannot attack own color

    def test_get_moves_white_knight_opening(self):
        """Check the opening moves of a white knight."""
        from_ = Square(2, 1)
        knight_moves = self.board.get_moves(from_)
        assert_that(knight_moves, contains_inanyorder((1, 3), (3, 3)))

    def test_get_moves_black_knight_opening(self):
        """Check the opening moves of a black knight."""
        from_ = Square(7, 8)
        knight_moves = self.board.get_moves(from_)
        assert_that(knight_moves, contains_inanyorder((6, 6), (8, 6)))

    def test_get_moves_knight_fork_attack(self):
        """Check if a knight at G3 can fork the king and rook, as well as other moves."""
        knight_board = Board("♖_♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-________-________-________-♟♟♘♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        from_ = Square(3, 7)
        knight_moves = knight_board.get_moves(from_)
        assert_that(knight_moves, contains_inanyorder((1, 8), (5, 8), (1, 6), (5, 6), (2, 5), (4, 5)))

    def test_get_moves_white_bishop_opening(self):
        """Check the opening moves of a white bishop."""
        from_ = Square(3, 1)
        bishop_moves = self.board.get_moves(from_)
        assert_that(bishop_moves, is_([]))

    def test_get_moves_black_bishop_opening(self):
        """Check the opening moves of a black bishop."""
        from_ = Square(3, 8)
        bishop_moves = self.board.get_moves(from_)
        assert_that(bishop_moves, is_([]))

    def test_get_moves_white_bishop_free(self):
        """Test get_moves for a white bishop in the middle of the board."""
        bishop_board = Board("♖♘_♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-________-____♗___-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        from_ = Square(5, 5)
        bishop_moves = bishop_board.get_moves(from_)
        assert_that(bishop_moves, contains_inanyorder(
            (4, 6), (3, 7),  # forward left
            (6, 6), (7, 7),  # forward right
            (4, 4), (3, 3),  # backward left
            (6, 4), (7, 3)   # backward right
        ))

    def test_get_moves_black_bishop_free(self):
        """Test get_moves for a black bishop in the middle of the board."""
        bishop_board = Board("♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-________-___♝____-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚_♞♜,W,0,0")
        from_ = Square(4, 5)
        bishop_moves = bishop_board.get_moves(from_)
        assert_that(bishop_moves, contains_inanyorder(
            (3, 6),  # (2, 7),  # forward left
            (5, 6),  # (6, 7),  # forward right
            (3, 4), (2, 3), (1, 2),  # backward left
            (5, 4), (6, 3), (7, 2)   # backward right
        ))

    def test_get_moves_white_rook_opening(self):
        """Test get_moves for the opening moves of a white rook."""
        from_ = Square(8, 1)
        rook_moves = self.board.get_moves(from_)
        assert_that(rook_moves, is_([]))

    def test_get_moves_black_rook_opening(self):
        """Test get_moves for the opening moves of a black rook."""
        from_ = Square(8, 8)
        rook_moves = self.board.get_moves(from_)
        assert_that(rook_moves, is_([]))

    def test_get_moves_white_rook_free(self):
        """Test get_moves for a white rook in the middle of the board."""
        rook_board = Board("♖♘♗♕♔♗♘_-♙♙♙♙♙♙♙♙-_♖______-________-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        from_ = Square(2, 3)
        rook_moves = rook_board.get_moves(from_)
        assert_that(rook_moves, contains_inanyorder(
            (2, 4), (2, 5), (2, 6), (2, 7),  # forward
            (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3),  # right
            (1, 3)  # left
            # none backward
        ))

    def test_get_moves_black_rook_free(self):
        """Test get_moves for a black rook in the middle of the board.

        The board looks like:
           ________________
        8 |♜|♞|♝|♛|♚|♝|♞|_|
        7 |♟|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|_|_|_|_|
        4 |_|_|_|_|_|_|_|_|
        3 |_|♜|_|_|_|_|_|_|
        2 |♙|♙|♙|♙|♙|♙|♙|♙|
        1 |♖|♘|♗|♕|♔|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """

        rook_board = Board("♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-_♜______-________-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞_,W,0,0")
        from_ = Square(2, 3)
        rook_moves = rook_board.get_moves(from_)
        assert_that(rook_moves, contains_inanyorder(
            (2, 4), (2, 5), (2, 6),  # forward
            (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3),  # right
            (1, 3),  # left
            (2, 2)  # backward
        ))

    def test_get_moves_white_queen_opening(self):
        """Test get_moves for the opening moves of a white queen."""
        from_ = Square(4, 1)
        queen_moves = self.board.get_moves(from_)
        assert_that(queen_moves, is_([]))

    def test_get_moves_black_queen_opening(self):
        """Test get_moves for the opening moves of a black queen."""
        from_ = Square(4, 8)
        queen_moves = self.board.get_moves(from_)
        assert_that(queen_moves, is_([]))

    def test_get_moves_white_queen_free(self):
        """Check the moves of a white queen in the open."""
        queen_board = Board("♖♘♗_♔♗♘♖-♙♙♙♙♙♙♙♙-________-___♕____-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        from_ = Square(4, 4)
        queen_moves = queen_board.get_moves(from_)
        assert_that(queen_moves, contains_inanyorder(
            (4, 5), (4, 6), (4, 7),  # forward
            (5, 5), (6, 6), (7, 7),  # forward right
            (5, 4), (6, 4), (7, 4), (8, 4),  # right
            (5, 3),  # backwards right
            (4, 3),  # backward
            (3, 3),  # backwards left
            (3, 4), (2, 4), (1, 4),  # left
            (3, 5), (2, 6), (1, 7)  # forward, left
        ))

    def test_get_moves_black_queen_free(self):
        """Check the moves of a black queen in the open."""
        queen_board = Board("♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-___♛____-________-________-♟♟♟♟♟♟♟♟-♜♞♝_♚♝♞♜,W,0,0")
        from_ = Square(4, 4)
        queen_moves = queen_board.get_moves(from_)
        assert_that(queen_moves, contains_inanyorder(
            (4, 5), (4, 6),  # forward
            (5, 5), (6, 6),  # forward right
            (5, 4), (6, 4), (7, 4), (8, 4),  # right
            (5, 3), (6, 2),  # backwards right
            (4, 3), (4, 2),  # backward
            (3, 3), (2, 2),  # backwards left
            (3, 4), (2, 4), (1, 4),  # left
            (3, 5), (2, 6)  # forward, left
        ))

    def test_get_moves_white_king_opening(self):
        """Check the opening moves of a white king."""
        from_ = Square(5, 1)
        king_moves = self.board.get_moves(from_)
        assert_that(king_moves, is_([]))

    def test_get_moves_black_king_opening(self):
        """Check the opening moves of a black king."""
        from_ = Square(5, 8)
        king_moves = self.board.get_moves(from_)
        assert_that(king_moves, is_([]))

    def test_get_moves_white_king_free(self):
        """Check the moves of a white king in the open."""
        king_board = Board("♖♘♗♕_♗♘♖-♙♙♙♙♙♙♙♙-________-___m♔____-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        from_ = Square(4, 4)
        king_moves = king_board.get_moves(from_)
        assert_that(king_moves, contains_inanyorder(
            (4, 5),  # forward
            (5, 5),  # forward right
            (5, 4),  # right
            (5, 3),  # backwards right
            (4, 3),  # backward
            (3, 3),  # backwards left
            (3, 4),  # left
            (3, 5)   # forward, left
        ))

    def test_get_moves_black_king_partially_free(self):
        """Check the moves of a black king in front of white pawns."""
        king_board = Board("♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-___m♚____-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛_♝♞♜,W,0,0")
        from_ = Square(4, 4)
        king_moves = king_board.get_moves(from_)
        assert_that(king_moves, contains_inanyorder(
            (4, 5),  # forward
            (5, 5),  # forward right
            (5, 4),  # right
            (3, 4),  # left
            (3, 5)   # forward, left
        ))

    def test_get_moves_pinned_knight(self):
        """Check that a pinned knight cannot move (as there is no way for it to still be blocking check if it moves)

        The board looks like:
           ________________
        8 |♖|♘|♗|♕|♔|♗|_|♖|
        7 |♙|♙|♙|♙|♘|♙|♙|♙|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|_|_|_|_|
        4 |_|_|_|_|♜|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♟|♟|♟|♟|♟|♟|♟|♟|
        1 |♜|♞|♝|♛|♚|♝|♞|_|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
        A B C D E F G H

        """
        pinned_board = Board("♖♘♗♕♔♗_♖-♙♙♙♙♘♙♙♙-________-________-____♜___-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞_,W,0,0")
        from_ = Square(5, 2)
        knight_moves = pinned_board.get_moves(from_)
        assert_that(knight_moves, is_([]))

    def test_get_moves_pawn_pinned_by_rook(self):
        """Test that a pawn pinned vertically by a rook can still move forward normally - in the direction it is pinned

        The board looks like:
           ________________
        8 |♜|♞|♝|♛|♚|♝|♞|_|
        7 |♟|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|♜|_|_|_|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♙|♙|♙|♙|♙|♙|♙|♙|
        1 |♖|♘|♗|♕|♔|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H

        """
        pinned_board = Board("♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-________-____♜___-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞_,W,0,0")
        from_ = Square(5, 2)
        pawn_moves = pinned_board.get_moves(from_)
        assert_that(pawn_moves, contains_inanyorder((5, 3), (5, 4)))

    def test_get_moves_pawn_pinned_by_rook_2(self):
        """Test that a pawn pinned vertically by a rook can still move forward normally but cannot attack

        The board looks like:
           ________________
        8 |♜|♞|♝|♛|♚|♝|♞|_|
        7 |♟|♟|♟|_|♟|_|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|♜|_|_|_|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|♟|_|♟|_|_|
        2 |♙|♙|♙|♙|♙|♙|♙|♙|
        1 |♖|♘|♗|♕|♔|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """
        pinned_board = Board("♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-___♟_♟__-________-____♜___-________-♟♟♟_♟_♟♟-♜♞♝♛♚♝♞_,W,0,0")
        from_ = Square(5, 2)
        pawn_moves = pinned_board.get_moves(from_)
        assert_that(pawn_moves, contains_inanyorder((5, 3), (5, 4)))

    def test_get_moves_pawn_pinned_by_rook_3(self):
        """Test that a pawn pinned horizontally by a rook can still move forward normally but cannot attack

        The board looks like:
           ________________
        8 |♜|♞|♝|♛|_|♝|♞|♜|  White pawn has double moved to D5. Black could
        7 |♟|♟|♟|♟|♟|_|♟|♟|  capture via en passant but that would put Black's
        6 |_|_|_|_|_|_|_|_|  king in check. Therefore can only move forward.
        5 |_|_|_|_|_|_|_|_|
        4 |♖|_|_|_|♙|♟|_|♚|
        3 |_|_|_|_|_|_|_|_|
        2 |♙|♙|♙|♙|_|♙|♙|♙|
        1 |♖|♘|♗|♕|♔|♗|♘|_|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """
        pinned_board = Board("♖♘♗♕♔♗♘_-♙♙♙♙_♙♙♙-________-♖___m♙♟_♚-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛_♝♞♜,W,0,0")
        from_ = Square(6, 4)
        pawn_moves = pinned_board.get_moves(from_)
        assert_that(pawn_moves, contains_inanyorder((6, 3)))

    def test_get_moves_pawn_pinned_by_rook_4(self):
        """Test that a pawn pinned horizontally by a rook can still move forward normally but cannot attack

        The board looks like:
           ________________
        8 |♜|♞|♝|♛|_|♝|♞|♜|  Black pawn is pinned so cannot move.
        7 |♟|♟|♟|♟|♟|_|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|_|_|_|_|
        4 |♖|_|_|_|_|♟|_|♚|
        3 |_|_|_|_|_|_|_|_|
        2 |♙|♙|♙|♙|♙|♙|♙|♙|
        1 |♖|♘|♗|♕|♔|♗|♘|_|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """
        pinned_board = Board("♖♘♗♕♔♗♘_-♙♙♙♙♙♙♙♙-________-♖____♟_♚-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛_♝♞♜,W,0,0")
        from_ = Square(6, 4)
        pawn_moves = pinned_board.get_moves(from_)
        assert_that(pawn_moves, is_([]))

    def test_get_moves_pawn_pinned_by_bishop(self):
        """Test that a pawn pinned by a bishop cannot move

        The board looks like:
           ________________
        8 |♜|♞|♝|♛|♚|♝|♞|♜|  Black pawn is pinned so cannot move.
        7 |♟|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|_|_|_|♗|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♙|♙|♙|♙|♙|♙|♙|♙|
        1 |♖|♘|♗|♕|♔|_|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """
        pinned_board = Board("♖♘♗♕♔_♘♖-♙♙♙♙♙♙♙♙-________-________-_______♗-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        from_ = Square(6, 7)
        pawn_moves = pinned_board.get_moves(from_)
        assert_that(pawn_moves, is_([]))

    def test_get_moves_pawn_pinned_by_bishop_2(self):
        """Test that a pawn pinned by a bishop cannot move unless it can capture attacker

        The board looks like:
           ________________
        8 |♜|♞|♝|♛|♚|♝|♞|♜|  Black pawn is pinned but can capture attacker.
        7 |♟|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|♗|_|
        5 |_|_|_|_|_|_|_|_|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♙|♙|♙|♙|♙|♙|♙|♙|
        1 |♖|♘|♗|♕|♔|_|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """
        pinned_board = Board("♖♘♗♕♔_♘♖-♙♙♙♙♙♙♙♙-________-________-________-______♗_-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        from_ = Square(6, 7)
        pawn_moves = pinned_board.get_moves(from_)
        assert_that(pawn_moves, contains_inanyorder((7, 6)))

    def test_get_moves_pawn_pinned_by_bishop_3(self):
        """Test that a pawn pinned by a bishop cannot move unless it can capture attacker

        The board looks like:
           ________________
        8 |♜|♞|♝|♛|♚|♝|♞|♜|  Black pawn is pinned but can capture attacker.
        7 |♟|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|♙|_|♗|_|
        5 |_|_|_|_|_|_|_|_|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♙|♙|♙|♙|_|♙|♙|♙|
        1 |♖|♘|♗|♕|♔|_|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """
        pinned_board = Board("♖♘♗♕♔_♘♖-♙♙♙♙_♙♙♙-________-________-________-____♙_♗_-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        from_ = Square(6, 7)
        pawn_moves = pinned_board.get_moves(from_)
        assert_that(pawn_moves, contains_inanyorder((7, 6)))

    def test_get_attackers(self):
        # Check black queens pawn E7
        to_ = Square(3, 7)
        attackers_3_7 = self.board._get_attackers(to_, Color.black)
        assert_that(attackers_3_7, contains_inanyorder((4, 8)))

    def test_get_attackers_1_a(self):
        # Test some white pawns
        to_ = Square(2, 3)
        attackers_2_3 = self.board._get_attackers(to_, Color.white)
        assert_that(attackers_2_3, contains_inanyorder((1, 2), (3, 2)))

    def test_get_attackers_1_b(self):
        # Two pawns and a knight can attack 3,3 (C3)
        to_ = Square(3, 3)
        attackers_3_3 = self.board._get_attackers(to_, Color.white)
        assert_that(attackers_3_3, contains_inanyorder((2, 2), (4, 2), (2, 1)))

    def test_get_attackers_1_c(self):
        # Check pawn in front of white rook
        to_ = Square(8, 2)
        attackers_8_2 = self.board._get_attackers(to_, Color.white)
        assert_that(attackers_8_2, contains_inanyorder((8, 1)))

    def test_get_attackers_1_e(self):
        # Check black kings pawn E7
        to_ = Square(6, 7)
        attackers_6_7 = self.board._get_attackers(to_, Color.black)
        assert_that(attackers_6_7, contains_inanyorder((5, 8)))

    def test_pawn_attackers_2(self):
        """Check pawn directly in front of white king

        Check that the king, queen, bishop and right knight all attack square B5

        The board looks like:
           ________________
        8 |♜|♞|♝|♛|♚|♝|♞|♜|
        7 |♟|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|_|_|_|_|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♙|♙|♙|♙|♙|♙|♙|♙|
        1 |♖|♘|♗|♕|♔|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """
        to_ = Square(5, 2)
        attackers_5_2 = self.board._get_attackers(to_, Color.white)
        assert_that(attackers_5_2, contains_inanyorder(
            (4, 1), (5, 1), (6, 1), (7, 1)
        ))

    def test_is_check_1(self):
        """Neither king starts off in check. Test for a fresh board."""
        assert_that(self.board.is_check(Color.black), is_(False))
        assert_that(self.board.is_check(Color.white), is_(False))

    def test_is_check_2(self):
        """Test white king in check from two black pawns

        The board looks like:
           ________________
        8 |♜|♞|♝|♛|♚|♝|♞|♜|
        7 |♟|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|♔|_|
        5 |_|_|_|_|_|_|_|_|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♙|♙|♙|♙|♙|♙|♙|♙|
        1 |♖|♘|♗|♕|_|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """
        check_board = Board("♖♘♗♕_♗♘♖-♙♙♙♙♙♙♙♙-________-________-________-______♔_-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        assert_that(check_board.is_check(Color.black), is_(False))
        assert_that(check_board.is_check(Color.white), is_(True))

    def test_is_check_3(self):
        """Test black king in check from white knight

        The board looks like:
           ________________
        8 |♜|♞|♝|♛|_|♝|♞|♜|
        7 |♟|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|♚|_|_|♖|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♙|♙|♙|♙|♙|♙|♙|♙|
        1 |♖|♘|♗|♕|♔|♗|♘|_|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """
        check_board = Board("♖♘♗♕♔♗♘_-♙♙♙♙♙♙♙♙-________-________-____♚__♖-________-♟♟♟♟♟♟♟♟-♜♞♝♛_♝♞♜,W,0,0")
        assert_that(check_board.is_check(Color.black), is_(True))
        assert_that(check_board.is_check(Color.white), is_(False))

    def test_is_check_4(self):
        """Test black king in check from white queen horizontally

        The board looks like:
           ________________
        8 |♜|♞|♝|♛|_|♝|♞|♜|
        7 |♟|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|♚|_|_|♕|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♙|♙|♙|♙|♙|♙|♙|♙|
        1 |♖|♘|♗|_|♔|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """
        check_board = Board("♖♘♗_♔♗♘♖-♙♙♙♙♙♙♙♙-________-________-____♚__♕-________-♟♟♟♟♟♟♟♟-♜♞♝♛_♝♞♜,W,0,0")
        assert_that(check_board.is_check(Color.black), is_(True))
        assert_that(check_board.is_check(Color.white), is_(False))

    def test_is_check_5(self):
        """Test black king in check from white queen vertically

        The board looks like:
           ________________
        8 |♜|♞|♝|♛|_|♝|♞|♜|
        7 |♟|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|♚|_|_|_|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|♕|_|_|_|
        2 |♙|♙|♙|♙|♙|♙|♙|♙|
        1 |♖|♘|♗|_|♔|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """
        check_board = Board("♖♘♗_♔♗♘♖-♙♙♙♙♙♙♙♙-____♕___-________-____♚___-________-♟♟♟♟♟♟♟♟-♜♞♝♛_♝♞♜,W,0,0")
        assert_that(check_board.is_check(Color.black), is_(True))
        assert_that(check_board.is_check(Color.white), is_(False))

    def test_is_check_6(self):
        """Test white king in check from black knight

        The board looks like:
           ________________
        8 |♜|_|♝|♛|♚|♝|♞|♜|
        7 |♟|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|♞|_|_|_|_|_|
        5 |_|_|_|_|_|_|_|_|
        4 |_|♔|_|_|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♙|♙|♙|♙|♙|♙|♙|♙|
        1 |♖|♘|♗|♕|_|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """
        check_board = Board("♖♘♗♕_♗♘♖-♙♙♙♙♙♙♙♙-________-_♔______-________-__♞_____-♟♟♟♟♟♟♟♟-♜_♝♛♚♝♞♜,W,0,0")
        assert_that(check_board.is_check(Color.black), is_(False))
        assert_that(check_board.is_check(Color.white), is_(True))

    def test_checkmate_1(self):
        """Test the '2 move' checkmate. King cannot move and no pieces can
        block.

          ________________
        8 |♜|♞|♝|_|♚|♝|♞|♜|
        7 |♟|♟|♟|♟|_|♟|♟|♟|
        6 |_|_|_|_|♟|_|_|_|
        5 |_|_|_|_|_|_|_|_|
        4 |_|_|_|_|_|♙|♙|♛|
        3 |_|_|_|_|_|_|_|_|
        2 |♙|♙|♙|♙|♙|_|_|♙|
        1 |♖|♘|♗|♕|♔|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """
        check_board = Board("♖♘♗♕♔♗♘♖-♙♙♙♙♙__♙-________-_____♙♙♛-________-___♟____-♟♟♟_♟♟♟♟-♜♞♝_♚♝♞♜,W,0,0")
        assert_that(check_board.is_checkmate(Color.black), is_(False))
        assert_that(check_board.is_checkmate(Color.white), is_(True))

    def test_checkmate_2(self):
        """Simliar to the '2 move' checkmate, king cannot move but there is a
        block.
          ________________
        8 |♜|♞|♝|_|♚|♝|♞|♜|
        7 |♟|♟|♟|♟|_|♟|♟|♟|
        6 |_|_|_|_|♟|_|_|_|
        5 |_|_|_|_|_|_|_|_|
        4 |_|_|_|_|_|♙|_|♛|
        3 |_|♙|_|_|_|_|_|_|
        2 |♙|_|♙|♙|♙|_|♙|♙|
        1 |♖|♘|♗|♕|♔|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """

        check_board = Board("♖♘♗♕♔♗♘♖-♙_♙♙♙_♙♙-_♙______-_____♙_♛-________-___♟____-♟♟♟_♟♟♟♟-♜♞♝_♚♝♞♜,W,0,0")
        assert_that(check_board.is_checkmate(Color.black), is_(False))
        assert_that(check_board.is_checkmate(Color.white), is_(False))

    def test_checkmate_3(self):
        """Simliar to the '2 move' checkmate, but king can move to escape.
          ________________
        8 |♜|♞|♝|_|♚|♝|♞|♜|
        7 |♟|♟|♟|♟|_|♟|♟|♟|
        6 |_|_|_|_|♟|_|_|_|
        5 |_|_|_|_|_|_|_|_|
        4 |_|_|_|_|_|♙|♙|♛|
        3 |_|_|_|♙|_|_|_|_|
        2 |♙|♙|♙|_|♙|_|_|♙|
        1 |♖|♘|♗|♕|♔|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """

        check_board = Board("♖♘♗♕♔♗♘♖-♙♙♙_♙__♙-___♙____-_____♙♙♛-________-___♟____-♟♟♟_♟♟♟♟-♜♞♝_♚♝♞♜,W,0,0")
        assert_that(check_board.is_checkmate(Color.black), is_(False))
        assert_that(check_board.is_checkmate(Color.white), is_(False))

    def test_checkmate_4(self):
        """Simliar to the '2 move' checkmate, but with a counter capture.
          ________________
        8 |♜|♞|♝|_|♚|♝|♞|♜|
        7 |♟|♟|♟|♟|_|♟|♟|♟|
        6 |_|_|_|_|♟|_|_|_|
        5 |_|_|_|_|_|_|_|_|
        4 |_|_|_|_|_|♙|♙|♛|
        3 |_|_|_|_|_|♘|_|_|
        2 |♙|♙|♙|♙|♙|_|_|♙|
        1 |♖|♘|♗|♕|♔|♗|_|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """

        check_board = Board("♖♘♗♕♔♗_♖-♙♙♙♙♙__♙-_____♘__-_____♙♙♛-________-___♟____-♟♟♟_♟♟♟♟-♜♞♝_♚♝♞♜,W,0,0")
        assert_that(check_board.is_checkmate(Color.black), is_(False))
        assert_that(check_board.is_checkmate(Color.white), is_(False))

    def test_checkmate_5(self):
        """Simliar to the '2 move' checkmate. There is an empty square to move
        but that is also threatened.
          ________________
        8 |♜|♞|♝|_|♚|♝|♞|♜|
        7 |♟|♟|_|♟|_|♟|♟|♟|
        6 |_|_|_|_|♟|_|_|_|
        5 |_|_|_|_|_|_|_|_|
        4 |_|_|_|_|_|♙|♙|♛|
        3 |_|_|♟|♙|_|_|_|_|
        2 |♙|♙|♙|_|♙|_|_|♙|
        1 |♖|♘|♗|♕|♔|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """

        check_board = Board("♖♘♗♕♔♗♘♖-♙♙♙_♙__♙-__♟♙____-_____♙♙♛-________-___♟____-♟♟__♟♟♟♟-♜♞♝_♚♝♞♜,W,0,0")
        assert_that(check_board.is_checkmate(Color.black), is_(False))
        assert_that(check_board.is_checkmate(Color.white), is_(True))

    def test_statemate_1(self):
        """At the start of a game there is no stalemate as each player has
        moves and enough pieces for checkmate.
        """
        assert_that(self.board.is_stalemate(), is_(False))

    def test_statemate_2(self):
        """White player cannot move any piece.
          ________________
        8 |♜|♞|♝|_|♚|♝|♞|♜|
        7 |_|_|_|_|_|♟|♟|_|
        6 |_|_|_|_|♟|_|_|_|
        5 |_|_|_|_|_|_|_|_|
        4 |♟|_|♟|_|_|_|_|_|
        3 |♙|♟|♙|♟|_|♛|_|♟|
        2 |_|♙|_|♙|_|_|_|♙|
        1 |_|♘|♗|_|_|_|♔|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """
        stale_board = Board("_♘♗___♔♖-_♙_♙___♙-♙♟♙♟_♛_♟-♟_♟_____-________-___♟____-_____♟♟_-♜♞♝_♚♝♞♜,W,0,0")
        assert_that(stale_board.is_stalemate(), is_(True))

    def test_stalemate_3(self):
        """If a player has only one bishop or knight they cannot checkmate
         their opponent. If they have two only knights they cannot force
         checkmate (except rare case with opponent having a lone pawn).
         This tests for stalemate where neither player can achieve checkmate.
        """
        stale_board = Board("_♘____♔_-________-________-________-________-________-________-____♚___,W,0,0")
        assert_that(stale_board.is_stalemate(), is_(True))

    def test_stalemate_4(self):
        """If a player has a pawn, they can promote it. So it is not stalemate.
        """
        stale_board = Board("______♔_-♙_______-________-________-________-________-________-____♚___,W,0,0")
        assert_that(stale_board.is_stalemate(), is_(False))

    # TODO: test more castling combinations, and +ve / -ve testing
    def test_get_castle_moves(self):
        """Test castling left for both Black and White Kings.
          ________________
        8 |♜|_|_|_|♚|_|_|♜|
        7 |♟|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|♟|_|_|_|
        5 |_|_|_|_|_|_|_|_|
        4 |♟|_|♟|_|_|_|_|_|
        3 |♙|♟|♙|♟|_|♛|_|♟|
        2 |♙|♙|♙|♙|♙|♙|♙|♙|
        1 |♖|_|_|_|♔|_|_|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """
        castle_board = Board("♖___♔__♖-♙♙♙♙♙♙♙♙-________-________-________-________-♟♟♟♟♟♟♟♟-♜___♚__♜,W,0,0")
        from_1 = Square(5, 1)
        from_2 = Square(5, 8)
        assert_that(castle_board._get_castle_moves(from_1), contains_inanyorder((3, 1), (7, 1)))
        assert_that(castle_board._get_castle_moves(from_2), contains_inanyorder((3, 8), (7, 8)))

    def test_white_king_castle_left(self):
        """Test castling left for White King."""
        castle_board = Board("♖___♔__♖-♙♙♙♙♙♙♙♙-________-________-________-________-♟♟♟♟♟♟♟♟-♜___♚__♜,W,0,0")

        white_king = castle_board.get_piece((5, 1))
        white_rook = castle_board.get_piece((1, 1))
        assert_that(white_king, is_(WhiteKing))
        assert_that(white_rook, is_(WhiteRook))
        castle_board.move_piece(Square(5, 1), Square(3, 1))
        assert_that(castle_board.get_piece((3, 1)), is_(white_king))
        assert_that(castle_board.get_piece((4, 1)), is_(white_rook))

    def test_white_king_castle_right(self):
        """Test castling right for White King."""
        castle_board = Board("♖___♔__♖-♙♙♙♙♙♙♙♙-________-________-________-________-♟♟♟♟♟♟♟♟-♜___♚__♜,W,0,0")

        white_king = castle_board.get_piece((5, 1))
        white_rook = castle_board.get_piece((8, 1))
        assert_that(white_king, is_(WhiteKing))
        assert_that(white_rook, is_(WhiteRook))
        castle_board.move_piece(Square(5, 1), Square(7, 1))
        assert_that(castle_board.get_piece((7, 1)), is_(white_king))
        assert_that(castle_board.get_piece((6, 1)), is_(white_rook))

    def test_black_king_castle_left(self):
        """Test castling left for Black King.

          ________________
        8 |♜|_|_|_|♚|_|_|♜|
        7 |♟|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |♜|_|_|_|_|♙|_|♔|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♙|♙|♙|♙|♙|♙|♙|♙|
        1 |♖|_|_|_|♔|_|_|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """
        castle_board = Board("♖___♔__♖-♙♙♙♙♙♙♙♙-________-________-________-________-♟♟♟♟♟♟♟♟-♜___♚__♜,B,0,0")

        black_king = castle_board.get_piece((5, 8))
        black_rook = castle_board.get_piece((1, 8))
        assert_that(black_king, is_(BlackKing))
        assert_that(black_rook, is_(BlackRook))
        castle_board.move_piece(Square(5, 8), Square(3, 8))
        assert_that(castle_board.get_piece((3, 8)), is_(black_king))
        assert_that(castle_board.get_piece((4, 8)), is_(black_rook))

    def test_black_king_castle_right(self):
        """Test castling right for Black King.

           ________________
        8 |♜|_|_|_|♚|_|_|♜|
        7 |♟|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |♜|_|_|_|_|♙|_|♔|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♙|♙|♙|♙|♙|♙|♙|♙|
        1 |♖|_|_|_|♔|_|_|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H

        """
        castle_board = Board("♖___♔__♖-♙♙♙♙♙♙♙♙-________-________-________-________-♟♟♟♟♟♟♟♟-♜___♚__♜,B,0,0")

        black_king = castle_board.get_piece((5, 8))
        black_rook = castle_board.get_piece((8, 8))

        assert_that(black_king, is_(BlackKing))
        assert_that(black_rook, is_(BlackRook))
        castle_board.move_piece(Square(5, 8), Square(7, 8))

        assert_that(castle_board.get_piece((7, 8)), is_(black_king))
        assert_that(castle_board.get_piece((6, 8)), is_(black_rook))

    def test_board_repr_1(self):
        """Serialize a board, restore it and re-serialize it, it is the same as the original?"""
        board_string = self.board.__repr__()
        board_string = repr(self.board)
        new_board = Board(board_string)
        new_board_string = repr(new_board)
        assert_that(board_string, equal_to(new_board_string))

    def test_move_pawn_forward_1(self):
        """Test if a pawn can move forward one space into an empty square."""
        board_ = Board()
        from_ = Square(1, 2)
        to_ = Square(1, 3)
        piece = board_.get_piece(from_)
        assert_that(board_.get_piece(to_), is_(None))
        # Move the white Pawn
        board_.move_piece(from_, to_)
        assert_that(board_.get_piece(from_), is_(None))
        assert_that(board_.get_piece(to_), is_(piece))

    def test_move_pawn_forward_2(self):
        """Test whether a black pawn can move forward two spaces into an empty square.
        """
        board_ = Board()

        # Move a white pawn first
        from_1 = Square(2, 2)
        to_1 = Square(2, 4)
        white_pawn = board_.get_piece(from_1)
        board_.move_piece(from_1, to_1)
        assert_that(board_.get_piece(from_1), is_(None))
        assert_that(board_.get_piece(to_1), is_(white_pawn))

        from_2 = Square(4, 7)
        to_2 = Square(4, 5)
        new_moves = [(4, 4)]
        assert_that(board_.get_piece(to_2), is_(None))
        black_pawn = board_.get_piece(from_2)
        # Move the Black Pawn
        board_.move_piece(from_2, to_2)
        assert_that(board_.get_piece(from_2), is_(None))
        assert_that(board_.get_piece(to_2), is_(black_pawn))
        assert_that(board_.get_moves(to_2), contains_inanyorder(*new_moves))

    # TODO: assertRaises (part of unittest doesn't appear to like custom exceptions)
#    def test_move_pawn_invalid(self):
#        """Test whether a pawn can move forward two spaces into an empty square."""
#        board_ = Board()
#        from_ = Square(4,7)
#        to_ = Square(4,4)
#        assert_that(board_.get_piece(to_), is_(None))
#        piece = board_.get_piece(from_)
        # Try to move the piece, check execption and that nothing changed
        # Commented out assrtRaises, see comment above
#        self.assertRaises(board.IllegalMoveException, board_.move_piece(from_, to_))
#        assert_that(board_.get_piece(from_), is_(piece))
#        assert_that(board_.get_piece(to_), is_(None))

    def test_move_knight(self):
        """Test whether a knight can move in its 'L' shape
        """
        board_ = Board()
        from_ = Square(2, 1)
        to_ = Square(3, 3)
        assert_that(board_.get_piece(to_), is_(None))
        piece = board_.get_piece(from_)
        # Move White Knight
        board_.move_piece(from_, to_)
        assert_that(board_.get_piece(from_), is_(None))
        assert_that(board_.get_piece(to_), is_(piece))

    def test_move_bishop(self):
        """Test whether a white bishop can move diagonally.
        """
        board_ = Board()
        # Move pawn out of the way 1st
        from_ = Square(4, 2)
        to_ = Square(4, 3)
        board_.move_piece(from_, to_)

        # Move a black pawn
        from_ = Square(4, 7)
        to_ = Square(4, 6)
        board_.move_piece(from_, to_)

        from_ = Square(3, 1)
        to_ = Square(7, 5)
        piece = board_.get_piece(from_)

        # Move White Bishop
        board_.move_piece(from_, to_)
        assert_that(board_.get_piece(from_), is_(None))
        assert_that(board_.get_piece(to_), is_(piece))

    def test_move_queen_forward(self):
        board_ = Board()
        # Move pawn out of the way 1st
        from_ = Square(4, 2)
        to_ = Square(4, 4)
        board_.move_piece(from_, to_)

        # Move a black pawn
        from_ = Square(4, 7)
        to_ = Square(4, 6)
        board_.move_piece(from_, to_)

        from_ = Square(4, 1)
        to_ = Square(4, 3)
        piece = board_.get_piece(from_)
        # Move White Queen
        board_.move_piece(from_, to_)
        assert_that(board_.get_piece(from_), is_(None))
        assert_that(board_.get_piece(to_), is_(piece))

    def test_move_rook(self):
        """Test the moves of a rook."""
        board_ = Board()

        # Move a white pawn
        from_1 = Square(4, 2)
        to_1 = Square(4, 3)
        board_.move_piece(from_1, to_1)

        # Move pawn out of the way 1st
        from_2 = Square(8, 7)
        to_2 = Square(8, 5)
        board_.move_piece(from_2, to_2)

        # Move a another white pawn
        from_3 = Square(2, 2)
        to_3 = Square(2, 3)
        board_.move_piece(from_3, to_3)

        from_4 = Square(8, 8)
        to_4 = Square(8, 6)
        piece = board_.get_piece(from_4)

        # Move black rook vertically
        board_.move_piece(from_4, to_4)
        assert_that(board_.get_piece(from_4), is_(None))
        assert_that(board_.get_piece(to_4), is_(piece))

        # Move a third white pawn
        from_5 = Square(1, 2)
        to_5 = Square(1, 3)
        board_.move_piece(from_5, to_5)

        # Move again horizontally
        from_ = to_4
        to_ = Square(4, 6)
        board_.move_piece(from_, to_)
        assert_that(board_.get_piece(from_), is_(None))
        assert_that(board_.get_piece(to_), is_(piece))

    def test_move_king_diagonally(self):
        """Test moving the king diagonally."""
        board_ = Board()
        # Move pawn out of the way 1st
        from_1 = Square(5, 2)
        to_1 = Square(5, 3)
        board_.move_piece(from_1, to_1)

        # Move a black knight (we need to do any black move)
        from_2 = Square(2, 8)
        to_2 = Square(3, 6)
        board_.move_piece(from_2, to_2)

        # Locate the king
        from_3 = Square(5, 1)
        to_3 = Square(5, 2)
        piece = board_.get_piece(from_3)

        # Move the king
        board_.move_piece(from_3, to_3)
        assert_that(board_.get_piece(from_3), is_(None))
        assert_that(board_.get_piece(to_3), is_(piece))

    def test_en_passant(self):
        """Test whether a pawn can capture another via en-passant.

        This does a lot of extra moves because it starts from a new board.
        """
        board_ = Board()
        # Move the white pawn first
        from_1 = Square(5, 2)
        to_1 = Square(5, 4)
        board_.move_piece(from_1, to_1)

        # Move the a black pawn to switch turn
        from_2 = Square(1, 7)
        to_2 = Square(1, 5)
        board_.move_piece(from_2, to_2)

        # Move it again, (we're allowed, the rules of a game don't apply just for board)
        from_3 = to_1
        to_3 = Square(5, 5)
        board_.move_piece(from_3, to_3)
        white_pawn = board_.get_piece(to_3)

        # Move a black pawn 'passed' this one
        black_pawn_loc = Square(4, 5)
        board_.move_piece(Square(4, 7), black_pawn_loc)

        # print board_.display()

        # Pre-move
        from_ = Square(5, 5)
        to_ = Square(4, 6)
        white_pawn = board_.get_piece(from_)
        black_pawn = board_.get_piece(black_pawn_loc)
        # Check the board is as we expect
        assert_that(board_.get_piece(from_), is_(white_pawn))
        assert_that(board_.get_piece(to_), is_(None))
        assert_that(board_.get_piece(black_pawn_loc), is_(black_pawn))

        # Capture via en passant
        board_.move_piece(from_, to_)
        assert_that(board_.get_piece(from_), is_(None))
        assert_that(board_.get_piece(to_), is_(white_pawn))
        assert_that(board_.get_piece(black_pawn_loc), is_(None))

    def test_en_passant_2(self):
        """In this test we should be able to capture via test_en_passant except
           that would put our king in check, therefore our pawn cannot move

           ________________
        8 |♜|♞|♝|♛|♚|♝|♞|_|
        7 |♟|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |♜|_|_|_|_|♙|_|♔|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♙|♙|♙|♙|♙|_|♙|♙|
        1 |♖|♘|♗|♕|_|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """

        chess_board = Board("♖♘♗♕_♗♘♖-♙♙♙♙♙_♙♙-________-________-♜____♙_♔-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞_,B,0,0")

        # Move the black pawn a doulbe step
        from_ = Square(5, 7)
        to_ = Square(5, 5)
        chess_board.move_piece(from_, to_)

        white_pawn_loc = Square(6, 5)
        pawn_moves = chess_board.get_moves(white_pawn_loc)

        # We can't capture the pawn because it would put our king in check, but we can move forward
        assert_that(pawn_moves, equal_to([(6, 6)]))

    def test_en_passant_3(self):
        """This is like test_en_passant_2 except the pawn can legally take the enemy piece
           via en passant.

           ________________
        8 |♜|♞|♝|♛|♚|♝|♞|♜|
        7 |♟|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|_|♙|_|♔|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♙|♙|♙|♙|♙|_|♙|♙|
        1 |♖|♘|♗|♕|_|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """

        chess_board = Board("♖♘♗♕_♗♘♖-♙♙♙♙♙_♙♙-________-________-_____♙_♔-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,B,0,0")

        # Move the black pawn a doulbe step
        from_ = Square(5, 7)
        to_ = Square(5, 5)
        chess_board.move_piece(from_, to_)

        white_pawn_loc = Square(6, 5)
        white_en_passant_attack = (5, 6)
        white_en_move_forward = (6, 6)

        pawn_moves = chess_board.get_moves(white_pawn_loc)

        #We can't capture the pawn because it would put our king in check
        assert_that(pawn_moves, contains_inanyorder(white_en_passant_attack, white_en_move_forward))


class TestSpecificScenarios(unittest.TestCase):
    u"""These are additional tests to check specific scenarios noticed during manual testing."""

    def test_four_move_check_mate(self):
        """This was found to not work correctly during manual testing.
           The king thought it could safely capture the queen ...

           The final board looks like the following:

           ________________
        8 |♜|_|♝|♛|♚|♝|♞|♜|
        7 |♟|♟|♟|_|_|♕|♟|♟|
        6 |_|_|♞|♟|_|_|_|_|
        5 |_|_|_|_|♟|_|_|_|
        4 |_|_|♗|_|♙|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♟|♙|♙|♙|_|♙|♙|♙|
        1 |♖|♘|♗|_|♔|_|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H

        """

        chess_board = Board()
        # Double move white pawn
        from_ = Square(5, 2)
        to_ = Square(5, 4)
        chess_board.move_piece(from_, to_)

        # Double move black pawn
        from_ = Square(5, 7)
        to_ = Square(5, 5)
        chess_board.move_piece(from_, to_)

        # Move out white bishop
        from_ = Square(6, 1)
        to_ = Square(3, 4)
        chess_board.move_piece(from_, to_)

        # Move out black queenside pawn
        from_ = Square(4, 7)
        to_ = Square(4, 6)
        chess_board.move_piece(from_, to_)

       # Move out white queen
        from_ = Square(4, 1)
        to_ = Square(6, 3)
        chess_board.move_piece(from_, to_)

        # Move out black queenside knight
        from_ = Square(2, 8)
        to_ = Square(3, 6)
        chess_board.move_piece(from_, to_)

        # Checkmate with white queen
        from_ = Square(6, 3)
        to_ = Square(6, 7)
        chess_board.move_piece(from_, to_)

        assert_that(chess_board.winner, is_(Color.white))
        print chess_board.display()


class TestPromotePawns(unittest.TestCase):
    u"""These tests check that a pawn can be promoted correctly."""

    def test_promote_pawn_to_queen(self):
        """Tests the promotion of a pawn to a queen.

           The board looks like the following:

           ________________
        8 |♜|♞|♝|♛|♚|♝|♞|♜|
        7 |_|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|_|_|_|_|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♟|♙|♙|♙|♙|♙|♙|♙|
        1 |_|♘|♗|♕|♔|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """

        chess_board = Board("_♘♗♕♔♗♘♖-♟♙♙♙♙♙♙♙-________-________-________-________-_♟♟♟♟♟♟_-♜♞♝♛♚♝♞♜,B,0,0")
        from_ = Square(1, 2)
        to_ = Square(1, 1)
        chess_board.move_piece(from_, to_)
        chess_board.promote_pawn(BlackQueen())
        black_queen = chess_board.get_piece(to_)
        assert_that(black_queen, instance_of(BlackQueen))

    def test_promote_pawn_to_rook(self):
        """Tests the promotion of a pawn to a rook.

           The board looks like the following:

           ________________
        8 |♜|♞|♝|♛|♚|♝|♞|♜|
        7 |_|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|_|_|_|_|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♟|♙|♙|♙|♙|♙|♙|♙|
        1 |_|♘|♗|♕|♔|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """

        chess_board = Board("_♘♗♕♔♗♘♖-♟♙♙♙♙♙♙♙-________-________-________-________-_♟♟♟♟♟♟_-♜♞♝♛♚♝♞♜,B,0,0")
        from_ = Square(1, 2)
        to_ = Square(1, 1)
        chess_board.move_piece(from_, to_)
        chess_board.promote_pawn(BlackRook())
        black_rook = chess_board.get_piece(to_)
        assert_that(black_rook, instance_of(BlackRook))

    def test_promote_pawn_to_bishop(self):
        """Tests the promotion of a pawn to a bishop.

           The board looks like the following:

           ________________
        8 |♜|♞|♝|♛|♚|♝|♞|♜|
        7 |_|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|_|_|_|_|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♟|♙|♙|♙|♙|♙|♙|♙|
        1 |_|♘|♗|♕|♔|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """

        chess_board = Board("_♘♗♕♔♗♘♖-♟♙♙♙♙♙♙♙-________-________-________-________-_♟♟♟♟♟♟_-♜♞♝♛♚♝♞♜,B,0,0")
        from_ = Square(1, 2)
        to_ = Square(1, 1)
        chess_board.move_piece(from_, to_)
        chess_board.promote_pawn(BlackBishop())
        black_bishop = chess_board.get_piece(to_)
        assert_that(black_bishop, instance_of(BlackBishop))

    def test_promote_pawn_to_knight(self):
        """Tests the promotion of a pawn to a knight.

           The board looks like the following:

           ________________
        8 |♜|♞|♝|♛|♚|♝|♞|♜|
        7 |_|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|_|_|_|_|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♟|♙|♙|♙|♙|♙|♙|♙|
        1 |_|♘|♗|♕|♔|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """

        chess_board = Board("_♘♗♕♔♗♘♖-♟♙♙♙♙♙♙♙-________-________-________-________-_♟♟♟♟♟♟_-♜♞♝♛♚♝♞♜,B,0,0")
        from_ = Square(1, 2)
        to_ = Square(1, 1)
        chess_board.move_piece(from_, to_)
        chess_board.promote_pawn(BlackKnight())
        black_knight = chess_board.get_piece(to_)
        assert_that(black_knight, instance_of(BlackKnight))

    def test_promote_pawn_to_king(self):
        """Tests the promotion of a pawn to a king. This is not allowed, so should raise TypeError

           The board looks like the following:

           ________________
        8 |♜|♞|♝|♛|♚|♝|♞|♜|
        7 |_|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|_|_|_|_|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♟|♙|♙|♙|♙|♙|♙|♙|
        1 |_|♘|♗|♕|♔|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """

        chess_board = Board("_♘♗♕♔♗♘♖-♟♙♙♙♙♙♙♙-________-________-________-________-_♟♟♟♟♟♟_-♜♞♝♛♚♝♞♜,B,0,0")
        from_ = Square(1, 2)
        to_ = Square(1, 1)
        chess_board.move_piece(from_, to_)
        # should raise an exception for an invalid piece
        self.assertRaises(TypeError, chess_board.promote_pawn, BlackKing)

    def test_promote_pawn_to_pawn(self):
        """Tests the promotion of a pawn to a pawn. This is not allowed, so should raise TypeError

           The board looks like the following:

           ________________
        8 |♜|♞|♝|♛|♚|♝|♞|♜|
        7 |_|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|_|_|_|_|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♟|♙|♙|♙|♙|♙|♙|♙|
        1 |_|♘|♗|♕|♔|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """

        chess_board = Board("_♘♗♕♔♗♘♖-♟♙♙♙♙♙♙♙-________-________-________-________-_♟♟♟♟♟♟_-♜♞♝♛♚♝♞♜,B,0,0")
        from_ = Square(1, 2)
        to_ = Square(1, 1)
        chess_board.move_piece(from_, to_)
        # should raise an exception for an invalid piece
        self.assertRaises(TypeError, chess_board.promote_pawn, BlackPawn)

    def test_promote_pawn_in_wrong_location(self):
        """Tests the promotion of a pawn to a in the wron location. This is not allowed, so should raise TypeError

           The board looks like the following:

           ________________
        8 |♜|♞|♝|♛|♚|♝|♞|♜|
        7 |♟|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|_|_|_|_|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♙|♙|♙|♙|♙|♙|♙|♙|
        1 |♖|♘|♗|♕|♔|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """

        chess_board = Board("♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-________-________-________-♟♟♟♟♟♟♟_-♜♞♝♛♚♝♞♜,B,0,0")

        # should raise an exception for an invalid piece
        self.assertRaises(IllegalMoveException, chess_board.promote_pawn, BlackKnight)

    def test_move_before_promote(self):
        """Tests that promotion is required before moving to the next move.

           The board looks like the following:

           ________________
        8 |♜|♞|♝|♛|♚|♝|♞|♜|
        7 |_|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|_|_|_|_|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♟|♙|♙|♙|♙|♙|♙|♙|
        1 |_|♘|♗|♕|♔|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """

        chess_board = Board("_♘♗♕♔♗♘♖-♟♙♙♙♙♙♙♙-________-________-________-________-_♟♟♟♟♟♟_-♜♞♝♛♚♝♞♜,B,0,0")
        from_ = Square(1, 2)
        to_ = Square(1, 1)
        chess_board.move_piece(from_, to_)

        from_2 = Square(2, 2)
        to_2 = Square(2, 3)
        # should raise an exception for because the previous peice has not been promoted
        self.assertRaises(IllegalMoveException, chess_board.move_piece, from_2, to_2)


class TestDisplayFunctions(unittest.TestCase):
    def setUp(self):
        pass

    @unittest.skip("Format not finalized.")
    def test_board_display_json(self):
        """This function tests that the display method produces valid JSON of a consistent format."""

        board = Board()

        expected_json = json.loads(u"""{
            "current_player":"white",
            "board": [
                {
                    "x": 1,
                    "y": 1,
                    "piece": "white_rook",
                    "color": "white",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 2,
                    "y": 1,
                    "piece": "white_knight",
                    "color": "white",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 3,
                    "y": 1,
                    "piece": "white_bishop",
                    "color": "white",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 4,
                    "y": 1,
                    "piece": "white_queen",
                    "color": "white",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 5,
                    "y": 1,
                    "piece": "white_king",
                    "color": "white",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 6,
                    "y": 1,
                    "piece": "white_bishop",
                    "color": "white",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 7,
                    "y": 1,
                    "piece": "white_knight",
                    "color": "white",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 8,
                    "y": 1,
                    "piece": "white_rook",
                    "color": "white",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                                {
                    "x": 1,
                    "y": 2,
                    "piece": "white_pawn",
                    "color": "white",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 2,
                    "y": 2,
                    "piece": "white_pawn",
                    "color": "white",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 3,
                    "y": 2,
                    "piece": "white_pawn",
                    "color": "white",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 4,
                    "y": 2,
                    "piece": "white_pawn",
                    "color": "white",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 5,
                    "y": 2,
                    "piece": "white_pawn",
                    "color": "white",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 6,
                    "y": 2,
                    "piece": "white_pawn",
                    "color": "white",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 7,
                    "y": 2,
                    "piece": "white_pawn",
                    "color": "white",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 8,
                    "y": 2,
                    "piece": "white_pawn",
                    "color": "white",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 1,
                    "y": 8,
                    "piece": "black_rook",
                    "color": "black",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 2,
                    "y": 8,
                    "piece": "black_knight",
                    "color": "black",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 3,
                    "y": 8,
                    "piece": "black_bishop",
                    "color": "black",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 4,
                    "y": 8,
                    "piece": "black_queen",
                    "color": "black",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 5,
                    "y": 8,
                    "piece": "black_king",
                    "color": "black",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 6,
                    "y": 8,
                    "piece": "black_bishop",
                    "color": "black",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 7,
                    "y": 8,
                    "piece": "black_knight",
                    "color": "black",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 8,
                    "y": 8,
                    "piece": "black_rook",
                    "color": "black",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                                {
                    "x": 1,
                    "y": 7,
                    "piece": "black_pawn",
                    "color": "black",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 2,
                    "y": 7,
                    "piece": "black_pawn",
                    "color": "black",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 3,
                    "y": 7,
                    "piece": "black_pawn",
                    "color": "black",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 4,
                    "y": 7,
                    "piece": "black_pawn",
                    "color": "black",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 5,
                    "y": 7,
                    "piece": "black_pawn",
                    "color": "black",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 6,
                    "y": 7,
                    "piece": "black_pawn",
                    "color": "black",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 7,
                    "y": 7,
                    "piece": "black_pawn",
                    "color": "black",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                },
                {
                    "x": 8,
                    "y": 7,
                    "piece": "black_pawn",
                    "color": "black",
                    "moved": false,
                    "moves": [],
                    "attacks": []
                }
            ],
            "previous_moves": [],
            "status": "IN_PROGRESS"
        }""")

        result_json = json.loads(board.json())

        assert_that(result_json[u'current_player'], equal_to(expected_json[u'current_player']))
        assert_that(result_json[u'previous_moves'], equal_to(expected_json[u'previous_moves']))
        assert_that(result_json[u'status'], equal_to(expected_json[u'status']))

        # Check that the board contains the same pieces
        assert_that(result_json[u'board'], contains_inanyorder(*expected_json[u'board']))


if __name__ == '__main__':
        unittest.main()
