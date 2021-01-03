from flask import Blueprint, jsonify

main = Blueprint('main', __name__)

@main.route('/metric_day_view', methods=['GET'])
def metric_day_view():

    day_change = []

    return jsonify({'day_change':day_change})

@main.route('/add_metric', methods=['POST'])
def add_metric():

    return 'Done', 201