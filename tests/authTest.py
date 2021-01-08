import os
import unittest
import json

from api.app import create_app, db
from api.models import User
from flask import g
from werkzeug.security import generate_password_hash


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

    def test_signup_login_logout_success(self):
        response = self.client.post('/signup', 
            data=self.payload1, 
            content_type='application/json',
            follow_redirects=False
        )
        self.assertEqual(302, response.status_code)

        response = self.client.post('/login',
            data=self.payload1, 
            content_type='application/json',
            follow_redirects=False
        )
        self.assertEqual(302, response.status_code)

        response = self.client.get('/logout', follow_redirects=False)
        self.assertEqual(302, response.status_code)

    def test_signup_success(self):
        response = self.client.post('/signup', 
            data=self.payload1, 
            content_type='application/json',
            follow_redirects=False
        )
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

    def test_login_success(self):
        u1 = User(email="foo.bar@gmail.com", password=generate_password_hash("password123", method='sha256'))
        db.session.add(u1)
        db.session.commit()
        g.user = u1
        response = self.client.post('/login',
            data=self.payload1, 
            content_type='application/json',
            follow_redirects=False
        )
        self.assertEqual(302, response.status_code)

    def test_login_failure(self):
        u1 = User(email="foo.bar@gmail.com", password=generate_password_hash("password123", method='sha256'))
        db.session.add(u1)
        db.session.commit()
        payload = json.dumps({"email":"foo.bar@gmail.com","password":"wrongPass"})
        response = self.client.post('/login',
            data=payload, 
            content_type='application/json',
            follow_redirects=False
        )
        self.assertEqual(401, response.status_code)
    

if __name__ == '__main__':
    unittest.main()