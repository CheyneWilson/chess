import numpy as np

_HAS_MOVED = 'm'
_EMPTY_SQUARE = '_'

class Colour(object): 
    code = '?'

    @classmethod
    def _get_colour(self, code):
        """Returns the class of the colour identified by its code.""" 
        for cls in Colour.__subclasses__():
            if cls.code == code:
                return cls
        
        raise ValueError("Invalid colour code '{0}.".format(code))


class Black(Colour): 
    code = 'B'


class White(Colour):
    code = 'W'


def _inverse_colour(colour):
    if colour is Black:
        return White
    elif colour is White:
        return Black
    else:
        raise ValueError("Invalid colour, expected Black or White")


class IllegalMoveException(Exception):
    """Raised when an attempt is made to move a piece illegally.

    Examples of illegal moves include moving a piece to a square it cannot
    move to, moving the King into check or moving a piece so as to leave the 
    king in check.
    """
    pass


class Move(object):
    from_ = None
    to_ = None
    piece = None
    # Did the the pawn moved two squares? Only valid for pawns
    double_move = False
    def __init__(self, piece, from_, to_):
        self.piece = piece
        self.from_ = from_
        self.to_ = to_
        if isinstance(piece,Pawn):
            if abs(from_[1] - to_[1]) == 2:  # The pawn moved two squares
                self.double_move = True
        else:
            self.double_move = False


class Square(object):
    """A single square on a chess board."""
    def __init__(self, loc, piece):
        self.location = loc
        self.piece = piece


