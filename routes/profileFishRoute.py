from flask import Blueprint

from controllers.profileFishController import add_profile, get_profile,get_profile_detail,update_profile,delete_profile

profileFishRoute = Blueprint('profileFishRoute', __name__)


profileFishRoute.route('/add', methods=['POST'])(add_profile)
profileFishRoute.route('/get/<username>', methods=['GET'])(get_profile)
profileFishRoute.route('/get_detail/<id>', methods=['GET'])(get_profile_detail)
profileFishRoute.route('/update/<id>', methods=['POST'])(update_profile)
profileFishRoute.route('/delete/<id>', methods=['POST'])(delete_profile)
