from flask import (Flask, Response, flash, redirect, render_template, request,
                   session, url_for)

from services.cameraService import (generate_frames, generate_frames_detect,
                                    record_screen, start_generate_frames,
                                    stop_generate_frames, )
# from app import gen


def start_camera():
    # start_generate_frames()
    # stop = False
    # return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    # return render_template('home_page.html', stop=stop)
    return 'camera_succcess'


def stop_camera():
    # stop_generate_frames()
    # stop = True
    # return render_template('home_page.html', stop=stop)
    return 'stop_success'


def video():
    # start_generate_frames()
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def video_detect():
    # start_generate_frames()
    return Response(generate_frames_detect(), mimetype='multipart/x-mixed-replace; boundary=frame')
    # return Response(generate_frames_detect(), mimetype='multipart/x-mixed-replace; boundary=frame')
