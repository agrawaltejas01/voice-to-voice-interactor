from connections.index import create_or_get_redis_client


def getContext(userId):
    redis_client = create_or_get_redis_client()
    return redis_client.get(userId)


def setContext(userId: str, data):
    redis_client = create_or_get_redis_client()
    return redis_client.set(userId, data)
