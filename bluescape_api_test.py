import requests
import pprint 
import local_settings

#will list all current workspaces for the logged in user


# Load the settings from local_settings.py for the current script
portal = local_settings.settings['bluescape']['api_portal']
organizationId = local_settings.settings['bluescape']['organizationId']
token = local_settings.settings['bluescape']['bearertoken']

# Define the API endpoint
API_version = 'v3'
#endpoint: list my workspaces
API_endpoint = '/' + API_version + '/users/me/workspaces'


the_request = requests.get(
    portal+API_endpoint,
    headers={"Authorization": "Bearer " + token,
            "Content-Type": "application/json"
            },
)

json_response = the_request.json()
pprint.pprint(json_response)