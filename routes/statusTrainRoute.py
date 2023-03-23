from flask import Blueprint

from controllers.statusTrainController import get_status_train, delete_status_train
statusTrainRoute = Blueprint('statusTrainRoute', __name__)

statusTrainRoute.route('/get/<username>', methods=['GET'])(get_status_train)
statusTrainRoute.route('/delete/<username>', methods=['GET'])(delete_status_train)
