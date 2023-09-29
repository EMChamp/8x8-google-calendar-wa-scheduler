import requests

url = "https://api.hubapi.com/crm/v3/objects/meetings/"
bearer_token = "pat-na1-39f78cff-4e8e-4172-ab62-e17c4f5e2252"
meeting_id = "40576378535"
querystring = {"archived":"false"}

headers = {
    'accept': "application/json",
    'authorization': "Bearer " + bearer_token
    }

response = requests.request("GET", url+meeting_id, headers=headers, params=querystring)

print(response.text)