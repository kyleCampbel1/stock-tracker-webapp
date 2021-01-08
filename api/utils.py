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

def getMetricHistory(market, hours):
    time_ago = (datetime.utcnow() - timedelta(hours=hours)).timestamp()
    change = Metric.query.filter(Metric.close_time>=time_ago, Metric.market_id==market.id).all()
    return change

def emailAlerts():
    for market in Markets.query.all():
        hour_change = getMetricHistory(market, 1)
        if len(hour_change) < 4: return
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