from routes.index import inputRoute
from routes.landing_page import landingPageRoute
from routes.recording_analyzer import recordingRoute
from connections.index import create_connections
from connections.redis_pubsub import subscribe_to_pub_sub
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.before_request
def before_request():
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return '', 204, headers


print("Setting up connections")
# Create Redis client when the first request comes in
create_connections()
# subscribe_to_pub_sub()


app.register_blueprint(inputRoute, url_prefix="/input")
app.register_blueprint(landingPageRoute, url_prefix="/landing_page")
app.register_blueprint(recordingRoute, url_prefix="/recording")


@app.route('/', methods=["GET"])
def health():
    return jsonify({"error": "Hello world"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5010)
