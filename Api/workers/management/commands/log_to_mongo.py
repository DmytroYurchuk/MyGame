import time
import redis
import logging
from pymongo import MongoClient
from redis import StrictRedis

from django.conf import settings
from django.core.management.base import BaseCommand

logger = logging.getLogger("log_to_mongo")

class Command(BaseCommand):
    args = "none"
    help = "Run worker that will log from redis to mongo"

    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)

    m_client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)

    SLEEP_TIMEOUT = 0.1 # in seconds

    def handle(self, *args, **options):
        logger.info("Start logs worker")
        pubsub = self.r.pubsub()
        pubsub.psubscribe('__keyspace@0__:*')

        coll = self.m_client.MyGame.logs

        while True:
            message = pubsub.get_message()
            if message and message.get("type") == "pmessage":
                post = {"ts": time.time(),
                        "channel": message.get("channel"),
                        "data": message.get("data")}
                post_id = coll.insert_one(post).inserted_id
                if not post_id:
                    logger.warning("Not logged message.")
            else:
                time.sleep(self.SLEEP_TIMEOUT)