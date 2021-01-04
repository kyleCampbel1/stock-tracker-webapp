from .app import db
def addMarketToUser(ticker):
    user = Users.query.filter_by(user.id=g.id).first()
    if not ticker in user.markets:
        market = Markets.query.filter_by(ticker=ticker).first()
        db.session.add(market) #needs to link the market to the user 

def addMarketToDb(ticker):
    market = Markets.query.filter_by(ticker=ticker).first()
    if market is None:
        new_market = Markets(ticker)
        db.session.add(new_market)
        db.session.commit()
    return