class Board(object):
    """A new implemenation of a chessboard."""
    _previous_move = None
    current_player = None
    turn = 0
    stalemate_count = 0

    _all_pieces = None
    _king_locations = None
    

    def __init__(self, board_string=None):
        if board_string is None:
            self._new_board()
        else:
            self._create_board_from_repr(board_string)

    def get_piece(self, location):
        """Returns the piece at the location specified or None if the square
        is empty.
        """
        return self._all_pieces[location]

    def is_in_check(self, colour):
        """Returns True if the King of the colour specified is in check.
        """
        pass

    def is_in_checkmate(self, colour):
        """Returns True if the King of the colour specified is in checkmate.
        """
        pass

    def _get_castle_moves(self, from_):
        """Returns the locations the king  located at from_ can castle to.
        """
        [x, y] = from_
        king = self.get_piece(from_)
        left_rook = self.get_piece((1, y))
        right_rook = self.get_piece((1, y))

        moves = []
        if king is None or king.has_moved is True:
            return moves

        enemy_colour = _inverse_colour(king.colour)

        # Castling left?
        if left_rook.has_moved is False:
            left_4 = (4,y)
            left_3 = (3,y)
            left_2 = (2,y)
            # Empty squares
            if self.get_piece(left_2) is None: 
                if self.get_piece(left_3) is None: 
                    if self.get_piece(left_4) is None:
                        # With no attackers?
                        if self._get_attackers(left_2, enemy_colour) == set([]):
                            if self._get_attackers(left_3, enemy_colour) == set([]):
                                if self._get_attackers(left_3, enemy_colour) == set([]):
                                    moves.append(left_3)

        # Castling right?
        if right_rook.has_moved is False:
            right_6 = (6,y)
            right_7 = (7,y)
            # Empty squares
            if self.get_piece(right_6) is None:
                if self.get_piece(right_7) is None:
                    # Witg no attackers?
                    if self._get_attackers(right_6, enemy_colour) == set([]):
                        if self._get_attackers(right_7, enemy_colour) == set([]):
                            moves.append(right_7)

        return moves

    def _is_castle_right(self, from_, to_):
        """Returns True if the move is to castle right.

        Castling is preformed by first moving the king two squares in the 
        direction to castle. The castling rook is then moved to the other 
        side of the king. This method returns True if the King has been 
        moved two squares to the right, or False otherwise. 
        """

        [from_x, from_y] = from_
        [to_x, to_y] = to_
        if to_x - from_x == 2:
            if from_y == to_y:
                return True
        return False

    def _is_castle_left(self, from_, to_):
        """Returns True if the move is to castle left.

        Castling is preformed by first moving the king two squares in the 
        direction to castle. The castling rook is then moved to the other 
        side of the king. This method returns True if the King has been 
        moved two squares to the right, or False otherwise. 
        """

        [from_x, from_y] = from_
        [to_x, to_y] = to_
        if to_x - from_x == -2:
            if from_y == to_y:
                return True
        return False

    def move_piece(self, from_, to_):
        """Move a piece from the location from_ to the location to_.

        Raises a ValueError if the move is not a legal chess move.
        """
        legal_moves = self.get_moves(from_)
        piece = self._all_pieces[from_]
        if legal_moves is not False:
            if to_ in legal_moves:
                piece.location = to_ # Update the internal location to the new location 

                if self._is_en_passant_attack(from_):
                    # Remove the pawn that moved previously as it has been captured
                    # via en passant
                    self._all_pieces[self._previous_move.to_] = None                    
                elif self._is_castle_left(from_, to_):
                    # Move the rook too
                    y = from_[1]
                    rook = self._all_pieces[(1,y)]
                    self._all_pieces[(1,y)] = None
                    self._all_pieces[(4,y)] = rook
                elif self._is_castle_right(from_, to_):
                    # Move the rook too
                    y = from_[1]
                    rook = self._all_pieces[(8,y)]
                    self._all_pieces[(8,y)] = None
                    self._all_pieces[(6,y)] = rook

                # Keep track of where the king is
                if isinstance(piece, King):
                    self._king_location[piece.colour] = to_

                # TODO: Somewhere we need to check if this puts our king into check
                # This is partially handled, as the king himself can't move into check
                # A lazy way would be to move, check, and then roll back state if board
                # is 'invalid'.

                self._all_pieces[from_] = None
                self._all_pieces[to_] = piece
                self._previous_move = Move(piece, from_, to_)

                # These data structures must be kept in sync
                assert isinstance(self._all_pieces[self._king_location[Black]], BlackKing)
                assert isinstance(self._all_pieces[self._king_location[White]], WhiteKing)

                return
        # Fall through error
        raise IllegalMoveException("Move of '{0}' from {1} to {2} is not legal.".format(
                         piece, from_, to_))

    def _is_adjacent(self, loc_a, loc_b):
        """Returns True if two squares are horizontally, vertically or diagonally adjacent (side by side).
        """
        if loc_a[0] - loc_b[0] <= 1:
            if loc_a[0] - loc_b[1] <= 1:
                if loc_a != loc_b:
                    return True
        return False

    def _get_attackers(self, loc, colour):
        """Returns all of the pieces of a given colour that can attack a given location.
        """
        # At the given square (loc) we imagine where we could attack with each
        # of our pieces. If we use a knight as example, if any of the squares it 
        # can attack contain an enemy knight then that enemy knight is an attacker.
        # If those squares contain any other piece then they are not. Likewise if
        # we imagine a biship at the location, any bishops or queen it can attack
        # can also attack it. This is repeated for rooks, pawns, king and queen
        # The piece in the squares that potentially attacks this one are checked
        # for enemy pieces that can attack.
        attackers = set([])

        if colour is Black:
            knight = WhiteKnight()
            rook = WhiteRook()
            bishop = WhiteBishop()
            pawn = WhitePawn(loc)
        elif colour is White:
            knight = BlackKnight()
            rook = BlackRook()
            bishop = BlackBishop()
            pawn = BlackPawn(loc)

        # Get the squares of any knights that can attack this square
        knight_squares = self._get_knight_bishop_queen_rook_king_moves(knight, loc)
        for k in knight_squares:
            piece = self.get_piece(k)
            if isinstance(piece, Knight):
                # Opponents knight - an attacker
                attackers.add(k)

        rooks_or_queen_squares = self._get_knight_bishop_queen_rook_king_moves(rook, loc)
        for r in rooks_or_queen_squares:
            piece = self.get_piece(r)
            if isinstance(piece, Rook) or isinstance(piece, Queen):
                attackers.add(r)
            elif isinstance(piece, King):
                # King can only attack adjacent squares
                if self._is_adjacent(r, loc):
                    attackers.add(r)

        bishop_or_queen_squares = self._get_knight_bishop_queen_rook_king_moves(bishop, loc)
        for b in bishop_or_queen_squares:
            piece = self.get_piece(b)
            if isinstance(piece, Bishop) or isinstance(piece, Queen):
                attackers.add(b)
            elif isinstance(piece, King):
                # King can only attack adjacent squares
                if self._is_adjacent(b, loc):
                    attackers.add(b)

        pawn_squares = self._get_pawn_moves(pawn, True)       
        for p in pawn_squares:
            piece = self.get_piece(p)
            if isinstance(piece, Pawn):
                attackers.add(p)

        return attackers

    def _get_pinned_directions(self, from_):
        """Returns the directions a piece is pinned or None if it is not pinned."""

        piece = self.get_piece(from_)
        assert piece is not None
        colour = piece.colour
        enemy_colour = _inverse_colour(colour)

        # A piece can only be pinned if it's in a line with the king
        king_loc = self._king_location[colour]

        pinned_vector = (king_loc[0] - from_[0], king_loc[1] - from_[1])
        # Since only queen, rook and bishop can pin, 
        # pinned_vector must normalze to one of (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (1, -1)

        [x, y] = pinned_vector

        if x == 0:
            y = y / abs(y)
        elif y == 0:
            x = x / abs(x)
        elif x == y or x == -y:
            x = x / abs(x)
            y = y / abs(y)
        else:
            # Can't be pinned
            return None

        pinned_direction = (x, y)
        negative_pinned_direction = (-x, -y)
        # We're only pinned if there is an attacker in this direction
        squares = self._get_squares(from_, pinned_direction)
        # The last square will contain an attacker if there is any
        enemy_piece= squares[-1].piece
        if enemy_piece is not None and enemy_piece.colour is enemy_colour:
            if negative_pinned_direction in enemy_piece.moves:
                return [pinned_direction, negative_pinned_direction]

        return None

    def get_moves(self, loc):
        """Returns all of the valid moves for piece in the given location.

        loc -- The location of the piece to get the possible moves for.
        returns -- a set of all the legal moves from loc by the chess piece.
        """
        
        piece = self.get_piece(loc)
        if piece is None:
            raise ValueError("Square at location {0} is empty".format(loc))

        if isinstance(piece, King):
            moves = self._get_knight_bishop_queen_rook_king_moves(piece, loc)
            enemy_colour = _inverse_colour(piece.colour)

            # Can't move king into check
            new_moves = []
            for m in moves:                
                if len(self._get_attackers(m, enemy_colour)) > 0:
                    pass
                else:
                    new_moves.append(m)
            moves = new_moves

            # Add any castling moves
            moves.extend(self._get_castle_moves(loc))
        else:
            # Check if this piece is pinned, and then pass the limited move vector to
            # the _get_*piece*_moves methods. They need to be restricted in what they
            # search. pinned_direction = self._get_pinned_directions(loc)

            if isinstance(piece, Pawn):
                moves = self._get_pawn_moves(piece)
            elif isinstance(piece, Queen) or isinstance(piece, Rook) or isinstance(piece, Bishop) or isinstance(piece,  Knight):
                # A pinned piece can only move in the vector it is pinned in
                moves = self._get_knight_bishop_queen_rook_king_moves(piece, loc)
            
        return moves

    # TODO: Use direction tp limit the moves this peice can make when pinned
    def _get_knight_bishop_queen_rook_king_moves(self, piece, loc, direction=None):
        """Returns all of the location any of these pieces can move to from the
        location specified.

        direction -- limits the valid moves to only the direction vector (both +ve and -ve)
        """
        squares = []
        locations = []


        for direction in piece.moves:
            squares += self._get_squares(loc, direction, piece.limit)

        for s in squares:
            if s.piece is None or s.piece.colour is not piece.colour:
                # Can move to empty locations or squares with opponents pieces
                locations.append(s.location)
        
        return locations

    # TODO: Use direction tp limit the moves this peice can make when pinned
    def _get_pawn_moves(self, piece, attacks_only=False, direction=None):
        """Returns all of the valid moves for a board in the location from_
        specified. Does not check if the move will put the mover into check.

        If attacks_only is True, then only returns the squares threatened by
        this piece.
        """

        #TODO check_is_pinned

        moves = []
        if not attacks_only:
            # Pawns can move one space forward
            if self.get_piece(piece.single_move()) is None:
                moves.append(piece.single_move())                
                if piece.has_moved is False:
                    # On their first move, they can double move
                    if self.get_piece(piece.double_move()) is None:                        
                        moves.append(piece.double_move())

        # Normal Attacks
        for square in piece.attack():
            target = self.get_piece(square)
            if target is not None and target.colour is not piece.colour:
                moves.append(square)

        # En passant?
        # If the previous move was a double move by a pawn, and that pawn has
        # moved to the left or the right of this piece, then it may be
        # captured via en passant.
        if self._previous_move is not None and self._previous_move.double_move:
            # Don't need to check left and right are valid as the previous
            # move will be, and this only passes on equality. Colour of piece
            # being attacked also guarenteed to be oponents in normal game
            if self._previous_move.to_ == piece.attack_en_passant_left():
                moves.append(piece.attack_left())
            elif self._previous_move.to_ == piece.attack_en_passant_right():
                moves.append(piece.attack_right())           

        return moves

    def _is_en_passant_attack(self, from_):
        """Returns True if an attack can be made from the location from_ via via en passant"""
        piece = self.get_piece(from_)
        # Only pawns can do en passant
        if isinstance(piece, Pawn): 
            # 1st move has no previous
            if self._previous_move is not None:  
                # En passant only possible when eneny pawn does double move
                if self._previous_move.double_move:  # Implies pawn
                    [x,y] = from_
                    [prev_x, prev_y] = self._previous_move.to_
                    if prev_y == y:  # Same row
                        if abs(prev_x - x) == 1 :  # Adjacent square
                            return True

        return False

    def _get_squares(self, from_, direction, limit=None):
        """Returns an ordered list of squares on a chess board from from_ in
        the direction dir_ given. This does not include the starting square.

        Stops when any of the following are True: another piece is encountered
        or limit is reached, or the move is off the board.
        """
        squares = []
        i = 1
        while limit is None or i <= limit:
            loc = tuple(np.array(from_) + i * np.array(direction))
            i += 1
            try:
                piece = self.get_piece(loc) # Will raise a KeyError if we step off the board
                square = Square(loc, piece)
                squares.append(square)
                if square.piece is not None:
                    # We've found another piece
                    break
            except KeyError:
                # We've stepped off the board
                break
        return squares


    def get_pieces(self, player):
        """Returns all of the pieces owned by a given player."""
        pass

    @staticmethod
    def _valid_location(loc):
        """Returns True if the location (x,y) is within chess board."""
        [x, y] = loc
        if 1 <= x <= 8 and 1 <= y <= 8:
            return True
        return False

    def _new_board(self):
        """Places all of the pieces on the chessboard in their starting
        positions and assign white player first turn."""
        self._previous_move = None
        self.turn = 0
        self.stalemate_count = 0
        self.current_player = White
        self._all_pieces = dict()
        self._king_location = dict()

        # Place all the White pieces on the board
        self._all_pieces[(1, 1)] = WhiteRook()
        self._all_pieces[(2, 1)] = WhiteKnight()
        self._all_pieces[(3, 1)] = WhiteBishop()
        self._all_pieces[(4, 1)] = WhiteQueen()
        self._all_pieces[(5, 1)] = WhiteKing()
        self._all_pieces[(6, 1)] = WhiteBishop()
        self._all_pieces[(7, 1)] = WhiteKnight()
        self._all_pieces[(8, 1)] = WhiteRook()
        self._all_pieces[(1, 2)] = WhitePawn((1, 2))
        self._all_pieces[(2, 2)] = WhitePawn((2, 2))
        self._all_pieces[(3, 2)] = WhitePawn((3, 2))
        self._all_pieces[(4, 2)] = WhitePawn((4, 2))
        self._all_pieces[(5, 2)] = WhitePawn((5, 2))
        self._all_pieces[(6, 2)] = WhitePawn((6, 2))
        self._all_pieces[(7, 2)] = WhitePawn((7, 2))
        self._all_pieces[(8, 2)] = WhitePawn((8, 2))

        # Place all the Black pieces on the board
        self._all_pieces[(1, 8)] = BlackRook()
        self._all_pieces[(2, 8)] = BlackKnight()
        self._all_pieces[(3, 8)] = BlackBishop()
        self._all_pieces[(4, 8)] = BlackQueen()        
        self._all_pieces[(5, 8)] = BlackKing()
        self._all_pieces[(6, 8)] = BlackBishop()
        self._all_pieces[(7, 8)] = BlackKnight()
        self._all_pieces[(8, 8)] = BlackRook()
        self._all_pieces[(1, 7)] = BlackPawn((1, 7))
        self._all_pieces[(2, 7)] = BlackPawn((2, 7))
        self._all_pieces[(3, 7)] = BlackPawn((3, 7))
        self._all_pieces[(4, 7)] = BlackPawn((4, 7))
        self._all_pieces[(5, 7)] = BlackPawn((5, 7))
        self._all_pieces[(6, 7)] = BlackPawn((6, 7))
        self._all_pieces[(7, 7)] = BlackPawn((7, 7))
        self._all_pieces[(8, 7)] = BlackPawn((8, 7))

        # Locate the black and white kings
        self._king_location[White] = (5, 1)
        self._king_location[Black] = (5, 8)

        # These data structures must be kept in sync
        assert isinstance(self._all_pieces[self._king_location[Black]], BlackKing)
        assert isinstance(self._all_pieces[self._king_location[White]], WhiteKing)        

        # Add all of the empty squares
        for x in xrange(1,9):
            for y in xrange(3, 7):
                self._all_pieces[(x,y)] = None
    
    def __repr__(self):
        """Returns a string representation of the chess board that can be reconstructed when passed to the constructor."""
        # 1 indexed chessboard, 1 <= x < 9, 1 <= y < 9
        # xrange would be more a more efficient implemenation but this is a
        # minor and in python 3.x we get this benefit implicitly
        board_string = u""

        for y in range(1, 9):
            for x in range(1, 9):
                piece = self._all_pieces.get((x, y))
                if piece is not None:
                    # Encode the state information that the piece 'has moved', so cannot castle
                    # This is encoded before the piece because it makes re-parsing easier
                    if (isinstance(piece, King) or isinstance(piece, Rook)):
                        if piece.has_moved is False:
                            pass
                        else:
                            board_string += _HAS_MOVED
                    board_string += piece.symbol
                else:
                    board_string += _EMPTY_SQUARE
            if y < 8:
                board_string += '-'

        board_repr =  u'{0},{1},{2},{3}'.format(board_string, self.current_player.code,self.turn, self.stalemate_count)
        return board_repr.encode('utf-8')

    def _create_board_from_repr(self, board_string):
        """Creates a new board from the board described by board_string."""
        unicode_board_string = board_string.decode('utf-8')
        [piece_string, player_colour_code, turn, stalemate_count] = unicode_board_string.split(u',')
        
        self._previous_move = None

        self.current_player = Colour._get_colour(player_colour_code)
        self.turn = turn
        self.stalemate_count = stalemate_count      
        self._all_pieces = dict()
        self._king_location = dict()

        row_strings = piece_string.split(u'-')
        y = 0
        for row in row_strings:
            y += 1
            x = 0
            has_moved = False
            for symbol in row:
                if symbol == _HAS_MOVED:
                    # This is meta data
                    has_moved = True
                else:
                    x += 1
                    loc = (x, y)
                    if symbol == _EMPTY_SQUARE:
                        self._all_pieces[loc] = None
                    else:
                        cls = Piece.get_piece_class(symbol)

                        if issubclass(cls, Pawn):
                            self._all_pieces[loc] = cls(loc)
                        elif issubclass(cls, King):
                            # Cannot handle multiple kings of the the same colour, just saying
                            self._king_location[cls.colour] = loc
                            self._all_pieces[loc] = cls(has_moved)
                        elif issubclass(cls, Rook): 
                            self._all_pieces[loc] = cls(has_moved)
                        elif issubclass(cls, Knight) or issubclass(cls, Bishop) \
                                or issubclass(cls, Queen): 
                            self._all_pieces[loc] = cls()
                        else:
                            raise ValueError("Invalid chess piece {0}".format(symbol))
                        has_moved = False

        # These data structures must be kept in sync
        assert isinstance(self._all_pieces[self._king_location[Black]], BlackKing)
        assert isinstance(self._all_pieces[self._king_location[White]], WhiteKing)

    def display(self):
        """Prints out a unicode representation of the chess board.
        """
        WHITE_SQUARE = u"\u25a8"
        BLACK_SQUARE = u"\u25a2"
        line = u""
        # 1 indexed chessboard, 1 <= x < 9
        for y in range(8, 0, -1):
            # Row number
            line += u"{0} ".format(y)
            for x in range(1, 9, 1):
                current_piece = self._all_pieces.get((x, y))
                if current_piece is not None:
                    # Display the piece on the square it occupies.
                    line += u"{0} ".format(current_piece.symbol)
                else:
                    # Paint empty squares black / white like a chess board.
                    # The bottom-right-hand corner (if visible) must be a white
                    # square.
                    if (x + y) % 2 == 0:
                        line += WHITE_SQUARE + u" "
                    else:
                        line += BLACK_SQUARE + u" "
            line += u"\n"
        else:
            line += u"  A B C D E F G H "
        return line


