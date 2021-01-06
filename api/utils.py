from flask import g
from .app import db
from .models import Markets, User, tags


def addMarketToUser(ticker):
    user = User.query.filter_by(id=g.user.id).first()
    # TODO enforce there is a user (should be due to earlier protocols)
    if not ticker in user.markets:
        market = Markets.query.filter_by(ticker=ticker).first()
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

def removeMarket(ticker):
    user = User.query.filter_by(id=g.user.id).first()
    market = Markets.query.filter_by(ticker=ticker).first()
    if user in market.users:
        market = Markets.query.filter_by(ticker=ticker).first()
        market.users.remove(user)
        db.session.commit()
    # TODO configure deleting market from Markets if there are no longer
    # any associated users
    return

def getDayHistory(market):
    time = datetime.now() - timedelta(days=1)
    day_ago = time.strftime("%s")
    day_change = Metric.query.filter_by(close_time>=day_ago, market_id=market.id).all()
    return day_change