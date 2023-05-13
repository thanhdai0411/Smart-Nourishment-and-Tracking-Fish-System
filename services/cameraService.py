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
from constant import BROKER_URL, BROKER_PORT, BROKER_USERNAME, BROKER_PASSWORD,PATH_MODEL_FISH_DIE,PATH_SAVE_STATE_LOAD_FISH_DIE,PATH_SAVE_TIME_SEND_MAIL, PATH_MODEL_FISH_NAME
import paho.mqtt.client as paho
from paho import mqtt

from constant import BROKER_URL, BROKER_PORT, BROKER_USERNAME,PATH_MODEL_USER_CUSTOM_NAME, BROKER_PASSWORD,MONGODB_URL,PATCH_COUNT_FISH, PATH_SAVE_STATE_LOAD_MODEL_DETECT

from subprocess import call
import random

db_client=MongoClient()
db_client = MongoClient(MONGODB_URL)
mydatabase = db_client["test"]
collection_name = mydatabase["amount_fish"]

# model_check =  open(PATH_SAVE_STATE_LOAD_MODEL_DETECT, 'r').read()
# model = None

# model_load = torch.hub.load('/home/doan/Desktop/DA/WebServer/Aquarium-Smart', 'custom', path=PATH_MODEL_FISH_NAME, source='local')
# print("model_start: ", model_load)
# model = model_load

# if(not model_check) :1
#     model_load = torch.hub.load('/home/doan/Desktop/DA/WebServer/Aquarium-Smart', 'custom', path=PATH_MODEL_FISH_NAME, source='local')
#     print("model_start: ", model_load)
#     model = model_load
#     open(PATH_SAVE_STATE_LOAD_MODEL_DETECT, 'w').write("ALREADY_FEED")



#   Frame size: 640x480
#     Frame rates: 30, 20, 10
#   Frame size: 352x288
#     Frame rates: 30, 20, 10
#   Frame size: 320x240
#     Frame rates: 30, 20, 10
#   Frame size: 176x144
#     Frame rates: 30, 20, 10
#   Frame size: 160x120
#     Frame rates: 30, 20, 10


#!MQTT SETUP ==========================================================

def on_connect(client, userdata, flags, rc, properties=None):
    print(">>>>>>Camera MQTT service connect mqtt %s. <<" % rc)

def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    print(msg.topic + ": " + str(msg.payload))  
    


    
# client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
num = random.random()
client = paho.Client("camera_service" + str(num))
client.on_connect = on_connect

# client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set(BROKER_USERNAME, BROKER_PASSWORD)
client.connect(BROKER_URL, BROKER_PORT)

client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

client.loop_start()

# client.loop_start()

#! END SETUP MQTT =======================================================================================


# TIME_DURATION = datetime.datetime.now() + datetime.timedelta(minutes=DURATION)

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)


