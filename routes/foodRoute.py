from flask import Blueprint
from controllers.foodController import add_food, get_food, delete_food, update_food, update_food_status

foodRoute = Blueprint('foodRoute', __name__)


foodRoute.route('/add', methods=['GET', 'POST'])(add_food)
foodRoute.route('/get/<username>')(get_food)
foodRoute.route('/delete/<id>', methods=['DELETE'])(delete_food)
foodRoute.route('/update/<id>', methods=['POST'])(update_food)
foodRoute.route('/update_status/<id>', methods=['POST'])(update_food_status)
