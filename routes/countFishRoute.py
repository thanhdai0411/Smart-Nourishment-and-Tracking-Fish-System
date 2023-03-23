from flask import Blueprint

from controllers.countFishController import get_count_fish,get_count_fish_by_date,get_count_fish_detail
countFishRoute = Blueprint('countFishRoute', __name__)

countFishRoute.route('/get')(get_count_fish)
countFishRoute.route('/get_date/<date>')(get_count_fish_by_date)
countFishRoute.route('/get_detail/<id>')(get_count_fish_detail)