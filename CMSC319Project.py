import os
import base64
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def getToken():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    # Build the authorization header
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    url = "https://accounts.spotify.com/api/token"  # must be exact
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    # Make the POST request
    response = requests.post(url, headers=headers, data=data)
    return response.json()["access_token"]

token=getToken()
print("TOKEN", token)

    
    