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

import torch

from flask_assets import Environment, Bundle
from flask_session import Session

from werkzeug.utils import secure_filename
import cv2
import os.path
import threading
from subprocess import call
from constant import BROKER_URL, BROKER_PORT, BROKER_USERNAME, BROKER_PASSWORD, SUCCESS_STATUS


app = Flask(__name__, static_url_path='/static')

# config session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# scss config~
assets = Environment(app)  # create an Environment instance
bundles = Bundle(
    'scss/styles.scss', 'scss/login_page.scss', 'scss/base.scss', 'scss/main.scss', 'scss/control_page.scss',
    filters='pyscss',
    output='css/main.css',
)

assets.register('scss_all', bundles)


# CONFIG
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config.from_object('config')
route(app)


#! train =======================================================================================
@app.route('/upload/train', methods=['GET'])
def train_model():
    dt_obj = datetime.now()
    timeCurrent = dt_obj.strftime("%d-%m-%Y - %H:%M")

    pl = 'Start/' + str(timeCurrent)

    print('Start train')
    client.publish("Train_model", payload=pl, qos=1)
    sleep(10)

    call(['python', 'F:\\Studyspace\\DoAn\\Aquarium\\yolov5\\train.py'])

    dt_obj_2 = datetime.now()
    timeComplete = dt_obj_2.strftime("%d-%m-%Y - %H:%M")

    pl2 = 'End/' + str(timeComplete)
    client.publish("Train_model", payload=pl2, qos=1)
    sleep(10)

    return redirect('/home')


#! =============================================================================================

# model = torch.hub.load('ultralytics/yolov5',
#                        'yolov5s', force_reload=True, pretrained=True)


# def generate_frames_detect():

#     global out, capture, rec_frame
#     camera = cv2.VideoCapture(0)
#     while True:
#         success, frame = camera.read()
#         if success:

#             ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
#             frame = buffer.tobytes()

#             # =====================================

#             img = Image.open(BytesIO(frame))
#             results = model(img, size=640)
#             # results = model(img)
#             results.print()

#             img = np.squeeze(results.render())  # RGB
#             # read image as BGR
#             img_BGR = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
#             frame = cv2.imencode('.jpg', img_BGR)[1].tobytes()
#             # =====================================

#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#         else:
#             pass


# @app.route('/main_detect')
# def main_detect():
#     return Response(generate_frames_detect(), mimetype='multipart/x-mixed-replace; boundary=frame')

#! =============================================================================================


UPLOAD_FOLDER = FOLDER_SAVE_IMAGES
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


if __name__ == "__main__":
    connectDB(app)
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
    client.subscribe("cloudmqtt", qos=1)

    # client.publish("encyclopedia/temperature", payload="hot", qos=1)

    client.loop()

    #! END SETUP MQTT =======================================================================================

    app.run(debug=True, threaded=True)
