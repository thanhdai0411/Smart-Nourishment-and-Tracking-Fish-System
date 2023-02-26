from flask import Blueprint

from controllers.profileFishController import add_profile

profileFishRoute = Blueprint('profileFishRoute', __name__)


profileFishRoute.route('/add', methods=['GET'])(add_profile)
