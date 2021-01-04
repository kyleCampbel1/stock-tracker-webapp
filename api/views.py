from flask import Blueprint, jsonify, request
from .app import db 

main = Blueprint('main', __name__)

@main.route('/<metric>_day_view', methods=['GET'])
def metric_day_view(metric):

    day_change = []

    return jsonify({'day_change':day_change})

@main.route('/add_metric', methods=['POST'])
def add_metric():

    metric_data = request.get_json()
    metric_ticker = metric_data['ticker']

    return 'Done', 201


@main.route('/remove_metric', methods=['DELETE'])
def remove_metric():
    metric_data = request.get_json()
    metric_ticker = metric_data['ticker']

    return 

# to be removed -- server side method
@main.route('/update_<metric>', methods=['PUT'])
def update_metric(metric):

    return

@main.route('/metric_rankings', methods=['GET'])
def metric_rankings():

    return

