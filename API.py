from flask import Flask, jsonify, request
from functools import wraps
from datetime import datetime
import pytz

app = Flask(__name__)

# In production, use environment variables or a secrets manager
API_TOKEN = "supersecrettoken123"

# Simple internal database of capital cities and their timezones
CITY_TIMEZONES = {
    "London": "Europe/London",
    "Paris": "Europe/Paris",
    "Washington": "America/New_York",
    "Tokyo": "Asia/Tokyo",
    "Canberra": "Australia/Sydney",
    "New Delhi": "Asia/Kolkata",
    "Ottawa": "America/Toronto",
    "Brasília": "America/Sao_Paulo"
}

# Token-required decorator
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            if token == API_TOKEN:
                return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized. Provide a valid Bearer token."}), 401
    return decorator

# Basic hello endpoint
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, world!"})

# Time endpoint
@app.route('/api/time', methods=['GET'])
@token_required
def get_time():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "Please provide a capital city using ?city=CityName"}), 400

    timezone = CITY_TIMEZONES.get(city)
    if not timezone:
        return jsonify({"error": f"{city} not found in database."}), 404

    tz = pytz.timezone(timezone)
    now = datetime.now(tz)
    utc_offset = now.strftime('%z')
    utc_offset_formatted = f"UTC{'+' if int(utc_offset) >= 0 else ''}{utc_offset[:3]}:{utc_offset[3:]}"

    return jsonify({
        "city": city,
        "local_time": now.strftime('%Y-%m-%d %H:%M:%S'),
        "utc_offset": utc_offset_formatted
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
