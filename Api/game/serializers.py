from rest_framework import serializers

class GameInitInput(serializers.Serializer):
    number = serializers.IntegerField(
        required=True,
        help_text="Number of players"
    )

class GameInitResult(serializers.Serializer):
    created = serializers.BooleanField(
        required=True,
        help_text="Created"
    )
    error = serializers.CharField(
        required=False,
        help_text="error"
    )

class GamePlayer(serializers.Serializer):
    id = serializers.CharField(
        required=True,
        help_text="Player id"
    )
    coords = serializers.ListField(
        required=True,
        help_text="Player coords",
        child=serializers.IntegerField()
    )

class GamePlayers(serializers.Serializer):
    players = GamePlayer(many=True)

class Player(serializers.Serializer):
    id = serializers.CharField(
        required=True,
        help_text="Player id"
    )
    coords = serializers.ListField(
        required=True,
        help_text="Player coords",
        child=serializers.IntegerField()
    )
    tasks = serializers.ListField(
        required=False
    )

class TaskInput(serializers.Serializer):
    name = serializers.CharField(
        required=True,
        help_text="Task name"
    )
    expire = serializers.IntegerField(
        required=True,
        help_text="Task expire"
    )
    delete = serializers.BooleanField(
        required=False,
        help_text="delete task"
    )

class TaskInputResult(serializers.Serializer):
    modified = serializers.BooleanField(
        required=True,
        help_text="Created"
    )
    error = serializers.CharField(
        required=False,
        help_text="error"
    )
