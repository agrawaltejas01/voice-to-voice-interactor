import redis

from config import Config

redis_client = None


def create_or_get_redis_client() -> redis.StrictRedis:
    global redis_client
    if redis_client is None:
        redis_client = redis.StrictRedis(
            host=Config.REDIS_HOST, port=int(Config.REDIS_PORT), db=0,
            password=Config.REDIS_PASS, username=Config.REDIS_USER)

    return redis_client


def create_connections():
    create_or_get_redis_client()
