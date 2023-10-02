from __future__ import print_function

import datetime
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Function to format a datetime object as a human-readable string
def format_datetime(dt):
    return dt.strftime('%A, %d %B %Y %H:%M')

# Function to check if a date is a weekday (Monday to Friday)
def is_weekday(date):
    return date.weekday() < 5  # Monday to Friday are 0 to 4


# Function to format time slots
def format_time_slot(slot, option_number):
    start_time = datetime.fromisoformat(slot["start"])
    end_time = datetime.fromisoformat(slot["end"])
    formatted_option = f"Option {option_number}) {start_time.strftime('%B %d, %I%p')} - {end_time.strftime('%I%p')}"
    return formatted_option

def get_next_weekday(now_singapore):
    # Check if it's a weekday and within the 9 AM to 6 PM time range
    if is_weekday(now_singapore) and now_singapore.hour < 9:
        # If today is a weekday and within the specified time range, use the current time
        start_singapore = now_singapore.replace(hour=9, minute=0, second=0, microsecond=0)
    elif is_weekday(now_singapore) and now_singapore.hour >=18:
        # Determine the number of days to add to get to the next weekday
        if now_singapore.weekday() in [0, 1, 2, 3]:
            next_weekday = now_singapore + datetime.timedelta(days=1)
        else:
            next_weekday = now_singapore + datetime.timedelta(days=3)

        # Set the start and end times for the next weekday
        start_singapore = next_weekday.replace(hour=9, minute=0, second=0, microsecond=0)
    elif is_weekday(now_singapore) and 9 <= now_singapore.hour < 18:
        #Pick the next timeslot at least an hour away
        next_weekday = now_singapore + datetime.timedelta(hours=1) #This needs to be one hour or the logic for retrieve events will break 
        start_singapore = next_weekday.replace(minute=0, second=0, microsecond=0)
    else:
        if now_singapore.weekday() == 5:
            next_weekday = now_singapore + datetime.timedelta(days=2)
        else:
            next_weekday = now_singapore + datetime.timedelta(days=1)
        start_singapore = next_weekday.replace(hour=9, minute=0, second=0, microsecond=0)
    return start_singapore

def is_valid_timeslot(timeslot):
    if is_weekday(timeslot) and 9 <= timeslot.hour < 18:
        return True
    else:
        return False

def retrieve_events():
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
        # Build Google calendar Service
        service = build('calendar', 'v3', credentials=creds)
        
        # Get current time in Singapore timezone
        singapore_timezone = datetime.timezone(datetime.timedelta(hours=8))  # UTC+8
        now_singapore = datetime.datetime.now(singapore_timezone)

        # Get Start of next Weekday
        start_singapore = get_next_weekday(now_singapore)

        # Create a list to store available time slots
        available_time_slots = []

        # Create a list to store human-readable date options
        date_options = []

        # Iterate through the time slots until there are at least 3.
        current_time = start_singapore
        option_number = 1
        iterator = 1
        print("current time = " + str(current_time))
        while len(available_time_slots) < 3:
            print(iterator)
            iterator+=1
            # Check if the current time slot is available
            events_result = service.events().list(calendarId='primary', timeMin=current_time.isoformat(),
                                                timeMax=(current_time + datetime.timedelta(hours=1)).isoformat(),
                                                maxResults=1, singleEvents=True, orderBy='startTime').execute()
            events = events_result.get('items', [])

            # If no event is scheduled, the slot is available
            if not events and is_valid_timeslot(current_time):
                slot_start = current_time
                slot_end = current_time + datetime.timedelta(hours=1)
                
                # Add the human-readable date option
                date_options.append(f"Option {option_number}: {format_datetime(slot_start)} - {format_datetime(slot_end)}")
                
                available_time_slots.append({'start': slot_start.isoformat(), 'end': slot_end.isoformat()})
                option_number+=1

            current_time = get_next_weekday(current_time)

        # Convert the list of date options to a human-readable string
        date_options_str = "\n".join(date_options)

        # Return the available_time_slots JSON and the human-readable date options as a tuple
        result = {
            "date_options": date_options_str,
            "timeslot1_start": available_time_slots[0]['start'],
            "timeslot1_end": available_time_slots[0]['end'],
            "timeslot2_start": available_time_slots[1]['start'],
            "timeslot2_end": available_time_slots[1]['end'],
            "timeslot3_start": available_time_slots[2]['start'],
            "timeslot3_end": available_time_slots[2]['end']
        }
        return result
            

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    retrieve_events()