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

    def test_signup_login_success(self):
        payload = json.dumps({
            'email':'foo.bar@gmail.com',
            'password':'password123'
        })
        response = self.client.post('/signup', 
            data=payload, 
            content_type='application/json',
            follow_redirects=False
        )
        self.assertEqual(302, response.status_code)

        response = self.client.post('/login',
            data=payload, 
            content_type='application/json',
            follow_redirects=False
        )
        self.assertEqual(302, response.status_code)

        response = self.client.get('/logout', follow_redirects=False)
        self.assertEqual(302, response.status_code)
    
    def test_signup_failure(self):
        payload = json.dumps({
            'email':'foo.bar@gmail.com',
        })
        response = self.client.post('/signup', 
            data=payload, 
            content_type='application/json',
            follow_redirects=False
        )
        self.assertEqual(400, response.status_code)
        payload = json.dumps({
            'password':'foo.bar@gmail.com',
        })
        self.assertEqual(400, response.status_code)

    def test_login_failure(self):
        payload = json.dumps({
            'email':'foo.bar@gmail.com',
            'password':'password123'
        })
        response = self.client.post('/signup', 
            data=payload, 
            content_type='application/json',
            follow_redirects=False
        )
        self.assertEqual(302, response.status_code)
        payload = json.dumps({
            'password':'foo.bar@gmail.com',
        })
        response = self.client.post('/login',
            data=payload, 
            content_type='application/json',
            follow_redirects=False
        )
        self.assertEqual(400, response.status_code)
    

if __name__ == '__main__':
    unittest.main()