class Piece(object):
    symbol = u'?'
    colour = None
    # A numerical limit to the number of squares this piece can move in
    # If none then it can move an unlimted amount in a direction
    limit = None  
 
    # Return a unicode encoded string representation
    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.symbol

    def move(self, location):
        """Move a piece to the location specified. Does not check if this
        is a legal chess move.
        """
        self.has_moved = True
        self.location = location

    @classmethod
    def get_piece_class(self, symbol):
        """Returns class the piece identified by its unicode symbol
           Raises a ValueError if the code is invalid.
        """ 
        for cls in Piece.__subclasses__():
            if cls.symbol == symbol:
                return cls
        
        raise ValueError()

class King(object):
    """The King chess piece.

    This should not be created directly, instead a BlackKing or WhiteKing
    should be instanciated.
    """
    def __new__(cls, *args, **kwargs):
        if cls is King:
            raise TypeError("King class may not be instantiated.")
        return object.__new__(cls, *args, **kwargs)

    moves = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1),
            (1, -1)]  # x,y
    limit = 1  # The King may only move one place via his move vectors
    has_moved = False


class WhiteKing(King, Piece):
    """The White King chess piece."""
    symbol = u'\u2654'
    colour = White

    def __init__(self, has_moved=False):
        self.has_moved = has_moved


