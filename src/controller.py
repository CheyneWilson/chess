# -*- coding: UTF-8 -*-

# import uuid
import json
import pickle

from board import Board, Square
from board import IllegalMoveException
from persistence import Persistence

from flask import Flask

app = Flask(__name__)

db = 'games.sqlite'


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/new/<type>")  # , methods=['POST']
def new(type):
    """Create a new game.

       type -- The type of game (PvP, or type of AI.)
    """

    white_player_id = 1  # str(uuid.uuid1())
    black_player_id = 2  # str(uuid.uuid1())

    board = Board()

    persistence = Persistence(db)

    game_id = persistence.save_new_game(white_player_id, black_player_id, pickle.dumps(board))

    resp = {
        u'board': board.display_json_2(),
        u'turn': board.turns_taken,
        u'player': board.current_player,
        u'game_id': game_id,
        u'white_player': white_player_id,
        u'black_player': black_player_id,
        u'moves': board.display_previous_moves(),
        u'winner': board.winner,
        u'status_code': u'NEW_GAME',
        u'status_message': u'New Game Created.',
    }

    return json.dumps(resp)


@app.route("/game/<game_id>")
def game(game_id):
    """ Returns the chess board for the game specified"""
    persistence = Persistence(db)
    game = persistence.load_game(game_id)
    board = pickle.loads(game.board)

    resp = {
        u'board': board.display_json_2(),
        u'turn': board.turns_taken,
        u'player': board.current_player,
        u'game_id': game_id,
        u'white_player': game.white_player_id,
        u'black_player': game.black_player_id,
        u'winner': board.winner,
        u'moves': board.display_previous_moves()
    }

    return json.dumps(resp)


@app.route("/list")
def list_all_games():
    persistence = Persistence(db)
    game_summary = persistence.list_games(None)
    return json.dumps(game_summary)


@app.route("/list/<player_id>")
def list_games(player_id):
    persistence = Persistence(db)
    game_summary = persistence.list_games(player_id)
    return json.dumps(game_summary)


@app.route("/game/<game_id>/from/<from_>/to/<to_>", methods=['POST', 'GET'])
def move_piece(game_id, from_, to_):
    """

    """
    persistence = Persistence(db)
    game = persistence.load_game(game_id)
    if (game is not None):
        try:
            board = pickle.loads(game.board)
            from_square = Square.fromName(from_)
            to_square = Square.fromName(to_)

            board.move_piece(from_square, to_square)
            winner = None  # TODO: Implement this

            persistence.update_game(game_id, pickle.dumps(board), winner)

            resp = {
                u'board': board.display_json_2(),
                u'turn': board.turns_taken,
                u'player': board.current_player,
                u'game_id': game_id,
                u'white_player': game.white_player_id,
                u'black_player': game.black_player_id,
                u'winner': board.winner,
                u'moves': board.display_previous_moves(),
                u'status_code': u'UPDATED',
                # TODO: Update to used previous_move property and {piece}
                u'status_message': u'Piece moved from {from_} to {to_}'.format(from_=from_, to_=to_)
            }
        except IllegalMoveException:
            #TODO: Prepare an error message
            resp = {
                'board': None,
                'turn': None,
                'error': 'Invalid move'
            }
    else:
        #TODO: Prepare an error message
        resp = {
            'board': None,
            'turn': None,
            'error': 'Could not find chess game for current player.'
        }

    return json.dumps(resp)


def get_game(pid):
    pass

if __name__ == "__main__":
    app.run(debug=True)
    # new('a')
