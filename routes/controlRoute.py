from flask import Blueprint
from controllers.controlDeviceController import render_page_control

controlRoute = Blueprint('controlRoute', __name__)


controlRoute.route('/')(render_page_control)
