# -*- coding: UTF-8 -*-
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.test import Client
from django.test import TestCase
from hamcrest import is_, assert_that, equal_to, contains_inanyorder  # , all_of, , instance_of
import json

from chess.views import ChessResponses


class CreateGameTest(TestCase):
    fixtures = ['test_users.json', ]

    def test_create_game(self):
        """
        Create a new game for the 'adam' user
        """
        username = 'adam'  # From fixtures
        url = '/chess/user/' + username + '/game/'
        c = Client()
        response = c.post(url)
        assert_that(response.status_code, is_(HTTP_200_OK))

        # The comparision with the board is tricky ... as the represenation is in flux. We will ignore here and test
        # explicitly elsewhere, even if it is just manually until the 'spec' finalizes
        content = json.loads(response.content)
        del content["board"]

        # Convert from JSON back to native python as it makes comparison easiest
        expected = json.loads(u"""{
                "id": 1,
                "active_player": "WHITE",
                "winner": "UNDECIDED",
                "black_player": 1000001,
                "white_player": 1000001,
                "board_code": "♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-________-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜"
        }""")

        assert_that(content, equal_to(expected))

    def test_create_game_2(self):
        """
        Create a new game for a user that does not exist
        """
        username = 'i_dont_exist'
        url = '/chess/user/' + username + '/game/'
        c = Client()
        response = c.post(url)
        assert_that(response.status_code, is_(HTTP_400_BAD_REQUEST))

        assert_that(json.loads(response.content), equal_to(ChessResponses.USER_DOES_NOT_EXIST))


class GetGameTest(TestCase):
    fixtures = ['test_users.json', ]

    def setUp(self):
        username = 'adam'  # From fixtures
        url = '/chess/user/' + username + '/game/'
        c = Client()

        # Create 10 games
        for i in range(0, 10):
            response = c.post(url)
            assert_that(response.status_code, is_(HTTP_200_OK))

    def test_list_games_1(self):
        """
        Testing listing games for Adam who has 10 games
        """
        username = 'adam'  # From fixtures
        url = '/chess/user/' + username + '/game/'
        c = Client()

        response = c.get(url)
        assert_that(response.status_code, is_(HTTP_200_OK))

        games = json.loads(response.content)
        assert_that(len(games), is_(10))

        for game in games:
            # TODO: Enhance validation as format is finalized, use Color.WHITE.name
            # Add checks for other properties
            assert_that(game["active_player"], equal_to("WHITE"))

    def test_list_games_2(self):
        """
        Testing listing games for a user that does not exist
        """
        username = 'i_dont_exist'
        url = '/chess/user/' + username + '/game/'
        c = Client()
        response = c.get(url)
        assert_that(response.status_code, is_(HTTP_400_BAD_REQUEST))
        assert_that(json.loads(response.content), equal_to(ChessResponses.USER_DOES_NOT_EXIST))

    def test_get_game_1(self):
        """
        Test loading a game that exists
        """
        username = 'adam'
        game_id = '1'
        url = '/chess/user/' + username + '/game/' + game_id
        c = Client()
        response = c.get(url)
        assert_that(response.status_code, is_(HTTP_200_OK))

        content = json.loads(response.content)
        # The comparision with the board is tricky ... as the represenation is in flux. We will ignore here and test
        # explicitly elsewhere, even if it is just manually until the 'spec' finalizes
        del content["board"]

        expected = json.loads(u"""{
                "id": 1,
                "active_player": "WHITE",
                "winner": "UNDECIDED",
                "black_player": 1000001,
                "white_player": 1000001,
                "board_code": "♖♘♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-________-________-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜"
        }""")
        assert_that(content, equal_to(expected))

    def test_get_game_2(self):
        """
        Test loading a game that does not exist
        """
        username = 'adam'
        game_id = '99'
        url = '/chess/user/' + username + '/game/' + game_id
        c = Client()
        response = c.get(url)
        assert_that(response.status_code, is_(HTTP_400_BAD_REQUEST))
        assert_that(json.loads(response.content), equal_to(ChessResponses.GAME_DOES_NOT_EXIST))

    def test_get_game_3(self):
        """
        Test loading a game when the username is wrong
        """
        username = 'adfas'
        game_id = '1'
        url = '/chess/user/' + username + '/game/' + game_id
        c = Client()
        response = c.get(url)
        assert_that(response.status_code, is_(HTTP_400_BAD_REQUEST))
        assert_that(json.loads(response.content), equal_to(ChessResponses.USER_DOES_NOT_EXIST))

    def test_get_game_4(self):
        """
        Test loading a game when the username exist
        """
        username = 'bob'
        game_id = '1'
        url = '/chess/user/' + username + '/game/' + game_id
        c = Client()
        response = c.get(url)
        assert_that(response.status_code, is_(HTTP_400_BAD_REQUEST))
        assert_that(json.loads(response.content), equal_to(ChessResponses.USER_IS_NOT_PLAYER))


