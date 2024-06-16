import json
from os import path

import mpld3
import yaml
from flask import (
    Flask,
    request,
    make_response,
    send_from_directory,
    current_app,
    send_file,
)
from flask_restx import Api, fields, Resource
from werkzeug.datastructures import FileStorage

from _logging._logger import get_logger
from data_base.mongo_wrapper import MongoWrapper
from nats_wrapper.nats_wrapper import send_message
from visualization.vizualization import plot

logger = get_logger(__name__)


def prepare_response(message: json, status: int):
    logger.info(f"Response:{message}")
    return message, status


api = Api(title="Deep learning API", default="DeepLearning")
app = Flask(__name__)
api.init_app(app)


@app.after_request
def after_request(response):
    logger.info(f"Request:{request}")

    logger.info(f"Request json:{request.get_json(silent=True)}")

    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE")
    return response


new_network_fields = api.model(
    "NewNetwork",
    {
        "name": fields.String(required=True),
        "layers": fields.List(
            fields.Raw(),
            required=True,
        ),
    },
)


@api.route("/network/new")
class NewNetwork(Resource):
    @api.doc(body=new_network_fields)
    @api.expect(new_network_fields, validate=True)
    def post(self):
        values = request.json
        response = send_message(
            service_name="new_network", data=values, logger=logger, config=read_config()
        )

        return prepare_response(response, 200)


compile_network_fields = api.model(
    "CompileNetwork",
    {
        "name": fields.String(required=True),
        "optimizer": fields.String(required=True),
        "loss": fields.String(required=True),
        "metrics": fields.List(fields.String(), required=False),
    },
)


@api.route("/network/compile")
class CompileNetwork(Resource):
    @api.doc(body=compile_network_fields)
    @api.expect(compile_network_fields, validate=True)
    def post(self):
        values = request.get_json()
        networks = send_message(
            service_name="get_networks_names",
            data="",
            logger=logger,
            config=read_config(),
        )
        if values["name"] not in networks["Networks"]:
            response = {"Message": f"Network {values['name']} not found."}
            return prepare_response(response, 200)

        response = send_message(
            service_name="compile_network",
            data=values,
            logger=logger,
            config=read_config(),
        )

        return prepare_response(response, 200)


train_network_fields = api.model(
    "TrainNetwork",
    {
        "name": fields.String(required=True),
        "data_set": fields.String(required=True),
        "epochs": fields.String(required=True),
        "batch_size": fields.String(required=True),
        "test_sample_size": fields.String(required=True),
    },
)


@api.route("/network/train")
class TrainNetwork(Resource):
    @api.doc(body=train_network_fields)
    @api.expect(train_network_fields, validate=True)
    def post(self):
        values = request.get_json()
        networks = send_message(
            service_name="get_networks_names",
            data="",
            logger=logger,
            config=read_config(),
        )

        if values["name"] not in networks["Networks"]:
            response = {"Message": f"Network {values['name']} not found."}
            return prepare_response(response, 200)

        network_details = send_message(
            service_name="get_network_details",
            data={"name": values["name"]},
            logger=logger,
            config=read_config(),
        )
        if not network_details["Compiled"]:
            response = {"Message": f"Network {values['name']} need to be compiled."}
            return prepare_response(response, 200)

        response = send_message(
            service_name="train_network",
            data=values,
            logger=logger,
            config=read_config(),
        )
        return prepare_response(response, 200)


delete_network_fields = api.model(
    "Resource",
    {
        "name": fields.String(required=True),
    },
)


@api.route("/network/delete")
class DeleteNetwork(Resource):
    @api.doc(body=delete_network_fields)
    @api.expect(delete_network_fields, validate=True)
    def delete(self):
        values = request.get_json()
        networks = send_message(
            service_name="get_networks_names",
            data="",
            logger=logger,
            config=read_config(),
        )
        if values["name"] not in networks["Networks"]:
            response = {"Message": f"Network {values['name']} not found."}
            return prepare_response(response, 200)

        response = send_message(
            service_name="delete_network",
            data=values,
            logger=logger,
            config=read_config(),
        )
        return prepare_response(response, 200)


evaluate_network_fields = api.model(
    "EvaluateNetwork",
    {
        "name": fields.String(required=True),
    },
)


@api.route("/network/evaluate")
class EvaluateNetwork(Resource):
    @api.doc(body=evaluate_network_fields)
    @api.expect(evaluate_network_fields, validate=True)
    def post(self):
        values = request.get_json()
        networks = send_message(
            service_name="get_networks_names",
            data="",
            logger=logger,
            config=read_config(),
        )
        if values["name"] not in networks["Networks"]:
            response = {"Message": f"Network {values['name']} not found."}
            return prepare_response(response, 200)

        response = send_message(
            service_name="evaluate_network",
            data=values,
            logger=logger,
            config=read_config(),
        )
        return prepare_response(response, 200)


