from .app import db
from .models import Markets, User, tags
from flask import g

def addMarketToUser(ticker):
    user = User.query.filter_by(id=g.user.id).first()
    # TODO enforce there is a user (should be due to earlier protocols)
    if not ticker in user.markets:
        market = Markets.query.filter_by(ticker=ticker).first()
        print(market)
        user.markets.append(market)
        db.session.commit()
    return

def addMarketToDb(ticker):
    market = Markets.query.filter_by(ticker=ticker).first()
    if not market:
        new_market = Markets(ticker=ticker)
        db.session.add(new_market)
        db.session.commit()
    
    return