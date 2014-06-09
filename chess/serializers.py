from rest_framework import serializers
from chess.models import GameModel


class GameModelSerializer(serializers.ModelSerializer):
    u"""


    """
    active_player = serializers.CharField(source=u'_active_player', read_only=True)
    winner = serializers.CharField(source=u'_winner', read_only=True)
    board_code = serializers.CharField(source=u'_board', read_only=True)

    board = serializers.SerializerMethodField(u'board_repr')
    promote_phase = serializers.SerializerMethodField(u'_is_promote_phase')

    # promoteable_pieces = serializers.SerializerMethodField('_promoteable_pieces')

    def board_repr(self, obj):
        u"""
        Returns a specialy formatted version of the board
        """
        return obj.board.display_json()

    def _is_promote_phase(self, obj):
        u"""
        Returns True if a pawn must be promoted, false otherwise
        """
        return obj.board.is_promote_phase()

    class Meta:
        model = GameModel

        fields = (
            u'id',
            u'active_player',
            u'winner',
            u'black_player',
            u'white_player',
            u'board',
            u'board_code',
            u'promote_phase',
            # u'promoteable_pieces'
        )
