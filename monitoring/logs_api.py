import sys
from os import path

import yaml
from flask import Flask
from flask_restx import Api, Resource

api = Api()
app = Flask(__name__)
api.init_app(app)

logs_path = path.join(path.dirname(path.realpath(__file__)), "../logs/logs.log")


def get_logs():
    try:
        with open(logs_path) as log_file:
            return log_file.readlines()[-1000:]
    except FileNotFoundError as ex:
        return f"No logs available: {ex} "


def get_logs_errors():
    with open(logs_path) as log_file:
        return [line for line in log_file.readlines()[-1000:] if "ERROR" in line]


@api.route('/logs/all')
class HealthCheck(Resource):
    @api.doc()
    def get(self):
        return get_logs()


@api.route('/logs/errors')
class HealthCheck(Resource):
    @api.doc()
    def get(self):
        return get_logs_errors()


def get_app():
    return app


def read_config():
    current_dir = path.join(path.dirname(path.realpath(__file__)))
    with open(path.join(current_dir, '../config.yaml')) as file:
        return yaml.safe_load(file)


if __name__ == '__main__':
    config = read_config()
    if len(sys.argv) == 1:
        port = config.get('log_api_port')
    else:
        port = sys.argv[1]

    get_app().run(host=config.get('flask_host'), port=port, threaded=False, debug=True)
