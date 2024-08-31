import base64
import os
from .index import create_or_get_redis_client

import json
import wave

STREAM_CHANNEL = "voice-stream"


stream_pubsub = None


def subscribe_to_pub_sub():
    if stream_pubsub is not None:
        return stream_pubsub
    redis_client = create_or_get_redis_client()
    pubsub = redis_client.pubsub()
    pubsub.subscribe(STREAM_CHANNEL)
    print(f"Subscribed to {STREAM_CHANNEL}. Waiting for message")

    output_file = 'output.wav'

    # Check if the file already exists
    file_exists = os.path.isfile(output_file)

    for message in pubsub.listen():
        if message and message['type'] == 'message':
            data = message['data']
            payload = data.decode('utf-8')
            payload_dict = json.loads(payload)
            if payload_dict and payload_dict['event'] == 'media':
                if 'media' in payload_dict and 'payload' in payload_dict['media']:
                    media_payload = base64.b64decode(
                        payload_dict['media']['payload'])
                    print(f"Received message payload: {media_payload}")

                    # If the file already exists, read the existing data
                    if file_exists:
                        with wave.open(output_file, 'rb') as wav_file:
                            params = wav_file.getparams()
                            existing_frames = wav_file.readframes(
                                wav_file.getnframes())
                    else:
                        # If the file doesn't exist, initialize parameters
                        params = (1, 2, 8000, 0, 'NONE', 'not compressed')
                        existing_frames = b''

                    # Write the combined data back to the file
                    with wave.open(output_file, 'wb') as wav_file:
                        wav_file.setparams(params)
                        wav_file.writeframes(existing_frames + media_payload)

                    file_exists = True

                    # Check if the payload contains a stop event
                    if payload_dict and payload_dict['event'] == 'stop':
                        # Stop processing the messages
                        break

    return pubsub


def listen_for_messages():
    pubsub = subscribe_to_pub_sub()
    for message in pubsub.listen():
        if message and message['type'] == 'message':
            print(f"Received message: {message['data']}")


# listen_for_messages()
