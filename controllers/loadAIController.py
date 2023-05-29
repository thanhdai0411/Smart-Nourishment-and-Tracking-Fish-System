from constant import AI_FILE_SAVE_MODEL, PATCH_FOOD_SETTING, DATA_FOR_AI, PATH_SATE_LOAD_AI, RGB_START_SYSTEM, RESULT_PREDIRECT_AI
import json
import datetime

import requests
from pymongo import MongoClient


from my_utils.handleFileTXT import  write_file_txt, read_file_txt ,read_file_json, write_file_json

from subprocess import call

MONGODB_URL = "mongodb+srv://thanhdai0411:thanhdai0411@cluster0.gsbucce.mongodb.net/?retryWrites=true&w=majority"

db_client=MongoClient()
db_client = MongoClient(MONGODB_URL)
mydatabase = db_client["test"]
collection_name = mydatabase["amount_fish"]



def loadDetectFishCheck  () :
    load_complete = read_file_txt(PATH_SATE_LOAD_AI)
    if(load_complete) :

        requests.get("http://0.0.0.0/camera/detect")
        
        # write_file_txt(PATH_SATE_LOAD_AI, "")

        # call(["python3",RGB_START_SYSTEM])

# def loadDetect  () :
#     load_complete = read_file_txt(PATH_SATE_LOAD_AI)
#     if(load_complete) :

#         requests.get("http://0.0.0.0/camera/detect")

        



def get_data_ai (time_real) :
        
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

    return data_predirect, list_time_data


    
def load_ai_feeder () :
    print(">>> ai feeder")
    json_object = read_file_json(PATCH_FOOD_SETTING)

    # with open(PATCH_FOOD_SETTING, 'r') as open_file:
    #     json_object = json.load(open_file)

    print(json_object)
    
    list_time = []
    old_food_setting = []
    for x in json_object:
        list_time.append(x["time"])
        old_food_setting.append({
            "time" : x["time"],
            "food_old" : x["amount_food"]
        })

    

    # time_real = ["07:00", "15:00", "22:00"]
    data_predirect, list_time_data = get_data_ai(list_time)
    
    #! read result predirect
    read_result_predirect = read_file_json(RESULT_PREDIRECT_AI)
    data_predirect_save = "4"
    result_predirect = "5"
    compare = []
    if (read_result_predirect) :
        data_predirect_save = read_result_predirect["data"]
        result_predirect = read_result_predirect["result"]

        compare = [x for x in data_predirect if x in data_predirect_save]
    
    print(len(compare), len(data_predirect),len(data_predirect_save) )

    if (len(compare) == len(data_predirect) and len(compare) == len(data_predirect_save) ) :
        loadDetectFishCheck()
        return  {
            "success" : 1, 
            "data" : result_predirect,
            "old_setting": old_food_setting
        } 
    else:
        import tensorflow as tf

        model_save = tf.keras.models.load_model(AI_FILE_SAVE_MODEL)

        #! predirect
        X_new = tf.reshape(data_predirect, (len(data_predirect), len(data_predirect[0]), 1))

        #redirect
        predictions = model_save.predict(X_new)
        
        # result
        result_predictions = predictions.tolist()

        # handle data return 
        result_ai = []
        for index, x in enumerate(list_time_data) : 
            result_final = {}
            for y in result_predictions:
                result_final["time"] = str(x)
                result_final["amount_ai"] = result_predictions[index][0]
            result_ai.append(result_final)



        print("result_ai: ", result_ai)

        write_file_json(RESULT_PREDIRECT_AI, {
            "data" : data_predirect, 
            "result" : result_ai
        })

        
        loadDetectFishCheck()

        return  {
            "success" : 1, 
            "data" : result_ai,
            "old_setting": old_food_setting
        }
    


