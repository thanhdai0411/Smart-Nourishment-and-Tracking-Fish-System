

import requests

def is_cnx_active():
    try:
        # urlopen('http://www.google.com', 1)
        request = requests.get('http://www.google.com', timeout=5)
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
	    print("No internet connection.")


while True:
    if is_cnx_active() is True:
        # Do somthing
        print("The internet connection is active")
        break
    else:
        print("Waiting connect")
        pass

from constant import BROKER_URL, BROKER_PORT, BROKER_USERNAME, BROKER_PASSWORD, PATH_TRAIN_MODEL, EMAIL_USERNAME, EMAIL_PASSWORD
from subprocess import call,Popen,check_call
from werkzeug.utils import secure_filename
from flask_session import Session
from flask_assets import Environment, Bundle
from io import BytesIO
from PIL import Image
from paho import mqtt
import paho.mqtt.client as paho
from config.db import connectDB
from routes.main import route
from constant import FOLDER_SAVE_IMAGES, BROKER_URL, BROKER_PORT, FOLDER_SAVE_LABELS,FOLDER_SAVE_IMAGES, PATH_SAVE_STATE_LOAD_FISH_DIE
from flask import Flask, render_template, Response, flash, request, redirect, url_for, session
from flask_cors import CORS, cross_origin
from datetime import datetime
from time import sleep
import numpy as np
from multiprocessing import  Value,Process,Queue
from cron import cron_food
from flask_redmail import RedMail
import urllib.request, json
import os
from my_utils.jsonFile import read_file_json, write_file_json
from my_models.statusTrainModel import StatusTrain
from my_utils.deleteNameTrainModel import deleteNameTrainModel

# from flask_crontab import Crontab

import random



app = Flask(__name__, static_url_path='/static')


# config session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "null"
Session(app)

#socket init 





# config emaial 

app.config["EMAIL_HOST"] = "smtp.gmail.com"
app.config["EMAIL_PORT"] = 587

app.config["EMAIL_USERNAME"] = EMAIL_USERNAME
app.config["EMAIL_PASSWORD"] = EMAIL_PASSWORD

app.config["EMAIL_SENDER"] = EMAIL_USERNAME

email = RedMail()
email.init_app(app)

# scss config~
assets = Environment(app)  # create an Environment instance
bundles = Bundle(
    'scss/styles.scss', 'scss/login_page.scss', 'scss/base.scss', 'scss/main.scss', 'scss/monitoring.scss','scss/responsive.scss',
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




#! train =======================================================================================

@app.route('/upload/train', methods=['POST'])
def train_model():
    print('Start train')
    
    check_status = StatusTrain.objects(status="WAITING")

    if check_status : 
        return 'TRAIN_BUSY'

    dt_obj = datetime.now()
    timeCurrent = dt_obj.strftime("%d/%m/%Y - %H:%M")
    name_fish = request.form.get("name_fish")
    action = request.form.get("action")
    
    action_text = ""

    if action == "TRAIN" :
        action_text = "Train model name " + name_fish
    else : 
        action_text = "Delete model name " + name_fish
        deleteNameTrainModel(name_fish)

    exist_folder_image_train = os.path.isdir(FOLDER_SAVE_IMAGES)
    if not exist_folder_image_train :
       
        return "NOT_LABEL_TRAIN"

    


    pl = 'Start=' + str(timeCurrent) + '=' + str(name_fish) + '=' + str(action_text)

    client.publish("Train_model", payload=pl, qos=1)

    username = request.cookies.get('username', None)

    newStatus = StatusTrain(status="WAITING",dateStart=timeCurrent, username=username,name_fish=name_fish,action=action_text)
    newStatus.save()
    
    sleep(5)
    
    # python train.py --img 640 --batch 16 --epochs 3 --data coco128.yaml --weights yolov5s.pt

    call(["python3",PATH_TRAIN_MODEL])

    dt_obj_2 = datetime.now()
    timeComplete = dt_obj_2.strftime("%d/%m/%Y - %H:%M")

    pl2 = 'End=' + str(timeComplete)+ '=' + str(name_fish) + '=' + str(action_text)
    client.publish("Train_model", payload=pl2, qos=1)

    updateStatus = StatusTrain.objects(name_fish=name_fish,status="WAITING")
    updateStatus.update(status="COMPLETE",dateEnd=timeComplete)
    # sleep(10)

    return 'ok'


@app.route("/send_mail", methods=["POST"])
def send_email():
    email_receiver = request.form.get('email')
    text = request.form.get('text')
    print(email_receiver, text)
    email.send(

        subject="Hi, I'm Smart Aquarium Notification !",
        receivers=email_receiver,
        html="""
            <p style="font-size : 18px">{{text}}</p>
        """,
        body_params={
                "text": text
            }
    )
    return "Sent"

#! =============================================================================================




UPLOAD_FOLDER = FOLDER_SAVE_IMAGES
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


if __name__ == "__main__":
    #!MQTT SETUP ==========================================================

    def on_connect(client, userdata, flags, rc, properties=None):
        print(" >>>>> Connect Main <<<<< %s." % rc)

    def on_publish(client, userdata, mid, properties=None):
        print("mid: " + str(mid))

    def on_subscribe(client, userdata, mid, granted_qos, properties=None):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_message(client, userdata, msg):
        print(msg.topic + ": " + str(msg.payload))  
        


        
    # client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
    num = random.random()
    client = paho.Client("main" + str(num))
    client.on_connect = on_connect

    # client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    # set username and password
    client.username_pw_set(BROKER_USERNAME, BROKER_PASSWORD)
    client.connect(BROKER_URL, BROKER_PORT)

    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.on_publish = on_publish

    client.subscribe("start_feed_fish")
    client.subscribe("fish_die")



    client.loop_start()

    #! END SETUP MQTT =======================================================================================

    recording_on = Value('b', True)
    p = Process(target=cron_food, args=(recording_on,))
    
    connectDB(app)
    p.start()  
    # !
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=5000, threads= 8) 
    # !

    # app.run(debug=True, threaded=True)


    app.run(host="0.0.0.0", port=5000,debug=True, threaded=True)


    p.join()



