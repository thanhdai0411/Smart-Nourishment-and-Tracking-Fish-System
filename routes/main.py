# from routes.testRoute import upload_label
from routes.homeRoute import homeRoute
from routes.uploadLabelRoute import uploadLabelsRoute
from routes.authRoute import authRoute
from routes.labelFishRoute import labelFishRoute
from routes.controlRoute import controlRoute
from routes.cameraRoute import cameraRoute
from routes.foodRoute import foodRoute
from routes.countFishRoute import countFishRoute
from routes.profileFishRoute import profileFishRoute


def route(app):

    app.register_blueprint(homeRoute, url_prefix='/')
    app.register_blueprint(uploadLabelsRoute, url_prefix='/upload/')
    app.register_blueprint(authRoute, url_prefix='/auth/')
    app.register_blueprint(labelFishRoute, url_prefix='/label/')
    app.register_blueprint(controlRoute, url_prefix='/control/')
    app.register_blueprint(cameraRoute, url_prefix='/camera/')
    app.register_blueprint(foodRoute, url_prefix='/food/')
    app.register_blueprint(countFishRoute, url_prefix='/count_fish/')
    app.register_blueprint(profileFishRoute, url_prefix='/profile_fish/')