class BlackKing(King, Piece):
    """The Black King chess piece."""
    symbol = u'\u265a'
    colour = Black

    def __init__(self, has_moved=False):
        self.has_moved = has_moved        


class Queen(object):
    """The Queen chess piece.

    This should not be created directly, instead a BlackQueen or WhiteQueen
    should be instanciated.
    """
    def __new__(cls, *args, **kwargs):
        if cls is Queen:
            raise TypeError("Queen class may not be instantiated.")
        return object.__new__(cls, *args, **kwargs)  

    moves = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1),
            (1, -1)]  # x,y


class WhiteQueen(Queen, Piece):
    """The White Queen chess piece."""
    symbol = u'\u2655'
    colour = White


class BlackQueen(Queen, Piece):
    """The Black Queen chess piece."""
    symbol = u'\u265b'
    colour = Black


class Rook(object):
    """The Rook (castle) chess piece.

    This should not be created directly, instead a BlackRook or WhiteRook
    should be instanciated.
    """
    def __new__(cls, *args, **kwargs):
        if cls is Rook:
            raise TypeError("Rook class may not be instantiated.")
        return object.__new__(cls, *args, **kwargs)   

    moves = [(1, 0), (0, 1), (-1, 0), (0, -1)] 
    has_moved = False


class WhiteRook(Rook, Piece):
    """The White Rook chess piece."""
    symbol = u'\u2656'
    colour = White

    def __init__(self, has_moved=False):
        self.has_moved = has_moved


