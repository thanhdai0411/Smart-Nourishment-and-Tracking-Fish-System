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


camera = cv2.VideoCapture(0)

global capture, rec_frame, grey, switch, neg, face, rec, out
capture = 0
grey = 0
neg = 0
face = 0
switch = 1
rec = 0


# try:
#     os.mkdir('./public/capture_camera')
#     os.mkdir('./public/record_camera')
# except OSError as error:
#     pass


# Load Pre-trained Model
# model = torch.hub.load('ultralytics/yolov5',
#                        'yolov5s', force_reload=True, pretrained=True)


def generate_frames_detect():

    model = torch.hub.load('ultralytics/yolov5',
                           'yolov5s')
    global out, capture, rec_frame
    while True:
        success, frame = camera.read()
        if success:

            ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
            frame = buffer.tobytes()

            # =====================================

            img = Image.open(io.BytesIO(frame))
            results = model(img, size=640)
            # results = model(img)
            results.print()

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
    global out, capture, rec_frame
    while True:
        success, frame = camera.read()
        if success:

            if(capture):
                capture = 0
                now = datetime.datetime.now()
                p = os.path.sep.join(
                    ['./public/capture_camera', "shot_{}.png".format(str(now).replace(":", ''))])
                cv2.imwrite(p, frame)

            if(rec):
                rec_frame = frame
                frame = cv2.putText(cv2.flip(
                    frame, 1), "Recording...", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4)
                frame = cv2.flip(frame, 1)

            ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        else:
            pass


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
