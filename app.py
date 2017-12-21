from flask import Flask, jsonify, abort, make_response,request
from src.market_watch import MarketWatch
app = Flask(__name__)


@app.route('/api/v1.0', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def welcome():
    """
    With no path specified, returns the following welcome message.
    :return: a JSON Welcome
    """
    welcome_msg = {
        "message": "Welcome to Crypto Alpha",
        "build": "Python Flask"
    }
    return make_response(jsonify(welcome_msg), 200)


@app.route('/<string:period>', methods=['POST', 'GET'])
def run_market_watch(period):
    msg = {
        "message": "Running",
    }
    MarketWatch().run(period)
    return make_response(jsonify(msg), 200)


@app.route('/', defaults={'path': ''})
@app.errorhandler(404)
def not_found_404(error):
    print(request)
    """
    If API aborts due to invalid input, return the below response.
    :param error: The error that caused the abort
    :return: JSON Object
    """
    return make_response(jsonify({'message': 'Not found, Invalid Parameters or URL'}), 404)