class TestMove_1(TestCase):
    """
    Tests the basics of chess moves.

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
    fixtures = ['test_users.json', ]

    def setUp(self):
        username = 'adam'  # From fixtures
        url = '/chess/user/' + username + '/game/'
        c = Client()

        # Create 10 games for adam
        for i in range(0, 10):
            response = c.post(url)
            assert_that(response.status_code, is_(HTTP_200_OK))

    def test_game_move_1(self):
        """
        Tests getting the moves for a pawn that can move.
        """
        username = 'adam'  # From fixtures
        game_id = 1
        from_ = 'A2'
        url = '/chess/user/' + username + '/game/' + str(game_id) + '/move/' + from_
        c = Client()

        response = c.get(url)
        content = json.loads(response.content)
        expected = json.loads(u"""{
            "from": "A2",
            "to": [
                {"capture": false, "square": "A3"},
                {"capture": false, "square": "A4"}
            ]
        }""")

        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(content["from"], equal_to(expected["from"]))
        assert_that(content["to"], contains_inanyorder(*expected["to"]))

    def test_game_move_2(self):
        """
        Tests getting the moves for a knight that can move.
        """
        username = 'adam'  # From fixtures
        game_id = 1
        from_ = 'B1'
        url = '/chess/user/' + username + '/game/' + str(game_id) + '/move/' + from_
        c = Client()

        response = c.get(url)
        content = json.loads(response.content)
        expected = json.loads(u"""{
            "from": "B1",
            "to": [
                {"capture": false, "square": "A3"},
                {"capture": false, "square": "C3"}
            ]
        }""")

        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(content["from"], equal_to(expected["from"]))
        assert_that(content["to"], contains_inanyorder(*expected["to"]))

    def test_game_move_3(self):
        """
        Tests getting the moves for a bishop that CANNOT move.
        """
        username = 'adam'  # From fixtures
        game_id = 1
        from_ = 'C1'
        url = '/chess/user/' + username + '/game/' + str(game_id) + '/move/' + from_
        c = Client()

        response = c.get(url)
        content = json.loads(response.content)
        expected = json.loads(u"""{
            "from": "C1",
            "to": []
        }""")

        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(content["from"], equal_to(expected["from"]))
        assert_that(content["to"], contains_inanyorder(*expected["to"]))

    def test_game_move_4(self):
        """
        Tests getting the moves for an EMPTY SQUARE
        """
        username = 'adam'  # From fixtures
        game_id = 1
        from_ = 'D4'
        url = '/chess/user/' + username + '/game/' + str(game_id) + '/move/' + from_
        c = Client()

        response = c.get(url)
        content = json.loads(response.content)
        expected = json.loads(u"""{
            "from": "D4",
            "to": []
        }""")

        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(content["from"], equal_to(expected["from"]))
        assert_that(content["to"], contains_inanyorder(*expected["to"]))

    def test_game_move_5(self):
        """
        Tests getting the moves for an ENEMY PIECE (that cannot move)
        """
        username = 'adam'  # From fixtures
        game_id = 1
        from_ = 'H1'
        url = '/chess/user/' + username + '/game/' + str(game_id) + '/move/' + from_
        c = Client()

        response = c.get(url)
        content = json.loads(response.content)
        expected = json.loads(u"""{
            "from": "H1",
            "to": []
        }""")

        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(content["from"], equal_to(expected["from"]))
        assert_that(content["to"], contains_inanyorder(*expected["to"]))

    def test_game_move_6(self):
        """
        Tests getting the moves for an ENEMY PIECE (that could move if it was their turn)
        """
        username = 'adam'  # From fixtures
        game_id = 1
        from_ = 'G7'
        url = '/chess/user/' + username + '/game/' + str(game_id) + '/move/' + from_
        c = Client()

        response = c.get(url)
        content = json.loads(response.content)
        expected = json.loads(u"""{
            "from": "G7",
            "to": []
        }""")

        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(content["from"], equal_to(expected["from"]))
        assert_that(content["to"], contains_inanyorder(*expected["to"]))

    def test_move_piece_1(self):
        """
        Tests moving a pawn one square.
        """
        username = 'adam'  # From fixtures
        game_id = 2
        from_ = 'A2'
        to_ = 'A3'
        url = '/chess/user/' + username + '/game/' + str(game_id) + '/move/' + from_ + '/' + to_
        c = Client()

        response = c.post(url)
        content = json.loads(response.content)
        # The comparision with the board is tricky ... as the represenation is in flux. We will ignore here and test
        # explicitly elsewhere, even if it is just manually until the 'spec' finalizes
        del content["board"]
        expected = json.loads(u"""{
                "id": 2,
                "active_player": "BLACK",
                "winner": "UNDECIDED",
                "black_player": 1000001,
                "white_player": 1000001,
                "board_code": "♖♘♗♕♔♗♘♖-_♙♙♙♙♙♙♙-♙_______-________-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜"
        }""")

        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(content, equal_to(expected))

    def test_move_piece_2(self):
        """
        Tests moving a pawn two squares.
        """
        username = 'adam'  # From fixtures
        game_id = 3
        from_ = 'A2'
        to_ = 'A4'
        url = '/chess/user/' + username + '/game/' + str(game_id) + '/move/' + from_ + '/' + to_
        c = Client()

        response = c.post(url)
        content = json.loads(response.content)
        # The comparision with the board is tricky ... as the represenation is in flux. We will ignore here and test
        # explicitly elsewhere, even if it is just manually until the 'spec' finalizes
        del content["board"]
        expected = json.loads(u"""{
                "id": 3,
                "active_player": "BLACK",
                "winner": "UNDECIDED",
                "black_player": 1000001,
                "white_player": 1000001,
                "board_code": "♖♘♗♕♔♗♘♖-_♙♙♙♙♙♙♙-________-♙_______-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜"
        }""")

        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(content, equal_to(expected))

    def test_move_piece_3(self):
        """
        Tests moving a knight
        """
        username = 'adam'  # From fixtures
        game_id = 4
        from_ = 'B1'
        to_ = 'C3'
        url = '/chess/user/' + username + '/game/' + str(game_id) + '/move/' + from_ + '/' + to_
        c = Client()

        response = c.post(url)
        content = json.loads(response.content)
        # The comparision with the board is tricky ... as the represenation is in flux. We will ignore here and test
        # explicitly elsewhere, even if it is just manually until the 'spec' finalizes
        del content["board"]
        expected = json.loads(u"""{
                "id": 4,
                "active_player": "BLACK",
                "winner": "UNDECIDED",
                "black_player": 1000001,
                "white_player": 1000001,
                "board_code": "♖_♗♕♔♗♘♖-♙♙♙♙♙♙♙♙-__♘_____-________-________-________-♟♟♟♟♟♟♟♟-♜♞♝♛♚♝♞♜"
        }""")

        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(content, equal_to(expected))

    def test_move_piece_4(self):
        """
        Tests trying to move a bishop (that CANNOT move)
        """
        username = 'adam'  # From fixtures
        game_id = 5
        from_ = 'C1'
        to_ = 'C3'
        url = '/chess/user/' + username + '/game/' + str(game_id) + '/move/' + from_ + '/' + to_
        c = Client()

        response = c.post(url)
        content = json.loads(response.content)

        assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))
        assert_that(content, equal_to(ChessResponses.MOVE_NOT_ALLOWED))

    def test_move_piece_5(self):
        """
        Tests moving an EMPTY square
        """
        username = 'adam'  # From fixtures
        game_id = 6
        from_ = 'F5'
        to_ = 'F6'
        url = '/chess/user/' + username + '/game/' + str(game_id) + '/move/' + from_ + '/' + to_
        c = Client()

        response = c.post(url)
        content = json.loads(response.content)

        assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))
        assert_that(content, equal_to(ChessResponses.SQUARE_IS_EMPTY))

    def test_move_piece_6(self):
        """
        Test moving an ENEMY PIECE (that cannot move)
        """
        username = 'adam'  # From fixtures
        game_id = 7
        from_ = 'H8'
        to_ = 'H6'
        url = '/chess/user/' + username + '/game/' + str(game_id) + '/move/' + from_ + '/' + to_
        c = Client()

        response = c.post(url)
        content = json.loads(response.content)

        assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))
        assert_that(content, equal_to(ChessResponses.CANNOT_MOVE_ENEMY_PIECE))

    def test_move_piece_7(self):
        """
        Test moving an ENEMY PIECE (that could move if it was their turn)
        """
        username = 'adam'  # From fixtures
        game_id = 8
        from_ = 'E7'
        to_ = 'E6'
        url = '/chess/user/' + username + '/game/' + str(game_id) + '/move/' + from_ + '/' + to_
        c = Client()

        response = c.post(url)
        content = json.loads(response.content)

        assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))
        assert_that(content, equal_to(ChessResponses.CANNOT_MOVE_ENEMY_PIECE))


class TestMoveList_1(TestCase):
    """
    Tests retrievign all moves for a player
    """
    fixtures = ['test_users.json', ]

    def setUp(self):
        """
        Create several new games to test against.

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

        username = 'adam'  # From fixtures
        url = '/chess/user/' + username + '/game/'
        c = Client()

        # Create 10 games for adam
        for i in range(0, 10):
            response = c.post(url)
            assert_that(response.status_code, is_(HTTP_200_OK))

    def test_white_player_moves(self):
        username = 'adam'  # From fixtures
        game_id = 1
        c = Client()

        from_list = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2']

        expected = []
        for from_ in from_list:
            url = '/chess/user/' + username + '/game/' + str(game_id) + '/move/' + from_
            response = c.get(url)
            assert_that(response.status_code, equal_to(HTTP_200_OK))
            content = json.loads(response.content)
            expected.append(content)

        url = '/chess/user/' + username + '/game/' + str(game_id) + '/move/'
        response = c.get(url)
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        content = json.loads(response.content)

        assert_that(content, contains_inanyorder(*expected))


