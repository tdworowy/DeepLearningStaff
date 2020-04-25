import json
from os import path

import mpld3
import yaml
from flask import Flask, request, make_response
from flask_restplus import Api, fields, Resource

from _logging._logger import get_logger
from data.data_provider import data_sources
from nats_wrapper.nats_wrapper import send_message
from visualization.vizualization import plot

logger = get_logger(__name__)


def prepare_response(message: json, status: int):
    logger.info(f"Response:{message}")
    return message, status


api = Api()
app = Flask(__name__)
api.init_app(app)


@app.after_request
def after_request(response):
    logger.info(f"Request:{request}")

    logger.info(f"Request json:{request.get_json(silent=True)}")

    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


new_network_fields = api.model('NewNetwork', {
    'name': fields.String(required=True),
    'layers': fields.List(fields.Raw(), required=True, ),
})


@api.route('/network/new')
class NewNetwork(Resource):
    @api.doc(body=new_network_fields)
    @api.expect(new_network_fields, validate=True)
    def post(self):
        values = request.json
        response = send_message(service_name="new_network",
                                data=values,
                                logger=logger,
                                config=read_config())

        return prepare_response(response, 200)


compile_network_fields = api.model('CompileNetwork', {
    'name': fields.String(required=True),
    'optimizer': fields.String(required=True),
    'loss': fields.String(required=True),
    'metrics': fields.List(fields.String(), required=False),
})


@api.route('/network/compile')
class CompileNetwork(Resource):
    @api.doc(body=compile_network_fields)
    @api.expect(compile_network_fields, validate=True)
    def post(self):
        values = request.get_json()
        networks = send_message(service_name="get_networks",
                                data="",
                                logger=logger,
                                config=read_config())
        if values["name"] not in networks['Networks']:
            response = {
                "Message": f"Network {values['name']} not found."
            }
            return prepare_response(response, 200)

        response = send_message(service_name="compile_network",
                                data=values,
                                logger=logger,
                                config=read_config())

        return prepare_response(response, 200)


train_network_fields = api.model('TrainNetwork', {
    'name': fields.String(required=True),
    'data_set': fields.String(required=True),
    'epochs': fields.String(required=True),
    'batch_size': fields.String(required=True),
    'test_sample_size': fields.String(required=True),
})


@api.route('/network/train')
class TrainNetwork(Resource):
    @api.doc(body=train_network_fields)
    @api.expect(train_network_fields, validate=True)
    def post(self):
        values = request.get_json()
        networks = send_message(service_name="get_networks",
                                data="",
                                logger=logger,
                                config=read_config())

        if values["name"] not in networks['Networks']:
            response = {
                "Message": f"Network {values['name']} not found."
            }
            return prepare_response(response, 200)

        network_details = send_message(service_name="get_network_details",
                                       data={'name': values["name"]},
                                       logger=logger,
                                       config=read_config())
        if not network_details["Compiled"]:
            response = {
                "Message": f"Network {values['name']} need to be compiled."
            }
            return prepare_response(response, 200)

        response = send_message(service_name="train_network",
                                data=values,
                                logger=logger,
                                config=read_config())
        return prepare_response(response, 200)


delete_network_fields = api.model('Resource', {
    'name': fields.String(required=True),
})


@api.route('/network/delete')
class DeleteNetwork(Resource):
    @api.doc(body=delete_network_fields)
    @api.expect(delete_network_fields, validate=True)
    def delete(self):
        values = request.get_json()
        networks = send_message(service_name="get_networks",
                                data="",
                                logger=logger,
                                config=read_config())
        if values["name"] not in networks['Networks']:
            response = {
                "Message": f"Network {values['name']} not found."
            }
            return prepare_response(response, 200)

        response = send_message(service_name="delete_network",
                                data=values,
                                logger=logger,
                                config=read_config())
        return prepare_response(response, 200)


evaluate_network_fields = api.model('EvaluateNetwork', {
    'name': fields.String(required=True),
})


@api.route('/network/evaluate')
class EvaluateNetwork(Resource):
    @api.doc(body=evaluate_network_fields)
    @api.expect(evaluate_network_fields, validate=True)
    def post(self):
        values = request.get_json()
        networks = send_message(service_name="get_networks",
                                data="",
                                logger=logger,
                                config=read_config())
        if values["name"] not in networks['Networks']:
            response = {
                "Message": f"Network {values['name']} not found."
            }
            return prepare_response(response, 200)

        response = send_message(service_name="evaluate_network",
                                data=values,
                                logger=logger,
                                config=read_config())
        return prepare_response(response, 200)


@api.route('/')
class Default(Resource):
    @api.doc()
    def get(self):
        response = {
            "Message": "API running"
        }
        return prepare_response(response, 200)


@api.route('/networks')
class GetNetworks(Resource):
    @api.doc()
    def get(self):
        response = send_message(service_name="get_networks",
                                data="",
                                logger=logger,
                                config=read_config())
        return prepare_response(response, 200)


@api.route('/network/<string:name>')
class NetworkDetails(Resource):
    @api.doc()
    def get(self, name: str):
        response = send_message(service_name="get_network_details",
                                data={'name': name},
                                logger=logger,
                                config=read_config())
        return prepare_response(response, 200)


@api.route('/network/history/<string:name>')
class NetworkHistory(Resource):
    @api.doc()
    def get(self, name: str):
        response = send_message(service_name="get_network_history",
                                data={'name': name},
                                logger=logger,
                                config=read_config())
        return prepare_response(response, 200)


@api.route('/network/plot/accuracy/<string:name>')
class PlotAccuracy(Resource):
    @api.doc()
    def get(self, name: str):
        history = send_message(service_name="get_network_history",
                               data={'name': name},
                               logger=logger,
                               config=read_config())
        history = history["History"]
        history = json.loads(history)
        acc = list(history['acc'].values())
        val_acc = list(history['val_acc'].values())
        epochs = range(1, len(acc) + 1)

        plt_html = mpld3.fig_to_html(plot(epochs=epochs,
                                          train_values=acc,
                                          validation_values=val_acc,
                                          metric="Accuracy"))
        headers = {'Content-Type': 'text/html'}
        return make_response(plt_html, 200, headers)


@api.route('/network/plot/loss/<string:name>')
class PlotLoss(Resource):
    @api.doc()
    def get(self, name: str):
        history = send_message(service_name="get_network_history",
                               data={'name': name},
                               logger=logger,
                               config=read_config())
        history = history["History"]
        history = json.loads(history)
        loss = list(history['loss'].values())
        val_loss = list(history['val_loss'].values())
        epochs = range(len(loss))

        plt_html = mpld3.fig_to_html(plot(epochs=epochs,
                                          train_values=loss,
                                          validation_values=val_loss,
                                          metric="Loss"))
        headers = {'Content-Type': 'text/html'}
        return make_response(plt_html, 200, headers)


@api.route('/data-sources')
class DataSources(Resource):
    @api.doc()
    def get(self):
        response = data_sources()
        response = {"Dat_Sources": response}
        return prepare_response(response, 200)


@api.route('/healthCheck')
class HealthCheck(Resource):
    @api.doc()
    def get(self):
        response = send_message(service_name="health_check",
                                data="",
                                logger=logger,
                                config=read_config())
        response = {
            "Message": response
        }
        return prepare_response(response, 200)


def get_app():
    return app


def read_config():
    current_dir = path.join(path.dirname(path.realpath(__file__)))
    with open(path.join(current_dir, '../config.yaml')) as file:
        return yaml.safe_load(file)
