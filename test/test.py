from pymongo import MongoClient
import json
from bson.objectid import ObjectId
import jsonpickle
import time
import datetime


def read_file_json(file) :
    with open(file, 'r') as open_file:
            json_object = json.load(open_file)
    return json_object   



MONGODB_URL = "mongodb+srv://thanhdai0411:thanhdai0411@cluster0.gsbucce.mongodb.net/?retryWrites=true&w=majority"

db_client=MongoClient()
db_client = MongoClient(MONGODB_URL)
mydatabase = db_client["test"]
collection_name = mydatabase["amount_fish"]

# get last date for check
time_real = ["07:00", "15:00", "22:00", "08:00"]

def get_data_ai () :
        
    get_date_last = collection_name.find()
    data_test = {}
    time_exist = []
    for y in get_date_last :
        time_end = y["time_start"]
        list_data_fish_count = y["fish_count"] 

        data_food = str(time_end.strftime('%d')) + "-" + str(time_end.strftime('%m')) + "-" + str(time_end.strftime('%Y')) 
        time_food = str(time_end.strftime('%H')) + ":" + str(time_end.strftime('%M')) 

        list_data_real  = []

        if (time_food in time_real) :
            time_exist.append(time_food)
            list_amount_fish = []
            for data_fc in list_data_fish_count :
                list_amount_fish.append(data_fc["amount"])
            
            data_test[time_food] = list_amount_fish
       

    time_exist = list(set(time_exist))
    data_predirect = []

    for x in time_exist :
        if(data_test[x]) :
            data_predirect.append(data_test[x])

    # print(data_predirect)

    data_final = []

    for y in data_predirect : 

        key_list = list(data_test.keys())
        val_list = list(data_test.values())
        
        position = val_list.index(y)

        # print(key_list[position])

        data_final.append({
            "time" : key_list[position], 
            "list_amount_fish" : y
        })


    max_length = max(len(d["list_amount_fish"]) for d in data_final)

    # loop data de add cho bang nhau het
    for i, d in enumerate(data_final):
        padded_array = d["list_amount_fish"] + [0] * (max_length - len(d["list_amount_fish"]))

        d["list_amount_fish"] = padded_array


    data_predirect = []
    list_time_data = []
    for x in data_final :
        amount_food = x["list_amount_fish"]
        time_food = x["time"]

    

        list_time_data.append(time_food)
        data_predirect.append(amount_food)


    # print(data_predirect)
    # print(list_time_data)

    return data_predirect, list_time_data

d,t = get_data_ai()

print(t, d)

# # #! predirect
# result_preditect = [[0.1], [0.2], [0.3]]

# # #! end predirect


# result_ai = []
# for index, x in enumerate(list_time_data) : 
#     result_final = {}
#     for y in result_preditect:
#         result_final["time"] = str(x)
#         result_final["amount_ai"] = result_preditect[index][0]
#     result_ai.append(result_final)

# print(result_ai)


