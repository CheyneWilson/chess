# -*- coding: UTF-8 -*-
from django.test import TestCase
from django.contrib.auth.models import User
from hamcrest import is_, assert_that, equal_to  # , all_of, contains_inanyorder, instance_of

from chess.models import ColorModel, WinnerModel, GameModel, MoveModel
from chess.color import Color
from chess.winner import Winner


class TestColorModel(TestCase):
    """
    Tests restoring state from Color model
    """
    def test_restore_black(self):
        black = ColorModel.objects.get(color=Color.BLACK)
        assert_that(black.color, is_(Color.BLACK))

    def test_restore_white(self):
        white = ColorModel.objects.get(color=Color.WHITE)
        assert_that(white.color, is_(Color.WHITE))


class TestWinnerModel(TestCase):
    """
    Tests restoring state from Winner model
    """
    def test_restore_draw(self):
        draw = WinnerModel.objects.get(winner=Winner.DRAW)
        assert_that(draw.winner, is_(Winner.DRAW))

    def test_restore_undecided(self):
        undecided = WinnerModel.objects.get(winner=Winner.UNDECIDED)
        assert_that(undecided.winner, is_(Winner.UNDECIDED))

    def test_restore_black(self):
        black = WinnerModel.objects.get(winner=Winner.BLACK)
        assert_that(black.winner, is_(Winner.BLACK))

    def test_restore_white(self):
        white = WinnerModel.objects.get(winner=Winner.WHITE)
        assert_that(white.winner, is_(Winner.WHITE))


class TestGameModel_1(TestCase):
    fixtures = ['test_users.json', ]

    def test_fixtures_working(self):
        user_1 = User.objects.get(username='adam')
        assert_that(user_1.first_name, is_('Adam'))

        user_2 = User.objects.get(username='bob')
        assert_that(user_2.first_name, is_('Bob'))

        user_3 = User.objects.get(username='charles')
        assert_that(user_3.first_name, is_('Charles'))

        user_4 = User.objects.get(username='david')
        assert_that(user_4.first_name, is_('David'))

    def test_create_game(self):
        user_1 = User.objects.get(username='adam')
        assert_that(user_1.first_name, is_('Adam'))

        user_2 = User.objects.get(username='bob')
        assert_that(user_2.first_name, is_('Bob'))

        game = GameModel.objects.create(white_player=user_1, black_player=user_2)

        assert_that(game._active_player.color, is_(Color.WHITE))
        assert_that(game._winner.winner, is_(Winner.UNDECIDED))

        # No moves should have been taken
        moves_queryset = MoveModel.objects.filter(game_id=game.id)
        self.assertRaises(MoveModel.DoesNotExist, moves_queryset.get)

        board_str = "♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-________-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜"
        assert_that(repr(game.board), equal_to(board_str))

        game.save()


class TestGameModel_2(TestCase):
    """
    Tests the loading of games. Only partial coverage
    """
    fixtures = ['test_users.json', ]

    def setUp(self):
        user_1 = User.objects.get(username='adam')
        assert_that(user_1.first_name, is_('Adam'))

        user_2 = User.objects.get(username='bob')
        assert_that(user_2.first_name, is_('Bob'))

        for i in range(1, 11):
            game = GameModel.objects.create(white_player=user_1, black_player=user_2)

            assert_that(game._active_player.color, is_(Color.WHITE))
            assert_that(game._winner.winner, is_(Winner.UNDECIDED))

            # No moves should have been taken
            moves_queryset = MoveModel.objects.filter(game_id=game.id)
            self.assertRaises(MoveModel.DoesNotExist, moves_queryset.get)

            board_str = "♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-________-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜"
            assert_that(repr(game.board), equal_to(board_str))

            game.save()
            assert_that(game.id, is_(i))

    def test_load_game(self):
        game = GameModel.objects.get(id=1)

        assert_that(game._active_player.color, is_(Color.WHITE))

        white_player = User.objects.get(username='adam')
        assert_that(game.white_player, is_(white_player))

        black_player = User.objects.get(username='bob')
        assert_that(game.black_player, is_(black_player))

    def test_load_game_2(self):
        game = GameModel.objects.get(id=2)

        game._active_player = ColorModel.objects.get(color=Color.BLACK)
        game.save()

    def test_load_active_player(self):
        game = GameModel.objects.get(id=3)
        assert_that(game.board.current_player, is_(Color.WHITE))


