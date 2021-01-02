import cryptowatch as cw

# metrics to create could be stored in DB from user end
# then createMetrics retrieves and forms the requests
#def createMetricData():
    # btc_data = {
    #     'exchange': 'binance',
    #     'pair': 'btcusdt',
    #     'route': 'summary'
    # }
    # eth_data = {
    #     'exchange': 'binance',
    #     'pair': 'ethbtc',
    #     'route': 'summary'
    # }
    # ltc_data = {
    #     'exchange': 'binance',
    #     'pair': 'ltcbtc',
    #     'route': 'summary'
    # }
    # nano_data = {
    #     'exchange': 'binance',
    #     'pair': 'nanobtc',
    #     'route': 'summary'
    # }
    #return
    # to be replaced with markets from db 
#     for market in kraken.markets:

#         # Forge current market ticker, like KRAKEN:BTCUSD
#         ticker = "{}:{}".format(market.exchange, market.pair).upper()
#         # Request weekly candles for that market
#         candles = cw.markets.get(ticker, ohlc=True, periods=["1w"])
#     return [btc_data, eth_data, ltc_data, nano_data]


# def query():
#     metrics = createMetricData()
#     for market in metrics:
        
#         print(response)
