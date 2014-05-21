from rest_framework import serializers
from chess.models import GameModel


class GameModelSerializer(serializers.ModelSerializer):
    active_player = serializers.CharField(source='_active_player', read_only=True)
    winner = serializers.CharField(source='_winner', read_only=True)
    board_code = serializers.CharField(source='_board', read_only=True)
    # black_player = serializers.CharField(source='black_player', read_only=True)
    # white_player = serializers.CharField(source='white_player', read_only=True)

    board = serializers.SerializerMethodField('board_repr')
    # promoteable_pieces = serializers.SerializerMethodField('promoteable_pieces_repr')

    def board_repr(self, obj):
        return obj.board.display_json()

    # def promoteable_pieces_repr(self, obj):
    #     return obj.board.promoteable_pieces()

    class Meta:
        model = GameModel

        fields = (
            'id',
            'active_player',
            'winner',
            'black_player',
            'white_player',
            'board',
            'board_code',
            # 'promoteable_pieces'
        )
