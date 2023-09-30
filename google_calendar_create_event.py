# Refer to the Python quickstart on how to setup the environment:
# https://developers.google.com/calendar/quickstart/python
# Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
# stored credentials.
from __future__ import print_function
from flask import jsonify
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def create_event(timeslot_start, timeslot_end):
    print('timeslot in create event  = ' + timeslot_start)
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'google_api_creds.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        event = {
            'summary': '8x8 Customer Meeting',
            'location': 'One George Street',
            'description': 'A chance to speak to a 8x8 support team expert.',
            'start': {
                'dateTime': timeslot_start,
                'timeZone': 'Asia/Singapore',
            },
            'end': {
                'dateTime': timeslot_end,
                'timeZone': 'Asia/Singapore',
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=2'
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
                ],
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        event_details = {
            'event_summary': event['summary'],
            'event_location': event['location'],
            'event_description': event['description'],
            'event_start': event['start']['dateTime'],
            'event_end': event['end']['dateTime'],
        }

        # Return the event details as a JSON response
        return jsonify(event_details)
    
    except HttpError as error:
        print(str(error))
        return jsonify({'error': str(error)}), 400


if __name__ == '__main__':
    create_event()