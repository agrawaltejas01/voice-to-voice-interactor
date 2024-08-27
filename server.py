from routes.index import inputRoute
from routes.landing_page import landingPageRoute
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os

from connections.index import create_connections


# from index import talk_to_me

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploaded_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

print("Setting up connections")
# Create Redis client when the first request comes in
create_connections()

app.register_blueprint(inputRoute, url_prefix="/input")
app.register_blueprint(landingPageRoute, url_prefix="/landing_page")


# @app.before_first_request
# def server_init():
#     print("Setting up connections")
#     # Create Redis client when the first request comes in
#     create_connections()


# @app.route('/upload', methods=['POST'])
# def upload_file():
#     print("Got the request")
#     # Check if a file part is present in the request
#     if 'file' not in request.files:
#         return jsonify({"error": "No file part in the request"}), 400

#     file = request.files['file']
#     # Check if a file is selected for uploading
#     if file.filename == '':
#         return jsonify({"error": "No file selected for uploading"}), 400

#     if file:
#         # Define the path to save the uploaded file
#         file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#         # Save the file to the specified directory
#         file.save(file_path)

#         # Call the transcription function and get the text
#         try:
#             success = talk_to_me(file_path)
#             # Return the transcription as a JSON response
#             # return jsonify({"success": "true"}), 200
#             return send_file("output.mp3", mimetype="audio/webm")
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500

#     return jsonify({"error": "Something went wrong"}), 500


@app.route('/', methods=["GET"])
def health():
    return jsonify({"error": "Hello world"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5010)
