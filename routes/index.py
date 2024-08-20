from flask import Blueprint, request, jsonify, send_file
from user_context.index import getContext, setContext

import os
from models.openai_with_file_backed_store import talk_to_me

inputRoute = Blueprint("/input", __name__)

UPLOAD_FOLDER = 'uploaded_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@inputRoute.route("/voice", methods=["POST"])
def voiceInput():
    userId = request.form.get('userId')
    if not userId:
        return jsonify({"error": "Invalid input, 'userId' is required"}), 400

    context = getContext(userId)

    if context is None:
        setContext(userId, "ABCD")

    print("Got the request")
    # Check if a file part is present in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    # Check if a file is selected for uploading
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    if file:
        # Define the path to save the uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        # Save the file to the specified directory
        file.save(file_path)

        # Call the transcription function and get the text
        try:
            success = talk_to_me(file_path)
            # Return the transcription as a JSON response
            # return jsonify({"success": "true"}), 200
            return send_file("output.mp3", mimetype="audio/webm")
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "Something went wrong"}), 500
