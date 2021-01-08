import os
import unittest
import json

from api.app import create_app, db
from api.models import User
from flask import g
from werkzeug.security import generate_password_hash