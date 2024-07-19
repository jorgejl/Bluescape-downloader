# Python Code (python 3.5+)
import requests
import pprint
import local_settings
import json
import os

#will list all current workspaces for the logged in user
#a download folder will be created for each workspace, a ./downloads folder 
#is expected to be in the same directory as this script



# Load the settings from local_settings.py for the current script
portal = local_settings.settings['bluescape']['api_portal']
organizationId = local_settings.settings['bluescape']['organizationId']
token = local_settings.settings['bluescape']['bearertoken']

# Define the API endpoint
API_version = 'v3'

#begin loop to list all workspaces and their images

#endpoint: list my workspaces
API_endpoint = '/' + API_version + '/users/me/workspaces'

the_request = requests.get(
    portal+API_endpoint,
    headers={"Authorization": "Bearer " + token,
            "Content-Type": "application/json"
            },
)

json_response = the_request.json()

# Create a menu with workspace names
workspaces = json_response['workspaces']
menu = {}
for i, workspace in enumerate(workspaces):
    menu[i+1] = workspace['name']

# Print the menu options
for key, value in menu.items():
    print(f"{key}. {value}")

# Ask the user to select a workspace
selected_option = input("Select a workspace: (CTRL+C to exit)")

# Get the selected workspace ID
selected_workspace = workspaces[int(selected_option)-1]
workspaceId = selected_workspace['id']

# Create a folder with the workspace ID as the name
folder_name = str(workspaceId)
folder_path = os.path.join( os.curdir, "downloads", folder_name)

os.makedirs(folder_path, exist_ok=True)

# Create a file inside the folder with the workspace name
file_name = "__workspace_name.txt"
file_path = os.path.join(folder_path, file_name)
with open(file_path, 'w') as file:
    file.write(selected_workspace['name'])

# Print the path of the created file
print(f"File created: {file_path}")

# Print the path of the created folder
print(f"Folder created: {folder_path}")

# download all images from a workspace
if __name__ == "__main__":
    # Get all the images from a workspace
    API_endpoint = '/' + API_version + '/workspaces/' + workspaceId + '/elements'

    the_request = requests.get(
       portal + API_endpoint,
       headers={"Authorization": "Bearer " + token,
                "Content-Type": "application/json"
                }
    )

    json_response = the_request.json()
    # Save the JSON response to a text file
    json_file_path = os.path.join(folder_path, (workspaceId + ".json"))
    with open(json_file_path, 'w') as file:
        file.write(json.dumps(json_response))

    # Print the path of the saved JSON file
    print(f"JSON response saved: {json_file_path}")
# Iterate over the contents of the JSON response
    items = json_response['data']

    for item in items:
        # Perform different actions based on the item type
        if item['type'] == "Image":
            # Get the image URL
            image_url = item['asset']['url']
            
            # Download the image
            response = requests.get(image_url)
            
            # Extract the image filename from the URL
            filename = item['filename']
            
            # Save the image to the workspace folder
            image_path = os.path.join(folder_path, filename)
            with open(image_path, 'wb') as file:
                file.write(response.content)
            
            # Print the path of the downloaded image
            print(f"Image downloaded: {image_path}")
        elif item['type'] == "Video":
            # Get the video URL
            video_url = item['asset']['url']
            
            # Download the video
            response = requests.get(video_url)
            
            # Extract the video filename from the URL
            filename = item['filename']
            
            # Save the video to the workspace folder
            video_path = os.path.join(folder_path, filename)
            with open(video_path, 'wb') as file:
                file.write(response.content)
            
            # Print the path of the downloaded video
            print(f"Video downloaded: {video_path}")           
        else:
            # Print a message for unsupported item types
            print(f"Unsupported item type, not performing any actions: {item['type']}")
