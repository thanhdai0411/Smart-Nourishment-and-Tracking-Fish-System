from flask import Blueprint

from controllers.uploadLabelsController import upload_labels
uploadLabelsRoute = Blueprint('uploadLabelsRoute', __name__)

uploadLabelsRoute.route('/labels', methods=['GET', 'POST'])(upload_labels)
