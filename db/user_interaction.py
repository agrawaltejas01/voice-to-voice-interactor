from connections.index import create_or_get_mongo_client
import json
from enum import Enum
import datetime

from config import Config

from aws import AWS_S3

INPUT = "INPUT"
OUTPUT = "OUTPUT"


def save_user_input(userId, input, context_and_input, file_path):

    s3 = AWS_S3()

    timeNow = datetime.datetime.utcnow()

    db = create_or_get_mongo_client()
    userInteractionCollection = db["user_interaction"]

    payload = {
        "userId": userId,
        "type": INPUT,
        "current_prompt": input["current_prompt"],
        "context_and_input": context_and_input,
        "created_at": timeNow
    }

    try:
        result = userInteractionCollection.insert_one(payload)
    except Exception as e:
        print(e)

    try:
        s3_file_path = userId + "/" + \
            str(result.inserted_id) + "_" + str(timeNow.now())
        s3.upload_file_to_s3(Config.USER_INTERACTION_BUCKET,
                             s3_file_path, "audio/mpeg", None, file_path)
    except Exception as e:
        print(e)

    return result


def save_output(userId, input, output):
    db = create_or_get_mongo_client()
    userInteractionCollection = db["user_interaction"]

    payload = {
        "userId": userId,
        "type": OUTPUT,
        "context_and_input": input,
        "current_output": output,
        "created_at": datetime.datetime.utcnow()
    }
    print("Output payload - ", payload)

    result = userInteractionCollection.insert_one(payload)
    print(result.acknowledged, result.inserted_id)

    return result
