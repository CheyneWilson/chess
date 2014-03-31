# import string
import json
from chess_color import Color
from chess_move import Move
from chess_square import Square
from chess_pieces import Piece, King, BlackKing, WhiteKing, Queen, WhiteQueen, BlackQueen, Rook, WhiteRook, \
    BlackRook, Bishop, WhiteBishop, BlackBishop, Knight, WhiteKnight, BlackKnight, Pawn, WhitePawn, BlackPawn, \
    PieceFactory

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
        if self._valid_location(location):
            return self._all_pieces.get(location, None)
        else:
            raise KeyError()

    def is_check(self, color):
        """Returns True if the King of the color specified is in check.
        """
        loc = self._king_location[color]
        enemy_color = Color.inverse(color)
        if len(self._get_attackers(loc, enemy_color)) > 0:
            return True
        return False

    def is_checkmate(self, color):
        """Returns True if the King of the color specified is in checkmate.
        """
        king_loc = self._king_location[color]
        enemy_color = Color.inverse(color)
        enemy_attacking_pieces = self._get_attackers(king_loc, enemy_color)

        if len(enemy_attacking_pieces) == 0:
            # Not under attack
            return False
        elif len(enemy_attacking_pieces) == 1:
            if len(self.get_moves(king_loc)) == 0:

                # Can't move
                # Can we capture the attacking piece?
                [enemy_loc] = enemy_attacking_pieces
                our_attackers = self._get_attackers(enemy_loc, color)
                for loc in our_attackers:  # If we have any...
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
                v = (enemy_loc[0] - king_loc.x, enemy_loc[1] - king_loc.y)
                attack_vector = self._normalize_vector(v)

                # Find all of the squares that block the path between the enemy piece ance kind
                blocking_squares, dummy_attacks = self._get_squares_2(king_loc, attack_vector, color)

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
            else:
                # Can move, not checkmate
                return False
        else:
            if len(self.get_moves(king_loc)) > 0:
                # Can move king
                return False
            else:
                # It is Impossible to capture / block 2 peices with one move
                return True

    def is_stalemate(self):
        """Check to see if the game is a stalemate.

        """
        # Check that at least one player has a pawn or more than 3 points
        color = self.current_player

        has_pawn = False
        white_score = 0
        black_score = 0
        for loc in self._all_pieces:
            piece = self._all_pieces[loc]
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
        for loc in self._all_pieces:
            piece = self._all_pieces[loc]
            if piece.color == color:
                square = Square(*loc)  # Need to cast from tuple to namedTuple loc
                if len(self.get_moves(square)) != 0:
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

    def _get_castle_moves(self, from_):
        u"""Returns the locations the king located at from_ can castle to."""
        assert(from_.x)
        assert(from_.y)
        # x, y = from_
        king = self.get_piece(from_)
        left_rook = self.get_piece((1, from_.y))
        right_rook = self.get_piece((8, from_.y))

        moves = []
        if king is None or king.has_moved is True:
            return moves

        enemy_color = Color.inverse(king.color)

        # Castling left?
        if left_rook is not None and left_rook.has_moved is False:
            left_4 = Square(4, from_.y)
            left_3 = Square(3, from_.y)
            left_2 = Square(2, from_.y)
            # Empty squares
            if self.get_piece(left_2) is None:
                if self.get_piece(left_3) is None:
                    if self.get_piece(left_4) is None:
                        # With no attackers?
                        if self._get_attackers(left_2, enemy_color) == set([]):
                            if self._get_attackers(left_3, enemy_color) == set([]):
                                if self._get_attackers(left_3, enemy_color) == set([]):
                                    moves.append(left_3)

        # Castling right?
        if right_rook is not None and right_rook.has_moved is False:
            right_6 = Square(6, from_.y)
            right_7 = Square(7, from_.y)
            # Empty squares
            if self.get_piece(right_6) is None:
                if self.get_piece(right_7) is None:
                    # With no attackers?
                    if self._get_attackers(right_6, enemy_color) == set([]):
                        if self._get_attackers(right_7, enemy_color) == set([]):
                            moves.append(right_7)

        return moves

    @staticmethod
    def _is_castle_right(from_, to_):
        """Returns True if the move is to castle right.

        Castling is preformed by first moving the king two squares in the
        direction to castle. The castling rook is then moved to the other
        side of the king. This method returns True if the King has been
        moved two squares to the right, or False otherwise.
        """
        if to_.x - from_.x == 2:
            if from_.y == to_.y:
                return True
        return False

    @staticmethod
    def _is_castle_left(from_, to_):
        """Returns True if the move is to castle left.

        Castling is preformed by first moving the king two squares in the
        direction to castle. The castling rook is then moved to the other
        side of the king. This method returns True if the King has been
        moved two squares to the right, or False otherwise.
        """
        if to_.x - from_.x == -2:
            if from_.y == to_.y:
                return True
        return False

    def move_piece(self, from_, to_):
        """Move a piece from the location from_ to the location to_.

        Raises -- A IllegalMoveException if the move is not a legal chess move.
        """
        assert(from_.x)
        assert(from_.y)
        assert(to_.x)
        assert(to_.y)

        if self.promote_pawn_location is not None:
            raise IllegalMoveException("Cannot move piece, previously moved pawn must be promoted first.")

        legal_moves = self.get_moves(from_)
        piece = self._all_pieces[from_]

        if self.current_player != piece.color:
            raise IllegalMoveException("Cannot move piece, it is not {color} player's turn.".format(piece.color))

        # Check to see if anyone has won, if they ha
        if self.winner is not None:
            raise IllegalMoveException("Cannot move piece, the game already has a winner {winner}".format(winner=self.winner))

        if legal_moves is not False:
            if to_ in legal_moves:
                piece.location = to_  # Update the internal location to the new location
                piece.has_moved = True

                if self._is_en_passant_attack(from_):
                    # Remove the pawn that moved previously as it has been captured
                    # via en passant
                    self._all_pieces[self.previous_moves[-1].to_] = None
                elif self._is_castle_left(from_, to_):
                    # Move the rook too
                    rook_loc = (1, from_.y)
                    rook = self._all_pieces.pop(rook_loc, None)
                    self._all_pieces[(4, from_.y)] = rook
                elif self._is_castle_right(from_, to_):
                    # Move the rook too
                    rook_loc = (8, from_.y)
                    rook = self._all_pieces.pop(rook_loc, None)
                    self._all_pieces[(6, from_.y)] = rook

                # Keep track of where the king is
                if isinstance(piece, King):
                    self._king_location[piece.color] = to_

                is_double_move = False  # Marks if a pawn is vulnerable to en passant
                if isinstance(piece, Pawn):
                    if abs(from_.y - to_.y) == 2:  # The pawn moved two squares
                        is_double_move = True
                    # Keep track of 50 move stalemate
                    self._stalemate_count = 0

                    # If pawn moves into end zone, it needs to be promoted
                    if to_.y == 1 or to_.y == 8:
                        self.promote_pawn_location = to_

                elif self._all_pieces.get(to_, None) is None:
                    # No capture
                    self._stalemate_count += 1
                else:
                    # A capture
                    self._stalemate_count = 0

                self._all_pieces.pop(from_, None)
                self._all_pieces[to_] = piece
                self.current_player = Color.inverse(self.current_player)

                self.previous_moves.append(Move(piece, from_, to_, is_double_move))

                # These data structures must be kept in sync
                assert isinstance(self._all_pieces[self._king_location[Color.black]], BlackKing)
                assert isinstance(self._all_pieces[self._king_location[Color.white]], WhiteKing)

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
        if self.stalemate_count <= 100:
            return True
        else:
            return False

    @staticmethod
    def _is_adjacent(loc_a, loc_b):
        """Returns True if two squares are horizontally, vertically or diagonally adjacent (side by side).
        """
        if loc_a.x - loc_b.x <= 1:
            if loc_a.y - loc_b.y <= 1:
                if loc_a != loc_b:
                    return True
        return False

    def promote_pawn(self, piece):
        """Promotes a pawn that has been moved to the last row. Should be called after move_piece.

            piece -- The peice to promote the pawn to. One of Queen, Rook, Bishop, Knight or their colored subclass.
                     The color of the promoted piece is the same as the color of the pawn.
        """
        if self.promote_pawn_location is None:
            raise IllegalMoveException("Cannot promote pawn, no pawn has been moved into end row")
        loc = self.promote_pawn_location
        pawn = self.get_piece(loc)
        assert(isinstance(pawn, Pawn))
        assert(loc.y == 8 or loc.y == 1)
        color = pawn.color

        if issubclass(piece, (Queen, Rook, Bishop, Knight)):
            self._all_pieces[loc] = PieceFactory.create(piece, color)
            self.promote_pawn_location = None  # Clear the promotion
        else:
            raise TypeError("Cannot promote pawn to {piece}.".format(piece=piece))

    def _get_attackers(self, to_, color, blocker=False):
        """Returns the locations of the pieces of the color specified that
        can attack the given location.

        to_    -- A Square(x, y) on the chess board
        color  -- The color of the attacking pieces
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
        dummy_moves, knight_attacks = self._get_knight_bishop_queen_rook_king_moves_2(knight, to_)
        for k in knight_attacks:
            piece = self.get_piece(k)
            if isinstance(piece, Knight):
                # Opponents knight - an attacker
                attackers.add(k)

        dummy_moves, rooks_or_queen_attacks = self._get_knight_bishop_queen_rook_king_moves_2(rook, to_)
        for r in rooks_or_queen_attacks:
            piece = self.get_piece(r)
            if isinstance(piece, Rook) or isinstance(piece, Queen):
                attackers.add(r)
            elif isinstance(piece, King):
                # King can only attack adjacent squares
                if self._is_adjacent(r, to_):
                    attackers.add(r)

        dummy_moves, bishop_or_queen_attacks = self._get_knight_bishop_queen_rook_king_moves_2(bishop, to_)
        for b in bishop_or_queen_attacks:
            piece = self.get_piece(b)
            if isinstance(piece, Bishop) or isinstance(piece, Queen):
                attackers.add(b)
            elif isinstance(piece, King):
                # King can only attack adjacent squares
                if self._is_adjacent(b, to_):
                    attackers.add(b)

        if blocker:
            pawn_squares = self._get_pawn_move_to(pawn_2, to_)
        else:
            pawn_squares = self._get_pawn_attacks(pawn)
        for p in pawn_squares:
            piece = self.get_piece(p)
            if isinstance(piece, Pawn):
                attackers.add(p)

        return attackers

    @staticmethod
    def _normalize_vector(vector):
        """Reduce length of the x and y parts of the veror to 1 while
        maintaining the same direction (if possible).

        vector  -- A tuple of the form (x, y)
        returns -- one of (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1),
                (1,-1) or if the vector cannot be normalized then returns None
        """
        x, y = vector

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
        """Returns the directions a piece is pinned or an empty set if it is not pinned.
        """
        assert(from_.x)
        assert(from_.y)

        piece = self.get_piece(from_)
        assert piece is not None
        color = piece.color

        # A piece can only be pinned if it's in a line with the king
        king_loc = self._king_location[color]
        pinned_vector = (from_.x - king_loc.x, from_.y - king_loc.y)

        # Since only queen, rook and bishop can pin
        # pinned_vector must normalze to one of (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (1, -1)
        vector = self._normalize_vector(pinned_vector)
        if vector is None:
            # Can't be pinned
            return set([])

        x, y = vector
        pinned_direction = (x, y)
        negative_pinned_direction = (-x, -y)

        # We're only pinned if there is an attacker in this direction
        # An execption to this is a pawn may be prevented from attacking
        # via en passant, but that is a rare case and the logic is handled
        # there to reduce general complexity
        moves, attacks = self._get_squares_2(from_, pinned_direction, color)

        # There is at maximum only 1 attacker an any given direction
        if len(attacks) == 1:

            enemy_piece = self.get_piece(attacks[0])

            # Check if the enemey pience can attack back
            if negative_pinned_direction in enemy_piece.attacks:
                # TODO: THIS LOCK WILL FAIL FOR PAWNS (false positive), should check if they can attack
                return set([pinned_direction, negative_pinned_direction])

        return set([])

    def get_moves(self, from_):
        u"""Returns a list of all the squares the piece in the given location can attack or move to."""
        moves, attacks = self.get_moves_and_attacks(from_)
        return moves + attacks

    def get_moves_and_attacks(self, from_):
        """Returns all of the valid moves for piece in the given location.

        from_ -- The location of the piece to get the possible moves for.
        returns -- a set of all the valid moves from loc by the chess piece.

        This returns all of the legal moves a piece can make. It is a subset
        of the locations a piece can move to, retstricted by other game
        conditions (like is the king in check).
        """
        assert(from_.x)
        assert(from_.y)

        piece = self.get_piece(from_)
        if piece is None:
            raise ValueError("Square at location {0} is empty".format(from_))

        if isinstance(piece, King):
            moves, attacks = self._get_knight_bishop_queen_rook_king_moves_2(piece, from_)
            moves.extend(self._get_castle_moves(from_))  # Add any castling moves

            enemy_color = Color.inverse(piece.color)

            #TODO: This could be simplified
            safe_moves = []
            safe_attacks = []
            for m in moves:
                if len(self._get_attackers(m, enemy_color)) > 0:
                    # Can't move king into check
                    pass
                else:
                    safe_moves.append(m)
            for a in attacks:
                if len(self._get_attackers(a, enemy_color)) > 0:
                    # Can't move king into check
                    pass
                else:
                    safe_attacks.append(a)
            return safe_moves, safe_attacks
        else:
            # Check if this piece is pinned, and then pass the limited move vector to
            # the _get_*piece*_moves methods. They need to be restricted in what they
            # search.
            pinned_directions = self._get_pinned_directions(from_)
            if isinstance(piece, Pawn):
                moves = self._get_pawn_moves(piece, from_, pinned_directions)
                attacks = self._get_pawn_attacks(piece, pinned_directions)

            elif isinstance(piece, Queen) or isinstance(piece, Rook) or \
                    isinstance(piece, Bishop) or isinstance(piece, Knight):
                # A pinned piece can only move in the vector it is pinned in
                moves, attacks = self._get_knight_bishop_queen_rook_king_moves_2(piece, from_, pinned_directions)

        return moves, attacks

    def _get_knight_bishop_queen_rook_king_moves_2(self, piece, from_, pinned=set([])):
        """Returns all of the location any of these pieces can move to from the location specified.


        loc     -- The location of the chess piece to move
        piece   -- The piece to find the moves for. It doesn not have to be the
                   same piece that is actually found at loc. This allows us to 'imagine' where you could move
                   from if that piece was there.
        pinned  -- A set of directions this piece is pinned (both  +/- vector)

        returns -- A two lists of x-y coords tuples representation the moves and attacks of the specified piece from
                   the location provided. [(x1,y1),(x2,y2),....(xm,ym)],[(xm+1,ym+1),....(xn,yn)]
        """
        all_attacks = []
        all_moves = []

        if len(pinned) != 0:
            # A piece cannot be pinned in more than one direction
            # If the piece is pinned vertically (or any other direction), it can still move in that direction
            move_vectors = pinned.intersection(piece.attacks)
        else:
            move_vectors = piece.attacks

        for direction in move_vectors:
            [moves, attacks] = self._get_squares_2(from_, direction, piece.color, piece.get_limit())
            all_attacks += attacks
            all_moves += moves

        return all_moves, all_attacks

    # I don't like the similarity in naming with _get_pawn_attacks (differing only by an s)
    def _get_pawn_attacks(self, pawn, pinned=set([])):
        """Returns the location a pawn can attack diagonnaly in one direction.

        pawn   -- The pawn to return the location it can attack
        pinned -- A set of directions this piece is pinned (both  +/- vector)
        """
        attacks = []

        for attack_dir in pawn.attacks:
            # Check if the piece can attack normally
            if len(pinned) == 0 or attack_dir in pinned:
                dummy_locs, enemy_locs = self._get_squares_2(pawn.location, attack_dir, pawn.color, 1)

                for enemy_location in enemy_locs:
                    # We can capture this normally
                    attacks.append(enemy_location)

        for en_passant_dir in pawn.en_passant():

            # en_passant_dir = pawn.en_passant_2(attack_dir)
            # Check if the pawn can attack via en passant
            # TODO: Draw out some chess boards in the comments to make this more
            # comprehensible to others reading the code. Will have to use unicode in
            # the source ... should be ok, it's 2013 now and ascii isn't the be all and end all
            dummy_locs, en_passant_locs = self._get_squares_2(pawn.location, en_passant_dir, pawn.color, 1)
            for en_passant_loc in en_passant_locs:

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

                        left_x = min(en_passant_loc.x, pawn.location.x)  # The left square
                        right_x = max(en_passant_loc.y, pawn.location.x)

                        # Search left and right halves to see if we're in a position where capturing
                        # via en passent would put us in check
                        king = None
                        attacker = None
                        for xi in reversed(range(1, left_x)):
                            piece = self.get_piece((xi, pawn.location.y))
                            if piece is not None:
                                if isinstance(piece, King) and piece.color == pawn.color:
                                    king = piece
                                elif piece is not pawn.color and (isinstance(piece, Queen) or isinstance(piece, Rook)):
                                    attacker = piece
                                break

                        if attacker is not None or king is not None:
                            for xi in range(right_x + 1, 9):
                                piece = self.get_piece((xi, pawn.location.y))
                                if piece is not None:
                                    if isinstance(piece, King) and piece.color == pawn.color:
                                        king = piece
                                    elif piece is not pawn.color and (isinstance(piece, Queen) or isinstance(piece, Rook)):
                                        attacker = piece
                                    break

                        if attacker is not None and king is not None:
                            # We're pinned
                            return []

                        attacks.append(pawn.en_passant_move(en_passant_dir))

        return attacks

    def _get_pawn_move_to(self, pawn, to_):
        """Returns the location of any pawns that can move to the location specified.

        This is restricted to pawns with the same color as the pawn supplied.

        """
        assert(to_.x)
        assert(to_.y)

        single_move_loc = (to_.x, to_.y - pawn.forward)
        double_move_loc = (to_.x, to_.y - 2 * pawn.forward)
        if self._valid_location(single_move_loc):
            piece = self.get_piece(single_move_loc)
            if isinstance(piece, pawn.__class__):
                return set([single_move_loc])
            if self._valid_location(double_move_loc):
                piece = self.get_piece(double_move_loc)
                if isinstance(piece, pawn.__class__) and not piece.has_moved:
                    return set([double_move_loc])
        return set([])

    def _get_pawn_moves(self, pawn, from_, pinned=set([])):
        """Returns all of the moves that a pawn can make from the given from_ location.
        """
        moves = []

        if (1, 0) in pinned:
            # Pinned horizontally, therefore cannot move or attack
            return moves

        # Check if the pawn is not pinned or only pinned vertically so can move forward
        if len(pinned) == 0 or (0, 1) in pinned:
            potential_moves = pawn.moves
            # Check that the squares are empty
            for loc in potential_moves:
                if self.get_piece(loc) is None:
                    moves.append(loc)
                else:
                    # hit another peice
                    break

        return moves

    def _is_en_passant_attack(self, from_):
        """Returns True if an attack can be made from the location from_ via via en passant"""
        piece = self.get_piece(from_)
        # Only pawns can do en passant
        if isinstance(piece, Pawn):
            # 1st move has no previous
            if len(self.previous_moves) > 0:
                # En passant only possible when eneny pawn does double move
                previous_move = self.previous_moves[-1]
                if previous_move.is_double_move:  # Implies pawn
                    if previous_move.to_.y == from_.y:  # Same row
                        if abs(previous_move.to_.x - from_.x) == 1:  # Adjacent square
                            return True

        return False

    def _get_squares_2(self, from_, direction, color, limit=None):
        """A re-write of _get_squares to avoid using the Square object for simplicity

        from_     -- The location to search from
        direction -- The direction to search in
        color     -- The color of this piece (we attack one ememy peice of the opposite color)

        """
        assert(from_.x)
        assert(from_.y)

        moves = []
        attacks = []

        dx, dy = direction
        i = 1
        while limit is None or i <= limit:
            loc = Square(from_.x + i * dx, from_.y + i * dy)
            i += 1
            try:
                piece = self.get_piece(loc)  # Will raise a KeyError if we step off the board

                if piece is None:
                    moves.append(loc)  # Empty square

                elif piece.color != color:
                    attacks.append(loc)  # We've found an enemy piece
                    break
                else:
                    # We've found one of our own peices
                    break

            except KeyError:
                # We've stepped off the board
                break
        return moves, attacks

    @staticmethod
    def _valid_location(loc):
        """Returns True if the location (x,y) is within chess board."""
        x, y = loc
        if 1 <= x <= 8 and 1 <= y <= 8:
            return True
        return False

    def _new_board(self):
        """Places all of the pieces on the chessboard in their starting
        positions and assign white player first turn."""
        self.previous_moves = []
        self.turn = 0
        self._stalemate_count = 0
        self.current_player = Color.white
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
        self._all_pieces[(1, 2)] = WhitePawn(Square(1, 2))
        self._all_pieces[(2, 2)] = WhitePawn(Square(2, 2))
        self._all_pieces[(3, 2)] = WhitePawn(Square(3, 2))
        self._all_pieces[(4, 2)] = WhitePawn(Square(4, 2))
        self._all_pieces[(5, 2)] = WhitePawn(Square(5, 2))
        self._all_pieces[(6, 2)] = WhitePawn(Square(6, 2))
        self._all_pieces[(7, 2)] = WhitePawn(Square(7, 2))
        self._all_pieces[(8, 2)] = WhitePawn(Square(8, 2))

        # Place all the Black pieces on the board
        self._all_pieces[(1, 8)] = BlackRook()
        self._all_pieces[(2, 8)] = BlackKnight()
        self._all_pieces[(3, 8)] = BlackBishop()
        self._all_pieces[(4, 8)] = BlackQueen()
        self._all_pieces[(5, 8)] = BlackKing()
        self._all_pieces[(6, 8)] = BlackBishop()
        self._all_pieces[(7, 8)] = BlackKnight()
        self._all_pieces[(8, 8)] = BlackRook()
        self._all_pieces[(1, 7)] = BlackPawn(Square(1, 7))
        self._all_pieces[(2, 7)] = BlackPawn(Square(2, 7))
        self._all_pieces[(3, 7)] = BlackPawn(Square(3, 7))
        self._all_pieces[(4, 7)] = BlackPawn(Square(4, 7))
        self._all_pieces[(5, 7)] = BlackPawn(Square(5, 7))
        self._all_pieces[(6, 7)] = BlackPawn(Square(6, 7))
        self._all_pieces[(7, 7)] = BlackPawn(Square(7, 7))
        self._all_pieces[(8, 7)] = BlackPawn(Square(8, 7))

        # Locate the black and white kings
        self._king_location[Color.white] = Square(5, 1)
        self._king_location[Color.black] = Square(5, 8)

        # These data structures must be kept in sync
        assert isinstance(self._all_pieces[self._king_location[Color.black]], BlackKing)
        assert isinstance(self._all_pieces[self._king_location[Color.white]], WhiteKing)

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
                board_string += u'-'

        board_repr = u'{0},{1},{2},{3}'.format(board_string, Color.code(self.current_player), self.turn, self._stalemate_count)
        return board_repr.encode('utf-8')

    def _create_board_from_repr(self, board_string):
        """Creates a new board from the board described by board_string."""
        unicode_board_string = board_string.decode('utf-8')
        [piece_string, player_color_code, turn, _stalemate_count] = unicode_board_string.split(u',')

        self.previous_moves = []

        self.current_player = Color.decode(player_color_code)

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
                    loc = Square(x, y)
                    if symbol == _EMPTY_SQUARE:
                        pass
                    else:
                        cls = Piece.get_piece_class(symbol)

                        if issubclass(cls, Pawn):
                            self._all_pieces[loc] = cls(loc)
                        elif issubclass(cls, King):
                            if cls.color in self._king_location:
                                # Cannot handle multiple kings of the the same color, just saying
                                # We already have a king of this color ... not good
                                raise InvalidBoardException(u"Multiple kings of the same color '{color}' present.".format(color=cls.color))

                            self._king_location[cls.color] = loc
                            self._all_pieces[loc] = cls(has_moved)
                        elif issubclass(cls, Rook):
                            self._all_pieces[loc] = cls(has_moved)
                        elif issubclass(cls, Knight) or issubclass(cls, Bishop) or issubclass(cls, Queen):
                            self._all_pieces[loc] = cls()
                        else:
                            raise ValueError(u"Invalid chess piece {0}".format(symbol))
                    has_moved = False

        # These data structures must be kept in sync
        assert isinstance(self._all_pieces[self._king_location[Color.black]], BlackKing)
        assert isinstance(self._all_pieces[self._king_location[Color.white]], WhiteKing)

    def display(self):
        """Prints out a unicode representation of the chess board."""
        WHITE_SQUARE = u"\u25a8"
        BLACK_SQUARE = u"\u25a2"
        line = u""
        # 1 indexed chessboard, 1 <= x < 9
        for y in range(8, 0, -1):  # TODO: Should use range reversed
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

    def display_previous_moves(self):
        return [move.display() for move in self.previous_moves]

    @staticmethod
    def _translate_squares(squares):
        """Converts to representation is more compatible with JSON notation. """
        new_squares = []
        for s in squares:
            new_squares.append({u'x': s.x, u'y': s.y})

        return new_squares

    def display_json(self):
        """Constructs a JSON representation of chess pieces."""
        super_board = []

        for y in range(1, 9, 1):
            super_board.append([])
            for x in range(1, 9, 1):
                from_ = Square(x, y)
                current_piece = self.get_piece(from_)
                square = {}

                if current_piece is not None:
                    moves, attacks = self.get_moves_and_attacks(from_)
                    square['piece'] = current_piece.simple_simbol
                    square['moves'] = [m.name for m in moves]  # self._translate_squares(moves)  # self._translate_squares(self.get_moves(from_))
                    square['attacks'] = [a.name for a in attacks]  # self._translate_squares(attacks)
                else:
                    square['piece'] = 'empty'
                    square['moves'] = []
                    square['attacks'] = []
                # square['highlight'] = None  # Used in front-end only

                super_board[y - 1].append(square)
        return super_board  # json.dumps(super_board)

    def display_json_2(self):
        """Constructs a JSON representation of chess pieces."""
        pieces = {}

        for loc in self._all_pieces:
            from_ = Square(*loc)

            current_piece = self.get_piece(from_)
            piece = {}

            moves, attacks = self.get_moves_and_attacks(from_)
            piece['position'] = from_.name
            piece['piece'] = current_piece.simple_simbol
            piece['moves'] = [m.name for m in moves]
            piece['attacks'] = [a.name for a in attacks]

            pieces[from_.name] = piece
        return pieces  # json.dumps(super_board)

    def json(self):
        """Output a json representation of the board
        """
        board = []
        for location in self._all_pieces:
            x, y = location
            piece = self._all_pieces[location]

            from_ = Square(x, y)
            moves, attacks = self.get_moves_and_attacks(from_)

            square = {}
            square[u'x'] = x
            square[u'y'] = y
            square[u'piece'] = piece.name
            square[u'color'] = piece.color
            square[u'moved'] = piece.has_moved
            square[u'moves'] = moves  # []  # board.get_moves(location)
            square[u'attacks'] = attacks  # []  # TODO: call method

            board.append(square)

        game = {}
        game[u'current_player'] = self.current_player  # .name
        game[u'board'] = board
        game[u'status'] = 'IN_PROGRESS'  # TODO: call method
        game[u'previous_moves'] = []

        return json.dumps(game)
