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
        self.met1 = Metric(market_id=1,close_time=1610100960.0, open_price=9580.0, high=39680.0, low=39574.7, 
            close=39604.1, volume=0.06128536, volume_quote=8521.798796526)
        self.met2 = Metric(market_id=1,close_time=1610123701.08435, open_price=9580.0, high=39680.0, low=39574.7, 
            close=39604.1, volume=0.21523387, volume_quote=8521.798796526)
        self.met3 = Metric(market_id=1,close_time=1610124061.41182, open_price=9580.0, high=39680.0, low=39574.7, 
            close=39604.1, volume=3.33267696, volume_quote=8521.798796526)
        self.met4 = Metric(market_id=1,close_time=1610124121.44782, open_price=9580.0, high=39680.0, low=39574.7, 
            close=39604.1, volume=8.54355811, volume_quote=8521.798796526)
        self.met5 = Metric(market_id=2,close_time=1610100960.0, open_price=9580.0, high=39680.0, low=39574.7, 
            close=39604.1, volume=5, volume_quote=8521.798796526)
        self.met6 = Metric(market_id=2,close_time=1610123701.08435, open_price=9580.0, high=39680.0, low=39574.7, 
            close=39604.1, volume=10, volume_quote=8521.798796526)
        self.met7 = Metric(market_id=2,close_time=1610124061.41182, open_price=9580.0, high=39680.0, low=39574.7, 
            close=39604.1, volume=2, volume_quote=8521.798796526)
        self.met8 = Metric(market_id=2,close_time=1610124121.44782, open_price=9580.0, high=39680.0, low=39574.7, 
            close=39604.1, volume=8, volume_quote=8521.798796526)

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
        response = self.client.post('/add_metric', 
            data=json.dumps({"ticker":"btcust","exchange":"biance"}), 
            content_type='application/json',
            follow_redirects=False
        )
        self.assertEqual(404, response.status_code) #request was not a real metric

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
        response = self.client.delete('/remove_metric', 
            data=json.dumps({"ticker":"btusdt","exchange":"biance"}), 
            content_type='application/json',
            follow_redirects=False
        )
        self.assertEqual(400,response.status_code) #not a valid metric
    
    def test_market_day_view(self):
        mar1 = Markets(ticker=self.ticker1)
        mar2 = Markets(ticker=self.ticker2)
        db.session.add_all([mar1,mar2, self.user])
        db.session.commit()
        self.user.markets.append(mar1)
        db.session.add_all([self.met1, self.met2, self.met3, self.met4, self.met5, self.met6, self.met7, self.met8])
        db.session.commit()
        with self.client.session_transaction() as sess:
            sess['user_id'] = self.user.id
        # user does have access
        resp = self.client.get('/btceur_kraken_day_view').get_json()['day_change']
        self.assertTrue(len(resp)==4)
        # user does not have access
        resp = self.client.get('/btcusdt_binance_day_view')
        self.assertEqual(400,resp.status_code)
        # not a real market
        resp = self.client.get('/btcust_binance_day_view')
        self.assertEqual(404,resp.status_code)

    def test_metric_rankings(self):
        mar1 = Markets(ticker=self.ticker1)
        mar2 = Markets(ticker=self.ticker2)
        db.session.add_all([mar1,mar2, self.user])
        db.session.commit()
        with self.client.session_transaction() as sess:
            sess['user_id'] = self.user.id
        resp = self.client.get('/metric_rankings').get_json()
        self.assertTrue(len(resp)==0) # no user metrics yet
        self.user.markets.append(mar1)
        self.user.markets.append(mar2)
        db.session.add_all([self.met1, self.met2, self.met3, self.met4, self.met5, self.met6, self.met7, self.met8])
        db.session.commit()
        # user does have access
        resp = self.client.get('/metric_rankings').get_json()
        self.assertTrue(len(resp)==2)