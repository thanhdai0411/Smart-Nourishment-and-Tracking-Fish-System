from flask import Blueprint

from controllers.authController import register_user, get_user, login_user, logout
authRoute = Blueprint('authRoute', __name__)

authRoute.route('/register', methods=['POST'])(register_user)
authRoute.route('/login', methods=['POST'])(login_user)
authRoute.route('/logout')(logout)
authRoute.route('/get/<username>', methods=['GET'])(get_user)
