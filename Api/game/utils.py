import random
from django.conf import settings

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
