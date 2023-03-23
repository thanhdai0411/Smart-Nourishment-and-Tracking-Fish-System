from flask import Blueprint

from controllers.emailNotifyController import add_email_notify, get_email_notify, delete_email_notify, update_email_notify
emailNotifyRoute = Blueprint('emailNotifyRoute', __name__)

emailNotifyRoute.route('/add', methods=['POST'])(add_email_notify)
emailNotifyRoute.route('/get/<username>', methods=['GET'])(get_email_notify)
emailNotifyRoute.route('/update/<username>', methods=['POST'])(update_email_notify)
emailNotifyRoute.route('/delete/<username>', methods=['GET'])(delete_email_notify)



