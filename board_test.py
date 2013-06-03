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

    def test_get_pawn_moves(self):
        # TODO: 
        # Add more tests for the following
        # * Cannot attack own colour
        # * En passent

        # Check that a pawn can move from it's starting position as
        # Either a single or double move
        white_pawn = board.WhitePawn((1,2))
        pawn_moves = self.board._get_moves((1,2), white_pawn)
        assert_that(pawn_moves, only_contains((1,3),(1,4)))

        # Check that a pawn that has moved can only move one space
        white_pawn_2_4 = board.WhitePawn((2,4))
        white_pawn_2_4.has_not_moved = False
        white_pawn_moves_from_2_4 = self.board._get_moves((1,2), white_pawn_2_4)        
        assert_that(white_pawn_moves_from_2_4, only_contains((2,5)))

        # Check that a white pawn with 3 Black pieces in front can attack
        # The two pieces on the sides only
        white_pawn_2_6 = board.WhitePawn((2,6))
        white_pawn_2_6.has_not_moved = False
        white_pawn_moves_from_2_6 = self.board._get_moves((2, 6), white_pawn_2_6)        
        assert_that(white_pawn_moves_from_2_6, only_contains((1, 7), (3, 7))) 

        # Check that a Black pawn can do a single or double move from its
        # starting position
        black_pawn = board.BlackPawn((8,7))
        black_pawn_starting_moves = self.board._get_moves((8,7), black_pawn)
        assert_that(black_pawn_starting_moves, only_contains((8,6),(8,5)))

        # Check that a black pawn next to the right board edge blocked by
        # two white pieces can attak the piece diagonally left
        black_pawn_8_3 = board.BlackPawn((8,3))
        black_pawn_moves_from_8_3 = self.board._get_moves((8,3), black_pawn_8_3)
        assert_that(black_pawn_moves_from_8_3, only_contains((7,2)))

        #Check that a black pawn can't attack it's own peices
        black_pawn_7_8 = board.BlackPawn((7,8))
        black_pawn_moves_from_7_8 = self.board._get_moves((7,8), black_pawn_7_8)
        assert_that(black_pawn_moves_from_7_8, is_([]))

    def test_get_knight_moves(self):
        # Check the opening moves of a white knight
        white_knight = board.WhiteKnight()
        white_knight_moves_from_2_1 = self.board._get_moves((2,1), white_knight)
        assert_that(white_knight_moves_from_2_1, only_contains((1, 3), (3, 3)))

        # Check the opening moves of a black knight
        black_knight = board.BlackKnight()
        black_knight_moves_from_7_8 = self.board._get_moves((7, 8), black_knight)
        assert_that(black_knight_moves_from_7_8, only_contains((6, 6), (8, 6)))

        # Check some common attacks and moves
        white_knight_moves_from_3_7 = self.board._get_moves((3,7), white_knight)
        assert_that(white_knight_moves_from_3_7,
            only_contains((1, 8), (5, 8), (1, 6), (5, 6), (2, 5), (4, 5)))        

    def test_get_bishop_moves(self):

        # Check the opening moves of a white bishop
        white_bishop = board.WhiteBishop()
        white_bishop_moves_from_3_1 = self.board._get_moves((3,1), white_bishop)
        assert_that(white_bishop_moves_from_3_1, is_([]))

        # Check the opening moves of a black bishop
        black_bishop = board.BlackBishop()
        black_bishop_moves_from_3_8 = self.board._get_moves((3,8), black_bishop)
        assert_that(black_bishop_moves_from_3_8, is_([])) 

        # Check some common moves and attacks
        black_bishop_moves_from_4_5 = self.board._get_moves((4,5), black_bishop)
        assert_that(black_bishop_moves_from_4_5, only_contains(
            (3, 6), #(2, 7),  # forward left
            (5, 6), #(6, 7),  # forward right
            (3, 4), (2, 3), (1, 2),  # backward left
            (5, 4), (6, 3), (7, 2)   # backward right
        ))

        white_bishop_moves_from_5_5 = self.board._get_moves((5,5), white_bishop)
        assert_that(white_bishop_moves_from_5_5, only_contains(
            (4, 6), (3, 7),  # forward left
            (6, 6), (7, 7),  # forward right
            (4, 4), (3, 3),  # backward left
            (6, 4), (7, 3)   # backward right
        ))

    def test_get_rook_moves(self):
        # Check the opening moves of a white rook
        white_rook = board.WhiteRook()
        white_rook_moves_from_8_1 = self.board._get_moves((8,1), white_rook)
        assert_that(white_rook_moves_from_8_1, is_([]))

        # Check the opening moves of a black rook
        black_rook = board.BlackRook()
        black_rook_moves_from_8_8 = self.board._get_moves((8,8), black_rook)
        assert_that(black_rook_moves_from_8_8, is_([]))

        # Check the moves of a white rook in the open
        white_rook_moves_from_2_3 = self.board._get_moves((2,3), white_rook)
        assert_that(white_rook_moves_from_2_3, only_contains(
            (2, 4), (2, 5), (2, 6), (2, 7),  # forward
            (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3),  # right
            (1, 3)  # left
            # none backward
        ))

        # Check the moves of a black rook in the open
        black_rook_moves_from_2_3 = self.board._get_moves((2,3), black_rook)
        assert_that(black_rook_moves_from_2_3, only_contains(
            (2, 4), (2, 5), (2, 6), (2, 6),  # forward
            (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3),  # right
            (1, 3),  # left
            (2, 2)  # backward
        ))

    def test_get_queen_moves(self):
        # Check the opening moves of a white queen
        white_queen = board.WhiteQueen()
        white_queen_moves_from_4_1 = self.board._get_moves((4,1), white_queen)
        assert_that(white_queen_moves_from_4_1, is_([]))

        # Check the opening moves of a black queen
        black_queen = board.BlackQueen()
        black_queen_moves_from_4_8 = self.board._get_moves((4,8), black_queen)
        assert_that(black_queen_moves_from_4_8, is_([]))

        # Check the moves of a white queen in the open
        white_queen_moves_from_4_4 = self.board._get_moves((4,4), white_queen)
        assert_that(white_queen_moves_from_4_4, only_contains(
            (4, 5), (4, 6), (4, 7),  # forward
            (5, 5), (6, 6), (7, 7),  # forward right
            (5, 4), (6, 4), (7, 4), (8, 4),  # right
            (5, 3),  # backwards right
            (4, 3),  # backward
            (3, 3),  # backwards left
            (3, 4), (2, 4), (1, 4),  # left
            (3, 5), (2, 6), (1, 7)  # forward, left
        ))

        # Check the moves of a black queen in the open
        black_queen_moves_from_4_4 = self.board._get_moves((4,4), black_queen)
        assert_that(black_queen_moves_from_4_4, only_contains(
            (4, 5), (4, 6), # forward
            (5, 5), (6, 6), # forward right
            (5, 4), (6, 4), (7, 4), (8, 4),  # right
            (5, 3), (6, 2), # backwards right
            (4, 3), (4, 2), # backward
            (3, 3), (2, 2), # backwards left
            (3, 4), (2, 4), (1, 4),  # left
            (3, 5), (2, 6)  # forward, left
        ))

    def test_get_attackers(self):
        # Test some white pawns
        attackers_2_3 = self.board._get_attackers((2, 3), board.White)
        assert_that(attackers_2_3, only_contains((1, 2), (3, 2)))

        # Two pawns and a knight can attack 3,3 (C3)
        attackers_3_3 = self.board._get_attackers((3, 3), board.White)
        assert_that(attackers_3_3, only_contains((2, 2), (4, 2), (2, 1))) 

        # Check pawn in front of white rook
        attackers_8_2 = self.board._get_attackers((8, 2), board.White)
        assert_that(attackers_8_2, only_contains((8, 1))) 

        # Check black kings pawn E7
        attackers_6_7 = self.board._get_attackers((6, 7), board.Black)
        assert_that(attackers_6_7, only_contains((5, 8))) 

        # Check black queens pawn E7
        attackers_3_7 = self.board._get_attackers((3, 7), board.Black)
        assert_that(attackers_3_7, only_contains((4, 8))) 

        # Check pawn directly in front of white king
        attackers_5_2 = self.board._get_attackers((5, 2), board.White)
        assert_that(attackers_5_2, only_contains(
            (4, 1), (5, 1), (6, 1), (7, 1)
        )) 


    def test_get_king_moves(self):
        # Check the opening moves of a white king
        white_king = board.WhiteKing()
        white_king_moves_from_5_1 = self.board._get_moves((5,1), white_king)
        assert_that(white_king_moves_from_5_1, is_([]))

        # Check the opening moves of a black king
        black_king = board.BlackKing()
        black_king_moves_from_5_8 = self.board._get_moves((5,8), black_king)
        assert_that(black_king_moves_from_5_8, is_([]))

        # Check the moves of a white king in the open
        white_king_moves_from_4_4 = self.board._get_moves((4,4), white_king)
        assert_that(white_king_moves_from_4_4, only_contains(
            (4, 5),  # forward
            (5, 5),  # forward right
            (5, 4),  # right
            (5, 3),  # backwards right
            (4, 3),  # backward
            (3, 3),  # backwards left
            (3, 4),  # left
            (3, 5)   # forward, left
        ))

        # Check the moves of a black king in front of white pawns
        black_king_moves_from_4_4 = self.board._get_moves((4,4), black_king)
        assert_that(black_king_moves_from_4_4, only_contains(
            (4, 5),  # forward
            (5, 5),  # forward right
            (5, 4),  # right
            (3, 4),  # left
            (3, 5)   # forward, left
        ))

    # TODO: test more castling combinations, and +ve / -ve testing
    def test_get_castle_moves(self):
        """Test castling left for both Black and White Kings."""
        castle_board = board.Board("♖___♔__♖-♙♙♙♙♙♙♙♙-________-________-________-________-♟♟♟♟♟♟♟♟-♜___♚__♜,W,0,0")
        assert_that(castle_board._get_castle_moves((5, 1)), only_contains((3, 1), (7, 1)))
        assert_that(castle_board._get_castle_moves((5, 8)), only_contains((3, 8), (7, 8)))

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
