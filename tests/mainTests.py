import os
import unittest
import json

from api.app import create_app, db
from api.models import User, Markets, Metric
from contextlib import contextmanager
from flask import appcontext_pushed, g, session
from werkzeug.security import generate_password_hash


class TestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        self.user = User(id=1, email="foo.bar@gmail.com", password=generate_password_hash("password123", method='sha256'))
        self.ticker1 = 'KRAKEN:BTCEUR'
        self.ticker2 = 'BINANCE:BTCUSDT'

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_getmarkets_auth(self):
        db.session.add(self.user)
        db.session.commit()
        m1 = Markets(ticker=self.ticker1)
        m2 = Markets(ticker=self.ticker2)
        db.session.add_all([m1,m2])
        db.session.commit()
        self.user.markets.append(m1)
        self.user.markets.append(m2)
        db.session.commit()
        with self.client.session_transaction() as sess:
            sess['user_id'] = self.user.id
        
        resp = self.client.get('/my_markets').get_json()['tickers']
        self.assertTrue(self.ticker1 in resp)
        self.assertTrue(self.ticker2 in resp)
    
    def test_getmarkets_noauth(self):
        # without an active user, we are redirected to login 
        resp = self.client.get('/my_markets')
        self.assertEqual(302, resp.status_code)

    def test_add_metric(self):
        db.session.add(self.user)
        db.session.commit()
        with self.client.session_transaction() as sess:
            sess['user_id'] = self.user.id
        response = self.client.post('/add_metric', 
            data=json.dumps({"ticker":"btceur","exchange":"kraken"}), 
            content_type='application/json',
            follow_redirects=False
        )
        self.assertEqual(201, response.status_code)
        response = self.client.post('/add_metric', 
            data=json.dumps({"ticker":"btcusdt","exchange":"binance"}), 
            content_type='application/json',
            follow_redirects=False
        )
        self.assertEqual(201, response.status_code)
        markets = Markets.query.all()
        self.assertTrue(len(markets)==2)
        user_metrics = User.query.first().markets
        self.assertTrue(user_metrics[0].ticker == self.ticker1)
        self.assertTrue(user_metrics[1].ticker == self.ticker2)

    def test_remove_metric(self):
        db.session.add(self.user)
        db.session.commit()
        with self.client.session_transaction() as sess:
            sess['user_id'] = self.user.id
        self.user.markets.append(Markets(ticker=self.ticker2))
        self.assertTrue(len(User.query.first().markets)==1)
        response = self.client.delete('/remove_metric', 
            data=json.dumps({"ticker":"btcusdt","exchange":"binance"}), 
            content_type='application/json',
            follow_redirects=False
        )
        self.assertEqual(204,response.status_code)
        self.assertTrue(len(User.query.first().markets)==0)

    def test_market_day_view(self):

    
    def test_metric_rankings(self):