class TestPromotePawn_1(TestCase):
    """
    Tests the promotion of pawns.
    """
    fixtures = ['test_users.json', ]

    def setUp(self):
        """
        Create several new games to test against.

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

        username = 'adam'  # From fixtures
        url = '/chess/user/' + username + '/game/'
        c = Client()

        # Create 10 games for adam
        for i in range(0, 10):
            response = c.post(url)
            assert_that(response.status_code, is_(HTTP_200_OK))

    def test_promote_black_and_white_pawns(self):
        """
        Tests the promotion of black and white pawns

        It is a mammoth test, but .. this needs to be tested

        * Also tests trying to move when not allowed because the other player hasn't promoted their pawn
        * Tests promotion to BlackRook and WhiteQueen
        """
        username = 'adam'  # From fixtures
        game_id = 1
        c = Client()

        white_move_list = [
            {
                "from": "A2",
                "to": "A4",
            },
            {
                "from": "A4",
                "to": "A5",
            },
            {
                "from": "A5",
                "to": "A6",
            },
            {
                "from": "A6",
                "to": "B7",
            },
            {
                "from": "B7",
                "to": "A8",
            },
        ]

        black_move_list = [
            {
                "from": "H7",
                "to": "H5"
            },
            {
                "from": "H5",
                "to": "H4"
            },
            {
                "from": "H4",
                "to": "H3"
            },
            {
                "from": "H3",
                "to": "G2"
            },
            {
                "from": "G2",
                "to": "H1"
            }
        ]

        # Move the black and white pawns towards the end
        ib = 0
        for move in white_move_list:
            url = '/chess/user/' + username + '/game/' + str(game_id) + '/move/' + move["from"] + '/' + move["to"]
            response = c.post(url)
            assert_that(response.status_code, equal_to(HTTP_200_OK))

            move_2 = black_move_list[ib]
            url_2 = '/chess/user/' + username + '/game/' + str(game_id) + '/move/' + \
                move_2["from"] + '/' + move_2["to"]
            response_2 = c.post(url_2)

            # The final black move should fail because white needs to promote their piece first, we inc ib before so
            # this check is correct
            ib += 1
            if ib < len(black_move_list):
                assert_that(response.status_code, equal_to(HTTP_200_OK))
            else:
                assert_that(response_2.status_code, equal_to(HTTP_400_BAD_REQUEST))
                content = json.loads(response_2.content)
                expected = ChessResponses.PAWN_MUST_BE_PROMOTED
                assert_that(content, equal_to(expected))

        # TODO:remove hardcode?
        promote_url = '/chess/user/' + username + '/game/' + str(game_id) + '/promote/' + 'WhiteQueen'

        response = c.post(promote_url)

        # The comparision with the board is tricky ... as the represenation is in flux. We will ignore here and test
        # explicitly elsewhere, even if it is just manually until the 'spec' finalizes
        content = json.loads(response.content)
        del content["board"]

        expected = json.loads(u"""{
                "id": 1,
                "active_player": "BLACK",
                "winner": "UNDECIDED",
                "black_player": 1000001,
                "white_player": 1000001,
                "board_code": "♖♘♗♕♔♗♘♖-_♙♙♙♙♙♟♙-________-________-________-________-♟_♟♟♟♟♟_-♕♞♝♛♚♝♞♜"
        }""")

        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(content, equal_to(expected))

        # now move the black pawn
        last_move = black_move_list[-1]
        move_url = '/chess/user/' + username + '/game/' + str(game_id) + '/move/' + last_move["from"] + '/' \
            + last_move["to"]

        response = c.post(move_url)

        # The comparision with the board is tricky ... as the represenation is in flux. We will ignore here and test
        # explicitly elsewhere, even if it is just manually until the 'spec' finalizes
        content = json.loads(response.content)
        del content["board"]

        expected = json.loads(u"""{
                "id": 1,
                "active_player": "BLACK",
                "winner": "UNDECIDED",
                "black_player": 1000001,
                "white_player": 1000001,
                "board_code": "♖♘♗♕♔♗♘♟-_♙♙♙♙♙_♙-________-________-________-________-♟_♟♟♟♟♟_-♕♞♝♛♚♝♞♜"
        }""")

        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(content, equal_to(expected))

        # now promote the black pawn, remove hardcode? - Nah, it's fine
        black_promote_url = '/chess/user/' + username + '/game/' + str(game_id) + '/promote/' + 'BlackRook'

        response = c.post(black_promote_url)

        # The comparision with the board is tricky ... as the represenation is in flux. We will ignore here and test
        # explicitly elsewhere, even if it is just manually until the 'spec' finalizes
        content = json.loads(response.content)
        del content["board"]
        expected = json.loads(u"""{
                "id": 1,
                "active_player": "WHITE",
                "winner": "UNDECIDED",
                "black_player": 1000001,
                "white_player": 1000001,
                "board_code": "♖♘♗♕♔♗♘♜-_♙♙♙♙♙_♙-________-________-________-________-♟_♟♟♟♟♟_-♕♞♝♛♚♝♞♜"
        }""")

        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(content, equal_to(expected))

    def test_get_white_promatable_pieces(self):
        """
        Reteive the pieces a white player can promote their pawns to
        """
        username = 'adam'  # From fixtures
        game_id = 2
        c = Client()
        url = '/chess/user/' + username + '/game/' + str(game_id) + '/promote/'
        response = c.get(url)
        content = json.loads(response.content)
        expected = json.loads("""
            [
                "WhiteBishop",
                "WhiteKnight",
                "WhiteQueen",
                "WhiteRook"
            ]
        """)

        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(content, expected)

    def test_get_black_promatable_pieces(self):
        """
        Reteive the pieces a black player can promote their pawns to
        """
        username = 'adam'  # From fixtures
        game_id = 3
        c = Client()
        from_ = 'A2'
        to_ = 'A3'

        # Move a white piece to switch turn.
        # This is necessary as in this test adam is playing as black and white
        url = '/chess/user/' + username + '/game/' + str(game_id) + '/move/' + from_ + '/' + to_
        response = c.post(url)
        assert_that(response.status_code, equal_to(HTTP_200_OK))

        url = '/chess/user/' + username + '/game/' + str(game_id) + '/promote/'
        response = c.get(url)
        content = json.loads(response.content)
        expected = json.loads("""
            [
                "BlackBishop",
                "BlackKnight",
                "BlackQueen",
                "BlackRook"
            ]
        """)

        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(content, expected)

    def test_promatable_pieces_3(self):
        """
        Reteive the pieces a black player can promote their pawns to
        """
        username = 'jack'  # Does not exist
        game_id = 2
        c = Client()

        url = '/chess/user/' + username + '/game/' + str(game_id) + '/promote/'
        response = c.get(url)
        content = json.loads(response.content)
        expected = ChessResponses.USER_IS_NOT_CURRENT_PLAYER

        assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))
        assert_that(content, expected)

    def test_promte_piece_when_not_allowed(self):
        username = 'adam'  # From fixtures
        game_id = 4
        c = Client()

        promote_url = '/chess/user/' + username + '/game/' + str(game_id) + '/promote/' + 'BlackRook'

        response = c.post(promote_url)
        expected = ChessResponses.NO_PAWN_TO_PROMOTE

        assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))
        assert_that(json.loads(response.content), equal_to(expected))


class TestChallenge(TestCase):

    def setUp(self):
        pass

    def test_challenge_player(self):
        """
        Bob challenges Adam, then lists challenges
        """
        pass

    def test_challenge_player_2(self):
        """
        Bob challenges Adam, Adam accepts
        """
        pass

    def test_challenge_player_3(self):
        """
        Bob challenges Adam, then bob cancels
        """
        pass

    def test_challenge_player_4(self):
        """
        Bob challenges a player that doesn't exist
        """
        pass

    def test_challenge_player_5(self):
        """
        Dave and Charles challenge bob. Bob challenges Adam. Outstanding challenges are viewed
        """
        pass

    def test_challenge_player_6(self):
        """
        Dave and Charles challenge bob. Bob challenges Adam. Adam accepts
        """
        pass

    def test_challenge_player_7(self):
        """
        Dave and Charles challenge bob. Bob challenges Adam. Bob accepts Dave's challenge
        """
        pass
