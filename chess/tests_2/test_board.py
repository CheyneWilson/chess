# -*- coding: UTF-8 -*-
# Unit tests for chess. Requires PyHamcrest to be installed.
# This can be easily done using any packaging tool (such as distribute).
# See https://code.google.com/p/hamcrest/ for more details on hamcrest matchers
from chess.board import Board, Color, King, Queen, Bishop, Knight, Rook, Pawn, BlackPawn, WhiteKing, WhiteRook, \
    BlackKing, BlackQueen, BlackRook, BlackBishop, BlackKnight, IllegalMoveException, WhiteKnight, WhitePawn, \
    IllegalPromotionException, PromotePieceException, Winner, Move
from hamcrest import is_, assert_that, equal_to, all_of, contains_inanyorder, instance_of
import unittest


# @unittest.skip("focusing on only one test")
class TestBoardFunctions(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_create_new_board(self):
        # Make sure that it is White player's turn to move
        white_player = Color.WHITE
        assert_that(self.board.current_player, equal_to(white_player))

        # Make sure a new board places all the pieces in the correct locations
        # Using 'internal' method get_piece check all of the White pieces
        assert_that(all_of(
            self.board.get_piece('A1'), is_(Rook)),
            self.board.get_piece('A1').color, is_(Color.WHITE)
        )
        assert_that(all_of(
            self.board.get_piece('B1'), is_(Knight)),
            self.board.get_piece('B1').color, is_(Color.WHITE)
        )
        assert_that(all_of(
            self.board.get_piece('C1'), is_(Bishop)),
            self.board.get_piece('C1').color, is_(Color.WHITE)
        )
        assert_that(all_of(
            self.board.get_piece('D1'), is_(King)),
            self.board.get_piece('D1').color, is_(Color.WHITE)
        )
        assert_that(all_of(
            self.board.get_piece('E1'), is_(Queen)),
            self.board.get_piece('E1').color, is_(Color.WHITE)
        )
        assert_that(all_of(
            self.board.get_piece('F1'), is_(Bishop)),
            self.board.get_piece('F1').color, is_(Color.WHITE)
        )
        assert_that(all_of(
            self.board.get_piece('G1'), is_(Knight)),
            self.board.get_piece('G1').color, is_(Color.WHITE)
        )
        assert_that(all_of(
            self.board.get_piece('H1'), is_(Rook)),
            self.board.get_piece('H1').color, is_(Color.WHITE)
        )
        assert_that(all_of(
            self.board.get_piece('A2'), is_(Pawn)),
            self.board.get_piece('A2').color, is_(Color.WHITE)
        )
        assert_that(all_of(
            self.board.get_piece('B2'), is_(Pawn)),
            self.board.get_piece('B2').color, is_(Color.WHITE)
        )
        assert_that(all_of(
            self.board.get_piece('B2'), is_(Pawn)),
            self.board.get_piece('B2').color, is_(Color.WHITE)
        )
        assert_that(all_of(
            self.board.get_piece('C2'), is_(Pawn)),
            self.board.get_piece('C2').color, is_(Color.WHITE)
        )
        assert_that(all_of(
            self.board.get_piece('D2'), is_(Pawn)),
            self.board.get_piece('D2').color, is_(Color.WHITE)
        )
        assert_that(all_of(
            self.board.get_piece('E2'), is_(Pawn)),
            self.board.get_piece('E2').color, is_(Color.WHITE)
        )
        assert_that(all_of(
            self.board.get_piece('F2'), is_(Pawn)),
            self.board.get_piece('F2').color, is_(Color.WHITE)
        )
        assert_that(all_of(
            self.board.get_piece('G2'), is_(Pawn)),
            self.board.get_piece('G2').color, is_(Color.WHITE)
        )
        assert_that(all_of(
            self.board.get_piece('H2'), is_(Pawn)),
            self.board.get_piece('H2').color, is_(Color.WHITE)
        )

        # Using 'internal' method get_piece check all of the Black pieces
        assert_that(all_of(
            self.board.get_piece('A8'), is_(Rook)),
            self.board.get_piece('A8').color, is_(Color.BLACK)
        )
        assert_that(all_of(
            self.board.get_piece('B8'), is_(Knight)),
            self.board.get_piece('B8').color, is_(Color.BLACK)
        )
        assert_that(all_of(
            self.board.get_piece('C8'), is_(Bishop)),
            self.board.get_piece('C8').color, is_(Color.BLACK)
        )
        assert_that(all_of(
            self.board.get_piece('D8'), is_(King)),
            self.board.get_piece('D8').color, is_(Color.BLACK)
        )
        assert_that(all_of(
            self.board.get_piece('E8'), is_(Queen)),
            self.board.get_piece('E8').color, is_(Color.BLACK)
        )
        assert_that(all_of(
            self.board.get_piece('F8'), is_(Bishop)),
            self.board.get_piece('F8').color, is_(Color.BLACK)
        )
        assert_that(all_of(
            self.board.get_piece('G8'), is_(Knight)),
            self.board.get_piece('G8').color, is_(Color.BLACK)
        )
        assert_that(all_of(
            self.board.get_piece('H8'), is_(Rook)),
            self.board.get_piece('H8').color, is_(Color.BLACK)
        )
        assert_that(all_of(
            self.board.get_piece('A7'), is_(Pawn)),
            self.board.get_piece('A7').color, is_(Color.BLACK)
        )
        assert_that(all_of(
            self.board.get_piece('B7'), is_(Pawn)),
            self.board.get_piece('B7').color, is_(Color.BLACK)
        )
        assert_that(all_of(
            self.board.get_piece('B7'), is_(Pawn)),
            self.board.get_piece('B7').color, is_(Color.BLACK)
        )
        assert_that(all_of(
            self.board.get_piece('C7'), is_(Pawn)),
            self.board.get_piece('C7').color, is_(Color.BLACK)
        )
        assert_that(all_of(
            self.board.get_piece('D7'), is_(Pawn)),
            self.board.get_piece('D7').color, is_(Color.BLACK)
        )
        assert_that(all_of(
            self.board.get_piece('E7'), is_(Pawn)),
            self.board.get_piece('E7').color, is_(Color.BLACK)
        )
        assert_that(all_of(
            self.board.get_piece('F7'), is_(Pawn)),
            self.board.get_piece('F7').color, is_(Color.BLACK)
        )
        assert_that(all_of(
            self.board.get_piece('G7'), is_(Pawn)),
            self.board.get_piece('G7').color, is_(Color.BLACK)
        )
        assert_that(all_of(
            self.board.get_piece('H7'), is_(Pawn)),
            self.board.get_piece('H7').color, is_(Color.BLACK)
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
        pawn_moves = self.board.get_moves('A2')
        assert_that(pawn_moves, contains_inanyorder('A3', 'A4'))

    def test_get_moves_opening_black_pawn(self):
        """Check that a black pawn can move from it's starting position as either a single or double move."""
        board = Board()
        board.current_player = Color.BLACK  # Change color to black
        pawn_moves = board.get_moves('F7')
        assert_that(pawn_moves, contains_inanyorder('F6', 'F5'))

    def test_get_moves_moved_white_pawn(self):
        """Check that a white pawn that has moved can only move one space (when nothing to attack)."""
        pawn_board = Board(u"♖♘♗♕♔♗♘♖-♙♙_♙♙♙♙♙-__♙_____-________-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜", Color.WHITE)
        pawn_moves = pawn_board.get_moves('C3')
        assert_that(pawn_moves, contains_inanyorder('C4'))

    def test_get_moves_white_pawn_attacks_both(self):
        """Check that a white pawn with 3 Black pieces in front can attack the two pieces on the sides only"""
        pawn_board = Board(u"♖♘♗♕♔♗♘♖-♙♙♙_♙♙♙♙-________-________-________-___♙___-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜", Color.WHITE)
        pawn_moves = pawn_board.get_moves('D6')
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
        pawn_board = Board(u"♖♘♗♕♔♗♘♖-♙♙♙♙♙♙__-________-______♙♙-_______♟-________-♟♟♟♟♟♟♟_-♜♞♝♛♚♝♞♜", Color.BLACK)
        pawn_moves = pawn_board.get_moves('H5')
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
        pawn_board = Board(u"♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-______♟♟-_______♟-________-♟♟♟♟♟♟♟_-♜♞♝♛♚♝♞♜", Color.WHITE)
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
        pawn_board = Board(u"♖♘♗♕♔♗__-♙♙♙♙♙♙♙♟-________-________-________-________-♟♟♟♟♟♟♟_-♜♞♝♛♚♝♞♜", Color.BLACK)
        pawn_moves = pawn_board.get_moves('H2')
        assert_that(pawn_moves, contains_inanyorder('H1'))

        pawn_moves = pawn_board.move_piece('H2', 'H1')
        assert_that(pawn_board.get_moves('H1'), is_(set([])))
        # self.assertRaises(IllegalMoveException, pawn_board.get_moves, 'H1')

    # TODO:
    # Add more tests for the following
    # * Cannot attack own color

    def test_get_moves_white_knight_opening(self):
        """Check the opening moves of a white knight."""
        knight_moves = self.board.get_moves('B1')
        assert_that(knight_moves, contains_inanyorder('A3', 'C3'))

    def test_get_moves_black_knight_opening(self):
        """Check the opening moves of a black knight."""
        board = Board()
        board.current_player = Color.BLACK  # Change player color for this test
        knight_moves = board.get_moves('G8')
        assert_that(knight_moves, contains_inanyorder('F6', 'H6'))

    def test_get_moves_knight_fork_attack(self):
        """Check if a knight at G3 can fork the king and rook, as well as other moves."""
        knight_board = Board(u"♖_♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-________-________-________-♟♟♘♟♟♟♟♟-♜♞♝♛♚♝♞♜", Color.WHITE)
        knight_moves = knight_board.get_moves('C7')
        assert_that(knight_moves, contains_inanyorder(
            'A8', 'E8', 'A6', 'E6', 'B5', 'D5'
        ))

    def test_get_moves_white_bishop_opening(self):
        """Check the opening moves of a white bishop."""
        bishop_moves = self.board.get_moves('C1')
        assert_that(bishop_moves, is_(set([])))

    def test_get_moves_black_bishop_opening(self):
        """Check the opening moves of a black bishop."""
        bishop_moves = self.board.get_moves('C8')
        assert_that(bishop_moves, is_(set([])))

    def test_get_moves_white_bishop_free(self):
        """Test get_moves for a white bishop in the middle of the board."""
        bishop_board = Board(u"♖♘_♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-________-____♗___-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜", Color.WHITE)
        bishop_moves = bishop_board.get_moves('E5')
        assert_that(bishop_moves, contains_inanyorder(
            'D6', 'C7',  # forward left
            'F6', 'G7',  # forward right
            'D4', 'C3',  # backward left
            'F4', 'G3'   # backward right
        ))

    def test_get_moves_black_bishop_free(self):
        """Test get_moves for a black bishop in the middle of the board."""
        bishop_board = Board(u"♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-________-___♝____-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚_♞♜", Color.BLACK)
        bishop_moves = bishop_board.get_moves('D5')
        assert_that(bishop_moves, contains_inanyorder(
            'C6',  # (2, 7),  # forward left
            'E6',  # (6, 7),  # forward right
            'C4', 'B3', 'A2',  # backward left
            'E4', 'F3', 'G2'   # backward right
        ))

    def test_get_moves_white_rook_opening(self):
        """Test get_moves for the opening moves of a white rook."""
        rook_moves = self.board.get_moves('H1')
        assert_that(rook_moves, is_(set([])))

    def test_get_moves_black_rook_opening(self):
        """Test get_moves for the opening moves of a black rook."""
        rook_moves = self.board.get_moves('H8')
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
        rook_board = Board(u"♖♘♗♕♔♗♘_-♙♙♙♙♙♙♙♙-_♖______-________-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜", Color.WHITE)
        rook_moves = rook_board.get_moves('B3')

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

        rook_board = Board(u"♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-_♜______-________-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞_", Color.BLACK)
        rook_moves = rook_board.get_moves('B3')
        assert_that(rook_moves, contains_inanyorder(
            'B4', 'B5', 'B6',  # backward
            'C3', 'D3', 'E3', 'F3', 'G3', 'H3',  # right
            'A3',  # left
            'B2'  # forward
        ))

    def test_get_moves_white_queen_opening(self):
        """Test get_moves for the opening moves of a white queen."""
        queen_moves = self.board.get_moves('D1')
        assert_that(queen_moves, is_(set([])))

    def test_get_moves_black_queen_opening(self):
        """Test get_moves for the opening moves of a black queen."""
        queen_moves = self.board.get_moves('D8')
        assert_that(queen_moves, is_(set([])))

    def test_get_moves_white_queen_free(self):
        """Check the moves of a white queen in the open."""
        queen_board = Board(u"♖♘♗_♔♗♘♖-♙♙♙♙♙♙♙♙-________-___♕____-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜", Color.WHITE)
        queen_moves = queen_board.get_moves('D4')
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
        queen_board = Board(u"♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-___♛____-________-________-♟♟♟♟♟♟♟♟-♜♞♝_♚♝♞♜", Color.BLACK)
        queen_moves = queen_board.get_moves('D4')
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
        king_moves = self.board.get_moves('E1')
        assert_that(king_moves, is_(set([])))

    def test_get_moves_black_king_opening(self):
        """Check the opening moves of a black king."""
        king_moves = self.board.get_moves('E8')
        assert_that(king_moves, is_(set([])))

    def test_get_moves_white_king_free(self):
        """Check the moves of a white king in the open."""
        king_board = Board(u"♖♘♗♕_♗♘♖-♙♙♙♙♙♙♙♙-________-___m♔____-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜", Color.WHITE)
        king_moves = king_board.get_moves('D4')
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
        king_board = Board(u"♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-___m♚____-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛_♝♞♜", Color.BLACK)
        king_moves = king_board.get_moves('D4')
        assert_that(king_moves, contains_inanyorder(
            'D5',  # forward
            'E5',  # forward right
            'E4',  # right
            'C4',  # left
            'C5'   # forward, left
        ))

    def test_is_check_1(self):
        """Neither king starts off in check. Test for a fresh board."""
        assert_that(self.board.is_check(Color.WHITE), is_(False))

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
        check_board = Board(u"♖♘♗♕_♗♘♖-♙♙♙♙♙♙♙♙-________-________-________-______♔_-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜", Color.WHITE)
        assert_that(check_board.is_check(Color.WHITE), is_(True))

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
        check_board = Board(u"♖♘♗♕♔♗♘_-♙♙♙♙♙♙♙♙-________-________-____♚__♖-________-♟♟♟♟♟♟♟♟-♜♞♝♛_♝♞♜", Color.BLACK)
        assert_that(check_board.is_check(Color.BLACK), is_(True))

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
        check_board = Board(u"♖♘♗_♔♗♘♖-♙♙♙♙♙♙♙♙-________-________-____♚__♕-________-♟♟♟♟♟♟♟♟-♜♞♝♛_♝♞♜", Color.BLACK)
        assert_that(check_board.is_check(Color.BLACK), is_(True))

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
        check_board = Board(u"♖♘♗_♔♗♘♖-♙♙♙♙♙♙♙♙-____♕___-________-____♚___-________-♟♟♟♟♟♟♟♟-♜♞♝♛_♝♞♜", Color.BLACK)
        assert_that(check_board.is_check(Color.BLACK), is_(True))

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
        check_board = Board(u"♖♘♗♕_♗♘♖-♙♙♙♙♙♙♙♙-________-_♔______-________-__♞_____-♟♟♟♟♟♟♟♟-♜_♝♛♚♝♞♜", Color.WHITE)
        assert_that(check_board.is_check(Color.WHITE), is_(True))

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
        check_board = Board(u"♖♘♗♕♔♗♘♖-♙♙♙♙♙__♙-________-_____♙♙♛-________-___♟____-♟♟♟_♟♟♟♟-♜♞♝_♚♝♞♜", Color.WHITE)
        assert_that(check_board.is_checkmate(Color.BLACK), is_(False))
        assert_that(check_board.is_checkmate(Color.WHITE), is_(True))

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

        check_board = Board(u"♖♘♗♕♔♗♘♖-♙_♙♙♙_♙♙-_♙______-_____♙_♛-________-___♟____-♟♟♟_♟♟♟♟-♜♞♝_♚♝♞♜", Color.WHITE)
        assert_that(check_board.is_checkmate(Color.BLACK), is_(False))
        assert_that(check_board.is_checkmate(Color.WHITE), is_(False))

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

        check_board = Board(u"♖♘♗♕♔♗♘♖-♙♙♙_♙__♙-___♙____-_____♙♙♛-________-___♟____-♟♟♟_♟♟♟♟-♜♞♝_♚♝♞♜", Color.WHITE)
        assert_that(check_board.is_checkmate(Color.BLACK), is_(False))
        assert_that(check_board.is_checkmate(Color.WHITE), is_(False))

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

        check_board = Board(u"♖♘♗♕♔♗_♖-♙♙♙♙♙__♙-_____♘__-_____♙♙♛-________-___♟____-♟♟♟_♟♟♟♟-♜♞♝_♚♝♞♜", Color.WHITE)
        assert_that(check_board.is_checkmate(Color.BLACK), is_(False))
        assert_that(check_board.is_checkmate(Color.WHITE), is_(False))

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

        check_board = Board(u"♖♘♗♕♔♗♘♖-♙♙♙_♙__♙-__♟♙____-_____♙♙♛-________-___♟____-♟♟__♟♟♟♟-♜♞♝_♚♝♞♜", Color.WHITE)
        assert_that(check_board.is_checkmate(Color.BLACK), is_(False))
        assert_that(check_board.is_checkmate(Color.WHITE), is_(True))

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

        check_board = Board(u"♖♘♗♕♔♗♘♖-♙♙♙_♙__♙-__♟♙____-_____♙♙♛-________-___♟____-♟♟__♟♟♟♟-♜♞♝_♚♝♞♜", Color.WHITE)

        # Check that we know the correct blocking squares
        # TODO: This should become it's own set of test cases
        blockers, attacker = check_board._get_blocking_squares(Color.WHITE)
        assert_that(attacker, is_('H4'))
        assert_that(blockers, is_(set(['F2', 'G3'])))

        king_loc = check_board._king_location[Color.WHITE]
        king_moves = check_board.get_moves(king_loc)
        assert_that(len(king_moves), is_(0))

        # Check if the black attacking queen can be captured
        white_attackers = check_board._get_attackers(attacker, Color.WHITE)
        assert_that(len(white_attackers), is_(0))

        # assert_that(check_board.is_checkmate(Color.BLACK), is_(False))
        # assert_that(check_board.is_checkmate(Color.WHITE), is_(True))

    def test_statemate_1(self):
        u"""At the start of a game there is no stalemate as each player has moves and enough pieces for checkmate."""
        assert_that(self.board.is_stalemate(Color.WHITE), is_(False))

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
        stale_board = Board(u"_♘♗___♔♖-_♙_♙___♙-♙♟♙♟_♛_♟-♟_♟_____-________-___♟____-_____♟♟_-♜♞♝_♚♝♞♜", Color.WHITE)
        assert_that(stale_board.is_stalemate(Color.WHITE), is_(True))

    def test_stalemate_3(self):
        """If a player has only one bishop or knight they cannot checkmate
         their opponent. If they have two only knights they cannot force
         checkmate (except rare case with opponent having a lone pawn).
         This tests for stalemate where neither player can achieve checkmate.
        """
        stale_board = Board(u"_♘____♔_-________-________-________-________-________-________-____♚___", Color.WHITE)
        assert_that(stale_board.is_stalemate(Color.WHITE), is_(True))

    def test_stalemate_4(self):
        """If a player has a pawn, they can promote it. So it is not stalemate.
        """
        stale_board = Board(u"______♔_-♙_______-________-________-________-________-________-____♚___", Color.WHITE)
        assert_that(stale_board.is_stalemate(Color.WHITE), is_(False))

    def test_board_repr_1(self):
        """Serialize a board, restore it and re-serialize it, it is the same as the original?"""
        board_string = repr(self.board)
        new_board = Board(board_string.decode('utf-8'))
        new_board_string = repr(new_board)
        assert_that(board_string, equal_to(new_board_string))

    def test_move_pawn_forward_1(self):
        """Test if a pawn can move forward one space into an empty square."""
        board_ = Board()

        piece = board_.get_piece('A2')
        assert_that(board_.get_piece('A3'), is_(None))
        # Move the white Pawn
        board_.move_piece('A2', 'A3')
        assert_that(board_.get_piece('A2'), is_(None))
        assert_that(board_.get_piece('A3'), is_(piece))

    def test_move_pawn_forward_2(self):
        """
        Test whether a black pawn can move forward two spaces into an empty square.
        """
        board_ = Board()

        # Move a white pawn first
        white_pawn = board_.get_piece('B2')

        board_.move_piece('B2', 'B4')
        assert_that(board_.get_piece('B2'), is_(None))
        assert_that(board_.get_piece('B4'), is_(white_pawn))

        assert_that(board_.get_piece('D5'), is_(None))
        black_pawn = board_.get_piece('D7')

        # Move the Black Pawn
        board_.move_piece('D7', 'D5')
        assert_that(board_.get_piece('D7'), is_(None))
        assert_that(board_.get_piece('D5'), is_(black_pawn))

        # Check pawn can move foward, ignoring that it is not BLACK's turn
        assert_that(board_.get_moves('D5', False), contains_inanyorder('D4'))

    def test_move_knight(self):
        """Test whether a knight can move in its 'L' shape
        """
        board_ = Board()
        assert_that(board_.get_piece('C3'), is_(None))
        piece = board_.get_piece('B1')
        # Move White Knight
        board_.move_piece('B1', 'C3')
        assert_that(board_.get_piece('B1'), is_(None))
        assert_that(board_.get_piece('C3'), is_(piece))

    def test_move_bishop(self):
        u"""Test whether a white bishop can move diagonally."""
        board_ = Board()
        # Move white pawn out of the way 1st
        board_.move_piece('D2', 'D3')

        # Move a black pawn
        board_.move_piece('D7', 'D6')

        piece = board_.get_piece('C1')

        # Move White Bishop
        board_.move_piece('C1', 'G5')
        assert_that(board_.get_piece('C1'), is_(None))
        assert_that(board_.get_piece('G5'), is_(piece))

    def test_move_queen_forward(self):
        board_ = Board()
        # Move pawn out of the way 1st
        board_.move_piece('D2', 'D4')

        # Move a black pawn
        board_.move_piece('D7', 'D6')

        piece = board_.get_piece('D1')
        # Move White Queen
        board_.move_piece('D1', 'D3')
        assert_that(board_.get_piece('D1'), is_(None))
        assert_that(board_.get_piece('D3'), is_(piece))

    def test_move_rook(self):
        """Test the moves of a rook."""
        board_ = Board()

        # Move a white pawn
        board_.move_piece('D2', 'D3')

        # Move pawn out of the way 1st
        board_.move_piece('H7', 'H5')

        # Move a another white pawn
        board_.move_piece('B2', 'B3')

        piece = board_.get_piece('H8')

        # Move black rook vertically
        board_.move_piece('H8', 'H6')
        assert_that(board_.get_piece('H8'), is_(None))
        assert_that(board_.get_piece('H6'), is_(piece))

        # Move a third white pawn
        board_.move_piece('A2', 'A3')

        # Move again horizontally
        board_.move_piece('H6', 'D6')
        assert_that(board_.get_piece('H6'), is_(None))
        assert_that(board_.get_piece('D6'), is_(piece))

    def test_move_king_diagonally(self):
        """Test moving the king diagonally."""
        board_ = Board()
        # Move pawn out of the way 1st
        board_.move_piece('E2', 'E3')

        # Move a black knight (we need to do any black move)
        board_.move_piece('B8', 'C6')

        # Locate the king
        piece = board_.get_piece('E1')

        # Move the king
        board_.move_piece('E1', 'E2')
        assert_that(board_.get_piece('E1'), is_(None))
        assert_that(board_.get_piece('E2'), is_(piece))

    def test_en_passant(self):
        """Test whether a pawn can capture another via en-passant.

        This does a lot of extra moves because it starts from a new board.
        """
        board_ = Board()
        # Move the white pawn first
        board_.move_piece('E2', 'E4')

        # Move the a black pawn to switch turn
        board_.move_piece('A7', 'A5')

        # Move it white pawn again
        board_.move_piece('E4', 'E5')
        white_pawn = board_.get_piece('E5')

        # Move a black pawn 'past' this one
        board_.move_piece('D7', 'D5')

        # print board_.display()

        # Pre-move
        white_pawn = board_.get_piece('E5')
        black_pawn = board_.get_piece('D5')
        # Check the board is as we expect
        assert_that(board_.get_piece('E5'), is_(white_pawn))
        assert_that(board_.get_piece('D6'), is_(None))
        assert_that(board_.get_piece('D5'), is_(black_pawn))

        # Capture via en passant
        board_.move_piece('E5', 'D6')
        assert_that(board_.get_piece('E5'), is_(None))
        assert_that(board_.get_piece('D6'), is_(white_pawn))
        assert_that(board_.get_piece('D5'), is_(None))

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

        chess_board = Board(u"♖♘♗♕_♗♘♖-♙♙♙♙♙_♙♙-________-________-♜____♙_♔-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞_", Color.BLACK)

        # Move the black pawn a doulbe step
        chess_board.move_piece('E7', 'E5')

        pawn_moves = chess_board.get_moves('F5')

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

        chess_board = Board(u"♖♘♗♕_♗♘♖-♙♙♙♙♙_♙♙-________-________-_____♙_♔-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜", Color.BLACK)

        # Move the black pawn a doulbe step
        chess_board.move_piece('E7', 'E5')

        white_pawn_loc = 'F5'
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

    @unittest.skip("This display method is being removed from the controller")
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
        chess_board.move_piece('E2', 'E4')

        # Double move black pawn
        chess_board.move_piece('E7', 'E5')

        # Move out white bishop
        chess_board.move_piece('F1', 'C4')

        # Move out black queenside pawn
        chess_board.move_piece('D7', 'D6')

       # Move out white queen
        chess_board.move_piece('D1', 'F3')

        # Move out black queenside knight
        chess_board.move_piece('B8', 'C6')

        # Checkmate with white queen
        chess_board.move_piece('F3', 'F7')

        assert_that(chess_board.winner, is_(Winner.WHITE))
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
        chess_board = Board(u"_m♖___♗♘♖-♙__m♔___♙-______♘_-________-___♝____-___♟♟♙__-____m♚__♟-♜♕_♛_♝♞♕", Color.BLACK)

        knight_moves = chess_board.get_moves('G8')
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

        chess_board = Board(u"♖♘♗_♔_♘♖-♙♙♙__♙♙♙-________-__♛_____-________-_____♞_♝-♟♟♟__♕__-♜♞_♖___m♚", Color.BLACK)

        king_moves = chess_board.get_moves('H8')
        assert_that(king_moves, is_(set([])))

        bishop_moves = chess_board.get_moves('H6')
        assert_that(bishop_moves, is_(set(['F8'])))

        knight_moves = chess_board.get_moves('F6')
        assert_that(knight_moves, is_(set(['E8', 'G8'])))

    def test_checkmate_stops_movement(self):
        """
        While manually testing this testcase was discoved. It is checkmate, so the king should not be able to move
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
        chess_board = Board(u"____♔_♘♖-♙♙♙___♙♙-__♘_____-__♟_____-_♟____♗_-________-♟___m♖___-___m♖__m♚_", Color.BLACK)
        checkmate = chess_board.is_checkmate(Color.BLACK)
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
        chess_board = Board(u"♖♘♗_♔♗♘♖-♙♙♙_♙♙♙♙-________-___♙____-___♟___♟-_♟___♞__-__♟_♟♟♟_-_♕♝♛♚♝_♜", Color.BLACK)

        moves = chess_board.get_moves('C8')
        assert_that(moves, is_(set(['A6', 'B7', 'D7', 'E6', 'F5', 'G4', 'H3'])))

    def test_en_passant_4(self):
        u""" White pawn double-moved from D2 to D4. Black pawn at E4 should be able to capture.
           ________________
        8 |♜|♞|♝|♛|♚|♝|♞|♜|
        7 |♟|♟|_|♟|_|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|♟|_|_|♙|_|_|
        4 |_|_|_|♙|♟|_|♙|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♙|♙|♙|_|♙|_|_|♙|
        1 |♖|♘|♗|♕|♔|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H
        """

        chess_board = Board(u"♖♘♗♕♔♗♘♖-♙♙♙_♙__♙-________-___♙♟_♙_-__♟__♙__-________-♟♟_♟_♟♟♟-♜♞♝♛♚♝♞♜", Color.BLACK)
        chess_board.previous_move = Move('WP', 'D2', 'D4', True)
        chess_board.move_piece('E4', 'D3')


class TestLegalMoves(unittest.TestCase):
    u"""These ares supplimentary test cases that check that moves are legal. They mainly involve check conditions."""

    def test_get_legal_moves_1(self):
        u"""This mainly checks we have no syntax errors."""
        chess_board = Board()
        moves = chess_board.get_moves('A2')
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

        chess_board = Board(u"♖♘♗♕♔♗_♖-♙♙♙♙_♙♙♙-____♘___-________-____♛___-________-♟♟♟♟♟♟♟_-♜♞♝_♚♝♞♜", Color.BLACK)
        e3_knight_moves = chess_board.get_moves('E3')
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

        chess_board = Board(u"_♘♗♕♔♗♘♖-♟♙♙♙♙♙♙♙-________-________-________-________-_♟♟♟♟♟♟_-♜♞♝♛♚♝♞♜", Color.BLACK)
        chess_board.move_piece('A2', 'A1')
        chess_board._promote_pawn(BlackQueen())
        black_queen = chess_board.get_piece('A1')
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

        chess_board = Board(u"_♘♗♕♔♗♘♖-♟♙♙♙♙♙♙♙-________-________-________-________-_♟♟♟♟♟♟_-♜♞♝♛♚♝♞♜", Color.BLACK)
        chess_board.move_piece('A2', 'A1')
        chess_board._promote_pawn(BlackRook())
        black_rook = chess_board.get_piece('A1')
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

        chess_board = Board(u"_♘♗♕♔♗♘♖-♟♙♙♙♙♙♙♙-________-________-________-________-_♟♟♟♟♟♟_-♜♞♝♛♚♝♞♜", Color.BLACK)
        chess_board.move_piece('A2', 'A1')
        chess_board._promote_pawn(BlackBishop())
        black_bishop = chess_board.get_piece('A1')
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

        chess_board = Board(u"_♘♗♕♔♗♘♖-♟♙♙♙♙♙♙♙-________-________-________-________-_♟♟♟♟♟♟_-♜♞♝♛♚♝♞♜", Color.BLACK)
        chess_board.move_piece('A2', 'A1')
        chess_board._promote_pawn(BlackKnight())
        black_knight = chess_board.get_piece('A1')
        assert_that(black_knight, instance_of(BlackKnight))

    def test_promote_pawn_to_king(self):
        """
        Tests the promotion of a pawn to a king. This is not allowed, so should raise an IllegalPromotionException

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

        chess_board = Board(u"_♘♗♕♔♗♘♖-♟♙♙♙♙♙♙♙-________-________-________-________-_♟♟♟♟♟♟_-♜♞♝♛♚♝♞♜", Color.BLACK)
        chess_board.move_piece('A2', 'A1')
        # should raise an exception for an invalid piece
        self.assertRaises(IllegalPromotionException, chess_board._promote_pawn, BlackKing)

    def test_promote_pawn_to_pawn(self):
        """Tests the promotion of a pawn to a pawn. This is not allowed, so should raise an IllegalPromotionException

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

        chess_board = Board(u"_♘♗♕♔♗♘♖-♟♙♙♙♙♙♙♙-________-________-________-________-_♟♟♟♟♟♟_-♜♞♝♛♚♝♞♜", Color.BLACK)
        chess_board.move_piece('A2', 'A1')
        # should raise an exception for an invalid piece
        self.assertRaises(IllegalPromotionException, chess_board._promote_pawn, BlackPawn)

    def test_promote_pawn_in_wrong_location(self):
        """
        Tests the promotion of a pawn when none present in end zone. This should raise an IllegalPromotionException

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

        chess_board = Board(u"♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-________-________-________-♟♟♟♟♟♟♟_-♜♞♝♛♚♝♞♜", Color.BLACK)

        # should raise an exception for an invalid piece
        self.assertRaises(IllegalPromotionException, chess_board._promote_pawn, BlackKnight)

    def test_move_before_promote(self):
        """
        Tests that promotion is required before moving to the next move.

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

        chess_board = Board(u"_♘♗♕♔♗♘♖-♟♙♙♙♙♙♙♙-________-________-________-________-_♟♟♟♟♟♟_-♜♞♝♛♚♝♞♜", Color.BLACK)
        chess_board.move_piece('A2', 'A1')

        # should raise an exception for because the previous peice has not been promoted
        self.assertRaises(PromotePieceException, chess_board.move_piece, 'B2', 'B3')


class TestCastlingFunctions(unittest.TestCase):
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
        castle_board = Board(u"♖___♔__♖-♙♙♙♙♙♙♙♙-________-________-________-________-♟♟♟♟♟♟♟♟-♜___♚__♜", Color.WHITE)
        assert_that(castle_board._get_castle_moves('E1'), contains_inanyorder('C1', 'G1'))
        assert_that(castle_board._get_castle_moves('E8'), contains_inanyorder('C8', 'G8'))

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
        castle_board = Board(u"♖___♔__♖-♙♙♙♙♙♙♙♙-________-________-________-________-♟♟♟♟♟♟♟♟-♜___♚__♜", Color.WHITE)
        white_king = castle_board.get_piece('E1')
        white_rook = castle_board.get_piece('A1')
        assert_that(white_king, is_(WhiteKing))
        assert_that(white_rook, is_(WhiteRook))
        castle_board.move_piece('E1', 'C1')
        assert_that(castle_board.get_piece('C1'), is_(white_king))
        assert_that(castle_board.get_piece('D1'), is_(white_rook))

    def test_white_king_castle_right(self):
        """Test castling right for White King."""
        castle_board = Board(u"♖___♔__♖-♙♙♙♙♙♙♙♙-________-________-________-________-♟♟♟♟♟♟♟♟-♜___♚__♜", Color.WHITE)

        white_king = castle_board.get_piece('E1')
        white_rook = castle_board.get_piece('H1')
        assert_that(white_king, is_(WhiteKing))
        assert_that(white_rook, is_(WhiteRook))
        castle_board.move_piece('E1', 'G1')
        assert_that(castle_board.get_piece('G1'), is_(white_king))
        assert_that(castle_board.get_piece('F1'), is_(white_rook))

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
        castle_board = Board(u"♖___♔__♖-♙♙♙♙♙♙♙♙-________-________-________-________-♟♟♟♟♟♟♟♟-♜___♚__♜", Color.BLACK)

        black_king = castle_board.get_piece('E8')
        black_rook = castle_board.get_piece('A8')
        assert_that(black_king, is_(BlackKing))
        assert_that(black_rook, is_(BlackRook))
        castle_board.move_piece('E8', 'C8')
        assert_that(castle_board.get_piece('C8'), is_(black_king))
        assert_that(castle_board.get_piece('D8'), is_(black_rook))

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
        castle_board = Board(u"♖___♔__♖-♙♙♙♙♙♙♙♙-________-________-________-________-♟♟♟♟♟♟♟♟-♜___♚__♜", Color.BLACK)

        black_king = castle_board.get_piece('E8')
        black_rook = castle_board.get_piece('H8')

        assert_that(black_king, is_(BlackKing))
        assert_that(black_rook, is_(BlackRook))
        castle_board.move_piece('E8', 'G8')

        assert_that(castle_board.get_piece('G8'), is_(black_king))
        assert_that(castle_board.get_piece('F8'), is_(black_rook))


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
        rook_board = Board(u"♖♘♗♕♔♗♘_-♙♙♙♙♙♙♙♙-_♖______-________-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜", Color.WHITE)
        from_ = 'B3'
        left = (-1, 0)
        right = (1, 0)
        up = (0, 1)
        down = (0, -1)

        up_moves, up_attack = rook_board._get_squares_in_direction(from_, up, Color.WHITE)
        assert_that(up_attack, is_('B7'))
        assert_that(up_moves, is_(set(['B4', 'B5', 'B6'])))

        down_moves, down_attack = rook_board._get_squares_in_direction(from_, down, Color.WHITE)
        assert_that(down_attack, is_(None))
        assert_that(down_moves, is_(set([])))

        left_moves, left_attack = rook_board._get_squares_in_direction(from_, left, Color.WHITE)
        assert_that(left_attack, is_(None))
        assert_that(left_moves, is_(set(['A3'])))

        right_moves, right_attack = rook_board._get_squares_in_direction(from_, right, Color.WHITE)
        assert_that(right_attack, is_(None))
        assert_that(right_moves, is_(
            set(['C3', 'D3', 'E3', 'F3', 'G3', 'H3'])
        ))

    def test_get_knight_moves_1(self):
        u"""A knight at B1 should be able to move to A3 and C3 from a new board

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
        board = Board()
        moves, attacks = board._get_knight_bishop_queen_rook_king_moves(WhiteKnight(), 'B1')
        assert_that(attacks, is_(set([])))
        assert_that(moves, is_(set(['A3', 'C3'])))

    def test_get_knight_moves_2(self):
        u"""A knight at B1 should be able to move to A3 and C3 from a new board. If instead the knight was
        a black knight then it should be able to also capture D2. This does not care about the actual piece in 'from_'

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
        board = Board()
        moves, attacks = board._get_knight_bishop_queen_rook_king_moves(BlackKnight(), 'B1')
        assert_that(attacks, is_(set(['D2'])))
        assert_that(moves, is_(set(['A3', 'C3'])))

    def test_get_low_level_pawn_moves_1(self):
        u"""A pawn should be able to move one or two squares.
        This is a low level method that doesn't care about player's turn.

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
        board = Board()
        from_ = 'D2'
        moves = board._get_pawn_moves(WhitePawn(), from_)
        assert_that(moves, is_(set(['D3', 'D4'])))

        attacks = board._get_pawn_attacks(WhitePawn(), from_)
        assert_that(attacks, is_(set([])))

    def test_get_low_level_pawn_moves_2(self):
        u"""A white pawn at 'D6' should be able to attack C7 and E7 but not move directly forward

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
        board = Board()
        from_ = 'D6'
        moves = board._get_pawn_moves(WhitePawn(), from_)
        assert_that(moves, is_(set([])))

        attacks = board._get_pawn_attacks(WhitePawn(), from_)
        assert_that(attacks, is_(set(['C7', 'E7'])))


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
        pinned_board = Board(u"♖♘♗♕♔♗_♖-♙♙♙♙♘♙♙♙-________-________-____♜___-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞_", Color.WHITE)
        pinned_by = pinned_board._pinned('E2')
        assert_that(pinned_by, is_('E5'))

    def test_pinned_by_rook_2(self):
        u"""The bishop should be pinned by the rook in A1.

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
        pinned_board = Board(u"♜_♗_♔♗♘♖-♙_♙_♙♙♙♙-________-________-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜", Color.BLACK)
        pinned = pinned_board._pinned('C1')
        assert_that(pinned, is_('A1'))

    def test_pinned_by_rook_3(self):
        u"""
        Check that a pinned knight can move as it is not pinned by pieces of the same color

        The board looks like:
           ________________
        8 |♜|♞|♝|♛|♚|♝|♞|_|
        7 |♟|♟|♟|♟|♟|♟|♟|♟|
        6 |_|_|_|_|_|_|_|_|
        5 |_|_|_|_|♖|_|_|_|
        4 |_|_|_|_|_|_|_|_|
        3 |_|_|_|_|_|_|_|_|
        2 |♙|♙|♙|♙|♘|♙|♙|♙|
        1 |♖|♘|♗|♕|♔|♗|_|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           A B C D E F G H

        """
        pinned_board = Board(u"♖♘♗♕♔♗_♖-♙♙♙♙♘♙♙♙-________-________-____♖___-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞_", Color.WHITE)
        pinned_by = pinned_board._pinned('E2')
        assert_that(pinned_by, is_(None))

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
        pinned_board = Board(u"♜_♗♕♔♗♘♖-♙_♙_♙♙♙♙-________-________-____♜___-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜", Color.BLACK)
        pinned = pinned_board._pinned('C1')
        assert_that(pinned, is_(None))

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
        pinned_board = Board(u"♜_♗_♔♗♘♖-♙_♙_♙♙♙♙-________-_______♝-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜", Color.BLACK)
        pinned = pinned_board._pinned('F2')
        assert_that(pinned, is_('H4'))

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
        pinned_board = Board(u"♖♘♗♕♔♗_♖-♙♙♙♙♘♙♙♙-________-________-____♜___-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞_", Color.WHITE)
        knight_moves = pinned_board.get_moves('E2')
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
        pinned_board = Board(u"♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-________-____♜___-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞_", Color.WHITE)
        pawn_moves = pinned_board.get_moves('E2')
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
        pinned_board = Board(u"♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-___♟_♟__-________-____♜___-________-♟♟♟_♟_♟♟-♜♞♝♛♚♝♞_", Color.WHITE)
        pawn_moves = pinned_board.get_moves('E2')
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
        pinned_board = Board(u"♖♘♗♕♔♗♘_-♙♙♙♙_♙♙♙-________-♖___m♙♟_♚-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛_♝♞♜", Color.BLACK)
        pawn_moves = pinned_board.get_moves('F4')
        assert_that(pawn_moves, contains_inanyorder('F3'))

    def test_get_moves_pawn_pinned_by_rook_4(self):
        """Test that a pawn pinned horizontally by a rook cannot move

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
        pinned_board = Board(u"♖♘♗♕♔♗♘_-♙♙♙♙♙♙♙♙-________-♖____♟_♚-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛_♝♞♜", Color.BLACK)
        pawn_moves = pinned_board.get_moves('F4')
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
        pinned_board = Board(u"♖♘♗♕♔_♘♖-♙♙♙♙♙♙♙♙-________-________-_______♗-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜", Color.WHITE)
        pawn_moves = pinned_board.get_moves('F7')
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
        pinned_board = Board(u"♖♘♗♕♔_♘♖-♙♙♙♙♙♙♙♙-________-________-________-______♗_-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜", Color.BLACK)
        pawn_moves = pinned_board.get_moves('F7')
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
        pinned_board = Board(u"♖♘♗♕♔_♘♖-♙♙♙♙_♙♙♙-________-________-________-____♙_♗_-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜", Color.BLACK)
        pawn_moves = pinned_board.get_moves('F7')
        assert_that(pawn_moves, contains_inanyorder('G6'))


class TestGetAttackers(unittest.TestCase):
    u"""Low level test cases for _get_attackers method. They all use the default board

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
    def test_get_attackers(self):
        # Check black queens pawn E7
        chessboard = Board()
        attackers_3_7 = chessboard._get_attackers('C7', Color.BLACK)
        assert_that(attackers_3_7, contains_inanyorder('D8'))

    def test_get_attackers_1_a(self):
        # Test some white pawns
        chessboard = Board()
        attackers_2_3 = chessboard._get_attackers('B3', Color.WHITE)
        assert_that(attackers_2_3, contains_inanyorder('A2', 'C2'))

    def test_get_attackers_1_b(self):
        # Two pawns and a knight can attack 3,3 (C3)
        chessboard = Board()
        attackers_3_3 = chessboard._get_attackers('C3', Color.WHITE)
        assert_that(attackers_3_3, contains_inanyorder('B1', 'B2', 'D2'))

    def test_get_attackers_1_c(self):
        # Check pawn in front of white rook
        chessboard = Board()
        attackers_8_2 = chessboard._get_attackers('H2', Color.WHITE)
        assert_that(attackers_8_2, contains_inanyorder('H1'))

    def test_get_attackers_1_e(self):
        # Check black kings pawn E7
        chessboard = Board()
        attackers_6_7 = chessboard._get_attackers('F7', Color.BLACK)
        assert_that(attackers_6_7, contains_inanyorder('E8'))

    def test_pawn_attackers_2(self):
        """Check pawn directly in front of white king

        Check that the king, queen, bishop and right knight all attack square B5

        """
        chessboard = Board()
        attackers_5_2 = chessboard._get_attackers('E2', Color.WHITE)
        assert_that(attackers_5_2, contains_inanyorder(
            'D1', 'E1', 'F1', 'G1'
        ))


if __name__ == '__main__':
        unittest.main()
