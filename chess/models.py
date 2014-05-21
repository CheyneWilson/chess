from chess.board import Board
from chess.color import Color
from chess.winner import Winner
from django.db import models
from django.contrib.auth.models import User
from random import random


class BoardField(models.Field):

    __metaclass__ = models.SubfieldBase

    description = u"TODO:"

    def __init__(self, *args, **kwargs):

        kwargs[u'max_length'] = 100  # This is sufficient for all the pieces, squares and annotations
        super(BoardField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(BoardField, self).deconstruct()
        del kwargs[u"max_length"]
        return name, path, args, kwargs

    def to_python(self, value):
        u"""Creates a new board from the board described by board_string."""
        if isinstance(value, Board):
            return value
        else:
            if value is not None:
                if len(value) == 0:  # Web requrests can provide an empty string
                    value = None
            return Board(value)

    def get_prep_value(self, board):
        return str(board)

    def get_internal_type(self):
        return u'CharField'

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)


class ColorField(models.Field):

    __metaclass__ = models.SubfieldBase

    description = u"A custom field that maps the color stored in the database to the correct Color Enum value."

    def __init__(self, *args, **kwargs):

        kwargs[u'max_length'] = 5  # This is sufficient for both Black/White
        super(ColorField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(ColorField, self).deconstruct()
        del kwargs[u"max_length"]
        return name, path, args, kwargs

    def to_python(self, color):
        u"""Creates a new board from the board described by board_string."""

        if isinstance(color, Color):
            return color
        else:
            try:
                return Color._member_map_[color]
            except KeyError:
                raise ValueError("Invalid color '{color}', should be 'BLACK' or 'WHITE'.".format(color))

    def get_prep_value(self, color):
        return color.name

    def get_internal_type(self):
        return u'CharField'

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)


class WinnerField(models.Field):

    __metaclass__ = models.SubfieldBase

    description = u"A custom field that maps the color stored in the database to the correct Winner Enum value."

    def __init__(self, *args, **kwargs):

        kwargs[u'max_length'] = 9  # This is sufficient for both Win/Loss/Draw/Undecided
        super(WinnerField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(WinnerField, self).deconstruct()
        del kwargs[u"max_length"]
        return name, path, args, kwargs

    def to_python(self, value):
        u"""Creates a new board from the board described by board_string."""
        if isinstance(value, Winner):
            return value
        else:
            try:
                return Winner._member_map_[value]
            except KeyError:
                raise Exception("Invalid {value}, should be 'BLACK', 'WHITE', 'DRAW' or 'UNDECIDED'"
                                .format(value=value))

    def get_prep_value(self, value):
        return value.name

    def get_internal_type(self):
        return u'CharField'

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)


class ColorModel(models.Model):
    class Meta:
        app_label = 'chess'
        db_table = 'chess_color'

    BLACK = Color.BLACK
    WHITE = Color.WHITE

    # For dropdowns
    COLOR_CHOICES = (
        (BLACK, u'Black'),
        (WHITE, u'White')
    )

    color = ColorField(
        choices=COLOR_CHOICES,
        default=WHITE,
        unique=True,
        editable=False
    )

    def __unicode__(self):
        return str(self.color.name)


class WinnerModel(models.Model):
    class Meta:
        app_label = 'chess'
        db_table = 'chess_winner'

    BLACK = Winner.BLACK
    WHITE = Winner.WHITE
    DRAW = Winner.DRAW
    UNDECIDED = Winner.UNDECIDED

    WINNER_CHOICES = (
        (BLACK, u'Black'),
        (WHITE, u'White'),
        (DRAW, u'Draw'),
        (UNDECIDED, u'Undecided')
    )

    winner = WinnerField(
        choices=WINNER_CHOICES,
        default=None,
        unique=True,
        editable=False
    )

    def __unicode__(self):
        return str(self.winner.name)


class GameModelManager(models.Manager):
    def create_game(self, player_1_username, player_2_username):
        """
        Create a new game with the black and white player determined at random.
        """
        # The default Mersenne Twister random should be sufficient for this
        players = [player_1_username, player_2_username]
        random.shuffle(players)
        game_model = self.create(white_player=players[0], black_player=players[1])
        return game_model


