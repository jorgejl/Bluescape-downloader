# Bluescape-downloader
Scripts to download Bluescape (Bluescape.com) content to the local computer, maintaining metadata.

## Important
The script expects a file named "local_settings.py" at the root. An example is provided. Please use that file to store any confidential information (id's, credentials, etc)

You can extract the bearer token from a valid chrome session by using developer tools. Go to "Application" > "Cookies" and find the "idToken" one, containing your bearer token.

You should also be able dynamically get it via OpenAuth2 but bluescape documentation seems to be a bit out of date for that part.

## Usage.
1. Validate your connections settings with bluescape_api_test.py
2. run bluescape_download.py, when prompted, select the workspace you want to backup.

## TODO:
- Double check to download the appropiate files (not just the previews).
- Decide what else we should include in the downloads (text, shapes, etc)
- Decide what to do with the rest of the metadata.
