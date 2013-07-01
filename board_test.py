# -*- coding: UTF-8 -*-
# Unit tests for chess. Requires PyHamcrest to be installed.
# This can be easily done using any packaging tool (such as distribute).
# See https://code.google.com/p/hamcrest/ for more details on hamcrest matchers.
import board
from hamcrest import *
import unittest

class TestBoardFunctions(unittest.TestCase):
    def setUp(self):
        self.board = board.Board()

    def test_create_new_board(self):
        # Make sure that it is White player's turn to move
        white_player = board.White
        assert_that(self.board.current_player, equal_to(white_player))

        # Make sure a new board places all the pieces in the correct locations
        # Using 'internal' method get_piece check all of the White pieces
        assert_that(all_of(
            self.board.get_piece((1,1)), is_(board.Rook)),
            self.board.get_piece((1,1)).colour, is_(board.White)
        )
        assert_that(all_of(
            self.board.get_piece((2,1)), is_(board.Knight)),
            self.board.get_piece((2,1)).colour, is_(board.White)
        )
        assert_that(all_of(
            self.board.get_piece((3,1)), is_(board.Bishop)),
            self.board.get_piece((3,1)).colour, is_(board.White)
        )
        assert_that(all_of(
            self.board.get_piece((4,1)), is_(board.King)),            
            self.board.get_piece((4,1)).colour, is_(board.White)
        )                
        assert_that(all_of(
            self.board.get_piece((5,1)), is_(board.Queen)),
            self.board.get_piece((5,1)).colour, is_(board.White)
        )
        assert_that(all_of(
            self.board.get_piece((6,1)), is_(board.Bishop)),
            self.board.get_piece((6,1)).colour, is_(board.White)
        )
        assert_that(all_of(
            self.board.get_piece((7,1)), is_(board.Knight)),
            self.board.get_piece((7,1)).colour, is_(board.White)
        )
        assert_that(all_of(
            self.board.get_piece((8,1)), is_(board.Rook)),
            self.board.get_piece((8,1)).colour, is_(board.White)
        )
        assert_that(all_of(
            self.board.get_piece((1,2)), is_(board.Pawn)),
            self.board.get_piece((1,2)).colour, is_(board.White)
        )
        assert_that(all_of(
            self.board.get_piece((2,2)), is_(board.Pawn)),
            self.board.get_piece((2,2)).colour, is_(board.White)
        )
        assert_that(all_of(
            self.board.get_piece((2,2)), is_(board.Pawn)),
            self.board.get_piece((2,2)).colour, is_(board.White)
        )
        assert_that(all_of(
            self.board.get_piece((3,2)), is_(board.Pawn)),
            self.board.get_piece((3,2)).colour, is_(board.White)
        )
        assert_that(all_of(
            self.board.get_piece((4,2)), is_(board.Pawn)),
            self.board.get_piece((4,2)).colour, is_(board.White)
        )
        assert_that(all_of(
            self.board.get_piece((5,2)), is_(board.Pawn)),
            self.board.get_piece((5,2)).colour, is_(board.White)
        )
        assert_that(all_of(
            self.board.get_piece((6,2)), is_(board.Pawn)),
            self.board.get_piece((6,2)).colour, is_(board.White)
        )
        assert_that(all_of(
            self.board.get_piece((7,2)), is_(board.Pawn)),
            self.board.get_piece((7,2)).colour, is_(board.White)
        )
        assert_that(all_of(
            self.board.get_piece((8,2)), is_(board.Pawn)),
            self.board.get_piece((8,2)).colour, is_(board.White)
        )

        # Using 'internal' method get_piece check all of the Black pieces
        assert_that(all_of(
            self.board.get_piece((1,8)), is_(board.Rook)),
            self.board.get_piece((1,8)).colour, is_(board.Black)
        )
        assert_that(all_of(
            self.board.get_piece((2,8)), is_(board.Knight)),
            self.board.get_piece((2,8)).colour, is_(board.Black)
        )
        assert_that(all_of(
            self.board.get_piece((3,8)), is_(board.Bishop)),
            self.board.get_piece((3,8)).colour, is_(board.Black)
        )
        assert_that(all_of(
            self.board.get_piece((4,8)), is_(board.King)),
            self.board.get_piece((4,8)).colour, is_(board.Black)
        )                
        assert_that(all_of(
            self.board.get_piece((5,8)), is_(board.Queen)),
            self.board.get_piece((5,8)).colour, is_(board.Black)
        )
        assert_that(all_of(
            self.board.get_piece((6,8)), is_(board.Bishop)),
            self.board.get_piece((6,8)).colour, is_(board.Black)
        )
        assert_that(all_of(
            self.board.get_piece((7,8)), is_(board.Knight)),
            self.board.get_piece((7,8)).colour, is_(board.Black)
        )
        assert_that(all_of(
            self.board.get_piece((8,8)), is_(board.Rook)),
            self.board.get_piece((8,8)).colour, is_(board.Black)
        )
        assert_that(all_of(
            self.board.get_piece((1,7)), is_(board.Pawn)),
            self.board.get_piece((1,7)).colour, is_(board.Black)
        )
        assert_that(all_of(
            self.board.get_piece((2,7)), is_(board.Pawn)),
            self.board.get_piece((2,7)).colour, is_(board.Black)
        )
        assert_that(all_of(
            self.board.get_piece((2,7)), is_(board.Pawn)),
            self.board.get_piece((2,7)).colour, is_(board.Black)
        )
        assert_that(all_of(
            self.board.get_piece((3,7)), is_(board.Pawn)),
            self.board.get_piece((3,7)).colour, is_(board.Black)
        )
        assert_that(all_of(
            self.board.get_piece((4,7)), is_(board.Pawn)),
            self.board.get_piece((4,7)).colour, is_(board.Black)
        )
        assert_that(all_of(
            self.board.get_piece((5,7)), is_(board.Pawn)),
            self.board.get_piece((5,7)).colour, is_(board.Black)
        )
        assert_that(all_of(
            self.board.get_piece((6,7)), is_(board.Pawn)),
            self.board.get_piece((6,7)).colour, is_(board.Black)
        )
        assert_that(all_of(
            self.board.get_piece((7,7)), is_(board.Pawn)),
            self.board.get_piece((7,7)).colour, is_(board.Black)
        )
        assert_that(all_of(
            self.board.get_piece((8,7)), is_(board.Pawn)),
            self.board.get_piece((8,7)).colour, is_(board.Black)
        )

        # Check all the other squares are empty
        # This will return a horrible error message if it fails,
        # not telling us which square is wrong, but at least we'll
        # know to dig deeper. 
        # Using range instead of xrange for if/when we go to python 3
        for x in range(1,9): 
            for y in range(3, 7):
                assert_that(self.board.get_piece((x,y)), is_(None))


    def test_get_moves_opening_white_pawn(self):
        """Check that a white pawn can move from it's starting position as either a single or double move."""
        pawn_moves = self.board.get_moves((1, 2))
        assert_that(pawn_moves, contains_inanyorder((1, 3), (1, 4)))

    def test_get_moves_opening_black_pawn(self):
        """Check that a black pawn can move from it's starting position as either a single or double move."""
        pawn_moves = self.board.get_moves((6, 7))
        assert_that(pawn_moves, contains_inanyorder((6, 6), (6, 5)))

    def test_get_moves_moved_white_pawn(self):
        """Check that a white pawn that has moved can only move one space (when nothing to attack)."""
        pawn_board = board.Board("♖♘♗♕♔♗♘♖-♙♙_♙♙♙♙♙-__♙_____-________-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        pawn_moves = pawn_board.get_moves((3, 3))
        assert_that(pawn_moves, contains_inanyorder((3, 4)))

    def test_get_moves_white_pawn_attacks_both(self):
        """Check that a white pawn with 3 Black pieces in front can attack the two pieces on the sides only"""
        pawn_board = board.Board("♖♘♗♕♔♗♘♖-♙♙♙_♙♙♙♙-________-________-________-___♙___-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        pawn_moves = pawn_board.get_moves((4, 6))
        assert_that(pawn_moves, contains_inanyorder((3, 7), (5, 7)))

    def test_get_moves_black_pawn_attack_left(self):
        """Check that a black pawn next to the right board edge blocked by two white pieces can attak the piece diagonally left"""
        pawn_board = board.Board("♖♘♗♕♔♗♘♖-♙♙♙♙♙♙__-________-______♙♙-_______♟-________-♟♟♟♟♟♟♟_-♜♞♝♛♚♝♞♜,W,0,0")
        pawn_moves = pawn_board.get_moves((8, 5))
        assert_that(pawn_moves, contains_inanyorder((7, 4)))

    def test_get_moves_black_pawn_cant_attack_black(self):
        """Check that a black pawn can't attack it's own pieces."""
        pawn_board = board.Board("♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-______♟♟-_______♟-________-♟♟♟♟♟♟♟_-♜♞♝♛♚♝♞♜,W,0,0")
        pawn_moves = pawn_board.get_moves((8, 5))
        assert_that(pawn_moves, is_(set([])))     

    # TODO: 
    # Add more tests for the following
    # * Cannot attack own colour

    def test_get_moves_white_knight_opening(self):
        """Check the opening moves of a white knight."""
        knight_moves = self.board.get_moves((2,1))
        assert_that(knight_moves, contains_inanyorder((1, 3), (3, 3)))

    def test_get_moves_black_knight_opening(self):
        """Check the opening moves of a black knight."""
        knight_moves = self.board.get_moves((7, 8))
        assert_that(knight_moves, contains_inanyorder((6, 6), (8, 6)))

    def test_get_moves_knight_fork_attack(self):
        """Check if a knight at G3 can fork the king and rook, as well as other moves."""
        knight_board = board.Board("♖_♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-________-________-________-♟♟♘♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        knight_moves = knight_board.get_moves((3, 7))
        assert_that(knight_moves, contains_inanyorder((1, 8), (5, 8), (1, 6), (5, 6), (2, 5), (4, 5)))        

    def test_get_moves_white_bishop_opening(self):
        """Check the opening moves of a white bishop."""
        bishop_moves = self.board.get_moves((3,1))
        assert_that(bishop_moves, is_([]))

    def test_get_moves_black_bishop_opening(self):
        """Check the opening moves of a black bishop."""
        bishop_moves = self.board.get_moves((3,8))
        assert_that(bishop_moves, is_([]))        

    def test_get_moves_white_bishop_free(self):
        """Test get_moves for a white bishop in the middle of the board."""
        bishop_board = board.Board("♖♘_♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-________-____♗___-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        bishop_moves = bishop_board.get_moves((5,5))
        assert_that(bishop_moves, contains_inanyorder(
            (4, 6), (3, 7),  # forward left
            (6, 6), (7, 7),  # forward right
            (4, 4), (3, 3),  # backward left
            (6, 4), (7, 3)   # backward right
        ))

    def test_get_moves_black_bishop_free(self):
        """Test get_moves for a black bishop in the middle of the board."""
        bishop_board = board.Board("♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-________-___♝____-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚_♞♜,W,0,0")        
        bishop_moves = bishop_board.get_moves((4,5))
        assert_that(bishop_moves, contains_inanyorder(
            (3, 6), #(2, 7),  # forward left
            (5, 6), #(6, 7),  # forward right
            (3, 4), (2, 3), (1, 2),  # backward left
            (5, 4), (6, 3), (7, 2)   # backward right
        ))        

    def test_get_moves_white_rook_opening(self):
        """Test get_moves for the opening moves of a white rook."""
        rook_moves = self.board.get_moves((8,1))
        assert_that(rook_moves, is_([]))

    def test_get_moves_black_rook_opening(self):
        """Test get_moves for the opening moves of a black rook."""
        rook_moves = self.board.get_moves((8,8))
        assert_that(rook_moves, is_([]))

    def test_get_moves_white_rook_free(self):
        """Test get_moves for a white rook in the middle of the board."""
        rook_board = board.Board("♖♘♗♕♔♗♘_-♙♙♙♙♙♙♙♙-_♖______-________-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        rook_moves = rook_board.get_moves((2,3))
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
        H |♜|♞|♝|♛|♚|♝|♞|_|  
        G |♟|♟|♟|♟|♟|♟|♟|♟|  
        F |_|_|_|_|_|_|_|_|  
        E |_|_|_|_|_|_|_|_|
        D |_|_|_|_|_|_|_|_|  
        C |_|♜|_|_|_|_|_|_|  
        B |♙|♙|♙|♙|♙|♙|♙|♙|  
        A |♖|♘|♗|♕|♔|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           1 2 3 4 5 6 7 8
        """

        rook_board = board.Board("♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-_♜______-________-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞_,W,0,0")
        rook_moves = rook_board.get_moves((2,3))
        assert_that(rook_moves, contains_inanyorder(
            (2, 4), (2, 5), (2, 6),  # forward
            (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3),  # right
            (1, 3),  # left
            (2, 2)  # backward
        ))   

    def test_get_moves_white_queen_opening(self):
        """Test get_moves for the opening moves of a white queen."""
        queen_moves = self.board.get_moves((4,1))
        assert_that(queen_moves, is_([]))

    def test_get_moves_black_queen_opening(self):
        """Test get_moves for the opening moves of a black queen."""
        queen_moves = self.board.get_moves((4,8))
        assert_that(queen_moves, is_([]))

    def test_get_moves_white_queen_free(self):
        """Check the moves of a white queen in the open."""
        queen_board = board.Board("♖♘♗_♔♗♘♖-♙♙♙♙♙♙♙♙-________-___♕____-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        queen_moves = queen_board.get_moves((4,4))
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
        queen_board = board.Board("♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-___♛____-________-________-♟♟♟♟♟♟♟♟-♜♞♝_♚♝♞♜,W,0,0")
        queen_moves = queen_board.get_moves((4,4))    
        assert_that(queen_moves, contains_inanyorder(
            (4, 5), (4, 6), # forward
            (5, 5), (6, 6), # forward right
            (5, 4), (6, 4), (7, 4), (8, 4),  # right
            (5, 3), (6, 2), # backwards right
            (4, 3), (4, 2), # backward
            (3, 3), (2, 2), # backwards left
            (3, 4), (2, 4), (1, 4),  # left
            (3, 5), (2, 6)  # forward, left
        ))

    def test_get_moves_white_king_opening(self):
        """Check the opening moves of a white king."""
        king_moves = self.board.get_moves((5,1))
        assert_that(king_moves, is_([]))

    def test_get_moves_black_king_opening(self):
        """Check the opening moves of a black king."""
        king_moves = self.board.get_moves((5,8))
        assert_that(king_moves, is_([]))

    def test_get_moves_white_king_free(self):
        """Check the moves of a white king in the open."""
        king_board = board.Board("♖♘♗♕_♗♘♖-♙♙♙♙♙♙♙♙-________-___m♔____-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        king_moves = king_board.get_moves((4,4))
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
        king_board = board.Board("♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-___m♚____-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛_♝♞♜,W,0,0")
        king_moves = king_board.get_moves((4,4))
        assert_that(king_moves, contains_inanyorder(
            (4, 5),  # forward
            (5, 5),  # forward right
            (5, 4),  # right
            (3, 4),  # left
            (3, 5)   # forward, left
        ))

    def test_get_moves_pinned_knight(self):
        """Check that a pinned knight cannot move (as there is no way for it to still be blocking check if it moves)."""
        pinned_board = board.Board("♖♘♗♕♔♗_♖-♙♙♙♙♘♙♙♙-________-________-____♜___-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞_,W,0,0")
        knight_moves = pinned_board.get_moves((5,2))
        assert_that(knight_moves, is_([]))


    def test_get_moves_pawn_pinned_by_rook(self):
        """Test that a pawn pinned vertically by a rook can still move forward normally - in the direction it is pinned.

        The board looks like:
           ________________
        H |♜|♞|♝|♛|♚|♝|♞|_|
        G |♟|♟|♟|♟|♟|♟|♟|♟|
        F |_|_|_|_|_|_|_|_|
        E |_|_|_|_|♜|_|_|_|
        D |_|_|_|_|_|_|_|_|
        C |_|_|_|_|_|_|_|_|
        B |♙|♙|♙|♙|♙|♙|♙|♙|
        A |♖|♘|♗|♕|♔|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           1 2 3 4 5 6 7 8

        """
        pinned_board = board.Board("♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-________-____♜___-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞_,W,0,0")
        pawn_moves = pinned_board.get_moves((5, 2))
        assert_that(pawn_moves, contains_inanyorder((5, 3), (5, 4)))

    def test_get_moves_pawn_pinned_by_rook_2(self):
        """Test that a pawn pinned vertically by a rook can still move forward normally but cannot attack

        The board looks like:
           ________________
        H |♜|♞|♝|♛|♚|♝|♞|_|
        G |♟|♟|♟|_|♟|_|♟|♟|
        F |_|_|_|_|_|_|_|_|
        E |_|_|_|_|♜|_|_|_|
        D |_|_|_|_|_|_|_|_|
        C |_|_|_|♟|_|♟|_|_|
        B |♙|♙|♙|♙|♙|♙|♙|♙|
        A |♖|♘|♗|♕|♔|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           1 2 3 4 5 6 7 8
        """
        pinned_board = board.Board("♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-___♟_♟__-________-____♜___-________-♟♟♟_♟_♟♟-♜♞♝♛♚♝♞_,W,0,0")
        pawn_moves = pinned_board.get_moves((5, 2))
        assert_that(pawn_moves, contains_inanyorder((5, 3), (5, 4)))

    def test_get_moves_pawn_pinned_by_rook_3(self):
        """Test that a pawn pinned horizontally by a rook can still move forward normally but cannot attack

        The board looks like:
           ________________
        H |♜|♞|♝|♛|_|♝|♞|♜|  White pawn has double moved to D5. Black could
        G |♟|♟|♟|♟|♟|_|♟|♟|  capture via en passant but that would put Black's
        F |_|_|_|_|_|_|_|_|  king in check. Therefore can only move forward.
        E |_|_|_|_|_|_|_|_|
        D |♖|_|_|_|♙|♟|_|♚|  
        C |_|_|_|_|_|_|_|_|  
        B |♙|♙|♙|♙|_|♙|♙|♙|  
        A |♖|♘|♗|♕|♔|♗|♘|_|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           1 2 3 4 5 6 7 8
        """
        pinned_board = board.Board("♖♘♗♕♔♗♘_-♙♙♙♙_♙♙♙-________-♖___m♙♟_♚-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛_♝♞♜,W,0,0")
        pawn_moves = pinned_board.get_moves((6, 4))
        assert_that(pawn_moves, contains_inanyorder((6, 3)))

    def test_get_moves_pawn_pinned_by_rook_4(self):
        """Test that a pawn pinned horizontally by a rook can still move forward normally but cannot attack

        The board looks like:
           ________________
        H |♜|♞|♝|♛|_|♝|♞|♜|  Black pawn is pinned so cannot move.
        G |♟|♟|♟|♟|♟|_|♟|♟|  
        F |_|_|_|_|_|_|_|_|  
        E |_|_|_|_|_|_|_|_|
        D |♖|_|_|_|_|♟|_|♚|  
        C |_|_|_|_|_|_|_|_|  
        B |♙|♙|♙|♙|♙|♙|♙|♙|  
        A |♖|♘|♗|♕|♔|♗|♘|_|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           1 2 3 4 5 6 7 8
        """
        pinned_board = board.Board("♖♘♗♕♔♗♘_-♙♙♙♙♙♙♙♙-________-♖____♟_♚-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛_♝♞♜,W,0,0")
        pawn_moves = pinned_board.get_moves((6, 4))
        assert_that(pawn_moves, is_(set([])))

    def test_get_moves_pawn_pinned_by_bishop(self):
        """Test that a pawn pinned by a bishop cannot move

        The board looks like:
           ________________
        H |♜|♞|♝|♛|♚|♝|♞|♜|  Black pawn is pinned so cannot move.
        G |♟|♟|♟|♟|♟|♟|♟|♟|  
        F |_|_|_|_|_|_|_|_|  
        E |_|_|_|_|_|_|_|♗|
        D |_|_|_|_|_|_|_|_|  
        C |_|_|_|_|_|_|_|_|  
        B |♙|♙|♙|♙|♙|♙|♙|♙|  
        A |♖|♘|♗|♕|♔|_|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           1 2 3 4 5 6 7 8
        """
        pinned_board = board.Board("♖♘♗♕♔_♘♖-♙♙♙♙♙♙♙♙-________-________-_______♗-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        pawn_moves = pinned_board.get_moves((6, 7))
        assert_that(pawn_moves, is_(set([])))

    def test_get_moves_pawn_pinned_by_bishop_2(self):
        """Test that a pawn pinned by a bishop cannot move unless it can capture attacker

        The board looks like:
           ________________
        H |♜|♞|♝|♛|♚|♝|♞|♜|  Black pawn is pinned but can capture attacker.
        G |♟|♟|♟|♟|♟|♟|♟|♟|  
        F |_|_|_|_|_|_|♗|_|  
        E |_|_|_|_|_|_|_|_|
        D |_|_|_|_|_|_|_|_|  
        C |_|_|_|_|_|_|_|_|  
        B |♙|♙|♙|♙|♙|♙|♙|♙|  
        A |♖|♘|♗|♕|♔|_|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           1 2 3 4 5 6 7 8
        """
        pinned_board = board.Board("♖♘♗♕♔_♘♖-♙♙♙♙♙♙♙♙-________-________-________-______♗_-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        pawn_moves = pinned_board.get_moves((6, 7))
        assert_that(pawn_moves, contains_inanyorder((7,6)))

    def test_get_moves_pawn_pinned_by_bishop_3(self):
        """Test that a pawn pinned by a bishop cannot move unless it can capture attacker

        The board looks like:
           ________________
        H |♜|♞|♝|♛|♚|♝|♞|♜|  Black pawn is pinned but can capture attacker.
        G |♟|♟|♟|♟|♟|♟|♟|♟|  
        F |_|_|_|_|♙|_|♗|_|  
        E |_|_|_|_|_|_|_|_|
        D |_|_|_|_|_|_|_|_|  
        C |_|_|_|_|_|_|_|_|  
        B |♙|♙|♙|♙|_|♙|♙|♙|  
        A |♖|♘|♗|♕|♔|_|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           1 2 3 4 5 6 7 8
        """
        pinned_board = board.Board("♖♘♗♕♔_♘♖-♙♙♙♙_♙♙♙-________-________-________-____♙_♗_-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜,W,0,0")
        pawn_moves = pinned_board.get_moves((6, 7))
        assert_that(pawn_moves, contains_inanyorder((7,6)))

    def test_get_attackers(self):
        # Test some white pawns
        attackers_2_3 = self.board._get_attackers((2, 3), board.White)
        assert_that(attackers_2_3, contains_inanyorder((1, 2), (3, 2)))

        # Two pawns and a knight can attack 3,3 (C3)
        attackers_3_3 = self.board._get_attackers((3, 3), board.White)
        assert_that(attackers_3_3, contains_inanyorder((2, 2), (4, 2), (2, 1))) 

        # Check pawn in front of white rook
        attackers_8_2 = self.board._get_attackers((8, 2), board.White)
        assert_that(attackers_8_2, contains_inanyorder((8, 1))) 

        # Check black kings pawn E7
        attackers_6_7 = self.board._get_attackers((6, 7), board.Black)
        assert_that(attackers_6_7, contains_inanyorder((5, 8))) 

        # Check black queens pawn E7
        attackers_3_7 = self.board._get_attackers((3, 7), board.Black)
        assert_that(attackers_3_7, contains_inanyorder((4, 8)))

    def test_pawn_attackers_2(self):
        """Check pawn directly in front of white king
        
        Check that the king, queen, bishop and right knight all attack square B5

        The board looks like:
           ________________
        H |♜|♞|♝|♛|♚|♝|♞|♜| 
        G |♟|♟|♟|♟|♟|♟|♟|♟|  
        F |_|_|_|_|_|_|_|_|  
        E |_|_|_|_|_|_|_|_|
        D |_|_|_|_|_|_|_|_|  
        C |_|_|_|_|_|_|_|_|  
        B |♙|♙|♙|♙|♙|♙|♙|♙|  
        A |♖|♘|♗|♕|♔|♗|♘|♖|
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
           1 2 3 4 5 6 7 8
        """
        attackers_5_2 = self.board._get_attackers((5, 2), board.White)
        assert_that(attackers_5_2, contains_inanyorder(
            (4, 1), (5, 1), (6, 1), (7, 1)
        ))

    # TODO: test more castling combinations, and +ve / -ve testing
    def test_get_castle_moves(self):
        """Test castling left for both Black and White Kings."""
        castle_board = board.Board("♖___♔__♖-♙♙♙♙♙♙♙♙-________-________-________-________-♟♟♟♟♟♟♟♟-♜___♚__♜,W,0,0")
        assert_that(castle_board._get_castle_moves((5, 1)), contains_inanyorder((3, 1), (7, 1)))
        assert_that(castle_board._get_castle_moves((5, 8)), contains_inanyorder((3, 8), (7, 8)))

    def test_white_king_castle_left(self):
        """Test castling left for White King."""
        castle_board = board.Board("♖___♔__♖-♙♙♙♙♙♙♙♙-________-________-________-________-♟♟♟♟♟♟♟♟-♜___♚__♜,W,0,0")

        white_king = castle_board.get_piece((5, 1))
        white_rook = castle_board.get_piece((1, 1))
        assert_that(white_king, is_(board.WhiteKing))
        assert_that(white_rook, is_(board.WhiteRook))
        castle_board.move_piece((5, 1), (3, 1))
        assert_that(castle_board.get_piece((3, 1)), is_(white_king))
        assert_that(castle_board.get_piece((4, 1)), is_(white_rook))

    def test_white_king_castle_right(self):
        """Test castling right for White King."""
        castle_board = board.Board("♖___♔__♖-♙♙♙♙♙♙♙♙-________-________-________-________-♟♟♟♟♟♟♟♟-♜___♚__♜,W,0,0")

        white_king = castle_board.get_piece((5, 1))
        white_rook = castle_board.get_piece((8, 1))
        assert_that(white_king, is_(board.WhiteKing))
        assert_that(white_rook, is_(board.WhiteRook))
        castle_board.move_piece((5, 1), (7, 1))
        assert_that(castle_board.get_piece((7, 1)), is_(white_king))
        assert_that(castle_board.get_piece((6, 1)), is_(white_rook))

    def test_black_king_castle_left(self):
        """Test castling left for Black King."""
        castle_board = board.Board("♖___♔__♖-♙♙♙♙♙♙♙♙-________-________-________-________-♟♟♟♟♟♟♟♟-♜___♚__♜,W,0,0")

        black_king = castle_board.get_piece((5, 8))
        black_rook = castle_board.get_piece((1, 8))
        assert_that(black_king, is_(board.BlackKing))
        assert_that(black_rook, is_(board.BlackRook))
        castle_board.move_piece((5, 8), (3, 8))
        assert_that(castle_board.get_piece((3, 8)), is_(black_king))
        assert_that(castle_board.get_piece((4, 8)), is_(black_rook))

    def test_black_king_castle_right(self):
        """Test castling right for Black King."""
        castle_board = board.Board("♖___♔__♖-♙♙♙♙♙♙♙♙-________-________-________-________-♟♟♟♟♟♟♟♟-♜___♚__♜,W,0,0")

        black_king = castle_board.get_piece((5, 8))
        black_rook = castle_board.get_piece((8, 8))
        assert_that(black_king, is_(board.BlackKing))
        assert_that(black_rook, is_(board.BlackRook))
        castle_board.move_piece((5, 8), (7, 8))
        assert_that(castle_board.get_piece((7, 8)), is_(black_king))
        assert_that(castle_board.get_piece((6, 8)), is_(black_rook))

    def test_board_repr_1(self):
        """Serialize a board, restore it and re-serialize it, it is the same as the original?"""
        board_string = self.board.__repr__()
        board_string = repr(self.board)
        new_board = board.Board(board_string)
        new_board_string = repr(new_board)
        assert_that(board_string, equal_to(new_board_string))

    def test_move_pawn_forward_1(self):
        """Test if a pawn can move forward one space into an empty square."""
        board_ = board.Board()
        from_ = (1,2)
        to_ = (1,3)
        piece = board_.get_piece(from_)
        assert_that(board_.get_piece(to_), is_(None))
        # Move the white Pawn
        board_.move_piece(from_, to_)
        assert_that(board_.get_piece(from_), is_(None))
        assert_that(board_.get_piece(to_), is_(piece))

    def test_move_pawn_forward_2(self):
        """Test whether a pawn can move forward two spaces into an empty square.
        """
        board_ = board.Board()
        from_ = (4,7)
        to_ = (4,5)
        assert_that(board_.get_piece(to_), is_(None))
        piece = board_.get_piece(from_)
        # Move the Black Pawn
        board_.move_piece(from_, to_)
        assert_that(board_.get_piece(from_), is_(None))
        assert_that(board_.get_piece(to_), is_(piece))

    # TODO: assertRaises (part of unittest doesn't appear to like custom exceptions)
#    def test_move_pawn_invalid(self):
#        """Test whether a pawn can move forward two spaces into an empty square."""
#        board_ = board.Board()
#        from_ = (4,7)
#        to_ = (4,4)
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
        board_ = board.Board()
        from_ = (2,1)
        to_ = (3,3)
        assert_that(board_.get_piece(to_), is_(None))
        piece = board_.get_piece(from_) 
        # Move White Knight
        board_.move_piece(from_, to_)
        assert_that(board_.get_piece(from_), is_(None))
        assert_that(board_.get_piece(to_), is_(piece))

    def test_move_bishop(self):
        """Test whether a bishop can move diagonally.
        """
        board_ = board.Board()
        # Move pawn out of the way 1st
        from_ = (4,2)
        to_ = (4,3)
        board_.move_piece(from_, to_)

        from_ = (3,1)
        to_ = (7,5)
        piece = board_.get_piece(from_)

        # Move White Bishop 
        board_.move_piece(from_, to_)
        assert_that(board_.get_piece(from_), is_(None))
        assert_that(board_.get_piece(to_), is_(piece))
               
    def test_move_queen_forward(self):
        board_ = board.Board()
        # Move pawn out of the way 1st
        from_ = (4,2)
        to_ = (4,4)
        board_.move_piece(from_, to_)

        from_ = (4,1)
        to_ = (4,3)
        piece = board_.get_piece(from_)
        # Move White Queen 
        board_.move_piece(from_, to_)
        assert_that(board_.get_piece(from_), is_(None))
        assert_that(board_.get_piece(to_), is_(piece))

    def test_move_rook(self):
        """Test the moves of a rook."""
        board_ = board.Board()
        # Move pawn out of the way 1st
        from_ = (8,7)
        to_ = (8,5)
        board_.move_piece(from_, to_)       

        from_ = (8,8)
        to_ = (8,6)
        piece = board_.get_piece(from_)
        # Move black rook vertially
        board_.move_piece(from_, to_)
        assert_that(board_.get_piece(from_), is_(None))
        assert_that(board_.get_piece(to_), is_(piece))

        # Move again horizontally
        from_ = to_
        to_ = (4,6)
        board_.move_piece(from_, to_)
        assert_that(board_.get_piece(from_), is_(None))
        assert_that(board_.get_piece(to_), is_(piece))

    def test_move_king_diagonally(self):
        """Test moving the king diagonally."""
        board_ = board.Board()
        # Move pawn out of the way 1st
        from_ = (5,2)
        to_ = (5,3)
        board_.move_piece(from_, to_)

        from_ = (5,1)
        to_ = (5,2)
        piece = board_.get_piece(from_)        

        # Move the king
        board_.move_piece(from_, to_)
        assert_that(board_.get_piece(from_), is_(None))
        assert_that(board_.get_piece(to_), is_(piece))


    def test_en_passant(self):
        """Test whether a pawn can capture another via en-passant."""
        board_ = board.Board()
        # Move the white pawn first
        from_ = (5,2)
        to_ = (5,4)
        board_.move_piece(from_, to_)

        # Move it again, (we're allowed, the rules of a game don't apply just for board)
        from_ = to_
        to_ = (5,5)
        board_.move_piece(from_, to_)   
        white_pawn = board_.get_piece(to_)
        
        # Move a black pawn 'passed' this one
        black_pawn_loc = (4,5)
        board_.move_piece((4,7), black_pawn_loc)
        
        print board_.display()

        # Pre-move
        from_ = (5,5)
        to_ = (4,6)        
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

if __name__ == '__main__':
        unittest.main()