class BlackRook(Rook, Piece):
    """The Black Rook chess piece."""
    symbol = u'\u265c'
    colour = Black

    def __init__(self, has_moved=False):
        self.has_moved = has_moved


class Bishop(object):
    """The Bishop chess piece.

    This should not be created directly, instead a BlackBishop or WhiteBishop
    should be instanciated.
    """
    def __new__(cls, *args, **kwargs):
        if cls is Bishop:
            raise TypeError("Bishop class may not be instantiated.")
        return object.__new__(cls, *args, **kwargs)   

    moves = [(1, 1), (-1, 1), (-1, -1), (1, -1)]  # x,y              


class WhiteBishop(Bishop, Piece):
    """The White Bishop chess piece."""
    symbol = u'\u2657'
    colour = White


class BlackBishop(Bishop, Piece):
    """The Black Bishop chess piece."""
    symbol = u'\u265d'
    colour = Black


class Knight(Piece):
    """The Knight chess piece.

    This should not be called directly, instead a BlackKnight or WhiteKnight
    should be instanciated.
    """
    def __new__(cls, *args, **kwargs):
        if cls is Knight:
            raise TypeError("Knight class may not be instantiated.")
        return object.__new__(cls, *args, **kwargs)

    # All moves a knight may make
    moves = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1),
            (-2, 1), (-1, 2)]  # x, y
    limit = 1  # Knights only move one place via their move vectors       

        
