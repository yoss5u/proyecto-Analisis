import json
import os as _os
import tweepy
from pymongo import MongoClient
import dotenv as _dotenv
_dotenv.load_dotenv()   
           
API_KEY = _os.environ["TWITTER_API_KEY"]
SECRET_KEY = _os.environ["TWITTER_API_SECRET_KEY"]
ACCESS_TOKEN = _os.environ["TWITTER_ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = _os.environ["TWITTER_ACCESS_TOKEN_TOKEN_SECRET"]
DBSOURCEFINAL = _os.environ["MY_DB_ACCESS"]

myclient = MongoClient(DBSOURCEFINAL, connect=False) 
db = myclient.get_database("twitter")
records = db.data

class TweetsListener(tweepy.StreamListener):
    def on_connect(self):
        print("Estoy conectado!")

    def on_status(self, status):
        if status.text.startswith("@IbaiLlanos"):
            print(type(status))
            print(type(status._json))
            print(f'{status.text} - {status.user.name} - {status.user.screen_name} - {status.user.location}')
            with open('data.json', 'w') as file:
                json.dump(status._json, file, indent=4)
            with open('data.json') as file: 
                file_data = json.load(file) 
                records.insert_one(file_data) 

    def on_error(self, status_code):
        print("Error", status_code)