class GameModel(models.Model):
    # objects = GameModelManager()

    class Meta:
        app_label = 'chess'
        db_table = 'chess_game'

    @classmethod
    def create(cls, white_player, black_player):
        game_model = cls(white_player=white_player, black_player=black_player)
        return game_model

    black_player = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_white_related")
    white_player = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_black_related")
    # The defaults are the same as prepropulated via the fixtures
    _active_player = models.ForeignKey(ColorModel, default=Color.WHITE.value)
    _winner = models.ForeignKey(WinnerModel, default=Winner.UNDECIDED.value)
    _board = BoardField(default=Board())

    # Previous moves are linked via a foreign key from MoveModel

    @property
    def board(self):
        """
        Instanciates a board including the other properties stored in the GameModel

        returns -- A board
        """
        board = self._board
        board.current_player = self._active_player.color
        board.winner = self._winner.winner

        try:
            board.previous_move = MoveModel.objects.filter(game_id=self.id).latest("id")
        except MoveModel.DoesNotExist:
            # New games don't have previos moves
            pass
        return board

        # return self.board

    @board.setter
    def board(self, board):
        """
        Updates a game_model from the information stored in a board. This also appends the previous move
        taken. This method SAVES THE BOARD when it is updated.

        board -- The controller to update the game from
        """
        self._active_player = ColorModel.objects.get(color=board.current_player)
        self._board = board
        self._winner = WinnerModel.objects.get(winner=board.winner)

        m = board.previous_move
        if m is not None:
            move_model = MoveModel.objects.create(
                game_id=self.id,
                from_loc=m.from_loc,
                to_loc=m.to_loc,
                piece=m.piece,
                double_move=m.double_move,
                capture=m.capture,
                queen_side_castle=m.queen_side_castle,
                king_side_castle=m.king_side_castle,
                check=m.check,
                checkmate=m.checkmate,
                display_value=m.display_value
            )

        # TODO: Should be  in an atomic transaction
        move_model.save()
        self.save()  # Including the save in here is ~iffy, BUT since we save the move, we should save the board as
                         # close as possible

    def active_player(self, username):
        """
        Check is the username provided is that of the active player

        username -- The username of the player

        Returns  -- True is the player is the current_player, False if not.
        """
        if self._active_player.color == Color.BLACK:
            if self.black_player.username == username:
                return True
        elif self._active_player.color == Color.WHITE:
            if self.white_player.username == username:
                return True

        return False

    def player_color(self, username):
        """
        Returns the color that the player with the username provided is playing as. If they are playing both
        colors, say in a hotseat manner, returns the color of the active player. If the player is no a player of
        this game, then returns None.

        username -- The username of the player
        """

        if (self.black_player.username == username):
            if (self.white_player.username == username):
                # Player is both
                return self._active_player.color
            else:
                return Color.BLACK
        elif (self.white_player.username == username):
            return Color.WHITE
        else:
            # User is not a player of this game.
            return None


class MoveModel(models.Model):
    ordering = ['id']

    class Meta:
        app_label = 'chess'
        db_table = 'chess_move'

    game = models.ForeignKey(GameModel)
    from_loc = models.CharField(max_length=2, db_column=u"from")
    to_loc = models.CharField(max_length=2, db_column=u"to")
    piece = models.CharField(max_length=2)
    double_move = models.NullBooleanField()
    capture = models.NullBooleanField()
    queen_side_castle = models.NullBooleanField()
    king_side_castle = models.NullBooleanField()
    check = models.NullBooleanField()
    checkmate = models.NullBooleanField()
    stalemate = models.NullBooleanField()
    promotion = models.CharField(max_length=2)
    # Due to how moves are simplifed to minimal representation, the individual properties are not enough to produce
    # the correct representation, we need addional board state info
    display_value = models.CharField(max_length=7, db_column=u"display", null=True)


class ChallengeModel(models.Model):
    """
    Represents one player challenging another
    """
    challenger = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_challenger_related")
    challengee = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_challengee_related")

    class Meta:
        app_label = 'chess'
        unique_together = ('challenger', 'challengee')
