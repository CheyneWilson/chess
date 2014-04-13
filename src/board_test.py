# -*- coding: UTF-8 -*-
# Unit tests for chess. Requires PyHamcrest to be installed.
# This can be easily done using any packaging tool (such as distribute).
# See https://code.google.com/p/hamcrest/ for more details on hamcrest matchers
from board import Board, Color, King, Queen, Bishop, Knight, Rook, Pawn, BlackPawn, WhiteKing, WhiteRook, \
    BlackKing, BlackQueen, BlackRook, BlackBishop, BlackKnight, IllegalMoveException, Square
from hamcrest import is_, assert_that, equal_to, all_of, contains_inanyorder, instance_of
import unittest
import json


# @unittest.skip("focusing on only one test")
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
            self.board.get_piece('a1'), is_(Rook)),
            self.board.get_piece('a1').color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece('b1'), is_(Knight)),
            self.board.get_piece('b1').color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece('c1'), is_(Bishop)),
            self.board.get_piece('c1').color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece('d1'), is_(King)),
            self.board.get_piece('d1').color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece('e1'), is_(Queen)),
            self.board.get_piece('e1').color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece('f1'), is_(Bishop)),
            self.board.get_piece('f1').color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece('g1'), is_(Knight)),
            self.board.get_piece('g1').color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece('h1'), is_(Rook)),
            self.board.get_piece('h1').color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece('a2'), is_(Pawn)),
            self.board.get_piece('a2').color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece('b2'), is_(Pawn)),
            self.board.get_piece('b2').color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece('b2'), is_(Pawn)),
            self.board.get_piece('b2').color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece('c2'), is_(Pawn)),
            self.board.get_piece('c2').color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece('d2'), is_(Pawn)),
            self.board.get_piece('d2').color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece('e2'), is_(Pawn)),
            self.board.get_piece('e2').color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece('f2'), is_(Pawn)),
            self.board.get_piece('f2').color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece('g2'), is_(Pawn)),
            self.board.get_piece('g2').color, is_(Color.white)
        )
        assert_that(all_of(
            self.board.get_piece('h2'), is_(Pawn)),
            self.board.get_piece('h2').color, is_(Color.white)
        )

        # Using 'internal' method get_piece check all of the Black pieces
        assert_that(all_of(
            self.board.get_piece('a8'), is_(Rook)),
            self.board.get_piece('a8').color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece('b8'), is_(Knight)),
            self.board.get_piece('b8').color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece('c8'), is_(Bishop)),
            self.board.get_piece('c8').color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece('d8'), is_(King)),
            self.board.get_piece('d8').color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece('e8'), is_(Queen)),
            self.board.get_piece('e8').color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece('f8'), is_(Bishop)),
            self.board.get_piece('f8').color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece('g8'), is_(Knight)),
            self.board.get_piece('g8').color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece('h8'), is_(Rook)),
            self.board.get_piece('h8').color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece('a7'), is_(Pawn)),
            self.board.get_piece('a7').color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece('b7'), is_(Pawn)),
            self.board.get_piece('b7').color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece('b7'), is_(Pawn)),
            self.board.get_piece('b7').color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece('c7'), is_(Pawn)),
            self.board.get_piece('c7').color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece('d7'), is_(Pawn)),
            self.board.get_piece('d7').color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece('e7'), is_(Pawn)),
            self.board.get_piece('e7').color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece('f7'), is_(Pawn)),
            self.board.get_piece('f7').color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece('g7'), is_(Pawn)),
            self.board.get_piece('g7').color, is_(Color.black)
        )
        assert_that(all_of(
            self.board.get_piece('h7'), is_(Pawn)),
            self.board.get_piece('h7').color, is_(Color.black)
        )

        # Check all the other squares are empty
        # This will return a horrible error message if it fails,
        # not telling us which square is wrong, but at least we'll
        # know to dig deeper.
        # Using range instead of xrange for if/when we go to python 3
        for x in range(1, 9):
            for y in range(3, 7):
                name = chr(ord(u'A') + x - 1) + str(y)
                assert_that(self.board.get_piece(name), is_(None))

    def test_get_moves_opening_white_pawn(self):
        """Check that a white pawn can move from it's starting position as either a single or double move."""
        pawn_moves = self.board.get_moves('a2')
        assert_that(pawn_moves, contains_inanyorder('A3', 'A4'))

    def test_get_moves_opening_black_pawn(self):
        """Check that a black pawn can move from it's starting position as either a single or double move."""
        pawn_moves = self.board.get_moves('f7')
        assert_that(pawn_moves, contains_inanyorder('F6', 'F5'))

    def test_get_moves_moved_white_pawn(self):
        """Check that a white pawn that has moved can only move one space (when nothing to attack)."""
        pawn_board = Board("♖♘♗♕♔♗♘♖-♙♙_♙♙♙♙♙-__♙_____-________-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        pawn_moves = pawn_board.get_moves('c3')
        assert_that(pawn_moves, contains_inanyorder('C4'))

    def test_get_moves_white_pawn_attacks_both(self):
        """Check that a white pawn with 3 Black pieces in front can attack the two pieces on the sides only"""
        pawn_board = Board("♖♘♗♕♔♗♘♖-♙♙♙_♙♙♙♙-________-________-________-___♙___-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        pawn_moves = pawn_board.get_moves('d6')
        assert_that(pawn_moves, contains_inanyorder('C7', 'E7'))

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
        pawn_moves = pawn_board.get_moves('h5')
        assert_that(pawn_moves, contains_inanyorder('G4'))

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
        pawn_moves = pawn_board.get_moves('H5')
        assert_that(pawn_moves, is_(set([])))

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
        pawn_moves = pawn_board.get_moves('h2')
        assert_that(pawn_moves, contains_inanyorder('H1'))

        pawn_moves = pawn_board.move_piece('h2', 'h1')

        self.assertRaises(IllegalMoveException, pawn_board.get_moves, 'h1')

    # TODO:
    # Add more tests for the following
    # * Cannot attack own color

    def test_get_moves_white_knight_opening(self):
        """Check the opening moves of a white knight."""
        knight_moves = self.board.get_moves('b1')
        assert_that(knight_moves, contains_inanyorder('A3', 'C3'))

    def test_get_moves_black_knight_opening(self):
        """Check the opening moves of a black knight."""
        knight_moves = self.board.get_moves('g8')
        assert_that(knight_moves, contains_inanyorder('F6', 'H6'))

    def test_get_moves_knight_fork_attack(self):
        """Check if a knight at G3 can fork the king and rook, as well as other moves."""
        knight_board = Board("♖_♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-________-________-________-♟♟♘♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        knight_moves = knight_board.get_moves('c7')
        assert_that(knight_moves, contains_inanyorder(
            'A8', 'E8', 'A6', 'E6', 'B5', 'D5'
        ))

    def test_get_moves_white_bishop_opening(self):
        """Check the opening moves of a white bishop."""
        bishop_moves = self.board.get_moves('c1')
        assert_that(bishop_moves, is_(set([])))

    def test_get_moves_black_bishop_opening(self):
        """Check the opening moves of a black bishop."""
        bishop_moves = self.board.get_moves('c8')
        assert_that(bishop_moves, is_(set([])))

    def test_get_moves_white_bishop_free(self):
        """Test get_moves for a white bishop in the middle of the board."""
        bishop_board = Board("♖♘_♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-________-____♗___-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        bishop_moves = bishop_board.get_moves('e5')
        assert_that(bishop_moves, contains_inanyorder(
            'D6', 'C7',  # forward left
            'F6', 'G7',  # forward right
            'D4', 'C3',  # backward left
            'F4', 'G3'   # backward right
        ))

    def test_get_moves_black_bishop_free(self):
        """Test get_moves for a black bishop in the middle of the board."""
        bishop_board = Board("♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-________-___♝____-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚_♞♜,W,0,0")
        bishop_moves = bishop_board.get_moves('d5')
        assert_that(bishop_moves, contains_inanyorder(
            'C6',  # (2, 7),  # forward left
            'E6',  # (6, 7),  # forward right
            'C4', 'B3', 'A2',  # backward left
            'E4', 'F3', 'G2'   # backward right
        ))

    def test_get_moves_white_rook_opening(self):
        """Test get_moves for the opening moves of a white rook."""
        rook_moves = self.board.get_moves('h1')
        assert_that(rook_moves, is_(set([])))

    def test_get_moves_black_rook_opening(self):
        """Test get_moves for the opening moves of a black rook."""
        rook_moves = self.board.get_moves('h8')
        assert_that(rook_moves, is_(set([])))

    def test_get_moves_white_rook_free(self):
        """Test get_moves for a white rook in the middle of the board.

        The board looks like:
           ________________
        8 |♜|♞|♝|♛|♚|♝|♞|♜|
        7 |♟|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|_|_|_|_|
        4 |_|_|_|_|_|_|_|_|
        3 |_|♖|_|_|_|_|_|_|
        2 |♙|♙|♙|♙|♙|♙|♙|♙|
        1 |♖|♘|♗|♕|♔|♗|♘|_|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H

        """
        rook_board = Board("♖♘♗♕♔♗♘_-♙♙♙♙♙♙♙♙-_♖______-________-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        rook_moves = rook_board.get_moves('b3')

        assert_that(rook_moves, contains_inanyorder(
            'B4', 'B5', 'B6', 'B7',  # FORWARD
            'C3', 'D3', 'E3', 'F3', 'G3', 'H3',  # RIGHT
            'A3'  # LEFT
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

        rook_board = Board("♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-_♜______-________-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞_,B,0,0")
        rook_moves = rook_board.get_moves('b3')
        assert_that(rook_moves, contains_inanyorder(
            'B4', 'B5', 'B6',  # backward
            'C3', 'D3', 'E3', 'F3', 'G3', 'H3',  # right
            'A3',  # left
            'B2'  # forward
        ))

    def test_get_moves_white_queen_opening(self):
        """Test get_moves for the opening moves of a white queen."""
        queen_moves = self.board.get_moves('d1')
        assert_that(queen_moves, is_(set([])))

    def test_get_moves_black_queen_opening(self):
        """Test get_moves for the opening moves of a black queen."""
        queen_moves = self.board.get_moves('d8')
        assert_that(queen_moves, is_(set([])))

    def test_get_moves_white_queen_free(self):
        """Check the moves of a white queen in the open."""
        queen_board = Board("♖♘♗_♔♗♘♖-♙♙♙♙♙♙♙♙-________-___♕____-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        queen_moves = queen_board.get_moves('d4')
        assert_that(queen_moves, contains_inanyorder(
            'D5', 'D6', 'D7',  # forward
            'E5', 'F6', 'G7',  # forward right
            'E4', 'F4', 'G4', 'H4',  # right
            'E3',  # backwards right
            'D3',  # backward
            'C3',  # backwards left
            'C4', 'B4', 'A4',  # left
            'C5', 'B6', 'A7'  # forward, left
        ))

    def test_get_moves_black_queen_free(self):
        """Check the moves of a black queen in the open."""
        queen_board = Board("♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-___♛____-________-________-♟♟♟♟♟♟♟♟-♜♞♝_♚♝♞♜,W,0,0")
        queen_moves = queen_board.get_moves('d4')
        assert_that(queen_moves, contains_inanyorder(
            'D5', 'D6',  # forward
            'E5', 'F6',  # forward right
            'E4', 'F4', 'G4', 'H4',  # right
            'E3', 'F2',  # backwards right
            'D3', 'D2',  # backward
            'C3', 'B2',  # backwards left
            'C4', 'B4', 'A4',  # left
            'C5', 'B6'  # forward, left
        ))

    def test_get_moves_white_king_opening(self):
        """Check the opening moves of a white king."""
        king_moves = self.board.get_moves('e1')
        assert_that(king_moves, is_(set([])))

    def test_get_moves_black_king_opening(self):
        """Check the opening moves of a black king."""
        king_moves = self.board.get_moves('e8')
        assert_that(king_moves, is_(set([])))

    def test_get_moves_white_king_free(self):
        """Check the moves of a white king in the open."""
        king_board = Board("♖♘♗♕_♗♘♖-♙♙♙♙♙♙♙♙-________-___m♔____-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        king_moves = king_board.get_moves('d4')
        assert_that(king_moves, contains_inanyorder(
            'D5',  # forward
            'E5',  # forward right
            'E4',  # right
            'E3',  # backwards right
            'D3',  # backward
            'C3',  # backwards left
            'C4',  # left
            'C5'   # forward, left
        ))

    def test_get_moves_black_king_partially_free(self):
        """Check the moves of a black king in front of white pawns."""
        king_board = Board("♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-___m♚____-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛_♝♞♜,W,0,0")
        king_moves = king_board.get_moves('d4')
        assert_that(king_moves, contains_inanyorder(
            'D5',  # forward
            'E5',  # forward right
            'E4',  # right
            'C4',  # left
            'C5'   # forward, left
        ))

    def test_get_moves_pinned_knight(self):
        """Check that a pinned knight cannot move (as there is no way for it to still be blocking check if it moves)

        The board looks like:
           ________________
        8 |♜|♞|♝|♛|♚|♝|♞|_|
        7 |♟|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|♜|_|_|_|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♙|♙|♙|♙|♘|♙|♙|♙|
        1 |♖|♘|♗|♕|♔|♗|_|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H

        """
        pinned_board = Board("♖♘♗♕♔♗_♖-♙♙♙♙♘♙♙♙-________-________-____♜___-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞_,W,0,0")
        knight_moves = pinned_board.get_moves('e2')
        assert_that(knight_moves, is_(set([])))

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
        pawn_moves = pinned_board.get_moves('e2')
        assert_that(pawn_moves, contains_inanyorder('E3', 'E4'))

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
        pawn_moves = pinned_board.get_moves('e2')
        assert_that(pawn_moves, contains_inanyorder('E3', 'E4'))

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
        pawn_moves = pinned_board.get_moves('f4')
        assert_that(pawn_moves, contains_inanyorder('F3'))

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
        pawn_moves = pinned_board.get_moves('f4')
        assert_that(pawn_moves, is_(set([])))

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
        pawn_moves = pinned_board.get_moves('f7')
        assert_that(pawn_moves, is_(set([])))

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
        pawn_moves = pinned_board.get_moves('f7')
        assert_that(pawn_moves, contains_inanyorder('G6'))

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
        pawn_moves = pinned_board.get_moves('f7')
        assert_that(pawn_moves, contains_inanyorder('G6'))

    def test_get_attackers(self):
        # Check black queens pawn E7
        to_ = Square('c7')
        d8 = Square('d8')
        attackers_3_7 = self.board._get_attackers(to_, Color.black)
        assert_that(attackers_3_7, contains_inanyorder(d8))

    def test_get_attackers_1_a(self):
        # Test some white pawns
        to_ = Square('b3')
        a2 = Square('a2')
        c2 = Square('c2')
        attackers_2_3 = self.board._get_attackers(to_, Color.white)
        assert_that(attackers_2_3, contains_inanyorder(a2, c2))

    def test_get_attackers_1_b(self):
        # Two pawns and a knight can attack 3,3 (C3)
        to_ = Square('c3')
        b1 = Square('b1')
        b2 = Square('b2')
        d2 = Square('d2')
        attackers_3_3 = self.board._get_attackers(to_, Color.white)
        assert_that(attackers_3_3, contains_inanyorder(b2, d2, b1))

    def test_get_attackers_1_c(self):
        # Check pawn in front of white rook
        to_ = Square('h2')
        h1 = Square('h1')
        attackers_8_2 = self.board._get_attackers(to_, Color.white)
        assert_that(attackers_8_2, contains_inanyorder(h1))

    def test_get_attackers_1_e(self):
        # Check black kings pawn E7
        to_ = Square('f7')
        e8 = Square('e8')
        attackers_6_7 = self.board._get_attackers(to_, Color.black)
        assert_that(attackers_6_7, contains_inanyorder(e8))

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
        to_ = Square('e2')
        attackers_5_2 = self.board._get_attackers(to_, Color.white)
        assert_that(attackers_5_2, contains_inanyorder(
            Square('d1'), Square('e1'), Square('f1'), Square('g1')
        ))

    def test_is_check_1(self):
        """Neither king starts off in check. Test for a fresh board."""
        assert_that(self.board.is_check(), is_(False))

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
        assert_that(check_board.is_check(), is_(True))

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
        check_board = Board("♖♘♗♕♔♗♘_-♙♙♙♙♙♙♙♙-________-________-____♚__♖-________-♟♟♟♟♟♟♟♟-♜♞♝♛_♝♞♜,B,0,0")
        assert_that(check_board.is_check(), is_(True))

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
        check_board = Board("♖♘♗_♔♗♘♖-♙♙♙♙♙♙♙♙-________-________-____♚__♕-________-♟♟♟♟♟♟♟♟-♜♞♝♛_♝♞♜,B,0,0")
        assert_that(check_board.is_check(), is_(True))

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
        check_board = Board("♖♘♗_♔♗♘♖-♙♙♙♙♙♙♙♙-____♕___-________-____♚___-________-♟♟♟♟♟♟♟♟-♜♞♝♛_♝♞♜,B,0,0")
        assert_that(check_board.is_check(), is_(True))

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
        assert_that(check_board.is_check(), is_(True))

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
        u"""Simliar to the '2 move' checkmate. There is an empty square to move but that is also threatened.
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

    def test_checkmate_5_b(self):
        u"""This is based off test_checkmate_5 which was failing. Tests the individual parts of this method

        Simliar to the '2 move' checkmate. There is an empty square to move but that is also threatened.
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

        # Check that we know the correct blocking squares
        # TODO: This should become it's own set of test cases
        blockers, attacker = check_board._get_blocking_squares()
        assert_that(attacker, is_(Square('h4')))
        assert_that(blockers, is_(set([Square('f2'), Square('g3')])))

        king_loc = check_board._king_location[Color.white]
        king_moves = check_board.get_moves(king_loc.name)
        assert_that(len(king_moves), is_(0))

        # Check if the black attacking queen can be captured
        white_attackers = check_board._get_attackers(attacker, Color.white)
        assert_that(len(white_attackers), is_(0))

        # assert_that(check_board.is_checkmate(Color.black), is_(False))
        # assert_that(check_board.is_checkmate(Color.white), is_(True))

    def test_statemate_1(self):
        u"""At the start of a game there is no stalemate as each player has moves and enough pieces for checkmate."""
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
        from_1 = Square('e1')
        from_2 = Square('e8')
        c1 = Square('c1')
        g1 = Square('g1')
        c8 = Square('c8')
        g8 = Square('g8')

        assert_that(castle_board._get_castle_moves(from_1), contains_inanyorder(c1, g1))
        assert_that(castle_board._get_castle_moves(from_2), contains_inanyorder(c8, g8))

    def test_white_king_castle_left(self):
        u"""Test castling left for White King.

           _______________
        8 |♜|_|_|_|♚|_|_|♜|
        7 |♟|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|_|_|_|_|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♙|♙|♙|♙|♙|♙|♙|♙|
        1 |♖|_|_|_|♔|_|_|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H

        """
        castle_board = Board("♖___♔__♖-♙♙♙♙♙♙♙♙-________-________-________-________-♟♟♟♟♟♟♟♟-♜___♚__♜,W,0,0")

        white_king = castle_board.get_piece('e1')
        white_rook = castle_board.get_piece('a1')
        assert_that(white_king, is_(WhiteKing))
        assert_that(white_rook, is_(WhiteRook))
        castle_board.move_piece('e1', 'c1')
        assert_that(castle_board.get_piece('c1'), is_(white_king))
        assert_that(castle_board.get_piece('d1'), is_(white_rook))

    def test_white_king_castle_right(self):
        """Test castling right for White King."""
        castle_board = Board("♖___♔__♖-♙♙♙♙♙♙♙♙-________-________-________-________-♟♟♟♟♟♟♟♟-♜___♚__♜,W,0,0")

        white_king = castle_board.get_piece('e1')
        white_rook = castle_board.get_piece('h1')
        assert_that(white_king, is_(WhiteKing))
        assert_that(white_rook, is_(WhiteRook))
        castle_board.move_piece('e1', 'g1')
        assert_that(castle_board.get_piece('g1'), is_(white_king))
        assert_that(castle_board.get_piece('f1'), is_(white_rook))

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

        black_king = castle_board.get_piece('e8')
        black_rook = castle_board.get_piece('a8')
        assert_that(black_king, is_(BlackKing))
        assert_that(black_rook, is_(BlackRook))
        castle_board.move_piece('e8', 'c8')
        assert_that(castle_board.get_piece('c8'), is_(black_king))
        assert_that(castle_board.get_piece('d8'), is_(black_rook))

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

        black_king = castle_board.get_piece('e8')
        black_rook = castle_board.get_piece('h8')

        assert_that(black_king, is_(BlackKing))
        assert_that(black_rook, is_(BlackRook))
        castle_board.move_piece('e8', 'g8')

        assert_that(castle_board.get_piece('g8'), is_(black_king))
        assert_that(castle_board.get_piece('f8'), is_(black_rook))

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

        piece = board_.get_piece('a2')
        assert_that(board_.get_piece('a3'), is_(None))
        # Move the white Pawn
        board_.move_piece('a2', 'a3')
        assert_that(board_.get_piece('a2'), is_(None))
        assert_that(board_.get_piece('a3'), is_(piece))

    def test_move_pawn_forward_2(self):
        """Test whether a black pawn can move forward two spaces into an empty square.
        """
        board_ = Board()

        # Move a white pawn first
        white_pawn = board_.get_piece('b2')

        board_.move_piece('b2', 'b4')
        assert_that(board_.get_piece('b2'), is_(None))
        assert_that(board_.get_piece('b4'), is_(white_pawn))

        assert_that(board_.get_piece('d5'), is_(None))
        black_pawn = board_.get_piece('d7')

        # Move the Black Pawn
        board_.move_piece('d7', 'd5')
        assert_that(board_.get_piece('d7'), is_(None))
        assert_that(board_.get_piece('d5'), is_(black_pawn))

        assert_that(board_.get_moves('d5'), contains_inanyorder('D4'))

    def test_move_knight(self):
        """Test whether a knight can move in its 'L' shape
        """
        board_ = Board()
        assert_that(board_.get_piece('c3'), is_(None))
        piece = board_.get_piece('b1')
        # Move White Knight
        board_.move_piece('b1', 'c3')
        assert_that(board_.get_piece('b1'), is_(None))
        assert_that(board_.get_piece('c3'), is_(piece))

    def test_move_bishop(self):
        u"""Test whether a white bishop can move diagonally."""
        board_ = Board()
        # Move white pawn out of the way 1st
        board_.move_piece('d2', 'd3')

        # Move a black pawn
        board_.move_piece('d7', 'd6')

        piece = board_.get_piece('c1')

        # Move White Bishop
        board_.move_piece('c1', 'g5')
        assert_that(board_.get_piece('c1'), is_(None))
        assert_that(board_.get_piece('g5'), is_(piece))

    def test_move_queen_forward(self):
        board_ = Board()
        # Move pawn out of the way 1st
        board_.move_piece('d2', 'd4')

        # Move a black pawn
        board_.move_piece('d7', 'd6')

        piece = board_.get_piece('d1')
        # Move White Queen
        board_.move_piece('d1', 'd3')
        assert_that(board_.get_piece('d1'), is_(None))
        assert_that(board_.get_piece('d3'), is_(piece))

    def test_move_rook(self):
        """Test the moves of a rook."""
        board_ = Board()

        # Move a white pawn
        board_.move_piece('d2', 'd3')

        # Move pawn out of the way 1st
        board_.move_piece('h7', 'h5')

        # Move a another white pawn
        board_.move_piece('b2', 'b3')

        piece = board_.get_piece('h8')

        # Move black rook vertically
        board_.move_piece('h8', 'h6')
        assert_that(board_.get_piece('h8'), is_(None))
        assert_that(board_.get_piece('h6'), is_(piece))

        # Move a third white pawn
        board_.move_piece('a2', 'a3')

        # Move again horizontally
        board_.move_piece('h6', 'd6')
        assert_that(board_.get_piece('h6'), is_(None))
        assert_that(board_.get_piece('d6'), is_(piece))

    def test_move_king_diagonally(self):
        """Test moving the king diagonally."""
        board_ = Board()
        # Move pawn out of the way 1st
        board_.move_piece('e2', 'e3')

        # Move a black knight (we need to do any black move)
        board_.move_piece('b8', 'c6')

        # Locate the king
        piece = board_.get_piece('e1')

        # Move the king
        board_.move_piece('e1', 'e2')
        assert_that(board_.get_piece('e1'), is_(None))
        assert_that(board_.get_piece('e2'), is_(piece))

    def test_en_passant(self):
        """Test whether a pawn can capture another via en-passant.

        This does a lot of extra moves because it starts from a new board.
        """
        board_ = Board()
        # Move the white pawn first
        board_.move_piece('e2', 'e4')

        # Move the a black pawn to switch turn
        board_.move_piece('a7', 'a5')

        # Move it white pawn again
        board_.move_piece('e4', 'e5')
        white_pawn = board_.get_piece('e5')

        # Move a black pawn 'past' this one
        board_.move_piece('d7', 'd5')

        # print board_.display()

        # Pre-move
        white_pawn = board_.get_piece('e5')
        black_pawn = board_.get_piece('d5')
        # Check the board is as we expect
        assert_that(board_.get_piece('e5'), is_(white_pawn))
        assert_that(board_.get_piece('d6'), is_(None))
        assert_that(board_.get_piece('d5'), is_(black_pawn))

        # Capture via en passant
        board_.move_piece('e5', 'd6')
        assert_that(board_.get_piece('e5'), is_(None))
        assert_that(board_.get_piece('d6'), is_(white_pawn))
        assert_that(board_.get_piece('d5'), is_(None))

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
        chess_board.move_piece('e7', 'e5')

        pawn_moves = chess_board.get_moves('f5')

        # We can't capture the pawn because it would put our king in check, but we can move forward
        assert_that(pawn_moves, equal_to(set(['F6'])))

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
        chess_board.move_piece('e7', 'e5')

        white_pawn_loc = 'f5'
        white_en_passant_attack = 'E6'
        white_en_move_forward = 'F6'

        pawn_moves = chess_board.get_moves(white_pawn_loc)

        #We can't capture the pawn because it would put our king in check
        assert_that(pawn_moves, contains_inanyorder(white_en_passant_attack, white_en_move_forward))


class TestDisplayMethods(unittest.TestCase):
    u"""Test the display methods"""

    def test_display(self):
        u"""Simply tests that the method runs without raising an exception"""
        board = Board()
        board.display()

    def test_display_json(self):
        u"""Simply tests that the method runs without raising an exception"""
        board = Board()
        board.display_json()


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
        chess_board.move_piece('e2', 'e4')

        # Double move black pawn
        chess_board.move_piece('e7', 'e5')

        # Move out white bishop
        chess_board.move_piece('f1', 'c4')

        # Move out black queenside pawn
        chess_board.move_piece('d7', 'd6')

       # Move out white queen
        chess_board.move_piece('d1', 'f3')

        # Move out black queenside knight
        chess_board.move_piece('b8', 'c6')

        # Checkmate with white queen
        chess_board.move_piece('f3', 'f7')

        assert_that(chess_board.winner, is_(Color.white))
        # print chess_board.display()

    def test_knight_can_capture_attacker(self):
        u""" White manually testing this testcase was discoved. The BlackKnight at G8 should be able to capture
        the pawn in F6 threatening the king in E7.
          ________________
        8 |♜|♕|_|♛|_|♝|♞|♕|
        7 |_|_|_|_|♚|_|_|♟|
        6 |_|_|_|♟|♟|♙|_|_|
        5 |_|_|_|♝|_|_|_|_|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|_|_|♘|_|
        2 |♙|_|_|♔|_|_|_|♙|
        1 |_|♖|_|_|_|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
           """
        chess_board = Board("_m♖___♗♘♖-♙__m♔___♙-______♘_-________-___♝____-___♟♟♙__-____m♚__♟-♜♕_♛_♝♞♕,B,0,0")
        knight_moves = chess_board.get_moves('g8')
        assert_that(knight_moves, is_(set(['F6'])))

    def test_knight_and_bishop_can_block_attacker(self):
        u""" White manually testing this testcase was discoved. The knight should be able to block the check.

          ________________
        8 |♜|♞|_|♖|_|_|_|♚|
        7 |♟|♟|♟|_|_|♕|_|_|
        6 |_|_|_|_|_|♞|_|♝|
        5 |_|_|_|_|_|_|_|_|
        4 |_|_|♛|_|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♙|♙|♙|_|_|♙|♙|♙|
        1 |♖|♘|♗|_|♔|_|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """

        chess_board = Board("♖♘♗_♔_♘♖-♙♙♙__♙♙♙-________-__♛_____-________-_____♞_♝-♟♟♟__♕__-♜♞_♖___m♚,B,0,0")

        king_moves = chess_board.get_moves('h8')
        assert_that(king_moves, is_(set([])))

        bishop_moves = chess_board.get_moves('h6')
        assert_that(bishop_moves, is_(set(['F8'])))

        knight_moves = chess_board.get_moves('f6')
        assert_that(knight_moves, is_(set(['E8', 'G8'])))

    def test_checkmate_stops_movement(self):
        u""" White manually testing this testcase was discoved. It is checkmate, so the king should not be able to move

           ________________
        8 |_|_|_|♖|_|_|♚|_|
        7 |♟|_|_|_|♖|_|_|_|
        6 |_|_|_|_|_|_|_|_|
        5 |_|♟|_|_|_|_|♗|_|
        4 |_|_|♟|_|_|_|_|_|
        3 |_|_|♘|_|_|_|_|_|
        2 |♙|♙|♙|_|_|_|♙|♙|
        1 |_|_|_|_|♔|_|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """
        chess_board = Board("____♔_♘♖-♙♙♙___♙♙-__♘_____-__♟_____-_♟____♗_-________-♟___m♖___-___m♖__m♚_,B,0,1")

        checkmate = chess_board.is_checkmate(Color.black)
        # h8 = Square('h8')
        # g8 = Square('g8')

        # print chess_board._get_attackers(h8, Color.white, ignore_king=True)
        # print chess_board._get_moves_and_attacks(g8)
        # from_, direction, color, limit=None, ignore_king=False):

        assert_that(checkmate, is_(True))

    def test_blackbishop_can_move(self):
        u"""While manually testing this scenario came up, where the bishop could not move tho it should be able to.

           ________________
        8 |_|♕|♝|♛|♚|♝|_|♜|
        7 |_|_|♟|_|♟|♟|♟|_|
        6 |_|♟|_|_|_|♞|_|_|
        5 |_|_|_|♟|_|_|_|♟|
        4 |_|_|_|♙|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♙|♙|♙|_|♙|♙|♙|♙|
        1 |♖|♘|♗|_|♔|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """
        chess_board = Board("♖♘♗_♔♗♘♖-♙♙♙_♙♙♙♙-________-___♙____-___♟___♟-_♟___♞__-__♟_♟♟♟_-_♕♝♛♚♝_♜,B,0,0")

        moves = chess_board.get_moves('c8')
        assert_that(moves, is_(set(['A6', 'B7', 'D7', 'E6', 'F5', 'G4', 'H3'])))
        # print chess_board._get_pinned_directions(from_)
        # print chess_board.get_moves('c8')


class TestLegalMoves(unittest.TestCase):
    u"""These ares supplimentary test cases that check that moves are legal. They mainly involve check conditions."""

    def test_get_legal_moves_1(self):
        u"""This mainly checks we have no syntax errors."""
        chess_board = Board()
        moves = chess_board.get_moves('a2')
        assert_that(moves, contains_inanyorder('A3', 'A4'))

    def test_knight_pinned(self):
        """That the knight cannot move because it would put the king in check

           The board looks like the following:

           ________________
        8 |♜|♞|♝|_|♚|♝|♞|♜|
        7 |♟|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|♛|_|_|_|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|♘|_|_|_|
        2 |♙|♙|♙|♙|_|♙|♙|♙|
        1 |♖|♘|♗|♕|♔|♗|_|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """

        chess_board = Board("♖♘♗♕♔♗_♖-♙♙♙♙_♙♙♙-____♘___-________-____♛___-________-♟♟♟♟♟♟♟_-♜♞♝_♚♝♞♜,B,0,0")
        e3_knight_moves = chess_board.get_moves('e3')
        assert_that(e3_knight_moves, is_(set([])))


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
        chess_board.move_piece('a2', 'a1')
        chess_board.promote_pawn(BlackQueen())
        black_queen = chess_board.get_piece('a1')
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
        chess_board.move_piece('a2', 'a1')
        chess_board.promote_pawn(BlackRook())
        black_rook = chess_board.get_piece('a1')
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
        chess_board.move_piece('a2', 'a1')
        chess_board.promote_pawn(BlackBishop())
        black_bishop = chess_board.get_piece('a1')
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
        chess_board.move_piece('a2', 'a1')
        chess_board.promote_pawn(BlackKnight())
        black_knight = chess_board.get_piece('a1')
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
        chess_board.move_piece('a2', 'a1')
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
        chess_board.move_piece('a2', 'a1')
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
        chess_board.move_piece('a2', 'a1')

        # should raise an exception for because the previous peice has not been promoted
        self.assertRaises(IllegalMoveException, chess_board.move_piece, 'b2', 'b3')


class TestDirectionSearch(unittest.TestCase):
    def test_get_squares_in_direction_1(self):
        """Test get_moves for a white rook in the middle of the board.

        The board looks like:
           ________________
        8 |♜|♞|♝|♛|♚|♝|♞|♜|
        7 |♟|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|_|_|_|_|
        4 |_|_|_|_|_|_|_|_|
        3 |_|♖|_|_|_|_|_|_|
        2 |♙|♙|♙|♙|♙|♙|♙|♙|
        1 |♖|♘|♗|♕|♔|♗|♘|_|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H

        """
        rook_board = Board("♖♘♗♕♔♗♘_-♙♙♙♙♙♙♙♙-_♖______-________-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        from_ = Square('b3')
        left = (-1, 0)
        right = (1, 0)
        up = (0, 1)
        down = (0, -1)

        up_moves, up_attack = rook_board._get_squares_in_direction(from_, up, Color.white)
        b7 = Square('b7')
        assert_that(up_attack, is_(b7))
        assert_that(up_moves, is_(set([Square('b4'), Square('b5'), Square('b6')])))

        down_moves, down_attack = rook_board._get_squares_in_direction(from_, down, Color.white)
        assert_that(down_attack, is_(None))
        assert_that(down_moves, is_(set([])))

        left_moves, left_attack = rook_board._get_squares_in_direction(from_, left, Color.white)
        assert_that(left_attack, is_(None))
        assert_that(left_moves, is_(set([Square('a3')])))

        right_moves, right_attack = rook_board._get_squares_in_direction(from_, right, Color.white)
        assert_that(right_attack, is_(None))
        assert_that(right_moves, is_(
            set([Square('c3'), Square('d3'), Square('e3'), Square('f3'), Square('g3'), Square('h3')])
        ))


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


class TestPinnedBy(unittest.TestCase):

    def test_pinned_by_rook(self):
        u"""Check that a pinned knight cannot move (as there is no way for it to still be blocking check if it moves)

        The board looks like:
           ________________
        8 |♜|♞|♝|♛|♚|♝|♞|_|
        7 |♟|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|♜|_|_|_|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♙|♙|♙|♙|♘|♙|♙|♙|
        1 |♖|♘|♗|♕|♔|♗|_|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H

        """
        pinned_board = Board("♖♘♗♕♔♗_♖-♙♙♙♙♘♙♙♙-________-________-____♜___-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞_,W,0,0")
        e2 = Square('e2')
        pinned_by = pinned_board._pinned(e2)
        assert_that(pinned_by, is_(Square('e5')))

    def test_not_pinned(self):
        u"""The bishop should not be pinned because the queen is also protecting the king

        The board looks like:
           ________________
        8 |♜|♞|♝|♛|♚|♝|♞|♜|
        7 |♟|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|_|_|_|_|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♙|_|♙|_|♙|♙|♙|♙|
        1 |♜|_|♗|♕|♔|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H

        """
        pinned_board = Board("♜_♗♕♔♗♘♖-♙_♙_♙♙♙♙-________-________-____♜___-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,B,0,0")
        c1 = Square('c1')
        pinned = pinned_board._pinned(c1)
        assert_that(pinned, is_(None))

    def test_pinned_by_rook_2(self):
        u"""The bishop should be pinned by the rook in a1.

        The board looks like:
           ________________
        8 |♜|♞|♝|♛|♚|♝|♞|♜|
        7 |♟|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|_|_|_|_|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♙|_|♙|_|♙|♙|♙|♙|
        1 |♜|_|♗|_|♔|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H

        """
        pinned_board = Board("♜_♗_♔♗♘♖-♙_♙_♙♙♙♙-________-________-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,B,0,0")
        c1 = Square('c1')
        pinned = pinned_board._pinned(c1)
        assert_that(pinned, is_(Square('a1')))

    def test_pinned_by_bishop(self):
        u"""The pawn should be pinned by the bishop at h4

        The board looks like:
           ________________
        8 |♜|♞|♝|♛|♚|♝|♞|♜|
        7 |♟|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|_|_|_|_|
        4 |_|_|_|_|_|_|_|♝|
        3 |_|_|_|_|_|_|_|_|
        2 |♙|_|♙|_|♙|♙|♙|♙|
        1 |_|_|♗|_|♔|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H

        """
        pinned_board = Board("♜_♗_♔♗♘♖-♙_♙_♙♙♙♙-________-_______♝-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,B,0,0")
        f2 = Square('f2')
        pinned = pinned_board._pinned(f2)
        assert_that(pinned, is_(Square('h4')))

if __name__ == '__main__':
        unittest.main()
