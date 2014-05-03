from color import Color
from move import Move
from square import Square, InvalidSquareException
from pieces import PieceFactory, King, BlackKing, WhiteKing, Queen, WhiteQueen, BlackQueen, Rook, WhiteRook, \
    BlackRook, Bishop, WhiteBishop, BlackBishop, Knight, WhiteKnight, BlackKnight, Pawn, WhitePawn, BlackPawn, \
    InvlaidPieceException
_HAS_MOVED = 'm'
_EMPTY_SQUARE = '_'


class IllegalMoveException(Exception):
    u"""Raised when an attempt is made to move a piece illegally.

    Examples of illegal moves include moving a piece to a square it cannot
    move to, moving the King into check or moving a piece so as to leave the
    king in check.
    """
    pass


class InvalidBoardException(Exception):
    u"""Returned if a chess board cannot represent a legal game board."""
    pass


class MovesAndAttacks(object):
    u"""Represents all of the moves and attacks a given piece can make"""
    moves = set([])
    attacks = set([])

    def __init__(self, moves, attacks):
        # Using union to force
        moves.union(moves)
        attacks.union(attacks)


class Board(object):
    u"""A new implemenation of a chessboard."""
    def __init__(self, board_string=None):
        self._stalemate_count = 0
        self._king_location = {}
        self._all_squares = {}
        self._previous_moves = []
        self.current_player = None
        self.promote_pawn_location = None
        if board_string is None:
            self._new_board()
        else:
            self._create_board_from_repr(board_string)

    def square(self, square_name=None, x=None, y=None):
        u"""Returns the square on a chess board.

        square_name -- The name of the chess square
        x -- The x-coordinate of the chess square, 1-indexed, left to right
        y -- The y-coordinate of the chess square, 1-indexed, white pieces start on 1 and 2, black on 7 and 8

        The square can be by specifying EITHER the name of the square OR the x, y coordinates.
        If both are specified then this method raises an exception.

        """

        key = Square(square_name=square_name, x=x, y=y).name
        square = self._all_squares.get(key, None)

        return square

    # TODO: replace with calls to square.piece ???
    def get_piece(self, from_):
        u"""Returns the piece at the location specified or None if the square is empty.

        from_ -- the name of the square, e.g A3, or H7
        """
        return self.square(from_).piece

    def is_check(self):
        u"""Returns True if the King of the active player color is in check."""
        color = self.current_player
        square_name = self._king_location[color]

        enemy_color = Color.inverse(color)
        if len(self._get_attackers(square_name, enemy_color)) > 0:
            return True
        return False

    def is_checkmate(self, color):
        u"""Returns True if the King of the color specified is in checkmate."""

        # color = self.current_player
        king_loc = self._king_location[color]
        blocking_square_names, enemy_square_name = self._get_blocking_squares()
        if blocking_square_names is None:
            # Not under attack
            return False
        if len(self.get_moves(king_loc)) > 0:
                # Can move king to safety
                return False
        else:
            if blocking_square_names is set([]):
                # Cannot block, cannot move king, checkmate
                return True
            else:
                # Check if we can capture attacker
                our_attacker_square_names = self._get_attackers(enemy_square_name, color)
                for name in our_attacker_square_names:  # If we have any...
                    square = self.square(name)
                    if isinstance(square.piece, King):
                        # If it's the king then since we know we can't
                        # legally move, ignore
                        continue
                    elif self._pinned(name) is None:
                        # Can capture the piece putting the king incheck
                        return False
                    else:
                        # Can't be pinned by piece causing check
                        # Therefore moving this piece is of no value
                        continue

                # Check if we can block
                for square in blocking_square_names:
                    # Find all of our pieces that can move into one of these squares
                    blocking_piece_locs = self._get_attackers(square, color, True)
                    for blocker_loc in blocking_piece_locs:
                        # We can't use the king to block itself
                        if king_loc != blocker_loc:
                            # Can block, not checkmate
                            return False

                # Can't move, and can't capture, checkmate

                return True

    def is_stalemate(self):
        u"""Check to see if the game is a stalemate."""
        # Check that at least one player has a pawn or more than 3 points
        color = self.current_player

        has_pawn = False
        white_score = 0
        black_score = 0
        for square_name in self._all_squares:
            piece = self._all_squares[square_name].piece
            if piece is None:
                continue
            if isinstance(piece, Pawn):
                has_pawn = True
            if piece.color == Color.white:
                white_score += piece.value
            elif piece.color == Color.black:
                black_score += piece.value
            else:
                raise ValueError()

        if black_score <= 3 and white_score <= 3 and not has_pawn:
            # Neither player can checkmate
            return True

        # Check whether the 'color' player can move any of their pieces
        for square_name in self._all_squares:
            piece = self._all_squares[square_name].piece
            if piece is None:
                continue
            if piece.color == color:
                if len(self.get_moves(square_name)) != 0:
                    # This player can move
                    return False
        else:
            # This player cannot move -> stalemate
            return True

    @property
    def turns_taken(self):
        u"""Returns the number of turns taken. Counts once for each players move."""
        return len(self._previous_moves)

    @property
    def winner(self):
        u"""Returns the color of the winning player, draw if the game is a stalemate or None if no-one has won yet."""
        if self.is_checkmate(Color.black):
            return Color.white
        elif self.is_checkmate(Color.white):
            return Color.black
        elif self.is_stalemate():
            return u"Draw"  # TODO: Do we need another state?
        else:
            return None

    @property
    def previous_move(self):
        u"""Returns the previous move made or None if no moves have been made."""
        if len(self._previous_moves) > 0:
            return self._previous_moves[-1]
        else:
            return None

    @previous_move.setter
    def previous_move(self, value):
        u"""Sets the previous move, appending it to all other moves."""
        self._previous_moves.append(value)

    def _get_castle_moves(self, from_):
        u"""Returns the locations the king located at from_square can castle to.

            from_ -- The location of the king
        """
        assert(len(from_) == 2)
        king_square = self.square(from_)
        king = king_square.piece

        left_rook = self.square(x=1, y=king_square.y).piece
        right_rook = self.square(x=8, y=king_square.y).piece

        moves = set([])
        if king is None or king.has_moved is True:
            return moves

        enemy_color = Color.inverse(king.color)

        # Castling left?
        if left_rook is not None and left_rook.has_moved is False:
            left_square_4 = self.square(x=4, y=king_square.y)
            left_square_3 = self.square(x=3, y=king_square.y)
            left_square_2 = self.square(x=2, y=king_square.y)
            # Empty squares
            if left_square_4.piece is None:
                if left_square_3.piece is None:
                    if left_square_2.piece is None:
                        # With no attackers?
                        if self._get_attackers(left_square_2.name, enemy_color) == set([]):
                            if self._get_attackers(left_square_3.name, enemy_color) == set([]):
                                if self._get_attackers(left_square_4.name, enemy_color) == set([]):
                                    moves.add(left_square_3.name)

        # Castling right?
        if right_rook is not None and right_rook.has_moved is False:
            right_square_6 = self.square(x=6, y=king_square.y)
            right_square_7 = self.square(x=7, y=king_square.y)
            # Empty squares
            if right_square_6.piece is None:
                if right_square_7.piece is None:
                    # With no attackers?
                    if self._get_attackers(right_square_6.name, enemy_color) == set([]):
                        if self._get_attackers(right_square_7.name, enemy_color) == set([]):
                            moves.add(right_square_7.name)

        return moves

    def _is_castle_right(self, from_, to_):
        u"""Returns True if the move is to castle right.

        Castling is preformed by first moving the king two squares in the
        direction to castle. The castling rook is then moved to the other
        side of the king. This method returns True if the King has been
        moved two squares to the right, or False otherwise.
        """
        king_square = self.square(from_)
        to_square = self.square(to_)

        if isinstance(king_square.piece, King):
            if king_square.piece.has_moved is False:
                if to_square.x - king_square.x == 2:
                    if king_square.y == to_square.y:
                        return True
        return False

    def _is_castle_left(self, from_, to_):
        u"""Returns True if the move is to castle left.

        Castling is preformed by first moving the king two squares in the
        direction to castle. The castling rook is then moved to the other
        side of the king. This method returns True if the King has been
        moved two squares to the right, or False otherwise.
        """
        king_square = self.square(from_)
        to_square = self.square(to_)

        if isinstance(king_square.piece, King):
            if king_square.piece.has_moved is False:
                if to_square.x - king_square.x == -2:
                    if king_square.y == to_square.y:
                        return True
        return False

    def move_piece(self, from_, to_):
        u"""Move a piece from the location from_name to the location to_.

        from_ -- A case sensitive string representing the square to move the piece from, eg B7
        to_   -- A case sensitive string representing the square to move the piece to, eg A5

        Raises -- A IllegalMoveException if the move is not a legal chess move.
        """

        if self.promote_pawn_location is not None:
            raise IllegalMoveException(u"Cannot move piece, previously moved pawn must be promoted first.")

        legal_moves = self.get_moves(from_)
        piece = self.square(from_).piece

        if self.current_player != piece.color:
            raise IllegalMoveException(u"Cannot move piece, it is not {color} player's turn.".format(piece.color))

        # Check to see if anyone has won, if they ha
        if self.winner is not None:
            raise IllegalMoveException(u"Cannot move piece, the game already has a winner {winner}".format(
                winner=self.winner))

        if to_.upper() in legal_moves:  # to_square.name is uppercase while to_name could be any case
            is_castle = False

            if self._is_en_passant_attack(from_):
                # Remove the pawn that moved previously as it has been captured via en passant
                self.square(self.previous_move.to_).piece = None
            elif self._is_castle_left(from_, to_):
                # Move the rook too
                from_square = self.square(from_)
                rook = self.square(x=1, y=from_square.y).pop()
                self.square(x=4, y=from_square.y).piece = rook
                is_castle = True
            elif self._is_castle_right(from_, to_):
                # Move the rook too
                from_square = self.square(from_)
                rook = self.square(x=8, y=from_square.y).pop()
                self.square(x=6, y=from_square.y).piece = rook
                is_castle = True

            # Keep track of where the king is
            if isinstance(piece, King):
                self._king_location[piece.color] = to_

            is_double_move = False  # Marks if a pawn is vulnerable to en passant
            if isinstance(piece, Pawn):
                if abs(self.square(from_).y - self.square(to_).y) == 2:  # The pawn moved two squares
                    is_double_move = True
                # Keep track of 50 move stalemate
                self._stalemate_count = 0

                # If pawn moves into end zone, it needs to be promoted
                if self.square(to_).y == 1 or self.square(to_).y == 8:
                    self.promote_pawn_location = to_

            if self.square(to_).piece is None:
                is_capture = False  # Moved into an empty square, append regular move
                self._stalemate_count += 1
            else:
                is_capture = True  # Captured an enemy piece, mark as a capture
                self._stalemate_count = 0

            # Finally move the piece
            self.square(to_).piece = self.square(from_).pop()
            self.square(to_).piece.has_moved = True

            # TODO: Could fold the logic into this, as from
            self.previous_move = Move(piece, from_, to_, is_double_move, is_capture, is_castle)

            # Do not change player if the current player still needs to promote their pawn
            if self.promote_pawn_location is None:
                self.current_player = Color.inverse(self.current_player)

            # These data structures must be kept in sync
            assert isinstance(self.square(self._king_location[Color.black]).piece, BlackKing)
            assert isinstance(self.square(self._king_location[Color.white]).piece, WhiteKing)

            return
        # Fall through error
        raise IllegalMoveException(u"Move of '{0}' from {1} to {2} is not legal.".format(piece, from_, to_))

    def is_fifty_move_stalemate(self):
        u"""Returns True if 50 consective moves have been taken by either
        player where no pawn has been advanced and no piece captured.

        The fifty move chess rule means a player *may choose* to call a game a
        draw at the start of their turn:
        http://en.wikipedia.org/wiki/Fifty-move_rule
        """
        # _stalemate_count gets incremented each time a player moves if they do not
        # capture a peice or advance a pawn. If a pawn is advanced or a piece is
        # captured then the counter is reset to 0. If _stalemate_count is greater
        # than 100 (50 per place), at the start of any turn a player (may) declare
        # a stalemate.
        if self.stalemate_count < 100:  # 50 moves each
            return False
        else:
            return True

    def promote_pawn(self, piece):
        u"""Promotes a pawn that has been moved to the last row. Should be called after move_piece.

            piece -- The peice to promote the pawn to. One of Queen, Rook, Bishop, Knight or their colored subclass.
                     The color of the promoted piece is the same as the color of the pawn.
        """
        if self.promote_pawn_location is None:
            raise IllegalMoveException("Cannot promote pawn, no pawn has been moved into end row")
        square = self.square(self.promote_pawn_location)
        pawn = square.piece
        assert(isinstance(pawn, Pawn))    # Must be a pawn
        assert(square.y == 8 or square.y == 1)  # Must be in the final row
        if (piece.color is not pawn.color):
            raise InvlaidPieceException("Cannot promote {pawn_color} pawn to {color} {piece}, it is the wrong color"
                                        .format(pawn_color=pawn.color, color=piece.color, piece=piece))

        if isinstance(piece, (Queen, Rook, Bishop, Knight)):
            square.piece = piece
            self.promote_pawn_location = None  # Clear the promotion
            self.current_player = Color.inverse(self.current_player)  # Change turn to next player
        else:
            raise TypeError("Cannot promote pawn to {piece}.".format(piece=piece))

    def promotable_pieces(self):
        u""""Returns a list of pieces that a pawn can be promoted to.

        returns -- a frozen set containing a Queen, Rook, Bishop and Knight with the same color as the
                   pawn in self.promote_pawn_location. If there is not pawn there, then returns an empty frozenset

        """
        if self.promote_pawn_location is not None:
            pawn = self.promote_pawn_location.piece
            if pawn.color is Color.white:
                return frozenset([WhiteQueen(True), WhiteRook(True), WhiteBishop(True), WhiteKnight(True)])
            elif pawn.color is Color.black:
                return frozenset([BlackQueen(True), BlackRook(True), BlackBishop(True), BlackKnight(True)])
            else:
                raise InvalidBoardException("Pawn to be promoted has no color.")
        else:
            # No pawns to be promoted
            return frozenset([])

    def _get_attackers(self, to_, color, blocker=False):
        u"""Returns the locations of the pieces of the color specified that can attack the given location.

        to_     -- A string representing a chess square, e.g 'E5'
        color   -- The color of the attacking or blocking piece.
        blocker -- If true, returns the locations of pawns that can move to to_ instead of attack it
        returns -- A set of strings representing each of the squares an attacker (or blocker) is located in
        """

        # At the given square (to_) we imagine where we could attack with each
        # of our pieces. If we use a knight as example, if any of the squares it
        # can attack contain an enemy knight then that enemy knight is an attacker.
        # If those squares contain any other piece then they are not. Likewise if
        # we imagine a bishop at the location, any bishops or queen it can attack
        # can also attack it. This is repeated for rooks, pawns, king and queen
        # The piece in the squares that potentially attacks this one are checked
        # for enemy pieces that can attack.
        assert(len(to_) == 2)
        attackers = set([])

        if color is Color.black:
            knight = WhiteKnight()
            rook = WhiteRook()
            bishop = WhiteBishop()
            pawn = WhitePawn(to_)
            pawn_2 = BlackPawn(to_)
        elif color is Color.white:
            knight = BlackKnight()
            rook = BlackRook()
            bishop = BlackBishop()
            pawn = BlackPawn(to_)
            pawn_2 = WhitePawn(to_)

        # Get the squares of any knights that can attack this square
        dummy_moves, knight_square_names = self._get_knight_bishop_queen_rook_king_moves(knight, to_)
        for name in knight_square_names:
            square = self.square(name)
            if isinstance(square.piece, Knight):
                # Opponents knight - an attacker
                attackers.add(name)

        dummy_moves, rooks_or_queen_square_names = self._get_knight_bishop_queen_rook_king_moves(rook, to_)
        for name in rooks_or_queen_square_names:
            square = self.square(name)
            if isinstance(square.piece, Rook) or isinstance(square.piece, Queen):
                attackers.add(name)
            elif isinstance(square.piece, King):
                # King can only attack adjacent squares
                if square.isAdjacent(to_):
                    attackers.add(name)

        dummy_moves, bishop_or_queen_square_names = self._get_knight_bishop_queen_rook_king_moves(bishop, to_)
        for name in bishop_or_queen_square_names:
            square = self.square(name)
            if isinstance(square.piece, Bishop) or isinstance(square.piece, Queen):
                attackers.add(name)
            elif isinstance(square.piece, King):
                # King can only attack adjacent squares
                if square.isAdjacent(to_):
                    attackers.add(name)

        if blocker:
            pawn_square_names = self._get_pawn_move_to(pawn_2, to_)
        else:
            pawn_square_names = self._get_pawn_attacks(pawn, to_)
        for name in pawn_square_names:
            square = self.square(name)
            if isinstance(square.piece, Pawn):
                attackers.add(name)

        return attackers

    def _pinned(self, from_):
        u"""Returns the location containing the piece that is pinning this one or None if not pinned.

        from_  -- The square name to check if the piece inside is pinned,
        """

        color = self.square(from_).piece.color
        king_square_name = self._king_location[color]

        king_square = self.square(self._king_location[color])
        pinned_direction = king_square.direction(from_)

        if pinned_direction is None:
            return None  # Not in line with king, can't be pinned

        # Get a list of squares, starting near the king and in a line away from him
        square_names = self._squares_in_direction(king_square_name, pinned_direction)

        maybe_pinned = False
        for n in square_names:
            s = self.square(n)
            if s.piece is None:
                continue  # blank square, keep looking
            else:
                if s.name == from_:
                    maybe_pinned = True
                elif maybe_pinned:
                    # Is the piece found an attacker..?
                    if pinned_direction in s.piece.attacks and s.piece.limit != 1:
                        return s.name
                    else:
                        return None
                else:
                    return None  # Found another piece betwen us and the king, therefore not pinned

    def _get_pinned_direction(self, from_):
        u"""Returns the directions a pinned is able to move or None if not pinned

            from_ -- The location of the piece to check for.
        """
        pinning_loc = self._pinned(from_)
        if pinning_loc is None:
            return None
        else:
            pinning_square = self.square(pinning_loc)
            dir_1 = pinning_square.direction(from_)
            dir_2 = (-dir_1[0], -dir_1[1])
            return set([dir_1, dir_2])

    def get_moves(self, from_):
        u"""Returns a list of all the squares the piece in the given location can attack or move to.

            from_ -- A string like 'A4' which represents the square with the piece to find the moves for
        """
        moves, attacks = self._get_moves_and_attacks(from_)
        square_names = moves.union(attacks)

        return square_names

    def _get_moves_and_attacks(self, from_):
        """Returns all of the valid moves for piece in the given location.

        from_ -- The location of the piece to get the possible moves for.
        returns -- a set of all the valid moves from loc by the chess piece.

        This returns all of the legal moves a piece can make. It is a subset
        of the locations a piece can move to, retstricted by other game conditions (like is the king in check).
        """

        assert (len(from_) == 2)
        piece = self.square(from_).piece

        if piece is None:
            # raise ValueError("Square at location {0} is empty".format(from_))
            return set([]), set([])

        if isinstance(piece, King):
            return self._get_king_moves_and_attacks(from_)
        else:
            # Check if this piece is pinned, and then pass the limited move vector to
            # the _get_*piece*_moves methods. They need to be restricted in what they
            # search.
            pinned_directions = self._get_pinned_direction(from_)
            if isinstance(piece, Pawn):
                moves = self._get_pawn_moves(piece, from_, pinned_directions)
                attacks = self._get_pawn_attacks(piece, from_, pinned_directions)

            elif isinstance(piece, Queen) or isinstance(piece, Rook) or \
                    isinstance(piece, Bishop) or isinstance(piece, Knight):
                # A pinned piece can only move in the vector it is pinned in
                moves, attacks = self._get_knight_bishop_queen_rook_king_moves(piece, from_, pinned_directions)

        if self.is_check():
            # King in check, can only move piece if it captures the attacker or blocks it
            blocking_squares, enemy_square = self._get_blocking_squares()
            moves = moves.intersection(blocking_squares)
            attacks = attacks.intersection(set([enemy_square]))

        return moves, attacks

    def _get_king_moves_and_attacks(self, from_):
        u"""Returns all of the moves that a king can make.

        The moves a king can make are highly restricted by the other pieces on the board.
        This method restricts the moves to those that do not put the king in check.

        king_square -- The square the king is in
        """

        king_square = self.square(from_)
        king = king_square.piece
        # Get all moves, these may be illegal, putting king in check
        moves, attacks = self._get_knight_bishop_queen_rook_king_moves(king, from_)
        # Add any castling moves, these are all legal
        moves = moves.union(self._get_castle_moves(from_))

        enemy_color = Color.inverse(king.color)
        threatened = set([])
        if self.is_check():
            # The king is likely blocking the square(s) behind it from the attacker(s)
            # We must count the square(s) as unsafe, because if the king moves there
            # he will still be in check

            enemy_square_names = self._get_attackers(from_, enemy_color)
            for name in enemy_square_names:
                square = self.square(name)
                x, y = square.direction(from_)
                if square.piece.limit != 1:
                    try:
                        behind = self.square(x=king_square.x + x, y=king_square.y + y).name
                        threatened.add(behind)
                    except InvalidSquareException:
                        continue

        safe_moves = set([])
        safe_attacks = set([])

        for m in moves:

            if len(self._get_attackers(m, enemy_color)) > 0:
                pass                 # Can't move king into check
            elif m in threatened:
                # If we're already in check, the king is blocking  a square from the attacker
                # If the king moves there, he will still be under attack.
                pass  # Can't move king into check
            else:

                safe_moves.add(m)
        for a in attacks:
            if len(self._get_attackers(a, enemy_color)) > 0:
                pass  # Can't move king into check
            elif a in threatened:
                pass  # Can't move king into check
            else:
                safe_attacks.add(a)
        return safe_moves, safe_attacks

    def _get_blocking_squares(self):
        u"""Returns two sets, one of the locations that a piece can move to, to block check, the other the location of
        the attacking piece.

        If there are multiple attackers, returns an empty set
        If the king is not in check returns None
        """
        color = self.current_player
        king_square_name = self._king_location[color]
        king_square = self.square(king_square_name)
        enemy_color = Color.inverse(color)
        enemy_attacking_pieces = self._get_attackers(king_square_name, enemy_color)

        if len(enemy_attacking_pieces) == 0:
            # Not under attack
            return None, None
        elif len(enemy_attacking_pieces) == 1:
                # It is possible to capture the attacker
                [enemy_loc] = enemy_attacking_pieces

                # Can we block the attacking piece?
                attack_vector = king_square.direction(enemy_loc)

                # Find all of the squares that block the path between the enemy piece and king
                return self._get_squares_in_direction(king_square_name, attack_vector, color)

        else:
            # We cannot block / capture multiple pieces in one move
            # It makes more sense to return an empty set, rather than all locations that
            # Must be captured or blocked
            return set([]), set([])

    def _get_knight_bishop_queen_rook_king_moves(self, piece, from_, pinned=None):
        """Returns all of the location any of these pieces can move to from the location specified.
           This does not restrict the king from moving into squares that are threatened.
           Call the higher level method _get_moves_and_attacks instead.


        from_     -- The location of the chess piece to move, e.g 'D7'
        piece   -- The piece to find the moves for. It doesn not have to be the
                   same piece that is actually found at loc. This allows us to 'imagine' where you could move
                   from if that piece was there.
        pinned  -- A set of directions this piece is pinned (both  +/- vector)

        returns -- A two lists of x-y coords tuples representation the moves and attacks of the specified piece from
                   the location provided. [(x1,y1),(x2,y2),....(xm,ym)],[(xm+1,ym+1),....(xn,yn)]
        """
        all_attacks = set([])
        all_moves = set([])

        if pinned is None:
            move_vectors = piece.attacks
        else:
            # A piece cannot be pinned in more than one direction
            # If the piece is pinned vertically (or any other direction), it can still move in that direction
            move_vectors = pinned.intersection(piece.attacks)

        for direction in move_vectors:
            moves, attack = self._get_squares_in_direction(from_, direction, piece.color, piece.limit)
            if attack is not None:
                all_attacks.add(attack)
            all_moves = all_moves.union(moves)

        return all_moves, all_attacks

    def _get_pawn_attacks(self, pawn, from_, pinned=None):
        u"""Returns the location a pawn can attack diagonnaly in one direction.

        pawn   -- The pawn to return the location it can attack
        from_  -- The location of the pawn
        pinned -- A set of directions this piece is pinned (both  +/- vector)
        """
        attacks = set([])

        for attack_dir in pawn.attacks:
            # Check if the piece can attack normally
            if pinned is None or attack_dir in pinned:
                dummy_locs, enemy_loc = self._get_squares_in_direction(from_, attack_dir, pawn.color, 1)

                if enemy_loc is not None:
                    # We can capture this normally
                    attacks.add(enemy_loc)

        for en_passant_dir in pawn.en_passant():

            # en_passant_dir = pawn.en_passant_2(attack_dir)
            # Check if the pawn can attack via en passant
            # TODO: Draw out some chess boards in the comments to make this more
            # comprehensible to others reading the code. Will have to use unicode in
            # the source ... should be ok, it's 2013 now and ascii isn't the be all and end all
            dummy_locs, en_passant_loc = self._get_squares_in_direction(from_, en_passant_dir, pawn.color, 1)
            if en_passant_loc is not None:

                previous_move = self.previous_move
                if self.previous_move is not None:
                    if previous_move.is_double_move and previous_move.to_ == en_passant_loc:

                        # We can attack this via en passant
                        # Don't need to check the following, implicity true
                        # if enemy_piece is not None and enemy_piece.color is not pawn.color:
                        # We can capture this normally

                        # We could be pinned by a rook or queen, but this is very rare
                        # Since two pieces are in the way, regular _get_pinned direction
                        # method will not work
                        en_passant_square = self.square(en_passant_loc)
                        from_square = self.square(from_)
                        left_x = min(en_passant_square.x, from_square.x)  # The left square
                        right_x = max(en_passant_square.x, from_square.x)

                        # Search left and right halves to see if we're in a position where capturing
                        # via en passent would put us in check
                        king = None
                        attacker = None
                        for xi in reversed(range(1, left_x)):
                            piece = self.square(x=xi, y=from_square.y).piece
                            if piece is not None:
                                if isinstance(piece, King) and piece.color == pawn.color:
                                    king = piece
                                elif piece.color != pawn.color and (isinstance(piece, Queen) or isinstance(piece, Rook)):
                                    attacker = piece
                                break

                        if attacker is not None or king is not None:
                            for xi in range(right_x + 1, 9):
                                piece = self.square(x=xi, y=from_square.y).piece
                                if piece is not None:
                                    if isinstance(piece, King) and piece.color == pawn.color:
                                        king = piece
                                    elif piece.color != pawn.color and (isinstance(piece, Queen) or isinstance(piece, Rook)):
                                        attacker = piece
                                    break

                        if attacker is not None and king is not None:
                            # We're pinned
                            return []

                        pawn_move_location = self.square(x=en_passant_square.x, y=from_square.y + pawn.forward)
                        attacks.add(pawn_move_location.name)

        return attacks

    def _get_pawn_move_to(self, pawn, to_):
        """Returns the location of any pawns that can move to the location specified.

        This is restricted to pawns with the same color as the pawn supplied.

        """
        assert(len(to_) == 2)
        try:
            to_square = self.square(to_)
            x = to_square.x
            y = to_square.y - pawn.forward
            single_move_square = self.square(x=x, y=y)
            if isinstance(single_move_square.piece, Pawn):
                return set([single_move_square.name])

            x = to_square.x
            y = to_square.y - 2 * pawn.forward
            double_move_square = self.square(x=x, y=y)
            if isinstance(double_move_square.piece, Pawn) and self._pawn_has_not_moved(double_move_square.name):
                return set([double_move_square.name])

        except InvalidSquareException:
            pass  # IllegalSquare, fall through
        return set([])

    def _get_pawn_moves(self, pawn, from_, pinned=None):
        u"""Returns all of the moves that a pawn can make from the given from_ location

        This does not include moves where the pawn captures an enemy piece but does check
        whether the pawn is pinned or not."""
        moves = set([])

        # Check if the pawn is not pinned or only pinned vertically so can move forward
        if pinned is None or (0, 1) in pinned:
            try:
                from_square = self.square(from_)
                single_move_loc = self.square(x=from_square.x, y=from_square.y + pawn.forward)
            except InvalidSquareException:
                raise IllegalMoveException("Pawn cannot move, it must be promoted instead.")

            if single_move_loc.piece is None:
                moves.add(single_move_loc.name)
                if self._pawn_has_not_moved(from_):
                    double_move_loc = self.square(x=from_square.x, y=from_square.y + 2 * pawn.forward)
                    if double_move_loc.piece is None:
                        moves.add(double_move_loc.name)
            return moves
        elif (1, 0) in pinned:
            # Pinned horizontally, therefore cannot move or attack
            return moves
        else:
            # Pinned diagonally
            pass
        return moves

    def _pawn_has_not_moved(self, from_):
        u"""Returns True if the pawn has moved, and False otherwise."""
        # Normally negation is avoided in method names, but this one exception seems warranted
        # as 'has not moved' is an atribute.
        square = self.square(from_)
        assert(isinstance(square.piece, Pawn))
        if square.piece.color == Color.black and square.y == 7:
            return True
        elif square.piece.color == Color.white and square.y == 2:
            return True
        else:
            return False

    def _is_en_passant_attack(self, from_):
        u"""Returns True if an attack can be made from the location from_ via via en passant"""

        from_square = self.square(from_)
        if isinstance(from_square.piece, Pawn):  # Only pawns can do en passant
            # 1st move has no previous
            previous_move = self.previous_move
            if previous_move is not None:
                # En passant only possible when eneny pawn does double move
                if previous_move.is_double_move:  # Implies pawn
                    if self.square(previous_move.to_).y == from_square.y:  # Same row
                        if abs(self.square(previous_move.to_).x - from_square.x) == 1:  # Adjacent square
                            return True

        return False

    def _squares_in_direction(self, from_, direction):
        u"""Returns all of the squares in the direction (x, y) tuple given, from this Square to the board edge.

        The direction is a (x, y) tuple representing a compass direction like north, east, south-west, etc.
        North is (0, 1), Northeast is (1, 1), Southwest is (-1, -1), etc

        from_     --
        direction --

        """
        dx, dy = direction
        assert(dx == 0 or abs(dx) == 1)
        assert(dy == 0 or abs(dy) == 1)

        from_square = self.square(from_)

        squares = []
        i = 1
        while True:
            try:
                x = from_square.x + i * dx
                y = from_square.y + i * dy
                loc = self.square(x=x, y=y)
                squares.append(loc.name)
                i += 1

            except InvalidSquareException:
                break  # Hit the edge of the baord
        return squares

    def _get_squares_in_direction(self, from_, direction, color, limit=None, all_squares=False):
        u"""Returns a list of moves, and attacks that can be made from the given square in a specific direction

        from_     -- The location to search from, e.g A2
        direction -- The direction to search in
        color     -- The color of this piece (we attack one enemy piece of the opposite color)
        limit     -- The maxium number of total squares to search/return
        ignore_blockers -- If this is true, returns all squares

        returns   -- An ordered list of square_names that are empty,
                     and 0-1 square_name that contains the first enemy piece encountered
        """
        # TODO: We're repeating logic, but the logic here is too specific

        from_square = self.square(from_)

        moves = set([])
        attack = None

        dx, dy = direction
        i = 1
        while limit is None or i <= limit:
            try:
                x = from_square.x + i * dx
                y = from_square.y + i * dy
                loc = self.square(x=x, y=y)
                i += 1
                if loc.piece is None or all_squares is True:
                    moves.add(loc.name)  # Empty square or we're after all squares
                elif loc.piece.color != color:
                    attack = loc.name  # We've found an enemy piece
                    break
                else:
                    # We've found one of our own pieces
                    break
            except InvalidSquareException:
                break
        return moves, attack

    def _new_board(self):
        u"""Places all of the pieces on the chessboard in their starting positions and assign
            white player first turn.
        """
        self._previous_moves = []
        self.turn = 0
        self._stalemate_count = 0
        self.current_player = Color.white
        self._king_location = dict()

        # Place all the White pieces on the board
        self._all_squares['A1'] = Square('A1', piece=WhiteRook())
        self._all_squares['B1'] = Square('B1', piece=WhiteKnight())
        self._all_squares['C1'] = Square('C1', piece=WhiteBishop())
        self._all_squares['D1'] = Square('D1', piece=WhiteQueen())
        self._all_squares['E1'] = Square('E1', piece=WhiteKing())
        self._all_squares['F1'] = Square('F1', piece=WhiteBishop())
        self._all_squares['G1'] = Square('G1', piece=WhiteKnight())
        self._all_squares['H1'] = Square('H1', piece=WhiteRook())
        self._all_squares['A2'] = Square('A2', piece=WhitePawn())
        self._all_squares['B2'] = Square('B2', piece=WhitePawn())
        self._all_squares['C2'] = Square('C2', piece=WhitePawn())
        self._all_squares['D2'] = Square('D2', piece=WhitePawn())
        self._all_squares['E2'] = Square('E2', piece=WhitePawn())
        self._all_squares['F2'] = Square('F2', piece=WhitePawn())
        self._all_squares['G2'] = Square('G2', piece=WhitePawn())
        self._all_squares['H2'] = Square('H2', piece=WhitePawn())

        # Place all the Black pieces on the board
        self._all_squares['A8'] = Square('A8', piece=BlackRook())
        self._all_squares['B8'] = Square('B8', piece=BlackKnight())
        self._all_squares['C8'] = Square('C8', piece=BlackBishop())
        self._all_squares['D8'] = Square('D8', piece=BlackQueen())
        self._all_squares['E8'] = Square('E8', piece=BlackKing())
        self._all_squares['F8'] = Square('F8', piece=BlackBishop())
        self._all_squares['G8'] = Square('G8', piece=BlackKnight())
        self._all_squares['H8'] = Square('H8', piece=BlackRook())
        self._all_squares['A7'] = Square('A7', piece=BlackPawn())
        self._all_squares['B7'] = Square('B7', piece=BlackPawn())
        self._all_squares['C7'] = Square('C7', piece=BlackPawn())
        self._all_squares['D7'] = Square('D7', piece=BlackPawn())
        self._all_squares['E7'] = Square('E7', piece=BlackPawn())
        self._all_squares['F7'] = Square('F7', piece=BlackPawn())
        self._all_squares['G7'] = Square('G7', piece=BlackPawn())
        self._all_squares['H7'] = Square('H7', piece=BlackPawn())

        # Initiliaze all of the other squares
        for x in range(1, 9):
            for y in range(3, 7):
                square = Square(x=x, y=y)
                self._all_squares[square.name] = square

        # Locate the black and white kings
        self._king_location[Color.white] = 'E1'
        self._king_location[Color.black] = 'E8'

        # These data structures must be kept in sync
        assert isinstance(self.square(self._king_location[Color.black]).piece, BlackKing)
        assert isinstance(self.square(self._king_location[Color.white]).piece, WhiteKing)

    def __repr__(self):
        u"""Returns a string representation of the chess board that can be reconstructed when passed to the
            constructor.
        """
        # 1 indexed chessboard, 1 <= x < 9, 1 <= y < 9
        # xrange would be more a more efficient implemenation but this is a
        # minor and in python 3.x we get this benefit implicitly
        board_string = u""

        for y in range(1, 9):
            for x in range(1, 9):
                piece = self.square(x=x, y=y).piece
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
                board_string += u'-'

        board_repr = u'{0},{1},{2},{3}'.format(board_string, Color.code(self.current_player), self.turn, self._stalemate_count)
        return board_repr.encode('utf-8')

    def _create_board_from_repr(self, board_string):
        u"""Creates a new board from the board described by board_string."""
        unicode_board_string = board_string.decode('utf-8')
        [piece_string, player_color_code, turn, _stalemate_count] = unicode_board_string.split(u',')

        self._previous_moves = []

        self.current_player = Color.decode(player_color_code)

        self.turn = int(turn)
        self._stalemate_count = int(_stalemate_count)
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
                    # square_name = Square.nameFromCoords(x, y)

                    if symbol == _EMPTY_SQUARE:
                        square = Square(x=x, y=y)
                        self._all_squares[square.name] = square
                    else:
                        # cls = Piece.get_piece_class(symbol)
                        piece = PieceFactory.createFromSymbol(symbol, has_moved)
                        square = Square(x=x, y=y)
                        square.piece = piece
                        self._all_squares[square.name] = square
                        if isinstance(piece, King):
                            if piece.color in self._king_location:
                                # Cannot handle multiple kings of the the same color, just saying
                                # We already have a king of this color ... not good
                                raise InvalidBoardException(u"Multiple kings of the color {color} present."
                                                            .format(color=piece.color))
                            else:
                                self._king_location[piece.color] = self.square(x=x, y=y).name

                    has_moved = False

        # These data structures must be kept in sync
        assert isinstance(self.square(self._king_location[Color.black]).piece, BlackKing)
        assert isinstance(self.square(self._king_location[Color.white]).piece, WhiteKing)

    def display(self):
        u"""Prints out a unicode representation of the chess board. Used mainly in command line testing."""
        WHITE_SQUARE = u"\u25a8"
        BLACK_SQUARE = u"\u25a2"
        line = u""
        for y in reversed(range(1, 9)):
            line += u"{0} ".format(y)  # Row number
            for x in range(1, 9, 1):
                # square_name = Square.nameFromCoords(x, y)
                current_piece = self.square(x=x, y=y).piece

                if current_piece is not None:
                    # Display the piece on the square it occupies.
                    line += u"{0} ".format(current_piece.symbol)
                else:
                    # Paint empty squares black / white like a chess board.
                    # The bottom-right-hand corner (if visible) must be a white square.
                    if (x + y) % 2 == 0:
                        line += WHITE_SQUARE + u" "
                    else:
                        line += BLACK_SQUARE + u" "
            line += u"\n"
        else:
            line += u"  A B C D E F G H "
        return line

    def display_previous_moves(self):
        u"""Creates a pretty print version of the previous chess moves taken."""
        return [move.display() for move in self._previous_moves]

    def display_json(self):
        u"""Constructs a simplified representation of the chess board and pieces that can be serailized to JSON
        via the python JSON library."""
        pieces = {}

        for square_name in self._all_squares:
            square = self.square(square_name)
            if square.piece is not None:

                display_piece = {}

                moves, attacks = self._get_moves_and_attacks(square_name)
                display_piece['position'] = square_name
                display_piece['piece'] = square.piece.name
                display_piece['moves'] = list(moves)
                display_piece['attacks'] = list(attacks)

                # Only highlight the current players pieces, but don't highlight if they need to promote a pawn,
                # just highlight that pawn
                display_piece['active'] = False
                if square.piece.color == self.current_player:
                    if self.promote_pawn_location is None:
                        display_piece['active'] = True
                    elif self.promote_pawn_location == square:
                        # It will always be the current players turn
                        display_piece['active'] = True

                pieces[square.name] = display_piece
        return pieces  # json.dumps(super_board)
