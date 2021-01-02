from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DB_URI'] = 'sqlite:///cryptoDatabase.db'

    return app