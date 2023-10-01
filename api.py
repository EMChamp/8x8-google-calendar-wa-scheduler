# save this as app.py
from flask import Flask, request
from google_calendar_create_event import create_event
from google_calendar_retrieve_events import retrieve_events
app = Flask(__name__)


@app.route("/create_meeting", methods=['POST'])
def create_meeting():
     # Retrieve JSON data from the request body
    request_data = request.get_json()

    # Extract the "start" and "end" parameters from the JSON data
    start = request_data.get('start')
    end = request_data.get('end')
    customer_email = request_data.get('customer_email')
    return create_event(start, end, customer_email)

@app.route("/retrieve_meetings")
def retrieve_meetings():
    return retrieve_events()


if __name__ == '__main__':
    app.run(debug=True, port=5003)