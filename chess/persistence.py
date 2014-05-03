# -*- coding: utf-8 -*-
# This file handles the persistence layer of the chess program.
# It is repsonsible for managing the saving and loading all of the games.
import collections
import sqlite3


def namedtuple_factory(cursor, row):
    # Credit where credit due: http://peter-hoffmann.com/2010/python-sqlite-namedtuple-factory.html
    """
    Usage:
    con.row_factory = namedtuple_factory
    """
    fields = [col[0] for col in cursor.description]
    Row = collections.namedtuple("Row", fields)
    return Row(*row)


class Persistence(object):
    database_name = u'test.db'

    def __init__(self, database_name='test.db'):
        """Creates and initializes a new database if one is not present."""

        self.database_name = database_name

        # Estabish a connection to games.db, or create database if not present
        con = sqlite3.connect(self.database_name)

        with con:
            cursor = con.cursor()

            cursor.execute(u"""CREATE TABLE IF NOT EXISTS game
                (id integer primary key, white_player_id integer, black_player_id integer
                , winner integer, board) """)
            cursor.execute(u"""CREATE UNIQUE INDEX IF NOT EXISTS game_id on game (id)""")  # Necessary?
            cursor.execute(u"""CREATE INDEX IF NOT EXISTS game_white_player_id on game (white_player_id)""")
            cursor.execute(u"""CREATE INDEX IF NOT EXISTS game_black_player_id on game (black_player_id)""")

    def load_game(self, game_id):
        """Returns the game with the id specified

        If there is no matching game, raises a ???
        """

        con = sqlite3.connect(self.database_name)
        con.row_factory = namedtuple_factory  # sqlite3.Row

        with con:

            cursor = con.cursor()
            game_query = [u"""SELECT g.id, g.white_player_id, g.black_player_id, g.winner, g.board
                FROM game g
                WHERE g.id = ?
                """, (game_id, )]

            cursor.execute(*game_query)
            row = cursor.fetchone()

        return row

    def list_games(self, player_id=None):
        """Returns a list of all games for the player specified.

        If player_id is specified, then returns a list of all games for that player.
        If no games are found for that player_id returns an empty list.

        If player_id is None, returns all games ever played.

        Games are returned in order they were played, the first game is in position 0.
        """

        games = []
        con = sqlite3.connect(self.database_name)
        con.row_factory = sqlite3.Row

        with con:
            cursor = con.cursor()
            if player_id is not None:
                query = [u"""SELECT g.id, g.white_player_id, g.black_player_id, g.winner, g.board
                            FROM game g
                            WHERE g.white_player_id = ?
                            OR g.black_player_id = ?
                            ORDER BY g.id ASC
                            """, (player_id, player_id)]
            else:
                query = [u"""SELECT g.id, g.white_player_id, g.black_player_id, g.winner, g.board
                            FROM game g
                            GROUP BY g.id
                            ORDER BY g.id ASC
                            """]

            for row in cursor.execute(*query):
                g = {}
                for col in row.keys():
                    g[col] = row[col]
                games.append(g)

        return games

    def save_new_game(self, white_player_id, black_player_id, board):
        """Creates a new game record and returns the game id.

            Note, this does not save any moves (as new games have no moves)
            -- Returns  the game_id that can be used to later load or update the game
        """
        con = sqlite3.connect(self.database_name)

        with con:
            cursor = con.cursor()

            query = [u"""INSERT INTO game (white_player_id, black_player_id, board)
                         VALUES (?, ?, ?)""",
                     (white_player_id, black_player_id, board)]

            cursor.execute(*query)
            con.commit()

            [game_id] = cursor.execute(u"""SELECT last_insert_rowid()""").fetchone()

        return game_id

    def update_game(self, game_id, board, winner):
        """Add a move to a game

        If game.id is set, and matches existing record, then update existing record
        If game.id is set, but does not match an existing record, throws an exception

        """
        con = sqlite3.connect(self.database_name)

        query = [u"""UPDATE game
                     SET winner = ?
                        , board = ?
                     WHERE id = ?""",
                 (winner, board, game_id)]

        with con:
            cursor = con.cursor()
            cursor.execute(*query)
            if con.total_changes == 1:
                con.commit()
            elif con.total_changes == 0:
                raise sqlite3.ProgrammingError(u"No game with id {id} found. No changes committed.".format(id=game_id))
            assert(con.total_changes < 2)  # Prevented due to unique constraint on id
