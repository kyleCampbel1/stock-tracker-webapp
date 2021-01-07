import functools
import numpy as np

from flask import abort, Blueprint, jsonify, redirect, url_for, request, flash, session, g
from .app import db 
from .models import User, Metric, Markets
from .utils import addMarketToDb, addMarketToUser, removeMarket, getDayHistory
from .cryptoClient import verifyTicker
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    user_data = request.get_json()
    if not user_data:
        abort(400)
    try:
        email = user_data['email']
        password = user_data['password']
    except KeyError:
        abort(400, {"error":"KeyError"})
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        abort(401, {"error":"Incorrect credentials"})

    session.clear()
    session['user_id'] = user.id 
    # if the above check passes, then we know the user has the right credentials
    return redirect(url_for('main.add_metric'))

@auth.route('/signup', methods=['POST'])
def signup():
    user_data = request.get_json()
    if not user_data:
        abort(400)
    try:
        email = user_data['email']
        password = user_data['password']
    except KeyError:
        abort(400, {"error":"KeyError"})
    # add the new user to the database
    if not email or not password:
        abort(400, {"error":"missing params"})
    elif User.query.filter_by(email=email).first() is not None:
        abort(400, {"error":"Email is already registered"})
    new_user = User(email=email, password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))

@auth.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()
    return 

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

main = Blueprint('main', __name__)

@main.route('/<ticker>_<exchange>_day_view', methods=['GET'])
@login_required
def metric_day_view(ticker, exchange):
    # end point will be of the form '/btcusdt_kraken_day_view'
    isValid, ticker1 = verifyTicker(ticker, exchange)
    if isValid:
        user = User.query.filter_by(id=g.user.id).first()
        market = Markets.query.filter_by(ticker=ticker1).first()
        if not market in user.markets:
            return "Permission denied, add this metric first"
        else: # query  24 hr data
            day_change = getDayHistory(market)
            resp = [metric.as_dict() for metric in day_change]
            return jsonify({'day_change':day_change})
    
    return "Invalid link or metric identifiers"

@main.route('/add_metric', methods=['POST'])
@login_required
def add_metric():
    metric_data = request.get_json()
    metric_ticker = metric_data['ticker']
    metric_exchange = metric_data['exchange']
    isValid, ticker = verifyTicker(metric_ticker, metric_exchange)

    if isValid:
        addMarketToDb(ticker)
        addMarketToUser(ticker)
    else:
        return 'Invalid Market Identifier Error'

    return 'Done', 201


@main.route('/remove_metric', methods=['DELETE'])
@login_required
def remove_metric():
    metric_data = request.get_json()
    metric_ticker = metric_data['ticker']
    metric_exchange = metric_data['exchange']
    isValid, ticker = verifyTicker(metric_ticker, metric_exchange)

    if isValid:
        removeMarket(ticker)
    return 'Done', 204

@main.route('/metric_rankings', methods=['GET'])
@login_required
def metric_rankings():
    user = User.query.filter_by(id=g.user.id).first()
    user_market_names = np.array([market.ticker for market in user.markets])
    deviations = np.ones(len(user.markets))
    for i, market in enumerate(user.markets):
        day_change = getDayHistory(market)
        volumes = np.array([metric.volume for metric in day_change])
        stdDev = np.std(volumes)
        deviations[i] = stdDev
    sortInds = np.argsort(deviations)
    #sortedDevs = deviations[sortInds]
    #sorted_metrics = user_market_names[sortInds]
    resp = {user_market_names[i]:deviations[i] for i in sortInds}
    return resp

@main.route('/my_markets', methods=['GET'])
@login_required
def my_markets():
    my_markets = User.query.filter_by(id=g.user.id).first().markets
    resp = [market.ticker for market in my_markets]
    return jsonify({"tickers":resp})



if __name__ == '__main__':
    unittest.main()