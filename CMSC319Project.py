import os
import base64
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

#VARIABLES
#Dictionary that maps "generic moods" to the specific audio features of Spotify's Data
# - Spotify doesn't understand "Happy", but the data has specific numerical values to describe the audio
# - The dictionary then maps the human moods with Spotify's audio features
moodFeatures = {
    "happy": {
        "target_valence": 0.9,
        "target_energy": 0.8,
        "seed_genres": "pop"
    },
    "sad": {
        "target_valence": 0.2,
        "target_energy": 0.3,
        "seed_genres": "acoustic"
    },
    "chill": {
        "target_valence": 0.5,
        "target_energy": 0.3,
        "seed_genres": "chill"
    },
    "energetic": {
        "target_valence": 0.7,
        "target_energy": 0.9,
        "seed_genres": "dance"
    },
    "dramatic": {
        "target_valence": 0.3,
        "target_energy": 0.8,
        "target_instrumentalness": 0.6,
        "seed_genres": "classical"
    },
    #ROMANCE COULD BE PROBLEM IN SEED GENRE
    "romantic": {
        "target_valence": 0.7,
        "target_energy": 0.4,
        "target_acousticness": 0.6,
        "seed_genres": "romance"
    },
    "focus": {
        "target_valence": 0.4,
        "target_energy": 0.2,
        "target_instrumentalness": 0.8,
        "seed_genres": "ambient"
    }
}

#METHODS

#Method to get Authorization Token
#-----Token acts as a pass to talk to Spotify Servers
#-----Spotify won't give data without having a valid token
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






    
    