@api.route("/")
class Default(Resource):
    @api.doc()
    def get(self):
        response = {"Message": "API running"}
        return prepare_response(response, 200)


@api.route("/networks")
class GetNetworks(Resource):
    @api.doc()
    def get(self):
        response = send_message(
            service_name="get_networks", data="", logger=logger, config=read_config()
        )
        return prepare_response(response, 200)


@api.route("/network/<string:name>")
class NetworkDetails(Resource):
    @api.doc()
    def get(self, name: str):
        response = send_message(
            service_name="get_network_details",
            data={"name": name},
            logger=logger,
            config=read_config(),
        )
        return prepare_response(response, 200)


def create_mongo(config) -> MongoWrapper:
    return MongoWrapper(
        mongo_host=config.get("mongo_host"),
        mongo_port=config.get("mongo_port"),
        data_base=config.get("mongo_base"),
        collection=config.get("mongo_collection"),
    )


def generate_hdf5_file(file_name: str, file_bytes: bytes):
    with open(file_name, "wb") as file:
        file.write(file_bytes)


@api.route("/network/export/<string:name>")
class NetworkExports(Resource):
    @api.doc()
    def get(self, name: str):
        file_name = f"{name}.hdf5"

        mongo_wrapper = create_mongo(read_config())
        data = mongo_wrapper.get_by_name(name)
        generate_hdf5_file(file_name, data["model"])

        return send_file(file_name, attachment_filename=file_name)


@api.route("/network/history/<string:name>")
class NetworkHistory(Resource):
    @api.doc()
    def get(self, name: str):
        response = send_message(
            service_name="get_network_history",
            data={"name": name},
            logger=logger,
            config=read_config(),
        )
        return prepare_response(response, 200)


@api.route("/network/plot/accuracy/<string:name>")
class PlotAccuracy(Resource):
    @api.doc()
    def get(self, name: str):
        history = send_message(
            service_name="get_network_history",
            data={"name": name},
            logger=logger,
            config=read_config(),
        )
        history = history["History"]
        history = json.loads(history)
        acc = list(history["acc"].values())
        val_acc = list(history["val_acc"].values())
        epochs = range(1, len(acc) + 1)

        plt_html = mpld3.fig_to_html(
            plot(
                epochs=epochs,
                train_values=acc,
                validation_values=val_acc,
                metric="Accuracy",
            )
        )
        headers = {"Content-Type": "text/html"}
        return make_response(plt_html, 200, headers)


@api.route("/network/plot/loss/<string:name>")
class PlotLoss(Resource):
    @api.doc()
    def get(self, name: str):
        history = send_message(
            service_name="get_network_history",
            data={"name": name},
            logger=logger,
            config=read_config(),
        )
        history = history["History"]
        history = json.loads(history)
        loss = list(history["loss"].values())
        val_loss = list(history["val_loss"].values())
        epochs = range(len(loss))

        plt_html = mpld3.fig_to_html(
            plot(
                epochs=epochs,
                train_values=loss,
                validation_values=val_loss,
                metric="Loss",
            )
        )
        headers = {"Content-Type": "text/html"}
        return make_response(plt_html, 200, headers)


@api.route("/data-sources")
class DataSources(Resource):
    @api.doc()
    def get(self):
        response = send_message(
            service_name="get_data_sources",
            data="",
            logger=logger,
            config=read_config(),
        )
        return prepare_response(response, 200)


upload_parser = api.parser()
upload_parser.add_argument("file", location="files", type=FileStorage, required=True)


@api.route("/upload-data-sources-file/<string:name>/<string:file_extension>")
class DataSourcesUpload(Resource):
    @api.expect(upload_parser, validate=False)
    @api.doc()
    def post(self, name: str, file_extension: str):
        args = upload_parser.parse_args()
        uploaded_file = args["file"]
        file_name = f"{name}.{file_extension}"
        uploaded_file.save(f"{name}.{file_extension}")

        response = send_message(
            service_name="add_data_source",
            data={"file_name": file_name},
            logger=logger,
            config=read_config(),
        )
        return prepare_response(response, 200)


@api.route("/download-data-sources-file/<string:name>")
class DataSourcesDownload(Resource):
    @api.doc()
    def get(self, name):
        uploads = current_app.root_path
        return send_from_directory(directory=uploads, filename=name)


@api.route("/healthCheck")
class HealthCheck(Resource):
    @api.doc()
    def get(self):
        response = send_message(
            service_name="health_check", data="", logger=logger, config=read_config()
        )
        response = {"Message": response}
        return prepare_response(response, 200)


def get_app():
    return app


def read_config():
    current_dir = path.join(path.dirname(path.realpath(__file__)))
    with open(path.join(current_dir, "../config.yaml")) as file:
        return yaml.safe_load(file)
