from flask import Blueprint

from controllers.loadAIController import load_ai_feeder
loadAIRoute = Blueprint('loadAIRoute', __name__)

loadAIRoute.route('/load')(load_ai_feeder)



