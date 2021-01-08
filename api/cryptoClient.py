import cryptowatch as cw
import json

from datetime import datetime
from .app import db
from .models import Metric, Markets

# metrics to create could be stored in DB from user end
# then createMetrics retrieves and forms the requests

# TODO: #3 startup procedure to populate first 24 hours of data

# TODO: #2 command to clear old data after a day

# TODO: #1 email users whose instant metrics triple the 1 hr rolling average

def query():
    
    for market in Markets.query.all():
        ticker = market.ticker
        # Request weekly candles for that market
        candle = cw.markets.get(ticker, ohlc=True, periods=['1m']) 
        processCandle(candle, market)
    return 

def processCandle(candle, market):

    # Each candle is a list of [close_timestamp, open, high, low, close, volume, volume_quote]
    new_metric = Metric(
        market_id=market.id,
        close_time=datetime.utcnow().timestamp(), 
        open_price=candle.of_1m[-1][1], 
        high=candle.of_1m[-1][2],
        low=candle.of_1m[-1][3],
        close=candle.of_1m[-1][4],
        volume=candle.of_1m[-1][5],
        volume_quote=candle.of_1m[-1][6]
        )
    db.session.add(new_metric)
    db.session.commit()
    #print(str(datetime.utcnow()), 'Done!')
    return

def verifyTicker(pair, exchange):
    ticker = "{}:{}".format(exchange, pair).upper()
    try:
        response = cw.markets.get(ticker).market
    except:
        return False, ticker
    return True, ticker
