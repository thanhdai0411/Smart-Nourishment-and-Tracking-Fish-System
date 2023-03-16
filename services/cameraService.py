import datetime
import io
import os
import time
from threading import Thread


import cv2
import numpy as np
import torch
from flask import (Flask, Response, flash, redirect, render_template, request,
                   url_for)
from PIL import Image
from pymongo import MongoClient
from flask_session import Session
from my_utils.jsonFile import write_file_json,read_file_json



# from constant import PATH_MODEL_FISH_DIE
from constant import BROKER_URL, BROKER_PORT, BROKER_USERNAME, BROKER_PASSWORD,PATH_MODEL_FISH_DIE,PATH_SAVE_STATE_LOAD_FISH_DIE,PATH_SAVE_TIME_SEND_MAIL
import paho.mqtt.client as paho
from paho import mqtt

from constant import BROKER_URL, BROKER_PORT, BROKER_USERNAME, BROKER_PASSWORD,MONGODB_URL,PATCH_COUNT_FISH

from subprocess import call

db_client=MongoClient()
db_client = MongoClient(MONGODB_URL)
mydatabase = db_client["test"]
collection_name = mydatabase["amount_fish"]


#!MQTT SETUP ==========================================================

def on_connect(client, userdata, flags, rc, properties=None):
    print("Camera service connect mqtt %s." % rc)

def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    print(msg.topic + ": " + str(msg.payload))  
    


    
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set(BROKER_USERNAME, BROKER_PASSWORD)
client.connect(BROKER_URL, BROKER_PORT)

client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish


client.loop_start()

#! END SETUP MQTT =======================================================================================


# TIME_DURATION = datetime.datetime.now() + datetime.timedelta(minutes=DURATION)


def generate_frames_detect():
    # open(PATH_SAVE_STATE_LOAD_FISH_DIE, 'w').write("")
   

    model = torch.hub.load('.', 'custom', path=PATH_MODEL_FISH_DIE, source='local')

    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    while True:
        success, frame = camera.read()
        if success:
            ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
            frame = buffer.tobytes()

            # =====================================

            img = Image.open(io.BytesIO(frame))
            results = model(img)
            # results = model(img)
            # results.print()

            count_detect = results.pandas().xyxy[0]['name']
            list_count_detect = list(count_detect) 
            
            if(len(list_count_detect) > 0) :
                print('Die count: ' + str(len(list_count_detect)))

            img = np.squeeze(results.render())  # RGB
            # read image as BGR
            img_BGR = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            frame = cv2.imencode('.jpg', img_BGR)[1].tobytes()
            

            already_load = open(PATH_SAVE_STATE_LOAD_FISH_DIE , 'r').read()
            if already_load :
                camera.release()
                break
            

            
            # =====================================

            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        else:
            pass

    
def generate_frames_detect_fish_die():



    # already_load = open(PATH_SAVE_STATE_LOAD_FISH_DIE , 'r').read()
    # model = ""
    # if not already_load :
    # open(PATH_SAVE_STATE_LOAD_FISH_DIE, 'w').write("ALREADY")

    print("load model fish die ...")

    model = torch.hub.load('.', 'custom', path=PATH_MODEL_FISH_DIE, source='local')

    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    time_send = None
    DURATION = 60


    

    while True:
        success, frame = camera.read()
        if success:
            ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
            frame = buffer.tobytes()

            # =====================================

            img = Image.open(io.BytesIO(frame))
            results = model(img)
            # results = model(img)
            # results.print()

            count_detect = results.pandas().xyxy[0]['name']
            list_count_detect = list(count_detect) 
            # if datetime.datetime.now() > TIME_DURATION:
            time_send_mail = open(PATH_SAVE_TIME_SEND_MAIL , 'r').read()
            print(time_send_mail)

            if time_send_mail : 
                datetime_object = datetime.datetime.fromisoformat(time_send_mail.strip())

                if(len(list_count_detect) > 0 and  datetime.datetime.now() >= datetime_object) :
                    time_send = datetime.datetime.now()  + datetime.timedelta(minutes=DURATION)
                    open(PATH_SAVE_TIME_SEND_MAIL , 'w').write(str(time_send))

                    print('Die count: ' + str(len(list_count_detect)))
                    client.publish("fish_die", payload=str(len(list_count_detect)), qos=1)
                    
            elif(len(list_count_detect) > 0) :
                time_send = datetime.datetime.now()  + datetime.timedelta(minutes=DURATION)
                open(PATH_SAVE_TIME_SEND_MAIL , 'w').write(str(time_send))

                print('Die count: ' + str(len(list_count_detect)))
                client.publish("fish_die", payload=str(len(list_count_detect)), qos=1)


            img = np.squeeze(results.render())  # RGB
        
            img_BGR = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            frame = cv2.imencode('.jpg', img_BGR)[1].tobytes()

            # release
            already_load = open(PATH_SAVE_STATE_LOAD_FISH_DIE , 'r').read()
            if already_load :
                camera.release()
                break

            

            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        else:
            pass
    # else :
    #     print("model: " + str(model))
    #     return 'ok'
    