class WhiteKnight(Knight, Piece):
    """The White Knight chess piece."""
    symbol = u'\u2658'
    colour = White


class BlackKnight(Knight, Piece):
    """The Black Knight chess piece."""
    symbol = u'\u265e'
    colour = Black        


class Pawn(object):
    """The Pawn chess piece.

    This should not be called directly, instead a  BlackPawn or WhitePawn
    should be instanciated.
    """
    def __new__(cls, *args, **kwargs):
        if cls is Pawn:
            raise TypeError("Pawn class may not be instantiated.")
        return object.__new__(cls, *args, **kwargs)

    def single_move(self):
        """Returns the location of the square infront of this piece.
        """
        return (self.location[0], self.location[1] + self.forward)

    def double_move(self):
        """Returns the location two squares infrom of this piece. 
        Can be the first move of this piece.
        """
        return (self.location[0], self.location[1] + 2 * self.forward)

    def attack(self):
        """Return the locations this piece can attack."""
        locations = []
        left = self.attack_left()
        right = self.attack_right()
        if left is not None:
            locations.append(left)
        if right is not None:
            locations.append(right)
        return locations

    def attack_left(self):
        """Return the left location this piece can attack."""
        # Used with en passant left
        x = self.location[0] - 1
        y = self.location[1] + self.forward
        if x >= 1:
            return (x, y)

    def attack_right(self):
        """Return the right location this piece can attack."""
        # Used with en passant right
        x = self.location[0] + 1
        y = self.location[1] + self.forward
        if x <= 8:
            return (x, y)

    def attack_en_passant(self, to_):
        """Returns the location this piece can capture via en passent when moving to to_.

        If the to_move is not valid, return None
        """
        # Effectively this is just attacking the piece beside us
        (x, y) = to_
        if self.location[1] == y:  # In the same row
            if abs(self.location[0] - x) == 1:  # Adjacent
                return (x, self.location[1])
        return None

    def attack_en_passant_left(self):
        """Return one of the locations this piece may attack a pawn via en passant.

        En passent is a special pawn capture which can occur immediately 
        after a player does a 'double move' from its starting position, and
        the oppoents pawn could have captured it had the same pawn moved only
        one square forward. The opponent captures the just-moved pawn as if 
        taking it "as it passes" through the first square.
        """
        x = self.location[0] - 1
        y = self.location[1]
        if x >= 1:            
            return (x,y)

    def attack_en_passant_right(self):
        """Return one of the locations this piece may attack a pawn via en passant.

        En passent is a special pawn capture which can occur immediately 
        after a player does a 'double move' from its starting position, and
        the oppoents pawn could have captured it had the same pawn moved only
        one square forward. The opponent captures the just-moved pawn as if 
        taking it "as it passes" through the first square.
        """        
        x = self.location[0] + 1
        y = self.location[1]
        if x <= 8:
            return (x,y)


class WhitePawn(Pawn, Piece):
    """A White Pawn chess piece."""
    symbol = u'\u2659'
    colour = White

    def __init__(self, location):
        if Board._valid_location(location):
            self.location = location
        else:
            raise ValueError("Invalid location {1}".format(location))

        # has_moved is used for determining if the pawn can double move
        if location[1] == 2:
            self.has_moved = False
        else:
            self.has_moved = True

        self.forward = 1  # Based off White starting at rows 1,2


class BlackPawn(Pawn, Piece):
    """A Black Pawn chess piece."""
    symbol = u'\u265f'
    colour = Black

    def __init__(self, location):
        if Board._valid_location(location):
            self.location = location
        else:
            raise ValueError("Invalid location {1}".format(location))

        # has_moved is used for determining if the pawn can double move
        if location[1] == 7:
            self.has_moved = False
        else:
            self.has_moved = True

        self.forward = -1 # Based off Black starting at rows 7,8
