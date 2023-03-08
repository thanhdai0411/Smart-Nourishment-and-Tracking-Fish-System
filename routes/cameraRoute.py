from flask import Blueprint

from controllers.cameraController import (start_camera, stop_camera, video,
                                          video_detect, video_detect_fish_die, video_count_fish)

cameraRoute = Blueprint('cameraRoute', __name__)

cameraRoute.route('fish_die', methods=['GET'])(video_detect_fish_die)
cameraRoute.route('play', methods=['GET'])(start_camera)
cameraRoute.route('stop', methods=['GET'])(stop_camera)
cameraRoute.route('video', methods=['GET'])(video)
cameraRoute.route('detect', methods=['GET'])(video_detect)
cameraRoute.route('count_fish', methods=['GET'])(video_count_fish)
