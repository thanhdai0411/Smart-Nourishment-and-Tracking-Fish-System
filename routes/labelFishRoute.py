from flask import Blueprint

from controllers.labelFishController import get_fish
labelFishRoute = Blueprint('labelFishRoute', __name__)

labelFishRoute.route('/get/<user_id>', methods=['GET'])(get_fish)
