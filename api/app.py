import click
import time

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    from .cryptoClient import query
    @app.cli.command("crypto")
    def crypto():
        query()

    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cryptoDatabase.db'
    app.config.from_pyfile('./config/debug_environment.cfg')

    db.init_app(app)

    # from .commands import comds
    # app.register_blueprint(comds)

    # blueprint for auth routes in our app
    from .views import auth 
    app.register_blueprint(auth)

    from .views import main
    app.register_blueprint(main)

    return app