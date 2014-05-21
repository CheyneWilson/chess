from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.http import HttpResponse
from django.template import RequestContext, loader
# from django.views.decorators.csrf import csrf_exempt

from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework.permissions import AllowAny  # , IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# from django.contrib.auth.forms import AuthenticationForm

from chess.models import GameModel, MoveModel, ChallengeModel

from chess.serializers import GameModelSerializer
from chess.board import IllegalMoveException, WrongPlayerException, InvlaidPieceException, \
    EmptySquareException, PromotePieceException, IllegalPromotionException

from chess.color import Color
import json


class ChessResponses(object):
    USER_IS_NOT_PLAYER = {"error": "User is not a player of this game"}
    USER_IS_NOT_CURRENT_PLAYER = {"error": "User is not the current player of this game"}  # Change to you?
    USER_DOES_NOT_EXIST = {"error": "User does not exist"}
    OPPONENT_DOES_NOT_EXIST = {"error": "Opponent does not exist"}
    GAME_DOES_NOT_EXIST = {"error": "Game does not exist"}
    MOVE_NOT_ALLOWED = {"error": "Move not allowed"}
    PIECE_IS_NOT_VALID = {"error": "Piece is not valid"}
    SQUARE_IS_EMPTY = {"error": "Square is empty"}
    CANNOT_MOVE_ENEMY_PIECE = {"error": "Cannot move enemy piece"}
    PAWN_MUST_BE_PROMOTED = {"error": "Cannot move piece, opponent must promote their pawn first"}
    NO_PAWN_TO_PROMOTE = {"error": "Cannot promote pawwn, there is no pawn able to be promoted"}
    USER_CANNOT_CHALLENGE_THEMSELF = {"errpr": "A player cannot challenge themself"}
    NO_CHALLENGE_EXISTS = {"error": "Cannot accept challenge with player, it does not exist"}
    CHALLENGE_ALREADY_EXISTS = {"error": "Challenge already exists, accept their challenge instead"}


class LoginResponses(object):
    LOGIN_SUCCESS = {"message": "Login success"}
    LOGOUT_SUCCESS = {"message": "Logout success"}
    LOGIN_FAILED = {"error": "Login failed"}


