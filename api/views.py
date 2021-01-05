import functools

from flask import Blueprint, jsonify, redirect, url_for, request, flash, session, g
from .app import db 
from .models import User
from cryptoClient import verifyTicker
from .utils import addMarketToDb, addMarketToUser
from werkzeug.security import generate_password_hash, check_password_hash



auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    user_data = request.get_json()
    email = user_data['email']
    password = user_data['password']

    user = User.query.filter_by(email=email).first()
    error = None
    if not user or not check_password_hash(user.password, password):
        error = 'Incorrect credentials'
    if error is None:
            session.clear()
            session['user_id'] = user.id 
            return redirect(url_for('main.add_metric'))
    # if the above check passes, then we know the user has the right credentials
    flash(error)
    return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

@auth.route('/signup', methods=['POST'])
def signup():
    user_data = request.get_json()
    email = user_data['email']
    password = user_data['password']
    # add the new user to the database
    error = None
    if not email:
        error = 'email is required.'
    elif not password:
        error = 'Password is required.'
    elif User.query.filter_by(email=email).first() is not None:
        error = 'Email {} is already registered.'.format(email)

    if error is None:
        new_user = User(email=email, password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    #flash(error)

    return redirect(url_for('auth.signup'))

@auth.route('/logout', methods=['POST'])
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

@main.route('/<metric>_day_view', methods=['GET'])
@login_required
def metric_day_view(metric):

    day_change = []

    return jsonify({'day_change':day_change})

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

    return 'Done', 201


@main.route('/remove_metric', methods=['DELETE'])
@login_required
def remove_metric():
    metric_data = request.get_json()
    metric_ticker = metric_data['ticker']
    metric_exchange = metric_data['exchange']
    isValid, ticker = verifyTicker(metric_ticker, metric_exchange)

    if isValid:
        new_market = Markets(ticker)

    return 

@main.route('/metric_rankings', methods=['GET'])
@login_required
def metric_rankings():

    return "hi"

@main.route('/my_markets', methods=['GET'])
@login_required
def my_markets():
    my_markets = User.query.filter_by(id=g.user.id).first().markets
    resp = [market.ticker for market in my_markets]
    return jsonify({"tickers":resp})


