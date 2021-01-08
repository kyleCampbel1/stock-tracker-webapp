import unittest
import json

from api.app import create_app, db
from api.cryptoClient import verifyTicker


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

    def test_verify_ticker(self):
        isTicker, ticker = verifyTicker('btcusdt','binance')
        self.assertTrue(isTicker)
        isTicker, ticker = verifyTicker('btceu','kraken')
        self.assertFalse(isTicker)
