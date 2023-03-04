from flask import (Flask, Response, flash, redirect, render_template, request,
                   session, url_for)

from services.cameraService import (generate_frames, generate_frames_detect,generate_frames_detect_fish_die,
                                    record_screen, start_generate_frames,
                                    stop_generate_frames,  )
# from app import gen


def start_camera():
    return 'camera_succcess'


def stop_camera():
    return 'stop_success'


def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def video_detect():
    return Response(generate_frames_detect(), mimetype='multipart/x-mixed-replace; boundary=frame')

def video_detect_fish_die():
    return Response(generate_frames_detect_fish_die(), mimetype='multipart/x-mixed-replace; boundary=frame')
