import cv2
from msilib.schema import Class
from flask import Flask, render_template, Response, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os.path

from services.cameraService import generate_frames, stop_generate_frames, start_generate_frames, capture_screen, record_screen, generate_frames_detect
from constant import SUCCESS_STATUS, ERROR_STATUS, FOLDER_SAVE_IMAGES, FOLDER_SAVE_LABELS

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

camera = cv2.VideoCapture(0)


def check_user():
    if session.get("username"):
        user = session.get('username')
        print(user + ' Login')
        return redirect("/home")


def render_landing_page():

    return render_template('landing_page.html')


def render_view_home():
    # check_user()
    if session.get("username"):
        user = session.get('username')
        print(user + ' Login')
        return redirect("/home")
    return render_template('landing_page.html')

    # return render_template('home.html')


def render_home_page():
    return render_template('home_page.html')


def render_monitor_page():
    return render_template('monitoring.html')


def render_view_camera():
    start_generate_frames()
    stop = False
    return render_template('camera.html', stop=stop)


def stop_camera():
    stop_generate_frames()
    stop = True
    return render_template('camera.html', stop=stop)


def start_camera():
    start_generate_frames()
    stop = False
    return render_template('camera.html', stop=stop)


def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def video_detect():
    return Response(generate_frames_detect(), mimetype='multipart/x-mixed-replace; boundary=frame')


def capture():
    capture_screen()
    stop = False
    return render_template('camera.html', stop=stop)


def record():
    record_screen()
    stop = False
    return render_template('camera.html', stop=stop)
