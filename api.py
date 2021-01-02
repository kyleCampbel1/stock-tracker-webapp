from flask import Blueprint

main = Blueprint('api', __name__)

@main.route('/get_metric', methods=['GET'])
def get_metric():

    return 'Done', 201