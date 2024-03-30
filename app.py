from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, render_template
from threading import Lock
from datetime import datetime
import json
import os
import sys

app = Flask(__name__)

# Request details are currently just stored in-memory, so they will be lost when the server is restarted.
request_details_list = []
lock = Lock()


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
def capture_request(path):
    global request_details

    print(f"Capturing {request.method} request for path: {path}", file=sys.stdout)

    with lock:
        request_details_list.insert(0, get_request_details(request, path))

    return display_request()

def get_request_details(request, path):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
              "timestamp": timestamp,
              "path": path,
              "method": request.method,
              "headers": dict(request.headers),
              "query_params": extract_query_params(),
              "body":  extract_body(),
          }

def extract_body():
    if not request.data:
        return "No body content"

    raw_body = request.get_data(as_text=True);

    try:
        json_body = json.loads(raw_body)
        return json.dumps(json_body, indent=4)
    except ValueError:
        return raw_body  # Not JSON or invalid JSON, use raw body

def extract_query_params():
    return {key: request.args[key] for key in request.args}


@app.route("/show", methods=["GET"])
def display_request():
    config = {
        "refresh_interval": os.getenv('REFRESH_INTERVAL', 3000)
    }

    return render_template("request_display.html", details_list=request_details_list, config=config)


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "false").lower() in ["true", "1", "t"]

    app.run(debug=debug)
