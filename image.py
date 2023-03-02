import base64
import os
import requests
import configparser

from google.oauth2.credentials import Credentials

# Load the OAuth 2.0 client ID and client secret from the configuration file
config = configparser.ConfigParser()
config.read("config.ini")

if not config.has_section('google'):
    print("OAuth 2.0 credentials are not set, please provide them in 'config.ini'")
    exit()
else:
    client_id = config.get('google', 'client_id')
    client_secret = config.get('google', 'client_secret')
    refresh_token = config.get('google','refresh_token')

# Obtain an OAuth 2.0 access token using the client ID and client secret
credentials = Credentials.from_authorized_user_info(info={'client_id':client_id, 'client_secret':client_secret,'refresh_token':refresh_token})
access_token = credentials.token

def search_image(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    try:
        with open(image_path, "rb") as f:
            image_data = f.read()
    except Exception as e:
        raise Exception(f"Failed to read image file: {e}") from e
    try:
        image_data = base64.b64encode(image_data).decode()
    except Exception as e:
        raise Exception(f"Failed to encode image file: {e}") from e

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    body = {
        "requests": [
            {
                "image": {
                    "content": image_data
                },
                "features": [
                    {
                        "type": "LANDMARK_DETECTION"
                    }
                ]
            }
        ]
    }
    try:
        response = requests.post("https://vision.googleapis.com/v1/images:annotate", json=body, headers=headers)
    except Exception as e:
        raise Exception(f"Failed to send request: {e}") from e

    if response.status_code != 200:
        raise Exception(f"Failed to search image: {response.text}")

    try:
        landmarks = response.json().get("responses", [{}])[0].get("landmarkAnnotations", [])
        if not landmarks:
            raise Exception("Image does not contain any landmark annotations")
    except (KeyError, IndexError) as e:
        raise Exception("Failed to extract landmark data from API response") from e

    locations = []
    for landmark in landmarks:
        try:
            location = landmark["locations"][0]["latLng"]
            locations.append((location['latitude'], location['longitude']))
        except (KeyError, IndexError) as e:
            raise Exception("Failed to extract location data from API response") from e

    return locations

# Test the function with an image
if not client_id or not client_secret:
    print("OAuth 2.0 credentials are not set")
else:
    try:
        locations = search_image("image.jpg")
        if locations:
            for location in locations:
                print(f"Latitude: {location[0]}, Longitude: {location[1]}")
        else:
            print("No location found")
    except Exception as e:
        print(f"Error: {e}")
