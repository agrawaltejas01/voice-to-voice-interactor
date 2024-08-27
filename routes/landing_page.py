from flask import Blueprint, request, jsonify, send_file, Request, copy_current_request_context
from db.landing_page import save_user_number

import os

landingPageRoute = Blueprint("/landing_page", __name__)


@landingPageRoute.route("/save_phone", methods=["POST"])
def savePhoneNumber():
    phoneNumber = request.json.get("phoneNumber")

    save_user_number(phoneNumber)
    return jsonify({"success": True}), 200
