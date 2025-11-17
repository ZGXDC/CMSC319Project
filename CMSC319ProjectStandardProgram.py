import os
import base64
import requests
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

#VARIABLES
#userMood will be the user's desired mood for the playlist
userMood = ''

#METHODS
#Method that returns specific audioFeatures of each human mood. 
# - Parameters are the "mood" - the user input mood and "neededData" - which key value is needed
# - "neededData" can only be "seed_genres", "target_valence", or "target_energy"
   # MoodFeatures Dictionary maps "generic moods" to the specific audio features of Spotify's Data
    # - Spotify doesn't understand "Happy", but the data has specific numerical values to describe the audio
    # - The dictionary then maps the human moods with Spotify's audio features
def getMoodFeaturesData(mood, neededData):
    moodFeatures = {
    "happy": {
        "target_valence": 0.9,
        "target_energy": 0.8,
        "seed_genres": ["pop"]
    },
    "sad": {
        "target_valence": 0.2,
        "target_energy": 0.3,
        "seed_genres": ["acoustic"]
    },
    "chill": {
        "target_valence": 0.5,
        "target_energy": 0.3,
        "seed_genres": ["chill"]
    },
    "energetic": {
        "target_valence": 0.7,
        "target_energy": 0.9,
        "seed_genres": ["dance"]
    },
    "dramatic": {
        "target_valence": 0.3,
        "target_energy": 0.8,
        "target_instrumentalness": 0.6,
        "seed_genres": ["classical"]
    },
    #ROMANCE COULD BE PROBLEM IN SEED GENRE
    "romantic": {
        "target_valence": 0.7,
        "target_energy": 0.4,
        "target_acousticness": 0.6,
        "seed_genres": ["r-n-b"]
    },
    "focus": {
        "target_valence": 0.4,
        "target_energy": 0.2,
        "target_instrumentalness": 0.8,
        "seed_genres": ["ambient"]
    }
    }
    specificMood = moodFeatures[mood]
    if neededData!="seed_genres":
        return specificMood[neededData]
    else:
        return specificMood[neededData][0]

#Method to get Authorization Token
# - Token acts as a pass to talk to Spotify Servers
# - Spotify won't give data without having a valid token
def getToken():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    if not client_id or not client_secret:
        raise Exception("CLIENT_ID or CLIENT_SECRET not set in environment variables.")

    auth_str = f"{client_id}:{client_secret}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    r = requests.post(url, headers=headers, data=data)
    if r.status_code != 200:
        raise Exception(f"Failed to get token: {r.text}")

    token_info = r.json()
    return token_info["access_token"]

#Queries Spotify API for songs based on genre of user-input mood
def searchTracks(genre, token, limit=10):
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}

    params = {
        "q": genre,    
        "type": "track",
        "limit": limit
    }

    r = requests.get(url, headers=headers, params=params)

    try:
        data = r.json()
        tracks = data["tracks"]["items"]
        results = []
        for t in tracks:
            name = t["name"]
            artist = t["artists"][0]["name"]
            results.append(f"{name} — {artist}")
        return results
    except Exception as e:
        print("Error decoding JSON:", e)
        print("Raw Response:", r.text)
        return []
  

#MAIN  
accessToken = getToken()
print("Welcome to Spotify Playlist Generator!")
print("Please select a mood (input the number, without a period) for your playlist from the following list:\n")
print("1. happy\n2. sad\n3. chill\n4. energetic\n5. dramatic\n6. romantic\n7. focus")


userMood = int(input())
genre = getMoodFeaturesData(userMood, "seed_genres")

tracks = searchTracks(genre, accessToken , limit=5)

# print("\nTop tracks:")
# for t in tracks:
#     print(t)
    
