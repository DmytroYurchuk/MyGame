from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

from . import utils

from . import serializers

class GameView(viewsets.ViewSet):
    get_serializer = serializers.GameInitInput
    @list_route(methods=["post"])
    def init(self, request):
        """
        description: API call to init new game field.

        Number - number of players
        """
        number = request.data.get("number")
        utils.clear_base()
        serializer = serializers.GameInitResult(utils.set_players(number))
        return Response(serializer.data, status=200)

    @list_route()
    def players(self, request):
        """
        description: API call to get all players coords.

        """
        players = ujson.loads(r.get("players"))
        serializer = serializers.GamePlayers({"players": players})
        return Response(serializer.data, status=200)


class PlayerView(viewsets.ViewSet):
    @detail_route()
    def info(self, request, pk):
        """
        description: API call to get one player info.

        """
        serializer = serializers.Player(utils.get_player(pk))
        return Response(serializer.data, status=200)

    get_serializer = serializers.TaskInput
    @detail_route(methods=["post"])
    def task(self, request, pk):
        """
        description: API call to set task for player.

        name - name of task

        expire - expire of task (in seconds)

        delete - boolean. Delete this task yes or no?

        """
        name = request.data.get("name")
        expire = request.data.get("expire")
        delete = request.data.get("delete")
        
        serializer = serializers.TaskInputResult(utils.task(pk, name=name, expire=expire, delete=delete))
        return Response(serializer.data, status=200)
