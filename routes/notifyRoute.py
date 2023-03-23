from flask import Blueprint

from controllers.notifyController import add_notify, get_notify, delete_notify, update_notify
notifyRoute = Blueprint('notifyRoute', __name__)

notifyRoute.route('/add', methods=['POST'])(add_notify)
notifyRoute.route('/get/<username>', methods=['GET'])(get_notify)
notifyRoute.route('/update/<username>', methods=['POST'])(update_notify)
notifyRoute.route('/delete/<username>', methods=['GET'])(delete_notify)