def generate_frames():
    # open(PATH_SAVE_STATE_LOAD_FISH_DIE, 'w').write("")

    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

    

    while True:
        success, frame = camera.read()
        if success:


            ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
            frame = buffer.tobytes()

            

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        else:
            # print("fail open camera")
            # print(success)
            pass

def generate_frames_count_fish():
    # # open(PATH_SAVE_STATE_LOAD_FISH_DIE, 'w').write("")

    
    PATH = "D:\\Studyspace\\DoAn\\Aquarium\\my_data\\12.mp4"
    camera = cv2.VideoCapture(PATH)
    # camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # camera.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
    
    year, month, day = time.strftime(
            '%Y'), time.strftime('%m'), time.strftime('%d')

    date_start =  str(day) + "-" + str(month) + "-" + str(year) 
    # now_start = datetime.datetime.now().strftime("%H:%M:%S.%f")
    now_start = datetime.datetime.now()



    init_data = {
        "date" : date_start,
        "time_start" : now_start,
        "fish_count" : []
    }

    collection_name.insert_one(init_data)

    item_details = collection_name.find_one({"time_start" : now_start})
    data_start_trans = str(1)+"="+str(item_details["_id"])
    client.publish("feed_fish", payload=data_start_trans, qos=1)




    DURATION = 30

    EDGE_TOP = 50
    EDGE_RIGHT = 500
    EDGE_BOTTOM = 350
    EDGE_LEFT = 100

    TIME_DURATION = datetime.datetime.now() + datetime.timedelta(seconds=DURATION)
    # time_duration = datetime.datetime.now()+datetime.timedelta(minutes=DURATION)

    

    while True:
        success, frame = camera.read()
        if success:
            img_cvt = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_cvtc = img_cvt.copy()
            cv2.rectangle(img_cvtc, (EDGE_LEFT, EDGE_TOP),
                  (EDGE_RIGHT, EDGE_BOTTOM), (0, 0, 255), 5)

            ROI = img_cvt[EDGE_TOP:EDGE_BOTTOM, EDGE_LEFT:EDGE_RIGHT]

            gray = cv2.cvtColor(ROI, cv2.COLOR_RGB2GRAY)
            blur = cv2.GaussianBlur(gray, (15, 15), 0)

            ret, threshold = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)

            contours, hierarchy = cv2.findContours(
                threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            cnt_info = []

            fish_contour = np.zeros(threshold.shape)
            count = 0
            for cnt in contours:

                area = round(cv2.contourArea(cnt))

                if area > 50 and 0 not in cnt:

                    if 0 or threshold.shape[1] - 1 not in (cnt[i][0][0] for i in range(len(cnt))):

                        if 0 or threshold.shape[0] - 1 not in (cnt[i][0][1] for i in range(len(cnt))):

                            cv2.drawContours(fish_contour, [cnt], 0, 255, -1)

                            count = count + 1


            print("Count fish : " + str(count))
            
            year, month, day = time.strftime(
                '%Y'), time.strftime('%m'), time.strftime('%d')

            # now = datetime.datetime.now().strftime("%H:%M:%S.%f")
            now = datetime.datetime.now()

            date_push =  str(day) + "-" + str(month) + "-" + str(year) 
            fish_count =  {"time" : now,"amount" : count}

            data_trans =  str(now) + "=" + str(count)

            client.publish("count_fish", payload=data_trans, qos=1)

            collection_name.update_one({"date" : date_push,"time_start" : now_start},{"$push" : {"fish_count" :fish_count}})
            

            time.sleep(0.3)

            if datetime.datetime.now() > TIME_DURATION:
                data_start_trans = str(0)+"="+str(item_details["_id"])
                # client.publish("feed_fish", payload=data_start_trans, qos=1)
                client.publish("start_eat", payload='0', qos=1)
                break



            ret, buffer = cv2.imencode('.jpg', cv2.flip(img_cvtc, 1))
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        else:
            # print("fail open camera")
            # print(success)
            pass

def handle_fail_open_camera() :
    print("")

def start_generate_frames():
    global camera, state_open_camera
    camera = cv2.VideoCapture(0)

def stop_generate_frames():
    global camera, state_open_camera
    camera.release()
    cv2.destroyAllWindows()

def record(out):
    global rec_frame
    while(rec):
        time.sleep(0.05)
        out.write(rec_frame)

def capture_screen():
    global capture
    capture = 1

def record_screen():
    global rec, out
    rec = not rec
    if(rec):
        now = datetime.datetime.now()
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('./public/record_camera/vid_{}.avi'.format(
            str(now).replace(":", '')), fourcc, 20.0, (640, 480))
        # Start new thread for recording the video
        thread = Thread(target=record, args=[out, ])
        thread.start()
    elif(rec == False):
        out.release()
