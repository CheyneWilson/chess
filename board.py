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
    """Returns the opposite colour to the one provided. """
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

class InvalidBoardException(Exception):
    """Returned if a chess board cannot represent a legal game board."""
    pass

class Move(object):
    from_ = None
    to_ = None
    piece = None
    # Did the the pawn moved two squares? Only valid for pawns
    is_double_move = False
    def __init__(self, piece, from_, to_):
        self.piece = piece
        self.from_ = from_
        self.to_ = to_
        if isinstance(piece,Pawn):
            if abs(from_[1] - to_[1]) == 2:  # The pawn moved two squares
                self.is_double_move = True
        else:
            self.is_double_move = False


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
    # _stalemate_count gets incremented each time a player moves if they do not
    # capture a peice or advance a pawn. If a pawn is advanced or a piece is
    # captured then the counter is reset to 0. If _stalemate_count is greater
    # than 100 (50 per place), at the start of any turn a player (may) declare
    # a stalemate.
    #
    # See http://en.wikipedia.org/wiki/Fifty-move_rule
    _stalemate_count = 0

    _all_pieces = None
    _king_location = None    

    def __init__(self, board_string=None):
        if board_string is None:
            self._new_board()
        else:
            self._create_board_from_repr(board_string)

    def get_piece(self, location):
        """Returns the piece at the location specified or None if the square
        is empty.
        """
        [x,y] = location
        if 1 <= x <= 8 and 1 <= y <= 8:
            return self._all_pieces.get(location, None)
        else:
            raise KeyError()

    def is_check(self, colour):
        """Returns True if the King of the colour specified is in check.
        """
        loc = self._king_location[colour]
        enemy_colour = _inverse_colour(colour)
        if len(self._get_attackers(loc, enemy_colour)) > 0:
            return True
        return False

    def is_checkmate(self, colour):
        """Returns True if the King of the colour specified is in checkmate.
        """
        king_loc = self._king_location[colour]
        enemy_colour = _inverse_colour(colour)
        enemy_attacking_pieces = self._get_attackers(king_loc, enemy_colour)

        if len(enemy_attacking_pieces) == 0:
            # Not under attack
            return False
        elif len(enemy_attacking_pieces) == 1:
            if len(self.get_moves(king_loc)) == 0:
                # Can't move
                # Can we capture the attacking piece?
                [enemy_loc] = enemy_attacking_pieces
                our_attackers = self._get_attackers(enemy_loc, colour)
                for loc in our_attackers: # If we have any...
                    if isinstance(self.get_piece(loc), King):
                        # If it's the king then since we know we can't
                        # legally move, ignore
                        continue
                    elif len(self._get_pinned_directions(loc)) == 0:
                        # Can capture the piece putting the king in 
                        # check
                        return False
                    else:
                        # Can't be pinned by piece causing check
                        # Therefore moving this piece is of no value
                        continue
                # Can we block the attacking piece?

                v = (enemy_loc[0]-king_loc[0], enemy_loc[1]-king_loc[1])
                attack_vector = self._normalize_vector(v)
                blocking_squares = self._get_squares(king_loc, attack_vector, capture=False)

                for s in blocking_squares:
                    # TODO: Find all the pieces that can move into these squares
                    # TODO: _get_attackers also counts itself... redundant call
                    block_locs = self._get_attackers(s.location, colour, True)
                    for b in block_locs:
                        if not isinstance(self.get_piece(b), King):
                            # Can block, not checkmate
                            return False

                # Can't move, and can't capture, checkmate
                return True
            else:
                # Can move, not checkmate
                return False
        else:
            # It is Impossible to capture / block 2 peices with one move
            return True

    def is_stalemate(self, colour):
        """Check to see if the specified player is in stalemate.

        colour -- The colour of the player to check if they're in statemate.

        """
        # Check that at least one player has a pawn or more than 3 points
        has_pawn = False
        white_score = 0
        black_score = 0
        for loc in self._all_pieces:
            piece = self._all_pieces[loc]
            if isinstance(piece, Pawn):
                has_pawn = True
            if piece.colour is White:
                white_score += piece.value
            elif piece.colour is Black:
                black_score += piece.value
            else:
                raise ValueError()

        if black_score <= 3 and white_score <= 3 and not has_pawn:
            # Neither player can checkmate
            return True

        # Check whether the 'colour' player can move any of their pieces
        for loc in self._all_pieces:
            piece = self._all_pieces[loc]
            if piece.colour is colour:
                if len(self.get_moves(loc)) != 0:
                    # This player can move
                    return False
        else:
            # This player cannot move -> stalemate
            return True

    def _get_castle_moves(self, from_):
        """Returns the locations the king located at from_ can castle to.
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
        if left_rook is not None and left_rook.has_moved is False:
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
        if right_rook is not None and right_rook.has_moved is False:
            right_6 = (6,y)
            right_7 = (7,y)
            # Empty squares
            if self.get_piece(right_6) is None:
                if self.get_piece(right_7) is None:
                    # With no attackers?
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

        Raises -- A ValueError if the move is not a legal chess move.
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

                # Keep track of 50 move stalemate
                if isinstance(piece, Pawn):
                    self._stalemate_count = 0
                elif self._all_pieces.get(to_, None) is None:
                    # No capture
                    self._stalemate_count += 1
                else:
                    # A capture
                    self._stalemate_count = 0

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

    def is_fifty_move_stalemate(self):
        """Returns True if 50 consective moves have been taken by either 
        player where no pawn has been advanced and no piece captured.

        The fifty move chess rule means a player *may choose* to call a game a
        draw at the start of their turn:
        http://en.wikipedia.org/wiki/Fifty-move_rule
        """
        if self.stalemate_count <= 100:
            return True
        else:
            return False

    def _is_adjacent(self, loc_a, loc_b):
        """Returns True if two squares are horizontally, vertically or diagonally adjacent (side by side).
        """
        if loc_a[0] - loc_b[0] <= 1:
            if loc_a[1] - loc_b[1] <= 1:
                if loc_a != loc_b:
                    return True
        return False

    def _get_attackers(self, loc, colour, blocker=False):
        """Returns the locations of the pieces of the colour specified that
        can attack the given location.

        loc     -- A (x, y) tuple representing the board location of the square.
        colour  -- The colour of the attacking pieces
        returns -- A set of (x,y) locations of all the pieces of the specified
                  colour that can attack the loc provided.
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
            pawn_2 = BlackPawn(loc)
        elif colour is White:
            knight = BlackKnight()
            rook = BlackRook()
            bishop = BlackBishop()
            pawn = BlackPawn(loc)
            pawn_2 = WhitePawn(loc)

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

        if blocker:
            pawn_squares = self._get_pawn_move_to(pawn_2, loc)
        else:
            pawn_squares = self._get_pawn_attacks(pawn)
        for p in pawn_squares:
            piece = self.get_piece(p)
            if isinstance(piece, Pawn):
                attackers.add(p)

        return attackers

    def _normalize_vector(self, vector):
        """Reduce lenth of the x and y parts of the veror to 1 while
        maintaining the same direction (if possible).

        vector  -- A tuple of the form (x, y)
        returns -- one of (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1),
                (1,-1) or if the vector cannot be normalized then returns None
        """
        [x, y] = vector 

        if x == 0:
            y = y / abs(y)
        elif y == 0:
            x = x / abs(x)
        elif x == y or x == -y:
            x = x / abs(x)
            y = y / abs(y)
        else:
            # Can't be normalized
            return None
        return (x, y)


    def _get_pinned_directions(self, from_):
        """Returns the directions a piece is pinned or an empty set if it is 
        not pinned.


        """

        piece = self.get_piece(from_)
        assert piece is not None
        colour = piece.colour
        enemy_colour = _inverse_colour(colour)

        # A piece can only be pinned if it's in a line with the king
        king_loc = self._king_location[colour]
        pinned_vector = (from_[0] - king_loc[0], from_[1] - king_loc[1])

        # Since only queen, rook and bishop can pin
        # pinned_vector must normalze to one of (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (1, -1)
        vector = self._normalize_vector(pinned_vector)
        if vector is None:
            # Can't be pinned
            return set([])

        [x, y] = vector
        pinned_direction = (x, y)
        negative_pinned_direction = (-x, -y)

        # We're only pinned if there is an attacker in this direction
        # An execption to this is a pawn may be prevented from attacking
        # via en passant, but that is a rare case and the logic is handled
        # there to reduce general complexity
        squares = self._get_squares(from_, pinned_direction)
    
        if not squares:
            # We can't be pinned by pieces not on the board
            return set([])

        # The last square will contain an attacker if there is any            
        enemy_piece= squares[-1].piece

        if enemy_piece is not None and enemy_piece.colour is enemy_colour:
            if negative_pinned_direction in enemy_piece.moves:
                return set([pinned_direction, negative_pinned_direction])

        return set([])

    def get_legal_moves(self, loc):
        """Returns all of the legal moves for a piece in a given location.

        loc -- The location of the piece to get the possible moves for.
        returns -- a set of all the valid moves from loc by the chess piece.

        This returns all of the legal moves a piece can make. It is a subset
        of the locations a piece can move to, retstricted by other game
        conditions (like is the king in check).
        """

        raise NotImplementedError()

        return None

    def get_moves(self, loc):
        """Returns all of the valid moves for piece in the given location.

        loc -- The location of the piece to get the possible moves for.
        returns -- a set of all the valid moves from loc by the chess piece.

        This does not take into account the game state (is the king in check).
        For that, call get_legal_moves instead.
        """
        
        piece = self.get_piece(loc)
        if piece is None:
            raise ValueError("Square at location {0} is empty".format(loc))

        if isinstance(piece, King):
            moves = self._get_knight_bishop_queen_rook_king_moves(piece, loc)
            enemy_colour = _inverse_colour(piece.colour)

            new_moves = []
            for m in moves:
                if len(self._get_attackers(m, enemy_colour)) > 0:
                    # Can't move king into check
                    pass
                else:
                    new_moves.append(m)
            moves = new_moves

            # Add any castling moves
            moves.extend(self._get_castle_moves(loc))
        else:
            # Check if this piece is pinned, and then pass the limited move vector to
            # the _get_*piece*_moves methods. They need to be restricted in what they
            # search. 
            pinned_directions = self._get_pinned_directions(loc)
            if isinstance(piece, Pawn):
                pawn_moves = self._get_pawn_moves(piece, pinned_directions)
                attacks = self._get_pawn_attacks(piece, pinned_directions)
                moves = pawn_moves | attacks
            elif isinstance(piece, Queen) or isinstance(piece, Rook) or isinstance(piece, Bishop) or isinstance(piece,  Knight):
                # A pinned piece can only move in the vector it is pinned in
                moves = self._get_knight_bishop_queen_rook_king_moves(piece, loc, pinned_directions)
            
        return moves

    def _get_knight_bishop_queen_rook_king_moves(self, piece, loc, pinned=set([])):
        """Returns all of the location any of these pieces can move to from the
        location specified.

        loc    -- The location of the chess piece
        piece  -- The piece to find the moves for. It doesn not have to be the
                  same piece that is actually found at loc.
        pinned -- A set of directions this piece is pinned (both  +/- vector)
        """
        squares = []
        locations = []

        if len(pinned) != 0:
            move_vectors = set.intersection(piece.moves, pinned)
        else:
            move_vectors = piece.moves

        for direction in move_vectors:
            squares += self._get_squares(loc, direction, piece.limit)

        for s in squares:
            if s.piece is None or s.piece.colour is not piece.colour:
                # Can move to empty locations or squares with opponents pieces
                locations.append(s.location)
        
        return locations

    def _get_pawn_attacks(self, pawn, pinned=set([])):
        """Returns all of the locations the pawn can attack.

        pawn   -- The pawn to return the location it can attack
        pinned -- A set of directions this piece is pinned (both  +/- vector)
        """
        left_attack = self._get_pawn_attack(pawn, pinned, True)
        right_attack = self._get_pawn_attack(pawn, pinned, False)
        return left_attack | right_attack

    # I don't like the similarity in naming with _get_pawn_attacks (differing only by an s)
    def _get_pawn_attack(self, pawn, pinned=set([]), left=True):
        """Returns the location a pawn can attack diagonnaly in one direction.

        pawn   -- The pawn to return the location it can attack
        left   -- If true check the left location, if false check right
        pinned -- A set of directions this piece is pinned (both  +/- vector)
        """
        attack = set([])
        [x, y] = pawn.location

        if left:
            attack_dir = pawn.attack_left
            en_passant_loc = (x - 1, y)
        else:
            attack_dir = pawn.attack_right
            en_passant_loc = (x + 1, y)

        # Check if the piece can attack normally
        if len(pinned) == 0 or attack_dir in pinned:
            enemy_squares = self._get_squares(pawn.location, attack_dir, 1)
            if not enemy_squares:
                # No squares to attack
                return set([])

            enemy_piece = enemy_squares[0].piece  
            enemy_location = enemy_squares[0].location
            if enemy_piece is not None and enemy_piece.colour is not pawn.colour:
                # We can capture this normally
                attack.add(enemy_squares[0].location)

            # Check if the pawn can attack via en passant
            # TODO: Draw out some chess boards in the comments to make this more
            # comprehensible to others reading the code. Will have to use unicode in
            # the source ... should be ok, it's 2013 now and ascii isn't the be all and end all
            if self._previous_move is not None and self._previous_move.is_double_move:
                if self._previous_move.to_ == en_passant_loc:
                    # We can attack this via en passant
                    # Don't need to check the following, implicity true
                    # if enemy_piece is not None and enemy_piece.colour is not pawn.colour:
                    # We can capture this normally

                    # We could be pinned by a rook or queen, but this is very rare
                    # Since two pieces are in the way, regular _get_pinned direction
                    # method will not work

                    king_rook_or_queen_loc = self._get_squares(enemy_location, (-1, 0))
                    king_rook_or_queen_loc_2 = self._get_squares(pawn.location, (1, 0))
                    if king_rook_or_queen_loc is not None and king_rook_or_queen_loc_2 is not None:
                        # There are some squares either side of pawns
                        piece_1 = self.get_piece(king_rook_or_queen_loc[0].location)
                        piece_2 = self.get_piece(king_rook_or_queen_loc_2[0].location)
                        if piece_1 is not None and piece_2 is not None:
                            # They're occupied
                            if piece_1.colour is pawn.colour and isinstance(piece_1, King):
                                # By our king
                                if piece_2 is not pawn.colour and (isinstance(piece_2, Queen) or isinstance(piece_2, Rook)):
                                    # And an enemy queen or rook, we're pinned, can't move
                                    return set([])
                            elif piece_2.colour is pawn.colour and isinstance(piece_2, King):
                                # By our king
                                if piece_1 is not pawn.colour and (isinstance(piece_1, Queen) or isinstance(piece_1, Rook)):
                                    # And an enemy queen or rook, we're pinned, can't move
                                    return set([])

                    # Not pinned, can attack via en passant
                    attack.add(enemy_squares[0].location)            

        return attack

    def _get_pawn_move_to(self, pawn, loc):
        [x, y] = loc
        single_move_loc = (x, y - pawn.forward)
        double_move_loc = (x, y - 2 * pawn.forward)
        if self._valid_location(single_move_loc):
            piece = self.get_piece(single_move_loc)
            if isinstance(piece, pawn.__class__):
                return set([single_move_loc])
            if self._valid_location(double_move_loc):
                piece = self.get_piece(double_move_loc)
                if isinstance(piece, pawn.__class__) and not piece.has_moved:
                    return set([double_move_loc])
        return set([])

    def _get_pawn_moves(self, pawn, pinned=set([])):
        """Returns all of the valid moves for a pawn excluding attacks."""
        moves = set([])

        if (1, 0) in pinned:
            # Pinned horizontally, therefore cannot move forward
            return moves
        
        # Check if the pawn is not pinned or only pinned vertically so can move forward    
        if len(pinned) == 0 or (0, 1) in pinned:
            # Pawns can move one space forward
            if self.get_piece(pawn.single_move()) is None:
                moves.add(pawn.single_move())
                if pawn.has_moved is False:
                    # On their first move, they can double move
                    if self.get_piece(pawn.double_move()) is None:                        
                        moves.add(pawn.double_move())
        return moves

    def _is_en_passant_attack(self, from_):
        """Returns True if an attack can be made from the location from_ via via en passant"""
        piece = self.get_piece(from_)
        # Only pawns can do en passant
        if isinstance(piece, Pawn): 
            # 1st move has no previous
            if self._previous_move is not None:  
                # En passant only possible when eneny pawn does double move
                if self._previous_move.is_double_move:  # Implies pawn
                    [x,y] = from_
                    [prev_x, prev_y] = self._previous_move.to_
                    if prev_y == y:  # Same row
                        if abs(prev_x - x) == 1 :  # Adjacent square
                            return True

        return False

    def _get_squares(self, from_, direction, limit=None, capture=True):
        """Returns an ordered list of squares on a chess board from from_ in
        the direction dir_ given. This does not include the starting square.

        Stops when any of the following are True: another piece is encountered
        or limit is reached, or the move is off the board.
        """
        squares = []

        [x, y] = from_
        [dx, dy] = direction
        i = 1
        while limit is None or i <= limit:
            loc = (x + i*dx, y + i*dy)
            i += 1
            try:
                piece = self.get_piece(loc) # Will raise a KeyError if we step off the board
                square = Square(loc, piece)
                if square.piece is None or capture is True:
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
        self._stalemate_count = 0
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
#        for x in xrange(1,9):
#            for y in xrange(3, 7):
#                self._all_pieces[(x,y)] = None
    
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

        board_repr =  u'{0},{1},{2},{3}'.format(board_string, self.current_player.code,self.turn, self._stalemate_count)
        return board_repr.encode('utf-8')

    def _create_board_from_repr(self, board_string):
        """Creates a new board from the board described by board_string."""
        unicode_board_string = board_string.decode('utf-8')
        [piece_string, player_colour_code, turn, _stalemate_count] = unicode_board_string.split(u',')
        
        self._previous_move = None

        self.current_player = Colour._get_colour(player_colour_code)
        self.turn = int(turn)
        self._stalemate_count = int(_stalemate_count)
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
                    # This is meta data, it isn't a piece, so don't increment x
                    has_moved = True
                else:
                    x += 1
                    loc = (x, y)
                    if symbol == _EMPTY_SQUARE:
                        pass
                    else:
                        cls = Piece.get_piece_class(symbol)

                        if issubclass(cls, Pawn):
                            self._all_pieces[loc] = cls(loc)
                        elif issubclass(cls, King):
                            if cls.colour in self._king_location:
                                # Cannot handle multiple kings of the the same colour, just saying
                                # We already have a king of this colour ... not good
                                raise InvalidBoardException()

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
        """Prints out a unicode representation of the chess board."""
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
    value = None  # Tradional chess values - used to determince some statemate

    def __str__(self):
        """Return a utf-8 encoded string representation of this chess piece."""
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        """Return the unicode string representation of this chess piece."""
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

    moves = set([(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)])  # x,y
    limit = 1  # The King may only move one place via his move vectors
    has_moved = False
    value = 0


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

    moves = set([(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)])  # x,y
    value = 9


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

    moves = set([(1, 0), (0, 1), (-1, 0), (0, -1)]) 
    has_moved = False
    value = 5


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

    moves = set([(1, 1), (-1, 1), (-1, -1), (1, -1)])  # x,y              
    value = 3

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
    moves = set([(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)])  # x, y
    limit = 1  # Knights only move one place via their move vectors       
    value = 3

        
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
    limit = 1  # Pawns can only attack/move 1 space (double move is treated special)
    left = (-1, 0)
    right = (1, 0)
    has_moved = False

    def __new__(cls, *args, **kwargs):
        if cls is Pawn:
            raise TypeError("Pawn class may not be instantiated.")
        return object.__new__(cls, *args, **kwargs)

    # HACK! Pawns use methods for their moves / attacks currently
    # This was placed here so we can treat them like all other pieses
    # when checking if a piece is pinned. Note - pawns can't pin a piece
    moves = set([])

    def single_move(self):
        """Returns the location of the square infront of this piece.
        """
        return (self.location[0], self.location[1] + self.forward)

    def double_move(self):
        """Returns the location two squares infront of this piece. 
        Can be the first move of this piece.
        """
        return (self.location[0], self.location[1] + 2 * self.forward)
    value = 1

class WhitePawn(Pawn, Piece):
    """A White Pawn chess piece."""
    symbol = u'\u2659'
    colour = White
    forward = 1  # Based off White starting at rows 1,2
    attack_left = (-1, 1)
    attack_right = (1, 1)

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


class BlackPawn(Pawn, Piece):
    """A Black Pawn chess piece."""
    symbol = u'\u265f'
    colour = Black
    forward = -1 # Based off Black starting at rows 7,8
    attack_left = (-1, -1)
    attack_right =(1, -1)

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

        