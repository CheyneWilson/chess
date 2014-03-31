from persistence import Persistence
from hamcrest import is_, assert_that, contains_inanyorder
from sqlite3 import ProgrammingError
import os
import unittest


class TestEmptyDatabase(unittest.TestCase):
    test_db = None

    @classmethod
    def setUpClass(cls):
        cls.test_db = 'unittest_1.sqlite'

        # Remove previous unit test database
        # This is not done in the teardown because it makes debugging easier
        if os.path.isfile(cls.test_db):
            os.remove(cls.test_db)

    def setUp(self):
        self.persitence = Persistence(TestEmptyDatabase.test_db)

    def test_list_all_games_empty(self):
        """Check that no games are returned - ensures we are starting unit tests a fresh.

        This test should return an empty list and no errors should be raised."""
        all_games = self.persitence.list_games()
        assert_that(all_games, is_([]))

    def test_list_player_games_empty(self):
        """Check that no games are returned - ensures we are starting unit tests a fresh.

        This test should return an empty list and no errors should be raised."""
        player_id = 76  # This player does not exist
        all_games = self.persitence.list_games(player_id)
        assert_that(all_games, is_([]))


class TestPersistenceFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_db = 'unittest_2.sqlite'

        cls.game_1 = {
            u"id": None,
            u"white_player_id": 1,
            u"board": """{"test_board":"foo 31"}""",  # This is nothing like the structure stored
            u"black_player_id": 2
        }

        # Remove previous unit test database
        if os.path.isfile(cls.test_db):
            os.remove(cls.test_db)

    def setUp(self):
        self.persitence = Persistence(TestPersistenceFunctions.test_db)

    def test_010_save_new_game(self):
        """Save a game_id and then assert that it is the same as saved


        """
        game = TestPersistenceFunctions.game_1

        # Save game 1 and keep game_id_id for future tests
        game_id = self.persitence.save_new_game(game[u"white_player_id"], game[u"black_player_id"], game[u"board"])

        # Retrieve game from storage
        returned_game = self.persitence.load_game(game_id)

        # Asset it matches what we persisted
        assert_that(returned_game[u"black_player_id"], is_(game[u"black_player_id"]))
        assert_that(returned_game[u"white_player_id"], is_(game[u"white_player_id"]))
        assert_that(returned_game[u"winner"], is_(None))  # Default
        assert_that(returned_game[u"board"], is_(game[u"board"]))

        # Persist this id to be reused..?
        game['id'] = game_id

    def test_020_update_game(self):
        """Update the game moves

        This depends on test_save_new_game and it's execution is hacky
        """
        updated_game = {
            u"id": TestPersistenceFunctions.game_1[u"id"],
            u"board": u"""{"test_board":"foo 32"}""",  # This is nothing like the structure stored
            u"winner": u"black"
        }

        self.persitence.update_game(updated_game[u"id"], updated_game[u"board"], updated_game[u"winner"])

        # Retrieve game from storage
        returned_game = self.persitence.load_game(updated_game[u"id"])

        # Asset it matches what we persisted
        assert_that(returned_game[u"id"], is_(updated_game[u"id"]))
        assert_that(returned_game[u"board"], is_(updated_game[u"board"]))
        assert_that(returned_game[u"winner"], is_(updated_game[u"winner"]))
        # And that other properties are unchanged
        game_1_a = TestPersistenceFunctions.game_1
        assert_that(returned_game[u"black_player_id"], is_(game_1_a[u"black_player_id"]))
        assert_that(returned_game[u"white_player_id"], is_(game_1_a[u"white_player_id"]))

        TestPersistenceFunctions.game_1_b = returned_game

    def test_030_update_game_wrong_id(self):
        """Tests updating a game that does not exist

        Should throw a ProgrammingError
        """

        bad_game_id = 123  # Does not exist
        winner = None
        board = u"""{"test_board":"foo 32"}"""  # This is nothing like the structure stored

        with self.assertRaises(ProgrammingError):
            self.persitence.update_game(bad_game_id, board, winner)

    def test_040_list_games_1(self):
        """Tests listing games. Depends on test_010_save_new_game"""
        id = 234
        games = self.persitence.list_games(id)  # This game id does not exist
        assert_that(games, is_([]))

    def test_041_list_games_2(self):
        """Tests listing games. Depends on test_010_save_new_game"""
        id = 1
        games = self.persitence.list_games(id)

        assert_that(games, contains_inanyorder(TestPersistenceFunctions.game_1_b))

if __name__ == '__main__':
        unittest.main()
