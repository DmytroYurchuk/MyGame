from django.conf import settings

settings.configure(
	MAP_X=10,
	MAP_Y=10,
	REDIS_HOST='127.0.0.1',
	REDIS_PORT=6379,
	MONGO_HOST='127.0.0.1',
	MONGO_PORT=27017,
	MAX_TASKS=4,
	PLAYER_VIEW=20)
