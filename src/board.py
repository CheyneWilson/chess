# import string
# import json
from chess_color import Color
from chess_move import Move
from chess_square import Square, InvalidSquareException
from chess_pieces import Piece, King, BlackKing, WhiteKing, Queen, WhiteQueen, BlackQueen, Rook, WhiteRook, \
    BlackRook, Bishop, WhiteBishop, BlackBishop, Knight, WhiteKnight, BlackKnight, Pawn, WhitePawn, BlackPawn, \
    InvlaidPieceException
_HAS_MOVED = 'm'
_EMPTY_SQUARE = '_'


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
    previous_moves = []
    current_player = None
    promote_pawn_location = None  # Marks whether we need to promote a piece

    # turn = 0
    # _stalemate_count gets incremented each time a player moves if they do not
    # capture a peice or advance a pawn. If a pawn is advanced or a piece is
    # captured then the counter is reset to 0. If _stalemate_count is greater
    # than 100 (50 per place), at the start of any turn a player (may) declare
    # a stalemate.
    #
    # See http://en.wikipedia.org/wiki/Fifty-move_rule
    _stalemate_count = 0
    _king_location = None

    def prePickle(self):
        u"""Pickle does not persist class variables, we must do that ourselves."""
        self._all_squares = Square.all_squares

    def postPickle(self):
        u"""Pickle does not persist class variables, we must do that ourselves."""
        # TODO: Can these be moved into __setstate__ and __getstate__
        # That 'may' not let us call the square object
        Square.all_squares = self._all_squares

    def __init__(self, board_string=None):
        if board_string is None:
            self._new_board()
        else:
            self._create_board_from_repr(board_string)

    def get_piece(self, from_):
        u"""Returns the piece at the location specified or None if the square is empty.

        from_ -- the name of the square, e.g A3, or H7
        """
        return Square(from_).piece

    def is_check(self):
        """Returns True if the King of the active player color is in check.
        """
        color = self.current_player
        loc = self._king_location[color]
        enemy_color = Color.inverse(color)
        if len(self._get_attackers(loc, enemy_color)) > 0:
            return True
        return False

    def is_checkmate(self, color):
        u"""Returns True if the King of the color specified is in checkmate."""

        # color = self.current_player
        king_loc = self._king_location[color]
        blocking_squares, enemy_square = self._get_blocking_squares()
        if blocking_squares is None:
            # Not under attack
            return False
        if len(self.get_moves(king_loc.name)) > 0:
                # Can move king to safety
                return False
        else:
            if blocking_squares is set([]):
                # Cannot block, cannot move king, checkmate
                return True
            else:
                # Check if we can capture attacker
                our_attackers = self._get_attackers(enemy_square, color)
                for loc in our_attackers:  # If we have any...

                    if isinstance(loc.piece, King):
                        # If it's the king then since we know we can't
                        # legally move, ignore
                        continue
                    elif self._pinned(loc) is None:
                        # Can capture the piece putting the king incheck
                        return False
                    else:
                        # Can't be pinned by piece causing check
                        # Therefore moving this piece is of no value
                        continue

                # Check if we can block

                for square in blocking_squares:
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
        """Check to see if the game is a stalemate.

        """
        # Check that at least one player has a pawn or more than 3 points
        color = self.current_player

        has_pawn = False
        white_score = 0
        black_score = 0
        for square in Square.all_squares:
            piece = square.piece
            if isinstance(square.piece, Pawn):
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
        for square in Square.all_squares:
            piece = square.piece
            if piece.color == color:
                if len(self.get_moves(square.name)) != 0:
                    # This player can move
                    return False
        else:
            # This player cannot move -> stalemate
            return True

    @property
    def turns_taken(self):
        u"""Returns the number of turns taken. Counts once for each players move."""
        return len(self.previous_moves)

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

    def _get_castle_moves(self, from_square):
        u"""Returns the locations the king located at from_square can castle to.

            from_square -- The location of the king
        """
        assert(from_square.x)
        assert(from_square.y)
        # x, y = from_square
        king = from_square.piece
        left_rook = Square.createFromCoords(1, from_square.y).piece
        right_rook = Square.createFromCoords(8, from_square.y).piece

        moves = set([])
        if king is None or king.has_moved is True:
            return moves

        enemy_color = Color.inverse(king.color)

        # Castling left?
        if left_rook is not None and left_rook.has_moved is False:
            left_4 = Square.createFromCoords(4, from_square.y)
            left_3 = Square.createFromCoords(3, from_square.y)
            left_2 = Square.createFromCoords(2, from_square.y)
            # Empty squares
            if left_2.piece is None:
                if left_3.piece is None:
                    if left_4.piece is None:
                        # With no attackers?
                        if self._get_attackers(left_2, enemy_color) == set([]):
                            if self._get_attackers(left_3, enemy_color) == set([]):
                                if self._get_attackers(left_3, enemy_color) == set([]):
                                    moves.add(left_3)

        # Castling right?
        if right_rook is not None and right_rook.has_moved is False:
            right_6 = Square.createFromCoords(6, from_square.y)
            right_7 = Square.createFromCoords(7, from_square.y)
            # Empty squares
            if right_6.piece is None:
                if right_7.piece is None:
                    # With no attackers?
                    if self._get_attackers(right_6, enemy_color) == set([]):
                        if self._get_attackers(right_7, enemy_color) == set([]):
                            moves.add(right_7)

        return moves

    @staticmethod
    def _is_castle_right(from_, to_):
        u"""Returns True if the move is to castle right.

        Castling is preformed by first moving the king two squares in the
        direction to castle. The castling rook is then moved to the other
        side of the king. This method returns True if the King has been
        moved two squares to the right, or False otherwise.
        """
        if isinstance(from_.piece, King):
            if from_.piece.has_moved is False:
                if to_.x - from_.x == 2:
                    if from_.y == to_.y:
                        return True
        return False

    @staticmethod
    def _is_castle_left(from_, to_):
        u"""Returns True if the move is to castle left.

        Castling is preformed by first moving the king two squares in the
        direction to castle. The castling rook is then moved to the other
        side of the king. This method returns True if the King has been
        moved two squares to the right, or False otherwise.
        """
        if isinstance(from_.piece, King):
            if from_.piece.has_moved is False:
                if to_.x - from_.x == -2:
                    if from_.y == to_.y:
                        return True
        return False

    def move_piece(self, from_, to_):
        """Move a piece from the location from_name to the location to_.

        from_ -- A (case insensitive) string representing the square to move the piece from, eg b7
        to_   -- A (case insensitive) string representing the square to move the piece to, eg A5

        Raises -- A IllegalMoveException if the move is not a legal chess move.
        """

        if self.promote_pawn_location is not None:
            raise IllegalMoveException("Cannot move piece, previously moved pawn must be promoted first.")

        from_square = Square(from_)
        to_square = Square(to_)
        legal_moves = self.get_moves(from_square.name)  # from_square.name handles case sensitivity

        piece = from_square.piece
        if self.current_player != piece.color:
            raise IllegalMoveException("Cannot move piece, it is not {color} player's turn.".format(piece.color))

        # Check to see if anyone has won, if they ha
        if self.winner is not None:
            raise IllegalMoveException("Cannot move piece, the game already has a winner {winner}".format(
                winner=self.winner))

        if to_square.name in legal_moves:  # to_square.name is uppercase while to_name could be any case
            is_castle = False

            if self._is_en_passant_attack(from_square):
                # Remove the pawn that moved previously as it has been captured via en passant
                self.previous_moves[-1].to_.piece = None
            elif self._is_castle_left(from_square, to_square):
                # Move the rook too
                rook = Square.createFromCoords(1, from_square.y).pop()
                Square.createFromCoords(4, from_square.y).piece = rook
                is_castle = True
            elif self._is_castle_right(from_square, to_square):
                # Move the rook too
                rook = Square.createFromCoords(8, from_square.y).pop()
                Square.createFromCoords(6, from_square.y).piece = rook
                is_castle = True

            # Keep track of where the king is
            if isinstance(piece, King):
                self._king_location[piece.color] = to_square

            is_double_move = False  # Marks if a pawn is vulnerable to en passant
            if isinstance(piece, Pawn):
                if abs(from_square.y - to_square.y) == 2:  # The pawn moved two squares
                    is_double_move = True
                # Keep track of 50 move stalemate
                self._stalemate_count = 0

                # If pawn moves into end zone, it needs to be promoted
                if to_square.y == 1 or to_square.y == 8:
                    self.promote_pawn_location = to_square

            if to_square.piece is None:
                is_capture = False  # Moved into an empty square, append regular move
                self._stalemate_count += 1
            else:
                is_capture = True  # Captured an enemy piece, mark as a capture
                self._stalemate_count = 0

            # Finally move the piece
            to_square.piece = from_square.pop()
            piece.has_moved = True

            # TODO: Could fold the logic into this, as from
            self.previous_moves.append(Move(piece, from_square, to_square, is_double_move, is_capture, is_castle))

            # Do not change player if the current player still needs to promote their pawn
            if self.promote_pawn_location is None:
                self.current_player = Color.inverse(self.current_player)

            # These data structures must be kept in sync
            assert isinstance(self._king_location[Color.black].piece, BlackKing)
            assert isinstance(self._king_location[Color.white].piece, WhiteKing)

            return
        # Fall through error
        raise IllegalMoveException("Move of '{0}' from {1} to {2} is not legal.".format(piece, from_, to_))

    def is_fifty_move_stalemate(self):
        """Returns True if 50 consective moves have been taken by either
        player where no pawn has been advanced and no piece captured.

        The fifty move chess rule means a player *may choose* to call a game a
        draw at the start of their turn:
        http://en.wikipedia.org/wiki/Fifty-move_rule
        """
        if self.stalemate_count < 99:  # 50 moves for one, 49 for the other ...
            return False
        else:
            return True

    def promote_pawn(self, piece):
        """Promotes a pawn that has been moved to the last row. Should be called after move_piece.

            piece -- The peice to promote the pawn to. One of Queen, Rook, Bishop, Knight or their colored subclass.
                     The color of the promoted piece is the same as the color of the pawn.
        """
        if self.promote_pawn_location is None:
            raise IllegalMoveException("Cannot promote pawn, no pawn has been moved into end row")
        loc = self.promote_pawn_location
        pawn = loc.piece
        assert(isinstance(pawn, Pawn))    # Must be a pawn
        assert(loc.y == 8 or loc.y == 1)  # Must be in the final row
        if (piece.color is not pawn.color):
            raise InvlaidPieceException("Cannot promote {pawn_color} pawn to {color} {piece}, it is the wrong color"
                                        .format(pawn_color=pawn.color, color=piece.color, piece=piece))

        if isinstance(piece, (Queen, Rook, Bishop, Knight)):
            loc.piece = piece
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
        """Returns the locations of the pieces of the color specified that can attack the given location.

        to_    -- A Square on the chess board
        color  -- The color of the attacking pieces.
        blocker -- If true, returns the locations of pawns that can move to to_ instead of attack it
        returns -- A set of (x,y) locations of all the pieces of the specified color that can attack the loc provided.
        """
        assert(to_.x)
        assert(to_.y)

        # At the given square (to_) we imagine where we could attack with each
        # of our pieces. If we use a knight as example, if any of the squares it
        # can attack contain an enemy knight then that enemy knight is an attacker.
        # If those squares contain any other piece then they are not. Likewise if
        # we imagine a bishop at the location, any bishops or queen it can attack
        # can also attack it. This is repeated for rooks, pawns, king and queen
        # The piece in the squares that potentially attacks this one are checked
        # for enemy pieces that can attack.
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
        dummy_moves, knight_attacks = self._get_knight_bishop_queen_rook_king_moves(knight, to_)
        for k in knight_attacks:
            if isinstance(k.piece, Knight):
                # Opponents knight - an attacker
                attackers.add(k)

        dummy_moves, rooks_or_queen_attacks = self._get_knight_bishop_queen_rook_king_moves(rook, to_)
        for r in rooks_or_queen_attacks:
            if isinstance(r.piece, Rook) or isinstance(r.piece, Queen):
                attackers.add(r)
            elif isinstance(r.piece, King):
                # King can only attack adjacent squares
                if r.isAdjacent(to_):
                    attackers.add(r)

        dummy_moves, bishop_or_queen_attacks = self._get_knight_bishop_queen_rook_king_moves(bishop, to_)
        for b in bishop_or_queen_attacks:
            if isinstance(b.piece, Bishop) or isinstance(b.piece, Queen):
                attackers.add(b)
            elif isinstance(b.piece, King):
                # King can only attack adjacent squares
                if b.isAdjacent(to_):
                    attackers.add(b)

        if blocker:
            pawn_squares = self._get_pawn_move_to(pawn_2, to_)
        else:
            pawn_squares = self._get_pawn_attacks(pawn, to_)
        for p in pawn_squares:
            if isinstance(p.piece, Pawn):
                attackers.add(p)

        return attackers

    def _pinned(self, from_):
        u"""Returns the Square containing the piece that is pinning this one or None if not pinned.

        from_  -- The square to check if the piece inside is pinned.
        """

        color = from_.piece.color
        king_loc = self._king_location[color]
        pinned_direction = king_loc.direction(from_)
        if pinned_direction is None:
            return None  # Not in line with king, can't be pinned

        # Get a list of squares, starting near the king and in a line away
        squares = king_loc.squares_in_direction(pinned_direction)
        maybe_pinned = False
        for s in squares:
            if s.piece is None:
                continue  # blank square, keep looking
            else:
                if s == from_:
                    maybe_pinned = True
                elif maybe_pinned:
                    # Is the piece found an attacker..?
                    if pinned_direction in s.piece.attacks and s.piece.limit != 1:
                        return s
                    else:
                        return None
                else:
                    return None  # Found another piece betwen us and the king, therefore not pinned

    def _get_pinned_directions(self, from_):
        u"""Returns the directions a pinned is able to move or None if not pinned

            from_ -- The location of the piece to check for.
        """
        pinning_square = self._pinned(from_)
        if pinning_square is None:
            return None
        else:
            return set([pinning_square.direction(from_), from_.direction(pinning_square)])

    def get_moves(self, from_):
        u"""Returns a list of all the squares the piece in the given location can attack or move to.

            from_ -- A string like 'A4' which represents the square with the piece to find the moves for
        """
        from_square = Square(from_)
        moves, attacks = self._get_moves_and_attacks(from_square)
        square_names = set([square.name for square in moves.union(attacks)])

        return square_names

    def _get_moves_and_attacks(self, from_):
        """Returns all of the valid moves for piece in the given location.

        from_ -- The location of the piece to get the possible moves for.
        returns -- a set of all the valid moves from loc by the chess piece.

        This returns all of the legal moves a piece can make. It is a subset
        of the locations a piece can move to, retstricted by other game conditions (like is the king in check).
        """
        piece = from_.piece

        if piece is None:
            raise ValueError("Square at location {0} is empty".format(from_))

        if isinstance(piece, King):
            return self._get_king_moves_and_attacks(from_)
        else:
            # Check if this piece is pinned, and then pass the limited move vector to
            # the _get_*piece*_moves methods. They need to be restricted in what they
            # search.
            pinned_directions = self._get_pinned_directions(from_)
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

    def _get_king_moves_and_attacks(self, king_square):
        u"""Returns all of the moves that a king can make.

        The moves a king can make are highly restricted by the other pieces on the board.
        This method restricts the moves to those that do not put the king in check.

        king_square -- The square the king is in
        """
        king = king_square.piece

        # Get all moves, these may be illegal, putting king in check
        moves, attacks = self._get_knight_bishop_queen_rook_king_moves(king, king_square)
        # Add any castling moves, these are all legal
        moves = moves.union(self._get_castle_moves(king_square))

        enemy_color = Color.inverse(king.color)
        threatened = set([])
        if self.is_check():
            # The king is likely blocking the square(s) behind it from the attacker(s)
            # We must count the square(s) as unsafe, because if the king moves there
            # he will still be in check

            enemy_squares = self._get_attackers(king_square, enemy_color)
            for square in enemy_squares:
                x, y = square.direction(king_square)
                if square.piece.limit != 1:
                    try:
                        behind = Square.createFromCoords(king_square.x + x, king_square.y + y)
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
        u"""Returns two sets, one of the locations that a piece can move to, to block check, the other the location of the attacking piece.

        If there are multiple attackers, returns an empty set
        If the king is not in check returns None
        """
        color = self.current_player
        king_loc = self._king_location[color]
        enemy_color = Color.inverse(color)
        enemy_attacking_pieces = self._get_attackers(king_loc, enemy_color)

        if len(enemy_attacking_pieces) == 0:
            # Not under attack
            return None, None
        elif len(enemy_attacking_pieces) == 1:
                # It is possible to capture the attacker
                [enemy_loc] = enemy_attacking_pieces

                # Can we block the attacking piece?
                attack_vector = king_loc.direction(enemy_loc)

                # Find all of the squares that block the path between the enemy piece and king
                return self._get_squares_in_direction(king_loc, attack_vector, color)

        else:
            # We cannot block / capture multiple pieces in one move
            # It makes more sense to return an empty set, rather than all locations that
            # Must be captured or blocked
            return set([]), set([])

    def _get_knight_bishop_queen_rook_king_moves(self, piece, from_, pinned=None):
        """Returns all of the location any of these pieces can move to from the location specified.
           This does not restrict the king from moving into squares that are threatened.
           Call the higher level method _get_moves_and_attacks instead.


        loc     -- The location of the chess piece to move
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

                if len(self.previous_moves) > 0:
                    previous_move = self.previous_moves[-1]

                    if previous_move.is_double_move and previous_move.to_ == en_passant_loc:

                        # We can attack this via en passant
                        # Don't need to check the following, implicity true
                        # if enemy_piece is not None and enemy_piece.color is not pawn.color:
                        # We can capture this normally

                        # We could be pinned by a rook or queen, but this is very rare
                        # Since two pieces are in the way, regular _get_pinned direction
                        # method will not work

                        left_x = min(en_passant_loc.x, from_.x)  # The left square
                        right_x = max(en_passant_loc.x, from_.x)

                        # Search left and right halves to see if we're in a position where capturing
                        # via en passent would put us in check
                        king = None
                        attacker = None
                        for xi in reversed(range(1, left_x)):
                            piece = Square.createFromCoords(xi, from_.y).piece
                            if piece is not None:
                                if isinstance(piece, King) and piece.color == pawn.color:
                                    king = piece
                                elif piece.color != pawn.color and (isinstance(piece, Queen) or isinstance(piece, Rook)):
                                    attacker = piece
                                break

                        if attacker is not None or king is not None:
                            for xi in range(right_x + 1, 9):
                                piece = Square.createFromCoords(xi, from_.y).piece
                                if piece is not None:
                                    if isinstance(piece, King) and piece.color == pawn.color:
                                        king = piece
                                    elif piece.color != pawn.color and (isinstance(piece, Queen) or isinstance(piece, Rook)):
                                        attacker = piece
                                    break

                        if attacker is not None and king is not None:
                            # We're pinned
                            return []

                        pawn_move_location = Square.createFromCoords(en_passant_loc.x, from_.y + pawn.forward)
                        attacks.add(pawn_move_location)

        return attacks

    def _get_pawn_move_to(self, pawn, to_):
        """Returns the location of any pawns that can move to the location specified.

        This is restricted to pawns with the same color as the pawn supplied.

        """
        assert(to_.x)
        assert(to_.y)
        try:
            single_move_loc = Square.createFromCoords(to_.x, to_.y - pawn.forward)
            if isinstance(single_move_loc.piece, pawn.__class__):
                return set([single_move_loc])

            double_move_loc = Square.createFromCoords(to_.x, to_.y - 2 * pawn.forward)
            if isinstance(double_move_loc.piece, pawn.__class__) and self._pawn_has_not_moved(pawn, double_move_loc):
                return set([double_move_loc])

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
                single_move_loc = Square.createFromCoords(from_.x, from_.y + pawn.forward)
            except InvalidSquareException:
                raise IllegalMoveException("Pawn cannot move, it must be promoted instead.")

            if single_move_loc.piece is None:
                moves.add(single_move_loc)
                if self._pawn_has_not_moved(pawn, from_):
                    double_move_loc = Square.createFromCoords(from_.x, from_.y + 2 * pawn.forward)
                    if double_move_loc.piece is None:
                        moves.add(double_move_loc)
            return moves
        elif (1, 0) in pinned:
            # Pinned horizontally, therefore cannot move or attack
            return moves
        else:
            # Pinned diagonally
            pass
        return moves

    def _pawn_has_not_moved(self, pawn, from_):
        # Normally negation is avoided in method names, but this one exception seems warranted
        # as 'has not moved' is an atribute.
        u"""Returns True if the pawn has moved, and False otherwise."""
        if Color.black == pawn.color and from_.y == 7:
            return True
        elif Color.white == pawn.color and from_.y == 2:
            return True
        else:
            return False

    def _is_en_passant_attack(self, from_):
        u"""Returns True if an attack can be made from the location from_ via via en passant"""

        if isinstance(from_.piece, Pawn):  # Only pawns can do en passant
            # 1st move has no previous
            if len(self.previous_moves) > 0:
                # En passant only possible when eneny pawn does double move
                previous_move = self.previous_moves[-1]
                if previous_move.is_double_move:  # Implies pawn
                    if previous_move.to_.y == from_.y:  # Same row
                        if abs(previous_move.to_.x - from_.x) == 1:  # Adjacent square
                            return True

        return False

    def _get_squares_in_direction(self, from_, direction, color, limit=None, all_squares=False):
        u"""Returns a list of moves, and attacks that can be made from the given square in a specific direction

        from_     -- The location to search from
        direction -- The direction to search in
        color     -- The color of this piece (we attack one enemy piece of the opposite color)
        limit     -- The maxium number of total squares to search/return
        ignore_blockers -- If this is true, returns all squares

        returns   -- An ordered list of squares where there piece can move into empty squares,
                     and 0-1 squares that contains a piece it can attack
        """
        # TODO: This should be modified to use the method on Square
        # We're repeating logic, but the logic here is too specific
        # Or at very leasy, need to rename this
        assert(from_.x)
        assert(from_.y)

        moves = set([])
        attack = None  # set([])

        dx, dy = direction
        i = 1
        while limit is None or i <= limit:
            try:
                loc = Square.createFromCoords(from_.x + i * dx, from_.y + i * dy)
                i += 1
                if loc.piece is None or all_squares is True:
                    moves.add(loc)  # Empty square or we're after all squares
                elif loc.piece.color != color:
                    attack = loc  # We've found an enemy piece
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
        self.previous_moves = []
        self.turn = 0
        self._stalemate_count = 0
        self.current_player = Color.white
        self._king_location = dict()

        # Place all the White pieces on the board
        Square.resetAllSquares()
        Square('A1').piece = WhiteRook()
        Square('B1').piece = WhiteKnight()
        Square('C1').piece = WhiteBishop()
        Square('D1').piece = WhiteQueen()
        Square('E1').piece = WhiteKing()
        Square('F1').piece = WhiteBishop()
        Square('G1').piece = WhiteKnight()
        Square('H1').piece = WhiteRook()
        Square('A2').piece = WhitePawn()
        Square('B2').piece = WhitePawn()
        Square('C2').piece = WhitePawn()
        Square('D2').piece = WhitePawn()
        Square('E2').piece = WhitePawn()
        Square('F2').piece = WhitePawn()
        Square('G2').piece = WhitePawn()
        Square('H2').piece = WhitePawn()

        # Place all the Black pieces on the board
        Square('A8').piece = BlackRook()
        Square('B8').piece = BlackKnight()
        Square('C8').piece = BlackBishop()
        Square('D8').piece = BlackQueen()
        Square('E8').piece = BlackKing()
        Square('F8').piece = BlackBishop()
        Square('G8').piece = BlackKnight()
        Square('H8').piece = BlackRook()
        Square('A7').piece = BlackPawn()
        Square('B7').piece = BlackPawn()
        Square('C7').piece = BlackPawn()
        Square('D7').piece = BlackPawn()
        Square('E7').piece = BlackPawn()
        Square('F7').piece = BlackPawn()
        Square('G7').piece = BlackPawn()
        Square('H7').piece = BlackPawn()

        # Locate the black and white kings
        self._king_location[Color.white] = Square('E1')
        self._king_location[Color.black] = Square('E8')

        # These data structures must be kept in sync
        assert isinstance(self._king_location[Color.black].piece, BlackKing)
        assert isinstance(self._king_location[Color.white].piece, WhiteKing)

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
                piece = Square.createFromCoords(x, y).piece
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
        Square.resetAllSquares()
        unicode_board_string = board_string.decode('utf-8')
        [piece_string, player_color_code, turn, _stalemate_count] = unicode_board_string.split(u',')

        self.previous_moves = []

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
                    loc = Square.createFromCoords(x, y)
                    if symbol == _EMPTY_SQUARE:
                        pass
                    else:
                        cls = Piece.get_piece_class(symbol)

                        if issubclass(cls, Pawn):
                            loc.piece = cls(loc)
                        elif issubclass(cls, King):
                            if cls.color in self._king_location:
                                # Cannot handle multiple kings of the the same color, just saying
                                # We already have a king of this color ... not good
                                raise InvalidBoardException(u"Multiple kings of the color {color} present."
                                                            .format(color=cls.color))

                            self._king_location[cls.color] = loc
                            loc.piece = cls(has_moved)
                        elif issubclass(cls, Rook):
                            loc.piece = cls(has_moved)
                        elif issubclass(cls, Knight) or issubclass(cls, Bishop) or issubclass(cls, Queen):
                            loc.piece = cls()
                        else:
                            raise ValueError(u"Invalid chess piece {0}".format(symbol))
                    has_moved = False

        # These data structures must be kept in sync
        assert isinstance(self._king_location[Color.black].piece, BlackKing)
        assert isinstance(self._king_location[Color.white].piece, WhiteKing)

    def display(self):
        u"""Prints out a unicode representation of the chess board. Used mainly in command line testing."""
        WHITE_SQUARE = u"\u25a8"
        BLACK_SQUARE = u"\u25a2"
        line = u""
        for y in reversed(range(1, 9)):
            line += u"{0} ".format(y)  # Row number
            for x in range(1, 9, 1):
                current_piece = Square.createFromCoords(x, y).piece
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
        return [move.display() for move in self.previous_moves]

    def display_json(self):
        u"""Constructs a simplified representation of the chess board and pieces that can be serailized to JSON
        via the python JSON library."""
        pieces = {}

        for square in Square.all_squares:

            display_piece = {}

            moves, attacks = self._get_moves_and_attacks(square)
            display_piece['position'] = square.name
            display_piece['piece'] = square.piece.name
            display_piece['moves'] = [m.name for m in moves]
            display_piece['attacks'] = [a.name for a in attacks]

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
