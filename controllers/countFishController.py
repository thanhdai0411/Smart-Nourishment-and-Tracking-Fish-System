from pymongo import MongoClient
from constant import MONGODB_URL, DATA_FOR_AI
import json
from bson.objectid import ObjectId
import jsonpickle
import datetime



db_client=MongoClient()
db_client = MongoClient(MONGODB_URL)
mydatabase = db_client["test"]
collection_name = mydatabase["amount_fish"]


def get_count_fish() : 
        
    # get last date for check
    get_date_last = collection_name.find().limit(1).sort([('_id',-1)])
    date_end = ''

    for y in get_date_last :
        time_end = y["time_start"]
        date_end = str(time_end.strftime('%d')) + "-" + str(time_end.strftime('%m')) + "-" + str(time_end.strftime('%Y')) 

    print("date_end: ", date_end)

    #  main handle
    item_details = collection_name.find()
    data = []
    for item in item_details:
        data.append((item))

    data_final  = []

    for x in data:
        
        time_run = x["time_start"]

        
        date_call = str(time_run.strftime('%d')) + "-" + str(time_run.strftime('%m')) + "-" + str(time_run.strftime('%Y')) 
        if(date_end == date_call):
            print("date_call: ", date_call)
            list_data_fish_count = x["fish_count"]  

            list_amount_fish = []

            for data_fc in list_data_fish_count :
                list_amount_fish.append(data_fc["amount"])

            data_final.append({
                "time" : time_run, 
                "list_amount_fish" : list_amount_fish

            })
        
    # tim max_length de add cho tat ca cac lish_amount_fish bang nhau de tao dataframe
    max_length = max(len(d["list_amount_fish"]) for d in data_final)

    # loop data de add cho bang nhau het
    for i, d in enumerate(data_final):
        padded_array = d["list_amount_fish"] + [0] * (max_length - len(d["list_amount_fish"]))

        d["list_amount_fish"] = padded_array

        
        
    data_predirect = []
    list_time_data = []
    day = ""

    for x in data_final :
        amount_food = x["list_amount_fish"]
        time_food = x["time"]

        time_food = datetime.datetime.strptime(str(time_food), '%Y-%m-%d %H:%M:%S.%f')

        print(time_food)

        time = time_food.strftime("%H:%M")
        day = time_food.strftime("%d-%m-%Y")

        list_time_data.append(time)
        data_predirect.append(amount_food)

   
    with open(DATA_FOR_AI, "w") as outfile:
        outfile.write(json.dumps({"amount_fish": data_predirect, "time" : list_time_data, "day" : day}, indent=4, sort_keys=True, default=str))





    return "OK"

            


def get_count_fish_last() : 
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
