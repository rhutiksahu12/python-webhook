from flask import Flask
from flask_cors import CORS
from app.webhook.routes import webhookRoute


# Creating our flask app
def create_app():

    app = Flask(__name__)
    CORS(app) 
    # registering all the blueprints
    app.register_blueprint(webhookRoute)
    
    return app