# Create your views here.
def index(request):
    template = loader.get_template(u'chess/index.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))


class LoginLogout(APIView):
    """
    Allows a user to login and logout
    """
    permission_classes = (AllowAny,)

    def post(self, request, do_logout=False):
        if do_logout:
            logout(request)
            return Response(LoginResponses.LOGOUT_SUCCESS)
        else:
            data = json.loads(request.body)
            # TOOD: Add default incase username or password is missing
            username = data.get("username", None)  # data["username"]
            password = data.get("password", None)  # data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return Response(LoginResponses.LOGIN_SUCCESS)

        return Response(LoginResponses.LOGIN_FAILED, HTTP_401_UNAUTHORIZED)


# @csrf_exempt
class AuthView(APIView):
    """
    This text is the description for this API
    username -- A first parameter
    password -- A second parameter
    """
    permission_classes = (AllowAny,)
    # authentication_classes

    def post(self, request, *args, **kwargs):

        # data = JSONParser().parse(request)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # username = request.POST['username']
        # password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                params = {"login": "Success"}
                return Response()
            else:
                # Return a 'disabled account' error message
                params = {
                    "login": 'Disabled'
                }
                return Response(params)
        else:
            # Return an 'invalid login' error message.
            params = {
                "login": request.POST  # "Failed"
            }
            return Response(params)

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response({})


class GameCreateOrList(APIView):
    """This class provides methods to create new games or list those created by a user."""
    permission_classes = (AllowAny, )

    def get(self, request, username, format=None):
        """
        Retrieve a list of all Games for the user

        username -- The username of the player to create the game for

        Raises -- An HTTP 400 error if the user does not exist
        """

        game_list = load_game_or_error(username)
        if isinstance(game_list, Response):
            return game_list

        serializer = GameModelSerializer(game_list, many=True)
        return Response(serializer.data)

    def post(self, request, username, format=None):
        """
        Create a new game

        username -- The username of the player to create the game for

        Raises -- An HTTP 400 error if the user does not exist
        """
        try:
            player = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(ChessResponses.USER_DOES_NOT_EXIST, status=HTTP_400_BAD_REQUEST)

        game = GameModel.objects.create(white_player=player, black_player=player)
        # game.black_player = player
        # game.white_player = player
        # game.active_player.color = Color.WHITE
        # game.board = Board()
        # game.save()

        serializer = GameModelSerializer(game)
        return Response(serializer.data)


class GameDetail(APIView):
    """Provides a method to retrieve a specific game."""
    permission_classes = (AllowAny,)

    def get(self, request, username, game_id, format=None):
        """
        Retrieve a game.

        username -- The username of the player to create the game for
        game_id  -- The game to load
        Raises -- An HTTP 400 error if the user does not exist or the game does not exist
        Returns -- The game information
        """

        game = load_game_or_error(username, game_id)
        if isinstance(game, Response):
            return game
        else:
            serializer = GameModelSerializer(game)
            return Response(serializer.data)


def load_game_or_error(username, game_id=None):
    """
    Retrieve a game.

    username -- The username of the player to create the game for
    game_id  -- The game to load

    Returns -- The game information or a Response with an HTTP status code explaining the problem.

    Usage -- TODO:

    """
    try:
        game_list = GameModel.objects.filter(
            Q(black_player__username=username) | Q(white_player__username=username)
        ).select_related('color', 'winner')  # TODO: Remove?
        if game_id is None:
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                return Response(ChessResponses.USER_DOES_NOT_EXIST, status=HTTP_400_BAD_REQUEST)
            else:
                return game_list
        else:
            game = game_list.get(id=game_id)
    except GameModel.DoesNotExist:
        # Determine why the error happened. This doesn't have to be as performant because it is not the common case
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(ChessResponses.USER_DOES_NOT_EXIST, status=HTTP_400_BAD_REQUEST)
        else:
            try:
                GameModel.objects.get(id=game_id)
            except GameModel.DoesNotExist:
                return Response(ChessResponses.GAME_DOES_NOT_EXIST, status=HTTP_400_BAD_REQUEST)
            else:
                return Response(ChessResponses.USER_IS_NOT_PLAYER, status=HTTP_400_BAD_REQUEST)

    return game


def username_color(game, username):
    if game.black_player.username == username:
        return Color.BLACK
    elif game.white_player.username == username:
        return Color.WHITE
    else:
        return None


def serilize_moves_and_attacks(from_, moves, attacks):
    moves_and_attacks = []

    # Format response
    for x in moves:
        moves_and_attacks.append({
            "square": x,
            "capture": False
        })

    for x in attacks:
        moves_and_attacks.append({
            "square": x,
            "capture": True
        })
    return {
        "from": from_,
        "to": moves_and_attacks
    }


class MoveList(APIView):
    """
    This view handles the moves that a player can make
    """
    permission_classes = (AllowAny,)

    def get(self, request, username, game_id):
        """
        Returns all the possible moves for all of the specified player's pieces.

        username -- The username of the player
        game_id  -- The game to list the possible moves for

        If it is not the players turn, then the moves will be an empty list.
        """
        game = load_game_or_error(username, game_id)
        if isinstance(game, Response):
            return game
        else:
            response = []

            if game.active_player(username):
                board = game.board
                for square in board.player_piece_squares(board.current_player):
                    moves, attacks = board._get_moves_and_attacks(square)

                    moves_and_attacks = serilize_moves_and_attacks(square, moves, attacks)
                    response.append(moves_and_attacks)

            return Response(response)


class MoveDetail(APIView):
    """
    This view handles the moves a players chess piece.
    """
    permission_classes = (AllowAny,)

    def get(self, request, username, game_id, from_loc, format=None):
        """
        Retrieves all of the possible moves from a given location

        username -- The username of the player
        game_id  -- The game to list the possible moves for
        from_loc    -- The square to move the piece from, e.g 'A3'

        Raises -- An HTTP 400 error if the user does not exist or the game does not exist
        Returns -- The game information
        """

        game = load_game_or_error(username, game_id)
        if isinstance(game, Response):
            return game
        else:
            board = game.board
            if board._piece_owned_by_current_player(from_loc):
                moves, attacks = board._get_moves_and_attacks(from_loc)
            else:
                moves = set([])
                attacks = set([])
            moves_and_attacks = serilize_moves_and_attacks(from_loc, moves, attacks)
            return Response(moves_and_attacks)
            # else:
            #     return Response(ChessResponses.USER_IS_NOT_CURRENT_PLAYER, status=HTTP_400_BAD_REQUEST)


class MovePiece(APIView):
    """
    Handles the moving of pieces
    """
    permission_classes = (AllowAny,)

    def post(self, request, username, game_id, from_loc, to_loc, format=None):
        u"""Move a piece from one square to another.

        username -- The username of the player
        game_id  -- The game to list the possible moves for
        from_loc    -- The square to move the piece from, e.g 'A3'
        to_loc      -- The square to move the piece to,  e.g 'A5'

        If it is not the players turn, then the game will not be updated
        """

        game = load_game_or_error(username, game_id)
        if isinstance(game, Response):
            return game
        elif game.active_player(username):
            board = game.board
        else:
            return Response(ChessResponses.USER_IS_NOT_CURRENT_PLAYER, status=HTTP_400_BAD_REQUEST)

        try:
            board.move_piece(from_loc, to_loc)
            game.board = board

        except IllegalMoveException:
            return Response(ChessResponses.MOVE_NOT_ALLOWED, HTTP_400_BAD_REQUEST)
        except EmptySquareException:
            return Response(ChessResponses.SQUARE_IS_EMPTY, HTTP_400_BAD_REQUEST)
        except WrongPlayerException:
            return Response(ChessResponses.CANNOT_MOVE_ENEMY_PIECE, HTTP_400_BAD_REQUEST)
        except PromotePieceException:
            return Response(ChessResponses.PAWN_MUST_BE_PROMOTED, HTTP_400_BAD_REQUEST)

        serializer = GameModelSerializer(game)
        return Response(serializer.data)


class PromotablePieces(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, username, game_id, pk=None):
        """Returns all the pieces that the pawn can be promoted to

        username -- The username of the player
        game_id  -- The game to list the possible moves for

        The color of the pieces is the same as that of the player with the username provided.
        """

        game = load_game_or_error(username, game_id)
        if isinstance(game, Response):
            return game
        else:
            board = game.board
            player_color = game.player_color(username)
            assert(player_color is not None)  # Guartenteed by load_game_or_error succeeding

            pieces = board.promotable_pieces(player_color)
            piece_names = [piece.__name__ for piece in pieces]

            return Response(piece_names)


class PromotePiece(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, username, game_id, piece, format=None):
        u"""Move a piece from one square to another.

        username -- The username of the player
        game_id  -- The game to list the possible moves for
        piece    -- The piece to promote the pawn to

        If it is not the players turn, then the game will not be updated
        """
        game = load_game_or_error(username, game_id)
        if isinstance(game, Response):
            return game
        elif game.active_player(username):  # The common case
            board = game.board
            try:
                board.promote_pawn(piece)  # TODO: The board method needs to be rewritten
                game.board = board
            except InvlaidPieceException:
                return Response(ChessResponses.PIECE_IS_NOT_VALID, HTTP_400_BAD_REQUEST)
            except IllegalPromotionException:
                return Response(ChessResponses.NO_PAWN_TO_PROMOTE, HTTP_400_BAD_REQUEST)

            serializer = GameModelSerializer(game)
            return Response(serializer.data)
        else:
            return Response(ChessResponses.USER_IS_NOT_CURRENT_PLAYER, status=HTTP_400_BAD_REQUEST)


class PreviousMoves(APIView):
    """
    Lists all of the previous moves for a game
    """
    permission_classes = (AllowAny,)

    def get(self, request, username, game_id):
        moves = MoveModel.objects.filter(game_id=game_id).all()

        resp = []
        for m in moves:
            if m.capture:
                operator = "x"
            else:
                operator = " "
                resp.append(m.from_loc + operator + m.to_loc)

        return Response(resp)


class ChallengeList(APIView):
    """
    List all of the players challenging the player
    """
    permission_classes = (AllowAny,)

    def get(self, request, username):
        """
        List all of the players challenging the player, and players they are challenging.
        """
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(ChessResponses.USER_DOES_NOT_EXIST, HTTP_400_BAD_REQUEST)

        incoming_challenges = ChallengeModel.objects.filter(challengee__username=username)
        challengers = [c.challenger.username for c in incoming_challenges]

        outgoing_challenges = ChallengeModel.objects.filter(challenger__username=username)
        challengees = [c.challengee.username for c in outgoing_challenges]

        resp = {
            "challengers": challengers,
            "challengees": challengees
        }
        return Response(resp)


class Challenge(APIView):
    """
    Challenge players to a game or accept a challenge a challenge from other players
    """
    permission_classes = (AllowAny,)

    def put(self, request, username, opponent):
        """
        Challenge a player to a game.

        A player cannot challenge themselves
        """
        if username != opponent:
            # First check if they have challenged us
            try:
                ChallengeModel.objects.get(challenger__username=opponent, challengee__username=username)
            except ChallengeModel.DoesNotExist:
                pass
            else:
                Response(ChessResponses.CHALLENGE_ALREADY_EXISTS)

            try:
                challenger = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response(ChessResponses.USER_DOES_NOT_EXIST)

            try:
                challengee = User.objects.get(username=opponent)
            except User.DoesNotExist:
                return Response(ChessResponses.OPPONENT_DOES_NOT_EXIST)

            try:
                ChallengeModel.objects.create(challenger=challenger, challengee=challengee)
            except IntegrityError:
                # Challenge already exists
                pass

            resp = {
                "message": "Challenge issued to opponent"
            }

            return Response(resp)
        else:
            return Response(ChessResponses.USER_CANNOT_CHALLENGE_THEMSELF)

    def delete(self, request, username, opponent):
        """
        Cancel a challenge
        """
        try:
            ChallengeModel.objects.filter(challenger__username=username, challengee__username=opponent).delete()
            ChallengeModel.objects.filter(challenger__username=opponent, challengee__username=username).delete()
        except IntegrityError:
            # Challenge already exists, do nothing
            pass
        else:
            resp = {
                "message": "Challenge deleted."
            }
            return Response(resp)

    def post(self, request, username, opponent):
        """
        Accept a challenge
        """
        try:
            challenge = ChallengeModel.objects.get(challenger__username=username, challengee__username=opponent)
        except ChallengeModel.DoesNotExist:
            return Response(ChessResponses.NO_CHALLENGE_EXISTS, HTTP_400_BAD_REQUEST)
        else:
            with transaction.atomic():
                challenge.delete()
                GameModel.objects.create_game(username, opponent)

                # TODO: need to place a message to alert the other player that the game has started!
            return Response("TODO:")


class MatchMake(APIView):
    pass


class ActivePlayers(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, username):
        """
        Return a list of active players excluding the current_player
        """
        # TODO: Currently returns all players
        users = User.objects.filter(~Q(username=username)).all()
        resp = [u.username for u in users]

        return Response(resp)

    def post(self, request, username):
        """
        Add the player to the list of active players.

        The active players is periodically reset, with inactive players delete
        """
        pass


class AiAgents(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, username):
        """
        Return a list of agents that a player can play against
        """
        resp = ['Not Implemented']
        return Response(resp)
