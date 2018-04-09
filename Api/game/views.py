import redis
import ujson
import time

from django.shortcuts import render
from django.conf import settings

from rest_framework import viewsets
from rest_framework import views
from rest_framework import exceptions
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.decorators import api_view, renderer_classes, detail_route, list_route
from rest_framework import response, schemas

from . import utils

from . import serializers

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)

class GameView(viewsets.ViewSet):
    get_serializer = serializers.GameInitInput
    @list_route(methods=["post"])
    def init(self, request):
        """
        description: API call to init new game field.

        Number - number of players
        """
        result = {"created": True}
        number = request.data.get("number")
        r.flushall()
        try:
            players_coords, players_dict = utils.generate_players(number)
            r.set("players", ujson.dumps(players_coords))
        except ValueError as e:
            result = {"created": False,
                      "error": str(e).split("\n")[0]}

        for number, player in players_dict.items():
            coords = utils.get_coords(number)
            neighbours = utils.get_neighbours(players_dict, coords)
            player_dict = {"id": player,
                           "number": number,
                           "coords": coords,
                           "neighbours": neighbours}
            r.set(utils.get_stored_player_id(player), ujson.dumps(player_dict))

        serializer = serializers.GameInitResult(result)
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
        raw_data = r.get(utils.get_stored_player_id(pk))
        if raw_data:
            player = ujson.loads(r.get(utils.get_stored_player_id(pk)))
            tasks = list()            
            for n in player.get("neighbours"):
                tasks_list = r.keys(utils.get_stored_task_id(n))
                _tasks = ["Task: {}, timeleft: {}".format(t.split(":")[-2], r.ttl(t)) for t in tasks_list]
                tasks.append({"player_id": n, "tasks": _tasks})
            player["tasks"] = tasks                
        else:
            player = None
        serializer = serializers.Player(player)
        return Response(serializer.data, status=200)

    get_serializer = serializers.TaskInput
    @detail_route(methods=["post"])
    def task(self, request, pk):
        """
        description: API call to set task for player.

        name - name of task

        expire - expire of task (in seconds)

        """
        name = request.data.get("name")
        expire = request.data.get("expire")
        delete = request.data.get("delete")
        if delete:
            to_del = r.keys(utils.get_stored_task_id(pk, name=name))
            for k in to_del:
                r.delete(k)
            return Response(serializers.TaskInputResult({"modified": True}).data, status=200)

        raw_data = r.get(utils.get_stored_player_id(pk))
        if raw_data is None:
            result = {"modified": False,
                      "error": "No user with this id"}
        else:
            if len(r.keys(utils.get_stored_task_id(pk))) >= settings.MAX_TASKS:
                result = {"modified": False,
                          "error": "Max tasks limit"}
            else:
                r.set(utils.get_stored_task_id(pk, time.time(), name), name, ex=expire)
                result = {"modified": True}

        serializer = serializers.TaskInputResult(result)
        return Response(serializer.data, status=200)
