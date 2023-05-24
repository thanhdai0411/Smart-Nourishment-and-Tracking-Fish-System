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


year, month, day = time.strftime(
        '%Y'), time.strftime('%m'), time.strftime('%d')

date_today =  str(day) + "-" + str(month) + "-" + str(year) 


time_real = "7:00"

get_date_last = collection_name.find().limit(1).sort([('_id',-1)])
date_end = ''

for y in get_date_last :
    time_end = y["time_start"]
    date_end = str(time_end.strftime('%d')) + "-" + str(time_end.strftime('%m')) + "-" + str(time_end.strftime('%Y')) 

if (date_end == date_today ) :
    print("equal")



# print("date_end: ", date_end)

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
        # print("date_call: ", date_call)
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



DATA_FOR_AI = "/home/doan/Desktop/DA/WebServer/Aquarium-Smart/ai_feeder/data_for_ai.json"
SETTING_FOOD = "/home/doan/Desktop/DA/WebServer/Aquarium-Smart/my_data/food_setting.json"


# !

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


# # save file json
with open(DATA_FOR_AI, "w") as outfile:
    outfile.write(json.dumps({"amount_fish": data_predirect, "time" : list_time_data, "day": day}, indent=4, sort_keys=True, default=str))


# !read


data = read_file_json(DATA_FOR_AI)

print(data["amount_fish"])
print(data["time"])
print(data["day"])



# #! predirect
# result_preditect = [[0.1], [0.2], [0.3]]

# #! end predirect


# result_ai = []
# for index, x in enumerate(list_time_data) : 
#     result_final = {}
#     for y in result_preditect:
#         result_final["time"] = str(x)
#         result_final["amount_ai"] = result_preditect[index][0]
#     result_ai.append(result_final)

# print(result_ai)