def generate_frames_detect():
    # open(PATH_SAVE_STATE_LOAD_FISH_DIE, 'w').write("")
   
    # client.publish("load_model_stream", payload="1", qos=1)
    # model = torch.hub.load('.', 'custom', path="", source='local')
    model = torch.hub.load('/home/doan/Desktop/DA/WebServer/Aquarium-Smart', 'custom', path=PATH_MODEL_FISH_NAME, source='local')
    # print("model_load: ", model)
    
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    client.publish("load_model_stream", payload="0", qos=1)

    while True:
        success, frame = camera.read()
        if success:
            ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
            frame = buffer.tobytes()

            # =====================================

            img = Image.open(io.BytesIO(frame))

            # model.conf = 0.5
            # iou = 0.45
            
            results = model(img)
            
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



    print("load model fish die ...")
    model = torch.hub.load('/home/doan/Desktop/DA/WebServer/Aquarium-Smart', 'custom', path=PATH_MODEL_FISH_DIE, source='local')


    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
    time_send = None
    DURATION = 60
    

    while True:
        success, frame = camera.read()
        if success:
            
            ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
            frame = buffer.tobytes()
            # =====================================
            img = Image.open(io.BytesIO(frame))

            model.conf = 0.6
            iou = 0.45

            results = model(img)


            img = np.squeeze(results.render())  # RGB
        
            img_BGR = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            width, height, _ = img_BGR.shape
            range_border = 20

            # ox1,ox2,oy1,oy2 = draw_rect_subtract(img_BGR, width, height, 0)
            cv2.rectangle(img_BGR, (range_border + 2,range_border ), (width + 20,height - 60), (255, 0, 0), 1)

            ox1 = range_border + 2
            ox2 = width + range_border
            oy1 = range_border
            oy2 = height - 60

            print(results.xyxy[0])
            
            check = []
            for box in results.xyxy[0]:
                x1, y1, x2, y2, conf, cls = box

        
                if(x1 >= ox1 and y1 >= oy1 and x2 <= ox2 and y2 <= oy2) :
                    # print("inside")
                    pass
                else :

                    check.append("die")



            time_send_mail = open(PATH_SAVE_TIME_SEND_MAIL , 'r').read()

            if(len(check) > 0) :
                print("die")


            
            

            if time_send_mail : 
                # datetime_object = date.fromisoformat(time_send_mail.strip())

                datetime_object = datetime.datetime.strptime(time_send_mail.strip(), "%Y-%m-%d %H:%M:%S.%f")
                # print(datetime.datetime.now(), datetime_object)

                if(len(check) > 0 and  datetime.datetime.now() >= datetime_object) :
                    time_send = datetime.datetime.now()  + datetime.timedelta(minutes=DURATION)
                    open(PATH_SAVE_TIME_SEND_MAIL , 'w').write(str(time_send))
                    client.publish("fish_die", payload=str(len(check)), qos=1)
                    
            elif(len(check) > 0) :
                time_send = datetime.datetime.now()  + datetime.timedelta(minutes=DURATION)
                open(PATH_SAVE_TIME_SEND_MAIL , 'w').write(str(time_send))
                client.publish("fish_die", payload=str(len(check)), qos=1)


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
    # client.publish("load_model_stream", payload="1", qos=1)

    camera = cv2.VideoCapture(0)
    
    # camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    # camera.set(cv2.CAP_PROP_FRAME_HEIGHT,240)


    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

    client.publish("load_model_stream", payload="0", qos=1)
    

    while True:
        success, frame = camera.read()
        if success:

            

            ret, buffer = cv2.imencode('.png', cv2.flip(frame, 1))
            frame = buffer.tobytes()

          

            
            already_load = open(PATH_SAVE_STATE_LOAD_FISH_DIE , 'r').read()
            if already_load :
                camera.release()
                break

            

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        else:
            # print("fail open camera")
            # print(success)
            pass

def generate_frames_count_fish():
    # # open(PATH_SAVE_STATE_LOAD_FISH_DIE, 'w').write("")

    
    PATH = "D:\\Studyspace\\DoAn\\Aquarium\\my_data\\12.mp4"
    camera = cv2.VideoCapture(0)
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

    # collection_name.insert_one(init_data)

    # item_details = collection_name.find_one({"time_start" : now_start})
    # data_start_trans = str(1)+"="+str(item_details["_id"])
    # client.publish("feed_fish", payload=data_start_trans, qos=1)


    DURATION = 30

    EDGE_TOP = 150
    EDGE_RIGHT = 700
    EDGE_BOTTOM = 600
    EDGE_LEFT = 200


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

                if area > 200 and 0 not in cnt:
                    if 0 or threshold.shape[1] - 1 not in (cnt[i][0][0] for i in range(len(cnt))):

                        if 0 or threshold.shape[0] - 1 not in (cnt[i][0][1] for i in range(len(cnt))):

                            cv2.drawContours(fish_contour, [cnt], 0, 255, -1)

                            count = count + 1


            print("Count fish : " + str(count))
            
            # year, month, day = time.strftime(
            #     '%Y'), time.strftime('%m'), time.strftime('%d')

            # # now = datetime.datetime.now().strftime("%H:%M:%S.%f")
            # now = datetime.datetime.now()

            # date_push =  str(day) + "-" + str(month) + "-" + str(year) 
            # fish_count =  {"time" : now,"amount" : count}

            # data_trans =  str(now) + "=" + str(count)

            # client.publish("count_fish", payload=data_trans, qos=1)

            # collection_name.update_one({"date" : date_push,"time_start" : now_start},{"$push" : {"fish_count" :fish_count}})
            

            # time.sleep(0.3)

            # if datetime.datetime.now() > TIME_DURATION:
            #     data_start_trans = str(0)+"="+str(item_details["_id"])
            #     # client.publish("feed_fish", payload=data_start_trans, qos=1)
            #     client.publish("start_eat", payload='0', qos=1)
            #     break




            # ret, buffer = cv2.imencode('.jpg')
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
