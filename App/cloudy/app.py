import os
import logging
import math
import platform
import time

from flask import Flask
from flask import jsonify
from flask import request

from cloudy.db import DB

from cloudy.conn import get_secret
from cloudy.dao import add_user
from cloudy.dao import get_all_users


logging.basicConfig(level=logging.INFO)

DB_URI = os.environ.get('DB_URI')
APP = Flask(__name__)
LOG = logging.getLogger('cloudy')


if DB_URI is None:
    conn_secret = get_secret()
    DB_URI = ('postgresql://'
              f'{conn_secret["username"]}:'
              f'{conn_secret["password"]}@'
              f'{conn_secret["host"]}:'
              f'{conn_secret["port"]}/'
              f'{conn_secret["dbname"]}')


APP.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB.init_app(APP)


def error_handler(exception):
    """
    Used when an exception happens in the flask app.
    """
    return jsonify(message=str(exception)), 502


APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, error_handler)


with APP.app_context():
    DB.create_all()


@APP.route('/', methods=["GET"])
def root():
    LOG.info(f'[{request.method}] {request.url}')
    return jsonify(
        {
            'hostname': platform.node(),
        }
    ), 200


@APP.route('/users', methods=["POST"])
def users_post():
    LOG.info(f'[{request.method}] {request.url}')
    return jsonify(add_user(**request.json))


@APP.route('/users', methods=["GET"])
def users_get():
    LOG.info(f'[{request.method}] {request.url}')
    return jsonify(get_all_users())


@APP.route('/load', methods=["GET"])
def load_get():
    LOG.info(f'[{request.method}] {request.url}')
    number = request.args.get('number', default=112272535095293, type=int)

    result = is_prime(number)

    return jsonify(
        {
            'number': number,
            'isPrime': result[0],
            'processingTime': result[1],
        }
    ), 200


def is_prime(n):
    t1 = time.perf_counter()
    if n % 2 == 0:
        return False, time.perf_counter() - t1
    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False, time.perf_counter() - t1
    return True, time.perf_counter() - t1


if __name__ == '__main__':
    APP.run(host='127.0.0.1', debug=True, port='8080')
