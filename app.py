from flask import Flask, request, jsonify
from datetime import datetime
import pytz
import json
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Load token from environment
API_TOKEN = os.getenv("API_TOKEN")

# Load city timezone data
with open('capitals.json') as f:
    CITY_TIMEZONES = json.load(f)

app = Flask(__name__)


@app.route("/api/time", methods=["GET"])
def get_time():
    token = request.headers.get("Authorization")
    if not token or token != f"Bearer {API_TOKEN}":
        return jsonify({"error": "Unauthorized. Please provide a valid token."}), 401

    city = request.args.get("city")
    if not city:
        return jsonify({"error": "Please provide a capital city in the query parameter, e.g., ?city=London"}), 400

    timezone_name = CITY_TIMEZONES.get(city)
    if not timezone_name:
        return jsonify({"error": f"{city} not found in the database."}), 404

    tz = pytz.timezone(timezone_name)
    now = datetime.now(tz)
    utc_offset = now.strftime('%z')
    utc_offset_formatted = f"UTC{'+' if int(utc_offset) >= 0 else ''}{utc_offset[:3]}:{utc_offset[3:]}"

    return jsonify({
        "city": city,
        "local_time": now.strftime('%Y-%m-%d %H:%M:%S'),
        "utc_offset": utc_offset_formatted
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
