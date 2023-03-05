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
from cv2 import cuda

cuda.printCudaDeviceInfo(0)

from constant import PATH_MODEL_FISH_DIE



# STD_DIMENSIONS =  {
#     "480p": (640, 480),
#     "720p": (1280, 720),
#     "1080p": (1920, 1080),
#     "4k": (3840, 2160),
# }

# 160.0 x 120.0
# 176.0 x 144.0
# 320.0 x 240.0
# 352.0 x 288.0
# 640.0 x 480.0
# 1024.0 x 768.0
# 1280.0 x 1024.0

# camera = cv2.VideoCapture(0)


# camera.set(cv2.CAP_PROP_FRAME_WIDTH, 352)
# camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 288)



# camera.release()


# try:
#     os.mkdir('./public/capture_camera')
#     os.mkdir('./public/record_camera')
# except OSError as error:
#     pass


# Load Pre-trained Model
# model = torch.hub.load('ultralytics/yolov5',
#                        'yolov5s', force_reload=True, pretrained=True)

# model_url = "/home/doan/DA/WebServer/Aquarium-Smart/train_complete/train/weights/best.pt"
# model_url = "/home/doan/DA/WebServer/Aquarium-Smart/model_fish_die.pt"


def generate_frames_detect():

    # model = torch.hub.load('ultralytics/yolov5',
    #                        'yolov5s')
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

            frame = cv2.resize(frame, (416,416))

            # =====================================

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        else:
            pass

def generate_frames_detect_fish_die():

    # model = torch.hub.load('ultralytics/yolov5',
    #                        'yolov5s')
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
            # =====================================

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        else:
            pass


def generate_frames():


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


def handle_fail_open_camera() :
    print("")

def start_generate_frames():
    global camera, state_open_camera
    camera = cv2.VideoCapture(0)


def stop_generate_frames():
    global camera, state_open_camera
    camera.release()
    cv2.destroyAllWindows()


# def camera_detect():
#     return Response(generate_frames_detect(), mimetype='multipart/x-mixed-replace; boundary=frame')


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
