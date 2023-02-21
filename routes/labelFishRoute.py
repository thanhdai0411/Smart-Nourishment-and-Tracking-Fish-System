from flask import Blueprint

from controllers.labelFishController import get_fish, get_data_present,delete_fish
labelFishRoute = Blueprint('labelFishRoute', __name__)

labelFishRoute.route('/get/<username>', methods=['GET'])(get_fish)
labelFishRoute.route('/delete/<username>/<fish_name>', methods=['DELETE'])(delete_fish)
labelFishRoute.route('/get/data_fish/<fish_name>', methods=['GET'])(get_data_present)
