from .app import db
from .models import Markets, User, tags
from flask import g

def addMarketToUser(ticker):
    user = User.query.filter_by(id=g.user.id).first()
    # TODO enforce there is a user (should be due to earlier protocols)
    if not ticker in user.markets:
        market = Markets.query.filter_by(ticker=ticker).first()
        sql = "INSERT INTO tags (user_id, market_id) VALUES ({}, {})".format(user.id, market.id)
        db.session.execute(sql)
    return

def addMarketToDb(ticker):
    market = Markets.query.filter_by(ticker=ticker).first()
    if market is None:
        new_market = Markets(ticker=ticker)
        db.session.add(new_market)
        db.session.commit()
    
    return