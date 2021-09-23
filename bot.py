import json
import os as _os
import tweepy
import mysql.connector
from mysql.connector import Error
from pymongo import MongoClient
import dotenv as _dotenv
_dotenv.load_dotenv()   
           
API_KEY = _os.environ["TWITTER_API_KEY"]
SECRET_KEY = _os.environ["TWITTER_API_SECRET_KEY"]
ACCESS_TOKEN = _os.environ["TWITTER_ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = _os.environ["TWITTER_ACCESS_TOKEN_TOKEN_SECRET"]
DBSOURCEFINAL = _os.environ["MY_DB_ACCESS"]
USER_DB = _os.environ["MY_USER_DB"]
PASS_DB = _os.environ["MY_PASS_DB"]
HOST_DB = _os.environ["MY_HOST_DB"]

myclient = MongoClient(DBSOURCEFINAL, connect=False) 
db = myclient.get_database("twitter")
records = db.data


def connectUser(us_id, us_id_str, us_name, us_screen_name, us_location, us_url, us_description, us_protected,
                        us_verified, us_followers_count, us_friends_count, us_listed_count,
                        us_favourites_count, us_statuses_count, us_created_at, us_utc_offset,
                        us_time_zone, us_profile_background_color, us_profile_background_image_url,
                        us_profile_background_image_url_https, us_profile_background_tile):
    """
    connect to MySQL database and insert twitter data
    """
    try:
        con = mysql.connector.connect(host=HOST_DB,
                                      database='tweepy', user=USER_DB, password=PASS_DB, charset='utf8')
        if con.is_connected():
            """
            Insert twitter data
            """
            cursor = con.cursor()
            # twitter, golf
            cursor.execute('SET NAMES utf8mb4')
            cursor.execute("SET CHARACTER SET utf8mb4")
            cursor.execute("SET character_set_connection=utf8mb4")


            #aGregar codigo insertar mysql
            query = "INSERT INTO tweet (created_at, id, id_str, usuario_id, text, source, truncated, " \
                    "in_reply_to_status_id, in_reply_to_status_id_str, in_reply_to_user_id, in_reply_to_user_id_str, " \
                    "in_reply_to_screen_name, geo, coordinates, place, contributors, is_quote_status, quote_count," \
                    " reply_count, retweet_count, favorite_count, filter_level," \
                    " lang, timestamp_ms) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                    "%s, %s, %s, %s, %s, %s, %s, %s) "
            cursor.execute(query, (created_at, id, id_str, usario_id, text, source, truncated, in_reply_to_status_id,
                                   in_reply_to_status_id_str, in_reply_to_user_id, in_reply_to_user_id_str, in_reply_to_screen_name,
                                   geo, coordinates, place, contributors, is_quote_status, quote_count, reply_count, retweet_count,
                                   favorite_count, filter_level, lang, timestamp_ms))

            con.commit()
    except Error as e:
        print(e)
    cursor.close()
    con.close()
    return


class TweetsListener(tweepy.StreamListener):
    def on_connect(self):
        print("Estoy conectado!")

    def on_status(self, status):
        if status.text.startswith("@IbaiLlanos"):
            print(type(status))
            print(type(status._json))
            print(f'{status.text} - {status.user.name} - {status.user.screen_name} - {status.user.location}')
            connectUser(status.user.id, status.user.id_str, status.user.name, status.user.screen_name,
                        status.user.location, status.user.url, status.user.description, status.user.protected,
                        status.user.verified, status.user.followers_count, status.user.friends_count, status.user.listed_count,
                        status.user.favourites_count, status.user.statuses_count, status.user.created_at, status.user.utc_offset,
                        status.user.time_zone, status.user.profile_background_color, status.user.profile_background_image_url,
                        status.user.profile_background_image_url_https, status.user.profile_background_tile)
            with open('data.json', 'w') as file:
                json.dump(status._json, file, indent=4)
            with open('data.json') as file: 
                file_data = json.load(file) 
                records.insert_one(file_data) 

    def on_error(self, status_code):
        print("Error", status_code)

def get_twitter_api():
    auth = tweepy.OAuthHandler(API_KEY, SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    apiTwitter = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return apiTwitter

def run():
    _streamClass = TweetsListener()
    _apiTwitter = get_twitter_api()
    streamingApi = tweepy.Stream(auth=_apiTwitter.auth, listener=_streamClass)
    streamingApi.filter(follow=['2754746065'])

if name == "main":
    run()