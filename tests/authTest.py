import os
import unittest
import json

from api.app import create_app, db
from api.models import User


class TestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_signup_login(self):
        payload = json.dumps({
            'email':'cam77.fbair@gmail.com',
            'password':'password123'
        })
        response = self.client.post('/signup', 
            data=payload, 
            content_type='application/json',
            follow_redirects=True
        )
        self.assertEqual(200, response.status_code)

        response = self.client.post('/login',
            data=payload, 
            content_type='application/json',
            follow_redirects=True
        )
        self.assertEqual(200, response.status_code)
    

if __name__ == '__main__':
    unittest.main()