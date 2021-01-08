import unittest

from api.cryptoClient import verifyTicker


class TestCase(unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_verify_ticker(self):
        isTicker, ticker = verifyTicker('btcusdt','binance')
        self.assertTrue(isTicker)
        isTicker, ticker = verifyTicker('btceu','kraken')
        self.assertFalse(isTicker)
