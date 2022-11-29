# from routes.testRoute import upload_label
from routes.homeRoute import homeRoute
from routes.uploadLabelRoute import uploadLabelsRoute
from routes.authRoute import authRoute
from routes.labelFishRoute import labelFishRoute
from routes.controlRoute import controlRoute
from routes.cameraRoute import cameraRoute


def route(app):

    app.register_blueprint(homeRoute, url_prefix='/')
    app.register_blueprint(uploadLabelsRoute, url_prefix='/upload/')
    app.register_blueprint(authRoute, url_prefix='/auth/')
    app.register_blueprint(labelFishRoute, url_prefix='/label/')
    app.register_blueprint(controlRoute, url_prefix='/control/')
    app.register_blueprint(cameraRoute, url_prefix='/camera/')
