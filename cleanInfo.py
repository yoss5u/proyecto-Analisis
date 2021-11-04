import re as regex
import json
from pymongo import MongoClient
from datetime import datetime

myClient = MongoClient(MONGODB, connect=False) 
db = myClient.get_database("twitter")
records = db.data

myLocalClient = MongoClient('localhost', 27017) 
dbLocal = myLocalClient.get_database('finaltwitter')
documentLocal = dbLocal.dataelon


def cleanInformation():
    count = 0
    x = records.find() 
    for data in x:
        if data["place"] is None:
            place_user = False
        else:   
            place_user = data["place"]["country"]
        document = {
            'date': datetime.strftime(datetime.strptime(data["created_at"],'%a %b %d %H:%M:%S +0000 %Y'), '%d-%m-%Y'),
            'id_tweet': data["id_str"],
            'text_tweet': data["text"],
            'source': regex.findall(r"\>(.*?)\<", data["source"])[0],
            'user_id': data["user"]["id_str"],
            'user_name': data["user"]["screen_name"],
            'user_protected': data["user"]["protected"],
            'user_verified': data["user"]["verified"],
            'user_created_profile': datetime.strftime(datetime.strptime(data["user"]["created_at"],'%a %b %d %H:%M:%S +0000 %Y'), '%d-%m-%Y'),
            'geolocation': data["geo"],
            'coordinates': data["coordinates"],
            'place_country': place_user,
            'lenguage': data["lang"]  
        }
        with open("dataClean.json", "w") as file:
            json.dump(document, file, indent=4)
        
        with open('dataClean.json') as file:                            
            file_data = json.load(file) 
            documentLocal.insert_one(file_data)
        count += 1
        print(count)

cleanInformation()