from flask import Blueprint, request, jsonify, send_file, Request, copy_current_request_context
from user_context.index import getContext, setContext, buildUserContext
from db.call_recording import get_recordings_to_analyze, mark_analysed

import os
from models.openai_with_file_backed_store import talk_to_me, generate_response_gpt3_with_file_context
from models.text_speech_interconverters import transcribe_audio_whisper

import time
from config import Config
from aws import AWS_S3

import concurrent.futures

recordingRoute = Blueprint("/recording", __name__)


def download_from_s3(path, local_file_name):
    bucket = Config.RECORDING_BUCKET
    s3 = AWS_S3()
    s3.download_file_from_s3(bucket, path, local_file_name)


def post_analysis_cleanup(recording_id, local_file_name):
    # mark_analysed(recording_id)
    os.remove(local_file_name)


@recordingRoute.route("/analyze", methods=["POST"])
def analyze_recording():
    recordings = get_recordings_to_analyze()
    recordings = list(recordings)

    if recordings is None:
        return jsonify({"success": False, "message": "No recordings to analyze"}), 200

    for recording in recordings:
        recording_id = recording["_id"]
        recording_url = recording["recording_url"]
        phone = recording["from"]

        local_file_name = phone + ".mp3"

        # process
        download_from_s3(recording_url, local_file_name)

        post_analysis_cleanup(recording_id, local_file_name)

    return jsonify({"success": True, "message": "Recordings analyzed"}), 200
