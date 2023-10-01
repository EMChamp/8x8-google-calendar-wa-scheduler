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

def generate_request_id(customer_email):
    # Generate a unique requestId based on current date, time, and guest email
        current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        request_id = f'{current_time}_{customer_email}'
        return request_id

def create_event(timeslot_start, timeslot_end, customer_email):
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
        request_id = generate_request_id(customer_email)
        event = {
            'summary': '8x8 Customer Meeting',
            'description': 'A chance to speak to a 8x8 support team expert.',
            'start': {
                'dateTime': timeslot_start,
                'timeZone': 'Asia/Singapore',
            },
            'end': {
                'dateTime': timeslot_end,
                'timeZone': 'Asia/Singapore',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
                ],
            },
            'attendees': [
                {'email': 'rommelsunga@gmail.com'},
                {'email': customer_email},
            ],
            'conferenceData': {
                'conferenceSolution': {
                    'key': {
                        "type":"addOn"
                    },
                    'name': '8x8'
                },
                'entryPoints': [
                    {
                        'entryPointType': 'video',
                        'uri': 'https://8x8.vc/8x8/'+request_id,  # Replace with your custom conference link
                        'label': 'https://8x8.vc/8x8/'+request_id,
                    }
                ]
            }
        }

        event_details = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1,sendUpdates="all").execute()

        # Return the event details as a JSON response
        return jsonify(event_details)
    
    except HttpError as error:
        print(str(error))
        return jsonify({'error': str(error)}), 400


if __name__ == '__main__':
    create_event()