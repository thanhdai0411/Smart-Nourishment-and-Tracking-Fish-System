from constant import MONGODB_URL
from flask_mongoengine import MongoEngine


def connectDB(app):

    try:
        app.config['MONGODB_HOST'] = MONGODB_URL
        db = MongoEngine(app)
        print('>>>> Connect MongoDB success !!')
    except Exception:
        print('>>>> Connect MongoDB fail')
