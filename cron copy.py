from pymongo import MongoClient

import datetime
import time
from time import sleep
from constant import PATCH_FOOD_SETTING
from my_models.foodModel import Food
from flask import request
from multiprocessing import Process, Value
import json
import os
import paho.mqtt.client as paho
from paho import mqtt
from subprocess import call
from constant import BROKER_URL, BROKER_PORT, BROKER_USERNAME, BROKER_PASSWORD, PATCH_COUNT_FISH, MONGODB_URL,PATH_SAVE_STATE_LOAD_FISH_DIE, PATH_SAVE_INFO_FEEDER, PATH_SAVE_DATE_UPDATE_DAILY_FOOD, PATH_SAVE_STATE_LOAD_MODEL_DETECT

from bson.objectid import ObjectId
import random
import requests

import serial


serial_port = serial.Serial(
        port = "/dev/ttyTHS1",
        baudrate = 115200,
       bytesize = serial.EIGHTBITS,
       parity = serial.PARITY_NONE,
       stopbits = serial.STOPBITS_ONE, 
       timeout = 1 ,
       xonxoff = False, 
       rtscts = False,
       dsrdtr = False, 
       writeTimeout = 1
)

from bson.objectid import ObjectId

# connect db

db_client=MongoClient()
db_client = MongoClient(MONGODB_URL)
mydatabase = db_client["test"]
collection_name = mydatabase["food"]

item_details = collection_name.find_one({"_id" : ObjectId("6440c184405d93a255bea871")})

print("item detail: ", item_details)




def write_file_json(data_write) : 
    with open(PATCH_FOOD_SETTING, "w") as open_file:
        open_file.write(json.dumps(data_write))

def read_file_json() : 
    with open(PATCH_FOOD_SETTING, 'r') as open_file:
            json_object = json.load(open_file)
    return json_object   

def serial_send(payload) :
    data_send = payload.decode("utf-8")  + '\n'
    print(data_send)
    serial_port.write(data_send.encode())

def check_state_device () :
        
    api_url = "http://0.0.0.0/state_device/get/led"
    response = requests.get(api_url)
    data = json.loads(response.json()['data'])[0]['state']
    serial_send(data.encode())

    api_url = "http://0.0.0.0/state_device/get/pump"
    response = requests.get(api_url)
    data = json.loads(response.json()['data'])[0]['state']
    serial_send(('L' + data + 'E').encode())

def update_food_daily() :
    year, month, day = time.strftime(
                    '%Y'), time.strftime('%m'), time.strftime('%d')

    date_start =  str(day) + "-" + str(month) + "-" + str(year) 

    read_date = open(PATH_SAVE_DATE_UPDATE_DAILY_FOOD , 'r').read()

    if(not read_date) :
        open(PATH_SAVE_DATE_UPDATE_DAILY_FOOD, 'w').write(date_start)

    # print(read_date.strip(),date_start)

    if(read_date.strip() != date_start ) :
        open(PATH_SAVE_DATE_UPDATE_DAILY_FOOD, 'w').write(date_start)
        api_url = "http://0.0.0.0/food/update_daily"
        response = requests.get(api_url)


