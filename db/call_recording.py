from connections.index import create_or_get_mongo_client

call_recording_collection = "callRecordings"


def get_recordings_to_analyze():
    db = create_or_get_mongo_client()
    userInteractionCollection = db[call_recording_collection]

    recordings = userInteractionCollection.find({
        "analysed": False
    })

    return recordings


def mark_analysed(recording_id):
    db = create_or_get_mongo_client()
    userInteractionCollection = db[call_recording_collection]

    return userInteractionCollection.update_one(
        {"_id": recording_id}, {"$set": {"analysed": True}})
