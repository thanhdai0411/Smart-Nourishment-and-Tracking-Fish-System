from flask import Blueprint

from controllers.homeController import (capture, record, render_home_page,
                                        render_landing_page,
                                        render_view_camera, render_view_home,
                                        start_camera, stop_camera,
                                        video, video_detect, render_monitor_page, render_profile_page)

homeRoute = Blueprint('homeRoute', __name__)


homeRoute.route('/')(render_view_home)
# homeRoute.route('/test')
# homeRoute.route('/landing_page')(render_landing_page)
homeRoute.route('/monitoring')(render_monitor_page)
homeRoute.route('/home')(render_home_page)
homeRoute.route('/profile')(render_profile_page)
# homeRoute.route('/camera')(render_view_camera)
# homeRoute.route('/stop_camera')(stop_camera)
# homeRoute.route('/start_camera')(start_camera)
# homeRoute.route('/create_camera')(video)
# homeRoute.route('/camera_detect')(video_detect)
# homeRoute.route('/record-camera')(record)
# homeRoute.route('/capture_camera')(capture)
