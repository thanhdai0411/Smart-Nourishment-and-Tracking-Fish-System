from flask import (Flask, Response, flash, redirect, render_template, request,
                   session, url_for)

from constant import PATH_SAVE_STATE_LOAD_FISH_DIE,PATCH_COUNT_FISH
import time
from services.cameraService import (generate_frames, generate_frames_detect,generate_frames_detect_fish_die, generate_frames_count_fish, stop_generate_frames  )
# from app import gen
from subprocess import call


def start_camera():
    return 'camera_succcess'


def stop_camera():
    # stop_generate_frames()
    return 'stop_success'

def cnt_fish_press():
    # stop_generate_frames()

    open(PATH_SAVE_STATE_LOAD_FISH_DIE, 'w').write("ALREADY_FEED")
    time.sleep(5)
    open(PATH_SAVE_STATE_LOAD_FISH_DIE, 'w').write("")
    
    call(["python3",PATCH_COUNT_FISH])
    return 'success'


def video():
    open(PATH_SAVE_STATE_LOAD_FISH_DIE, 'w').write("ALREADY_FEED")
    time.sleep(5)
    open(PATH_SAVE_STATE_LOAD_FISH_DIE, 'w').write("")

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def video_detect():
    open(PATH_SAVE_STATE_LOAD_FISH_DIE, 'w').write("ALREADY_FEED")
    time.sleep(5)
    open(PATH_SAVE_STATE_LOAD_FISH_DIE, 'w').write("")

    return Response(generate_frames_detect(), mimetype='multipart/x-mixed-replace; boundary=frame')

def video_detect_fish_die():
    open(PATH_SAVE_STATE_LOAD_FISH_DIE, 'w').write("ALREADY_FEED")
    time.sleep(5)
    open(PATH_SAVE_STATE_LOAD_FISH_DIE, 'w').write("")


    return Response(generate_frames_detect_fish_die(), mimetype='multipart/x-mixed-replace; boundary=frame')

def video_count_fish() :
    return Response(generate_frames_count_fish(), mimetype='multipart/x-mixed-replace; boundary=frame')
