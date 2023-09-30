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


def list_calendars():
        # # Get List of Calendars
        # calendarlist_result = service.calendarList().list().execute()
        # calendars = calendarlist_result.get('items',[])
        # # Extract 'id' parameters using list comprehension
        # id_list = [entry['id'] for entry in calendars]

        # # Print the list of 'id' parameters
        # print(id_list)
        return

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

        # Check if it's a weekday and within the 9 AM to 6 PM time range
        if is_weekday(now_singapore) and 9 <= now_singapore.hour < 18:
            # If today is a weekday and within the specified time range, use the current time
            start_singapore = now_singapore.replace(hour=9, minute=0, second=0, microsecond=0)
            end_singapore = now_singapore.replace(hour=18, minute=0, second=0, microsecond=0)
        else:
            # If today is not a weekday or not within the time range, find the nearest upcoming weekday
            next_weekday = now_singapore + datetime.timedelta(days=(7 - now_singapore.weekday()))
            start_singapore = next_weekday.replace(hour=9, minute=0, second=0, microsecond=0)
            end_singapore = next_weekday.replace(hour=18, minute=0, second=0, microsecond=0)

        # Create a list to store available time slots
        available_time_slots = []

        # Create a list to store human-readable date options
        date_options = []

        # Iterate through the time slots
        current_time = start_singapore
        option_number = 1
        while current_time < end_singapore and len(available_time_slots) < 3:

            # Check if the current time slot is available
            events_result = service.events().list(calendarId='primary', timeMin=current_time.isoformat(),
                                                timeMax=(current_time + datetime.timedelta(hours=1)).isoformat(),
                                                maxResults=1, singleEvents=True, orderBy='startTime').execute()
            events = events_result.get('items', [])
            if not events:
                # If no event is scheduled, the slot is available
                slot_start = current_time
                slot_end = current_time + datetime.timedelta(hours=1)
                
                # Add the human-readable date option
                date_options.append(f"Option {option_number}: {format_datetime(slot_start)} - {format_datetime(slot_end)}")
                
                available_time_slots.append({'start': slot_start.isoformat(), 'end': slot_end.isoformat()})
            
            current_time += datetime.timedelta(hours=1)
            option_number+=1

        # Convert the list of date options to a human-readable string
        date_options_str = "\n".join(date_options)

        # Return the available_time_slots JSON and the human-readable date options as a tuple
        result = {
            "date_options": date_options_str,
            "available_time_slots": available_time_slots
        }

        print(str(result))
        return result
            

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    retrieve_events()