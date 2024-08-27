from flask import Blueprint, request, jsonify, send_file, Request, copy_current_request_context
from user_context.index import getContext, setContext, buildUserContext
from db.user_interaction import save_user_input, save_output

import os
from models.openai_with_file_backed_store import talk_to_me, generate_response_gpt3_with_file_context
from models.text_speech_interconverters import transcribe_audio_whisper

import time

import concurrent.futures

inputRoute = Blueprint("/input", __name__)

UPLOAD_FOLDER = 'uploaded_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def getTextFromAudio(req: Request):
    error = None
    current_prompt = None
    if 'file' not in request.files:
        error = jsonify({"error": "No file part in the request"})

    file = request.files['file']
    # Check if a file is selected for uploading
    if file.filename == '':
        error = jsonify({"error": "No file selected for uploading"})
        return error

    if file:
        # Define the path to save the uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        # Save the file to the specified directory
        file.save(file_path)

        # Call the transcription function and get the text
        try:
            current_prompt = transcribe_audio_whisper(file_path)
            # success = talk_to_me(file_path)
            # Return the transcription as a JSON response
            # return jsonify({"success": "true"}), 200
            # return send_file("output.mp3", mimetype="audio/webm")
        except Exception as e:
            error = jsonify({"error": str(e)})

    return current_prompt, file_path, error


def inputBlock(req, userId):
    @copy_current_request_context
    def get_text_from_audio_wrapped(req):
        return getTextFromAudio(req)

    context = []
    current_context = []

    # Create a ThreadPoolExecutor to run functions in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit both functions to the executor
        future_context = executor.submit(buildUserContext, userId)
        future_prompt = executor.submit(get_text_from_audio_wrapped, request)

        # Wait for both to complete and get the results
        context = future_context.result()
        current_prompt, file_path, error = future_prompt.result()

    if error == None:
        current_context = context
        print(current_prompt)
        context.append({
            "role": "user",
            "content": current_prompt
        })

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(
            save_user_input, userId, {"current_context": current_context, "current_prompt": current_prompt}, context, file_path)

    return context, error


def saveContextWithResponse(userId, current_context_and_input, answer):
    current_context_and_input.append({
        "role": "system",
        "content": answer
    })
    setContext(userId, current_context_and_input)


def processingBlock(current_context_and_input, userId):

    print(current_context_and_input)
    answer = generate_response_gpt3_with_file_context(
        current_context_and_input)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(
            saveContextWithResponse, userId, current_context_and_input, answer)
        executor.submit(
            save_output, userId, current_context_and_input, answer
        )

    return answer


@inputRoute.route("/voice", methods=["POST"])
def voiceInput():
    userId = request.form.get('userId')
    if not userId:
        return jsonify({"error": "Invalid input, 'userId' is required"}), 400

    start_time = time.time()

    context_and_input, error = inputBlock(
        request, userId)
    if error is not None:
        return error, 400

    # answer = processingBlock(context_and_input, userId)

    end_time = time.time()
    duration = end_time - start_time

    return jsonify({"current_prompt": context_and_input, "duration": duration}), 200
    # return jsonify({"ans": answer, "duration": duration}), 200
