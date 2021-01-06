import os
import unittest
import json

from api.app import create_app, db
from api.models import User, Markets, Metric
from contextlib import contextmanager
from flask import appcontext_pushed, g, session


@contextmanager
def user_set(app, user):
    def handler(sender, **kwargs):
        g.user = user
    with appcontext_pushed.connected_to(handler, app):
        yield

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

    def test_get_markets(self):
        u1 = User(email='john@yahoo.com', password='12345')
        db.session.add(u1)
        db.session.commit()
        exchange1 = 'kraken'
        pair1 = 'btceur'
        ticker1 = "{}:{}".format(exchange1, pair1).upper()
        exchange2 = 'binance'
        pair2 = 'btcusdt'
        ticker2 = "{}:{}".format(exchange2, pair2).upper()
        m1 = Markets(ticker=ticker1)
        m2 = Markets(ticker=ticker2)
        db.session.add(m1)
        db.session.add(m2)
        db.session.commit()
        u1.markets.append(m1)
        u1.markets.append(m2)
        db.session.commit()
        
        with self.app.app_context:
            user_set(self.app, u1)

        resp = self.client.get('/my_markets')
        self.assertEqual(len(resp['tickers']), 2)
        
