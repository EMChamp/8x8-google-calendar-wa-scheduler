import hubspot
from pprint import pprint
from hubspot.crm.owners import ApiException

client = hubspot.Client.create(access_token="pat-na1-39f78cff-4e8e-4172-ab62-e17c4f5e2252")

try:
    api_response = client.crm.owners.owners_api.get_page(limit=100, archived=False)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling owners_api->get_page: %s\n" % e)