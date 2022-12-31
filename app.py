from constant import BROKER_URL, BROKER_PORT, BROKER_USERNAME, BROKER_PASSWORD, SUCCESS_STATUS
from subprocess import call
import os.path
import cv2
from werkzeug.utils import secure_filename
from flask_session import Session
from flask_assets import Environment, Bundle
import torch
from flask_socketio import send, emit, SocketIO
from io import BytesIO
from PIL import Image
from paho import mqtt
import paho.mqtt.client as paho
from config.db import connectDB
from routes.main import route
from constant import FOLDER_SAVE_IMAGES, BROKER_URL, BROKER_PORT
from flask import Flask, render_template, Response, flash, request, redirect, url_for, session
from flask_cors import CORS, cross_origin
from datetime import datetime
from time import sleep
import numpy as np
from multiprocessing import Process, Value
from cron import cron_food
import redis
from my_models.foodModel import Food

# from flask_crontab import Crontab


app = Flask(__name__, static_url_path='/static')
# crontab = Crontab(app)

# config session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# scss config~
assets = Environment(app)  # create an Environment instance
bundles = Bundle(
    'scss/styles.scss', 'scss/login_page.scss', 'scss/base.scss', 'scss/main.scss', 'scss/monitoring.scss',
    filters='pyscss',
    output='css/main.css',
)

assets.register('scss_all', bundles)


# CONFIG
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config.from_object('config')
route(app)
# ==========

#! cron =======================================================================================


# def cron_food(loop_on):

#     while True:
#         if loop_on.value == True:
#             dt_obj = datetime.now()
#             time_on = dt_obj.replace(hour=16, minute=41, second=0)
#             time_on2 = dt_obj.replace(hour=16, minute=42, second=0)
#             time_present = dt_obj.replace(hour=dt_obj.hour, minute=dt_obj.minute,
#                                           second=dt_obj.second)
#             if(time_on == time_present):
#                 print('Hey Hey , Cron Food 1')

#             elif(time_on2 == time_present):
#                 print('Hey Hey , Cron Food 2')
#         sleep(1)


#! train =======================================================================================


@app.route('/upload/train', methods=['GET'])
def train_model():
    dt_obj = datetime.now()
    timeCurrent = dt_obj.strftime("%d/%m/%Y - %H:%M")

    pl = 'Start=' + str(timeCurrent)

    print('Start train')
    client.publish("Train_model", payload=pl, qos=1)
    sleep(10)

    call(['python', 'F:\\Studyspace\\DoAn\\Aquarium\\train.py'])

    dt_obj_2 = datetime.now()
    timeComplete = dt_obj_2.strftime("%d/%m/%Y - %H:%M")

    pl2 = 'End=' + str(timeComplete)
    client.publish("Train_model", payload=pl2, qos=1)
    sleep(10)

    return redirect('/home')


#! =============================================================================================


UPLOAD_FOLDER = FOLDER_SAVE_IMAGES
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    

if __name__ == "__main__":

    #!MQTT SETUP ==========================================================

    def on_connect(client, userdata, flags, rc, properties=None):
        print("Connect received with code %s." % rc)

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

    # subscribe to all topics of encyclopedia by using the wildcard "#"
    # client.subscribe("cloudmqtt", qos=1)

    # client.publish("encyclopedia/temperature", payload="hot", qos=1)

    # client.loop()
    client.loop_start()

    #! END SETUP MQTT =======================================================================================

    connectDB(app)

    recording_on = Value('b', True)
    p = Process(target=cron_food, args=(recording_on,))
    p.start()

    app.run(debug=True, threaded=True)

    p.join()
