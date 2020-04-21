import json

import pandas as pd
from keras import models
from _logging._logger import get_logger
from datetime import datetime

logger = get_logger(__name__)


class ModelWrapper:
    def __init__(self, name: str, model: models, compiled: bool, trained: bool, history_json: json = None,
                 update_time_stamp=None):
        self.trained = trained
        self.compiled = compiled
        self.model = model
        self.name = name
        self.history_json = history_json
        self.update_time_stamp = update_time_stamp
        self.deleted = False


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class KerasWrapper(metaclass=Singleton):

    def __init__(self, _models: dict = None):
        if _models:
            self.models = _models
        else:
            self.models = dict()

    def add_model(self, name: str, model: models, compiled=False, trained=False):
        logger.info(f"Add new Model {name}")
        self.models[name] = ModelWrapper(name=name,
                                         model=model,
                                         compiled=compiled,
                                         trained=trained)
        self.models[name].update_time_stamp = datetime.now()

    def compile(self, model_name: str, optimizer: str, loss: str, metrics: list):
        logger.info(f"Compiled model {model_name}")
        self.get_model(model_name).model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
        self.get_model(model_name).compiled = True
        self.get_model(model_name).update_time_stamp = datetime.now()

    def train(self, model_name: str, train_data, train_labels, val_data, val_labels, epochs: int, batch_size: int):
        logger.info(f"Train model {model_name}")
        history = self.get_model(model_name).model.fit(train_data, train_labels,
                                                       epochs=epochs,
                                                       batch_size=batch_size,
                                                       validation_data=(val_data, val_labels))
        self.get_model(model_name).trained = True
        self.get_model(model_name).history_json = pd.DataFrame.from_dict(history.history).to_json()
        self.get_model(model_name).update_time_stamp = datetime.now()

    def evaluate(self, model_name: str, test_data, test_labels):
        logger.info(f"Evaluate model {model_name}")
        return self.get_model(model_name).model.evaluate(test_data, test_labels)

    def serialize_model(self, model_name: str, path: str):
        self.get_model(model_name).model.save(path)

    def delete_network(self, model_name: str):
        self.get_model(model_name).deleted = True

    def get_models_names(self) -> list:
        if self.models:
            return [model.name for model in list(self.models.values()) if not model.deleted]
        else:
            return []

    def get_models(self) -> list or None:
        if self.models:
            return [model for model in list(self.models.values()) if not model.deleted]
        else:
            return None

    def get_model(self, model_name: str):
        return self.models[model_name] if not self.models[model_name].deleted else None

    def get_deleted_models_names(self) -> list:
        if self.models:
            return [model.name for model in list(self.models.values()) if model.deleted]
        else:
            return []
