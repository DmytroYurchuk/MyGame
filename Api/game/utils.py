import redis
import random
import ujson
import time

from pymongo import MongoClient
from django.conf import settings

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)
m_client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)

def generate_players(number):
	max_square = settings.MAP_X * settings.MAP_Y
	players = random.sample(range(max_square), number)
	return [{"id": i, "coords": get_coords(n)} for i, n in enumerate(players)], {p: i for i, p in enumerate(players)}

def get_coords(player_number):
	return [player_number % settings.MAP_X, player_number // settings.MAP_X]

def get_number(coords):
	return coords[0] + coords[1]*settings.MAP_X 

def get_view(coord):
	return set([(min(max(x, 0), settings.MAP_X), min(max(y, 0), settings.MAP_Y))
	    for x in range(coord[0] - int(settings.PLAYER_VIEW/2), coord[0] + int(settings.PLAYER_VIEW/2))
	    for y in range(coord[1] - int(settings.PLAYER_VIEW/2), coord[1] + int(settings.PLAYER_VIEW/2))])

def get_neighbours(players_dict, coords):
	player_view = get_view(coords)
	return [players_dict.get(get_number(v)) for v in player_view if players_dict.get(get_number(v)) is not None]

def get_stored_player_id(n):
	return "player:{}".format(n)

def get_stored_task_id(player_id, ts=None, name=None):
	if ts and name:
		return "task:{}:{}:{}".format(player_id, name, ts)
	if name:
		return "task:{}:{}:*".format(player_id, name)
	return "task:{}:*".format(player_id)

def clear_base():
    r.flushall()
    db = m_client.MyGame
    if "logs" in db.collection_names():
        db.logs.rename("logs_{}".format(time.time()))

def set_players(number):
    try:
        players_coords, players_dict = generate_players(number)
        r.set("players", ujson.dumps(players_coords))
    except ValueError as e:
        return {"created": False,
                "error": str(e).split("\n")[0]}

    for number, player in players_dict.items():
        coords = get_coords(number)
        neighbours = set(get_neighbours(players_dict, coords))
        player_dict = {"id": player,
                       "number": number,
                       "coords": coords,
                       "neighbours": neighbours}
        r.set(get_stored_player_id(player), ujson.dumps(player_dict))
    return {"created": True}

def get_players():
    return {"players": ujson.loads(r.get("players"))}

def get_player(p_id):
    raw_data = r.get(get_stored_player_id(p_id))
    if raw_data:
        player = ujson.loads(r.get(get_stored_player_id(p_id)))
        tasks = list()            
        for n in player.get("neighbours"):
            tasks_list = r.keys(get_stored_task_id(n))
            _tasks = ["Task: {}, timeleft: {}".format(t.split(":")[-2], r.ttl(t)) for t in tasks_list]
            tasks.append({"player_id": n, "tasks": _tasks})
        player["tasks"] = tasks                
    else:
        player = None
    return player

def task(p_id, name, expire, delete=False):
    if delete:
        to_del = r.keys(get_stored_task_id(p_id, name=name))
        for k in to_del:
            r.delete(k)
        return {"modified": True}

    raw_data = r.get(get_stored_player_id(p_id))
    if raw_data is None:
        return {"modified": False,
                "error": "No user with this id"}
    elif len(r.keys(get_stored_task_id(p_id))) >= settings.MAX_TASKS:
        return {"modified": False,
                "error": "Max tasks limit"}
    r.set(get_stored_task_id(p_id, time.time(), name), name, ex=expire)
    return {"modified": True}