class TestMoveModel(TestCase):
    fixtures = ['test_users.json', ]

    game_id = None

    def setUp(self):
        # Create a game
        user_1 = User.objects.get(username='adam')
        assert_that(user_1.first_name, is_('Adam'))

        user_2 = User.objects.get(username='bob')
        assert_that(user_2.first_name, is_('Bob'))

        game = GameModel.objects.create(white_player=user_1, black_player=user_2)
        game.save()

        self.game_id = game.id

    def test_add_move(self):

        move = MoveModel.objects.create(game_id=self.game_id)
        move.from_loc = "A2"
        move.to_loc = "A4"

        move.save()

        loaded_move = MoveModel.objects.get(game_id=self.game_id)
        assert_that(loaded_move.from_loc, equal_to("A2"))
        assert_that(loaded_move.to_loc, equal_to("A4"))

    def test_add_two_moves(self):

        move_1 = MoveModel.objects.create(game_id=self.game_id)
        move_1.from_loc = "A2"
        move_1.to_loc = "A4"
        move_1.save()

        move_2 = MoveModel.objects.create(game_id=self.game_id)
        move_2.from_loc = "C7"
        move_2.to_loc = "C8"
        move_2.save()

        all_moves = MoveModel.objects.filter(game_id=self.game_id)
        assert_that(len(all_moves), equal_to(2))

        loaded_move_1 = all_moves[0]
        loaded_move_2 = all_moves[1]

        # Moves should be orded in created order
        assert_that(loaded_move_1.from_loc, equal_to("A2"))
        assert_that(loaded_move_1.to_loc, equal_to("A4"))

        assert_that(loaded_move_2.from_loc, equal_to("C7"))
        assert_that(loaded_move_2.to_loc, equal_to("C8"))

    def test_add_many_moves(self):
        """
        Tests the saving of multiple moves using the double-splat operator to
        expand the collection
        """

        move_data = [
            {
                "from_loc": 'A1',
                "to_loc": "A2",
                "piece": u'♖',
                "double_move": False,
                "capture": True,
                "queen_side_castle": False,
                "king_side_castle": False,
                "check": False,
                "checkmate": False,
                "display_value": None
            },
            {
                "from_loc": 'C2',
                "to_loc": "E5",
                "piece": u'♘',
                "double_move": False,
                "capture": False,
                "queen_side_castle": False,
                "king_side_castle": False,
                "check": True,
                "checkmate": False
            },
            {
                "from_loc": 'E2',
                "to_loc": "E5",
                "piece": u'♔',
                "double_move": None,
                "capture": None,
                "queen_side_castle": None,
                "king_side_castle": None,
                "check": None,
                "checkmate": None
            },
        ]

        for data in move_data:
            move = MoveModel.objects.create(game_id=self.game_id, **data)
            move.save()

        query_set = MoveModel.objects.filter(game_id=self.game_id)

        i = 0
        for data in move_data:
            loaded_move = query_set[i]
            assert_that(loaded_move.from_loc, equal_to(data["from_loc"]))
            assert_that(loaded_move.to_loc, equal_to(data["to_loc"]))
            assert_that(loaded_move.piece, equal_to(data["piece"]))
            assert_that(loaded_move.double_move, equal_to(data["double_move"]))
            assert_that(loaded_move.capture, equal_to(data["capture"]))
            assert_that(loaded_move.queen_side_castle, equal_to(data["queen_side_castle"]))
            assert_that(loaded_move.king_side_castle, equal_to(data["king_side_castle"]))
            assert_that(loaded_move.check, equal_to(data["check"]))
            assert_that(loaded_move.checkmate, equal_to(data["checkmate"]))
            i += 1


class TestMoveModel_2(TestCase):
    fixtures = ['test_users.json', ]
    game_id = None

    move_data = [
        {
            "from_loc": 'A1',
            "to_loc": "A2",
            "piece": u'♖',
            "double_move": False,
            "capture": True,
            "queen_side_castle": False,
            "king_side_castle": False,
            "check": False,
            "checkmate": False,
            "display_value": None
        },
        {
            "from_loc": 'C2',
            "to_loc": "E5",
            "piece": u'♘',
            "double_move": False,
            "capture": False,
            "queen_side_castle": False,
            "king_side_castle": False,
            "check": True,
            "checkmate": False
        },
        {
            "from_loc": 'E2',
            "to_loc": "E5",
            "piece": u'♔',
            "double_move": None,
            "capture": None,
            "queen_side_castle": None,
            "king_side_castle": None,
            "check": None,
            "checkmate": None
        },
    ]

    def setUp(self):
        # Create a game
        user_1 = User.objects.get(username='adam')
        assert_that(user_1.first_name, is_('Adam'))

        user_2 = User.objects.get(username='bob')
        assert_that(user_2.first_name, is_('Bob'))

        game = GameModel.objects.create(white_player=user_1, black_player=user_2)
        game.save()

        self.game_id = game.id

        """
        Tests the saving of multiple moves using the double-splat operator to
        expand the collection
        """

        for data in self.move_data:
            move = MoveModel.objects.create(game_id=self.game_id, **data)
            move.save()

    def test_retrieve_last_move(self):
        loaded_move = MoveModel.objects.filter(game_id=self.game_id).latest("id")
        last = self.move_data[-1]

        assert_that(loaded_move.from_loc, equal_to(last["from_loc"]))
        assert_that(loaded_move.to_loc, equal_to(last["to_loc"]))
        assert_that(loaded_move.piece, equal_to(last["piece"]))
        assert_that(loaded_move.double_move, equal_to(last["double_move"]))
        assert_that(loaded_move.capture, equal_to(last["capture"]))
        assert_that(loaded_move.queen_side_castle, equal_to(last["queen_side_castle"]))
        assert_that(loaded_move.king_side_castle, equal_to(last["king_side_castle"]))
        assert_that(loaded_move.check, equal_to(last["check"]))
        assert_that(loaded_move.checkmate, equal_to(last["checkmate"]))
