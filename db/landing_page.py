from connections.index import create_or_get_mongo_client
import datetime


def save_user_number(phoneNumber):
    timeNow = datetime.datetime.utcnow()

    db = create_or_get_mongo_client()
    landingPageCollection = db["landing_page"]

    payload = {
        "phone_number": phoneNumber,
        "created_at": timeNow,
        "reached_out": False
    }

    try:
        result = landingPageCollection.insert_one(payload)
    except Exception as e:
        print(e)
