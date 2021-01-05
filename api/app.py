from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cryptoDatabase.db'
    app.config.from_pyfile('./config/debug_environment.cfg')

    db.init_app(app)

    # blueprint for auth routes in our app
    from .views import auth 
    app.register_blueprint(auth)

    from .views import main
    app.register_blueprint(main)

    return app