from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
import config


def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']= config.SECRET_KEY
    app.config['MAIL_SERVER'] = config.MAIL_SERVER
    app.config['MAIL_PORT'] = config.MAIL_PORT
    app.config['MAIL_USE_TLS'] = config.MAIL_USE_TLS
    app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD
    
    CORS(app)
    from .login import auth
    app.register_blueprint(auth,url_prefix="/")
    from .admin import admin
    app.register_blueprint(admin,url_prefix="/")
    from .magors import promos_api
    app.register_blueprint(promos_api,url_prefix="/")
    from .teacher import teacher
    app.register_blueprint(teacher,url_prefix="/")
    from .student import student
    app.register_blueprint(student,url_prefix="/")
    return app

