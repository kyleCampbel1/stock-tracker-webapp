import click
import os
import time

from config import config
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
mail = Mail()

def create_app(config_name='default'):

    app = Flask(__name__)
    
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .cryptoClient import query
    from .utils import emailAlerts
    @app.cli.command("crypto")
    def crypto():
        query()
        emailAlerts()

    db.init_app(app)
    mail.init_app(app)

    # blueprint for auth routes in our app
    from .views import auth 
    app.register_blueprint(auth)

    from .views import main
    app.register_blueprint(main)

    return app
