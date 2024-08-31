import redis
from pymongo import MongoClient, database
from bson import ObjectId
import logging


from config import Config

redis_client = None
db = None


def create_or_get_redis_client() -> redis.StrictRedis:
    global redis_client
    if redis_client is None:
        redis_client = redis.StrictRedis(
            host=Config.REDIS_HOST, port=int(Config.REDIS_PORT), db=0,
            password=Config.REDIS_PASS, username=Config.REDIS_USER)

    return redis_client


def create_or_get_mongo_client() -> database.Database[database._DocumentType]:
    global db
    if db is None:
        print("New DB connection")

        logging.basicConfig()
        logging.getLogger('pymongo.command').setLevel(logging.DEBUG)

        mongo = MongoClient(Config.MONGO_URI)

        db = mongo.get_database(Config.MONGO_DB)
    else:
        print("DB connection reused")
    return db


def create_connections():
    create_or_get_redis_client()
    create_or_get_mongo_client()
