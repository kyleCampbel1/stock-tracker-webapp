from flask import Blueprint, jsonify, request, g, session
from .app import db 
from .auth import login_required
from cryptoClient import verifyTicker
from .utils import addMarketToDb, addMarketToUser

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

    return

