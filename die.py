# already_load = open(PATH_SAVE_STATE_LOAD_FISH_DIE , 'r').read()
# model = ""
# if not already_load :
# open(PATH_SAVE_STATE_LOAD_FISH_DIE, 'w').write("ALREADY")
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




print("load model fish die ...")

model = torch.hub.load('.', 'custom', path="/home/doan/Desktop/DA/WebServer/Aquarium-Smart/model_fish_die.pt", source='local')
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
        # if datetime.datetime.now() > TIME_DURATION:
        


        img = np.squeeze(results.render())  # RGB

        img_BGR = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        frame = cv2.imencode('.jpg', img_BGR)[1].tobytes()
        cv2.imshow("Edge", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    else:
        pass