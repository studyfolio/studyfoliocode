from flask import Flask
from flask_cors import CORS
import config

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']= config.SECRET_KEY
    CORS(app)
    from .login import auth
    app.register_blueprint(auth,url_prefix="/")
    from .admin import admin
    app.register_blueprint(admin,url_prefix="/")

    return app

