import cryptowatch as cw

from datetime import datetime, timedelta
from .app import db
from .models import Metric, Markets

# metrics to create could be stored in DB from user end
# then createMetrics retrieves and forms the requests

# TODO: #3 startup procedure to populate first 24 hours of data

# TODO: #2 command to clear old data after a day

# TODO: #1 email users whose instant metrics triple the 1 hr rolling average

def query():
    
    for market in Markets.query.all():
        # Forge current market ticker, like KRAKEN:BTCUSD
        #ticker = "{}:{}".format(exchange, pair).upper()
        ticker = market.ticker
        # Request weekly candles for that market
        candle = cw.markets.get(ticker, ohlc=True, periods=['1m']) 
        processCandle(candle, market)
    return 

def processCandle(candle, market):

    # Each candle is a list of [close_timestamp, open, high, low, close, volume, volume_quote]
    new_metric = Metric(
        market_id=market.id,
        close_time=candle.of_1m[-1][0], 
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
    response = cw.markets.get(ticker)
    # if response['error'] is not None:
    #     return False, ticker
    # TODO #4 if response is error return false
    return True, ticker
