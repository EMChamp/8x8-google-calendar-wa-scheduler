import requests,json

# Define your variable for hubspot_owner_id
hubspot_owner_id = "554091640"  # Replace with the actual value

url = "https://api.hubapi.com/crm/v3/objects/meetings"
bearer_token = "pat-na1-39f78cff-4e8e-4172-ab62-e17c4f5e2252"
# Use the variable in the payload
payload = {
    "properties": {
        "hs_timestamp": "2019-10-01T03:30:17.883Z",
        "hs_meeting_body": "The first meeting to discuss options",
        "hs_meeting_title": "Intro meeting",
        "hubspot_owner_id": hubspot_owner_id,  # Use the variable here
        "hs_meeting_outcome": "SCHEDULED",
        "hs_meeting_end_time": "2023-10-04T12:00:00.000Z",
        "hs_meeting_location": "Remote",
        "hs_meeting_start_time": "2023-10-04T13:00:00.000Z",
        "hs_meeting_external_url": "https://Zoom.com/0000",
        "hs_internal_meeting_notes": "These are the meeting notes"
    }
}

headers = {
    'accept': "application/json",
    'content-type': "application/json",
    'authorization': "Bearer " + bearer_token
}

# Convert the payload dictionary to JSON
payload_json = json.dumps(payload)

response = requests.request("POST", url, data=payload_json, headers=headers)

print(response.text)
