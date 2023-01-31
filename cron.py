import datetime
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
from constant import BROKER_URL, BROKER_PORT, BROKER_USERNAME, BROKER_PASSWORD, PATCH_COUNT_FISH


def write_file_json(data_write) : 
    with open(PATCH_FOOD_SETTING, "w") as open_file:
        open_file.write(json.dumps(data_write))

def read_file_json() : 
    with open(PATCH_FOOD_SETTING, 'r') as open_file:
            json_object = json.load(open_file)
    return json_object   



def cron_food(loop_on):
    try:
        def on_connect(client, userdata, flags, rc, properties=None):
            print("Connect MQTT Crond ")

        def on_publish(client, userdata, mid, properties=None):
            print("mid: " + str(mid))

        def on_subscribe(client, userdata, mid, granted_qos, properties=None):
            print("Subscribed: " + str(mid) + " " + str(granted_qos))

        def on_message(client, userdata, msg):
            print(msg.topic + ": " + str(msg.payload))
            controlLamp = msg.topic == "control_lamp"
            controlAIFood = msg.topic == "control_ai_food"
            controlFood = msg.topic == "control_food"

            if(controlLamp and msg.payload == b'1'):
                print('ON LAMP')
            if(controlLamp and msg.payload == b'0'):
                print('OFF LAMP')

            # !===============================================================
            if(controlAIFood and msg.payload == b'1'):
                print('ON AI FOOD')
                try :
                    

                    json_object = read_file_json()
                    
                    json_object.append({'username': "MODE_AI"})

                    write_file_json(json_object)
                    
                except Exception:
                    handle_exception()
                
    
            if(controlAIFood and msg.payload == b'0'):
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
                

            # !===============================================================

            if(controlFood and msg.payload == b'1'):
                print('ON FOOD TIME')
            if(controlFood and msg.payload == b'0'):
                print('OFF FOOD TIME')

        client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
        client.on_connect = on_connect

        client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        # set username and password
        client.username_pw_set(BROKER_USERNAME, BROKER_PASSWORD)
        client.connect(BROKER_URL, BROKER_PORT)

        client.on_subscribe = on_subscribe
        client.on_message = on_message
        client.on_publish = on_publish

        # subscribe to all topics of encyclopedia by using the wildcard "#"
        client.subscribe("control_lamp", qos=1)
        client.subscribe("control_ai_food", qos=1)
        client.subscribe("control_food", qos=1)

        # client.publish("encyclopedia/temperature", payload="hot", qos=1)

        # client.loop()
        client.loop_start()

        while True:
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

                            # print(time_setting, amount_food)

                            dt_obj = datetime.datetime.now()

                            time_on = dt_obj.replace(hour=int(hour), minute=int(minute), second=0,microsecond=0)

                            time_present = dt_obj.replace(hour=dt_obj.hour, minute=dt_obj.minute,
                                                        second=dt_obj.second, microsecond=0)
                            if(time_on == time_present ):
                                print('Hey Hey , Cron Food')

                                json_object = read_file_json()
                                json_object.append({'username': "START_CRON"})
                                write_file_json(json_object)

                                call(['python', PATCH_COUNT_FISH])
                                id = food["_id"]["$oid"]
                                complete = str(id) + "=COMPLETE"
                                client.publish("food_complete", payload=complete, qos=1)
                    else:
                        print('Not setting food')

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

