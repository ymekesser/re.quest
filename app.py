from flask import Flask, request, render_template
from threading import Lock
from datetime import datetime
import json

app = Flask(__name__)

# Use a global variable to store the request details so it can be updated on each request
# and displayed when the page is refreshed.
request_details_list = []
lock = Lock()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def capture_request(path):
    global request_details

    with lock:
        query_params = {key: request.args[key] for key in request.args}
        body = request.get_data(as_text=True) if request.data else 'No body content'
        
        # Try to pretty-print JSON body
        try:
            json_body = json.loads(body)
            pretty_body = json.dumps(json_body, indent=4)
        except ValueError:
            pretty_body = body  # Not JSON or invalid JSON, use raw body

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Insert new request at the beginning of the list
        request_details_list.insert(0, {
            "timestamp": timestamp,
            "path": path,
            "method": request.method,
            "headers": dict(request.headers),
            "query_params": query_params,
            "body": pretty_body,
        })

    # Redirect to the display route to show the captured details
    return display_request()

@app.route('/show', methods=['GET'])
def display_request():
    # Render the template with the request details
    return render_template('request_display.html', details_list=request_details_list)

if __name__ == '__main__':
    app.run(debug=True)