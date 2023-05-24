from pymongo import MongoClient

import json
from bson.objectid import ObjectId
import jsonpickle
import datetime

import requests

MONGODB_URL = "mongodb+srv://thanhdai0411:thanhdai0411@cluster0.gsbucce.mongodb.net/?retryWrites=true&w=majority"

db_client=MongoClient()
db_client = MongoClient(MONGODB_URL)
mydatabase = db_client["test"]
collection_name = mydatabase["email_notify"]

email = collection_name.find_one({"username": "Smart"})["email"]


url = "http://0.0.0.0/send_mail"
text_send = f"[{datetime.datetime.now()}]: Dead fish found"

myobj = {'email': email, "text":text_send }

x = requests.post(url, headers = {'User-Agent': 'Mozilla/5.0'}, data = myobj)

print(x.text)

