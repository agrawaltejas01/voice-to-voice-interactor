from connections.index import create_or_get_mongo_client
import datetime


def save_user_number(phoneNumber):
    timeNow = datetime.datetime.utcnow()

    db = create_or_get_mongo_client()
    landingPageCollection = db["landing_page"]

    try:
        result = landingPageCollection.update_one(
            {"phone_number": phoneNumber},
            {
                "$set": {"phone_number": phoneNumber, "last_signed_up": timeNow, "reached_out": False},
                "$inc": {"no_of_signups": 1}
            },
            True
        )
    except Exception as e:
        print(e)
