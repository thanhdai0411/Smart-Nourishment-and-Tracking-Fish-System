
from io import BytesIO
import cv2
import torch
import numpy as np

from PIL import Image
from flask import Flask, render_template, Response, flash, request, redirect, url_for, session
app = Flask(__name__, static_url_path='/static')

model = torch.hub.load(
    "ultralytics/yolov5", "yolov5s"
)

print('Flask on ')


def gen():
    cap = cv2.VideoCapture(0)
    # Read until video is completed
    while(cap.isOpened()):

        # Set Model Settings

        success, frame = cap.read()
        if success == True:

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # print(type(frame))

            img = Image.open(BytesIO(frame))
            results = model(img, size=640)
            results.print()

            # convert remove single-dimensional entries from the shape of an array
            img = np.squeeze(results.render())  # RGB
            # read image as BGR
            img_BGR = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # BGR

        else:
            break

        frame = cv2.imencode('.jpg', img_BGR)[1].tobytes()
        # print(frame)

        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/detect')
def detect():
    # start_generate_frames()
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

    # return Response(generate_frames_detect(), mimetype='multipart/x-mixed-replace; boundary=frame')
app.run(debug=True, threaded=True)