def cron_food(loop_on):
        
    check_state_device()
    
    try:
        def on_connect(client, userdata, flags, rc, properties=None):
            print(">>>>> Connect MQTT Crond <<<< ")

        def on_publish(client, userdata, mid, properties=None):
            print("mid: " + str(mid))

        def on_subscribe(client, userdata, mid, granted_qos, properties=None):
            print("Subscribed: " + str(mid) + " " + str(granted_qos))

        def on_message(client, userdata, msg):
            print(msg.topic + ": " + str(msg.payload))
            controlAIFood = msg.topic == "control_ai_food"
            controlRGB = msg.topic == "rgb_control"
            controlRelay = msg.topic == "relay_control"
            controlMotor = msg.topic == "motor_control"
            # controlFood = msg.topic == "control_food"

           

            # !===============================================================
            if(controlAIFood and msg.payload == b'1'):
                print('ON AI FOOD')
                try :
                    

                    json_object = read_file_json()
                    
                    json_object.append({'username': "MODE_AI"})

                    write_file_json(json_object)
                    
                except Exception:
                    handle_exception()
            elif(controlAIFood and msg.payload == b'0'):
                print('OFF AI FOOD')
                
                try :
                    
                    json_object = read_file_json()

                    length = len(json_object)
                    modeAI =  json_object[length-1]["username"]

                    if(modeAI == "MODE_AI") :
                        json_object.remove({'username': "MODE_AI"})
                        write_file_json(json_object)

                        

                except Exception :
                    handle_exception()
            elif (controlRGB):

                serial_send(msg.payload)

            elif (controlRelay):
              
                serial_send(msg.payload)

            elif (controlMotor):
                serial_send(msg.payload)

    
            # !===============================================================

            
        num = random.random()
        client = paho.Client("cron"+ str(num))
        # client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
        client.on_connect = on_connect

        # client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        # set username and password
        client.username_pw_set(BROKER_USERNAME, BROKER_PASSWORD)
        client.connect(BROKER_URL, BROKER_PORT)

        client.on_subscribe = on_subscribe
        client.on_message = on_message
        client.on_publish = on_publish

        # subscribe to all topics of encyclopedia by using the wildcard "#"
        client.subscribe("control_ai_food", qos=1)
        client.subscribe("rgb_control", qos=1)
        client.subscribe("relay_control", qos=1)
        client.subscribe("motor_control", qos=1)


        # client.loop()
        client.loop_start()

        while True:
            # !update status food daily 
            update_food_daily()

            #! delete check state model for next load   
            # state_model = open(PATH_SAVE_STATE_LOAD_MODEL_DETECT, 'r').read()

            # if(state_model) :
            #     open(PATH_SAVE_STATE_LOAD_MODEL_DETECT, 'w').write("")



            
            if loop_on.value == True :



                # foods = open(PATCH_FOOD_SETTING, "r").read()
                fileEmpty = os.stat(PATCH_FOOD_SETTING).st_size == 0
                fileSize = os.stat(PATCH_FOOD_SETTING).st_size
                if not fileEmpty and fileSize > 2  : 

                    
                    json_object = read_file_json()

                    length = len(json_object) 
                    mode =  json_object[length-1]["username"]

                    if json_object and length > 0 and not mode == "MODE_AI" and not mode == "START_CRON" :
                        for food in json_object:

                            time_setting = food["time"]
                            hour = time_setting.split(":")[0]
                            minute = time_setting.split(":")[1]
                            amount_food = food["amount_food"]
                            
                           
                            dt_obj = datetime.datetime.now()

                            time_on = dt_obj.replace(hour=int(hour), minute=int(minute), second=0,microsecond=0)

                            time_present = dt_obj.replace(hour=dt_obj.hour, minute=dt_obj.minute,
                                                        second=dt_obj.second, microsecond=0)
                            if(time_on == time_present ):

                                open(PATH_SAVE_STATE_LOAD_FISH_DIE, 'w').write("ALREADY_FEED")
                                print('Hey Hey , Cron Food'  + str(time_on) + " Lượng thức ăn: " + str(amount_food))


                                json_object = read_file_json()
                                json_object.append({'username': "START_CRON"})
                                write_file_json(json_object)
                                
                                id = food["_id"]["$oid"]
                                
                                client.publish("start_eat", payload='0', qos=1)

                                # client.publish("rgb_control", payload="R255G255B255E", qos=1)
                                serial_send("R255G255B255E".encode())
                                sleep(1)

                                open(PATH_SAVE_INFO_FEEDER, 'w').write(amount_food)


                                # RUN MOTOR
                                controlMotor =  "M" + str(int(float(amount_food)*1000)) + "E"
                                print( "motor control : "+ str(controlMotor))

                                serial_send(controlMotor.encode())
                                # client.publish("motor_control", payload=str(controlMotor), qos=1)

                                # CALL COUNT FISH
                                call(['python3', PATCH_COUNT_FISH])

                                # COMPLETE COUNT FISH
                                open(PATH_SAVE_STATE_LOAD_FISH_DIE, 'w').write("")

                                complete = str(id) + "=COMPLETE"

                                client.publish("start_eat", payload=complete, qos=1)
                                
                    else:
                        print('Not setting food')
                        sleep(1)
                        if(mode == "START_CRON") :
                            json_object.remove({'username': "START_CRON"})
                            write_file_json(json_object)
                            

                        
            sleep(1)

        
    except Exception:
        print("Thoat Crond")
        handle_exception()

def handle_exception():
    print("handle_exception")
    recording_on = Value('b', True)
    cron_food(recording_on)
