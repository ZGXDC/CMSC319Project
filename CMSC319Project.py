from dotenv import load_dotenv
import os

load_dotenv()

clientID = os.getenv("CLIENT_ID")
clientSecret = os.getenv("CLIENT_SECRET")

print(clientID, clientSecret)