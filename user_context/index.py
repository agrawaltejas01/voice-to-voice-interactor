from connections.index import create_or_get_redis_client
import json


def getContext(userId):
    redis_client = create_or_get_redis_client()
    return redis_client.get(userId)


def setContext(userId: str, data):
    redis_client = create_or_get_redis_client()
    result = redis_client.set(userId, json.dumps(data))
    print("Inside set context", str(userId), str(data), result)
    return True


def freshContext():

    return [{"role": "system", "content": "You are a helpful assistant that helps me with anything. \
                Use mix of english and the language that you got input in, like Indians do in day to day life. \
                Not completely local language, not completely hindi, and not completely english as well.\
                    Always output your response in english writing, even if the sentence is spoken in english, hinglish or mix."}],


def buildUserContext(userId):
    redis_client = create_or_get_redis_client()
    existingContext = redis_client.get(userId)

    if existingContext is None:
        existingContext = list(freshContext())
    else:
        existingContext = json.loads(existingContext)

    # Ensure that existingContext is a list of dictionaries
    if not isinstance(existingContext, list):
        existingContext = [existingContext]

    return existingContext
