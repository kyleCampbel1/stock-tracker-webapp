from flask import g
from flask_mail import Message
from .app import db, mail
from datetime import datetime, timedelta
from .models import Markets, Metric, User, tags

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
    # TODO #5 configure deleting market from Markets if there are no longer
    # any associated users -- would cascade delete to Metric
    return

def getDayHistory(market):
    day_ago = (datetime.utcnow() - timedelta(days=1)).timestamp()
    day_change = Metric.query.filter(Metric.close_time>=day_ago, Metric.market_id==market.id).all()
    return day_change

def emailAlerts():
    for market in Markets.query.all():
        hour_ago = (datetime.utcnow() - timedelta(hours=1)).timestamp()
        hour_change = Metric.query.filter(Metric.market_id==market.id, Metric.close_time>=hour_ago).all()
        if len(hour_change) < 3: return
        most_recent_data_point = hour_change.pop().volume
        num_pts = len(hour_change)
        accum = 0
        for pt in hour_change:
            accum += pt.volume
        avg = accum/num_pts or accum
        if most_recent_data_point >= 3*avg:
            sendMail(market)
    return

def sendMail(market):
    msgtxt = "Hello, your metric {} volume just tripled its 1hr average.".format(market.ticker)
    for user in market.users:
        msg = Message()
        msg.body = msgtxt
        msg.recipients = [user.email]
        mail.send(msg)
    return