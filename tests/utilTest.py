import os
import unittest
import json

from api.app import create_app, db
from api.models import User, Metric, Markets
from flask import g


class TestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        self.payload1 = json.dumps({
            "email":"foo.bar@gmail.com",
            "password":"password123"
        })

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()