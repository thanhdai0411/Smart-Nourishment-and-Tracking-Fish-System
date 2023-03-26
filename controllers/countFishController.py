from pymongo import MongoClient
from constant import MONGODB_URL
import json
from bson.objectid import ObjectId
import jsonpickle



db_client=MongoClient()
db_client = MongoClient(MONGODB_URL)
mydatabase = db_client["test"]
collection_name = mydatabase["amount_fish"]


def get_count_fish() : 
    try :
        item_details = collection_name.find()
        data = []
        for item in item_details:
            item['time_start'] =  str(item['time_start'])
            item['_id'] = str(item['_id'])
            data.append((item))
        
        return jsonpickle.encode(data)
    except(Exception):
        return {
            "success": 0,
            'message': Exception,
        }

def get_count_fish_by_date(date) : 
    try :
        item_details = collection_name.find({"date" : date})
        data = []
        for item in item_details:
            item['time_start'] =  str(item['time_start'])
            item['_id'] = str(item['_id'])
            data.append((item))
        return jsonpickle.encode(data)
    except(Exception):
        return {
            "success": 0,
            'message': Exception,
        }

def get_count_fish_detail(id) : 
    try :
        item_details = collection_name.find_one({"_id" : ObjectId(id)})
        item_details['time_start'] =  str(item_details['time_start'])
        item_details['_id'] = str(item_details['_id'])
        return item_details
    except(Exception):
        return {
            "success": 0,
            'message': Exception,
        }
