# save this as app.py
from flask import Flask
from google_calendar_create_event import create_event
from google_calendar_retrieve_events import retrieve_events
app = Flask(__name__)


@app.route("/create_meeting")
def create_meeting():
    return create_event()

@app.route("/retrieve_meetings")
def retrieve_meetings():
    return retrieve_events()
   


if __name__ == '__main__':
    app.run(debug=True, port=5003)