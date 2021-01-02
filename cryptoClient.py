import cryptowatch as cw
from datetime import datetime, timedelta

# metrics to create could be stored in DB from user end
# then createMetrics retrieves and forms the requests


# TODO: startup procedure of first 24 hours of data

# TODO: create limiter to turn off once queries exceed limit

def query():
    exchange = 'binance'
    pairs = ['btcusdt', 'ethbtc', 'ltcbtc', 'nanobtc']
    for pair in pairs:
        # Forge current market ticker, like KRAKEN:BTCUSD
        ticker = "{}:{}".format(exchange, pair).upper()
        print(ticker)
        # Request weekly candles for that market
        time = datetime.now() - timedelta(minutes=1)
        min_ago = time.strftime("%s")
        candle = cw.markets.get(ticker, ohlc=True, periods=['1m']) 
        processCandle(candle)
    return 


def processCandle(candle):

    # Each candle is a list of [close_timestamp, open, high, low, close, volume, volume_quote]
    print('made it')
    return


def main():

    data = query()
    print(data)

if __name__ == "__main__":
    main()