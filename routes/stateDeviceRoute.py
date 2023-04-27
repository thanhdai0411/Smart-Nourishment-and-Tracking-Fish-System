from flask import Blueprint

from controllers.stateDeviceController import update_status, get_status, init_status
stateDeviceRoute = Blueprint('stateDeviceRoute', __name__)

stateDeviceRoute.route('/init', methods=['POST'])(init_status)
stateDeviceRoute.route('/update/<device>', methods=['PUT'])(update_status)
stateDeviceRoute.route('/get/<device>', methods=['GET'])(get_status)



