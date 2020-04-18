import pymongo

from _logging._logger import get_logger

logger = get_logger(__name__)


def catch_exception(func):
    def __wrapper(*args, **kwrgs):
        try:
            func_name = func.__name__
            res = func(*args, **kwrgs)
            logger.debug(f"Method {func_name} executed correctly.")
            return res
        except Exception as ex:
            logger.error(f"Mongo DB exception {ex}")

    return __wrapper


class MongoWrapper:
    @catch_exception
    def __init__(self, mongo_host: str,mongo_port: str, data_base: str, collection: str):
        url = f"mongodb://{mongo_host}:{mongo_port}/"
        self.client = pymongo.MongoClient(url, serverSelectionTimeoutMS=5000)
        self.db = self.client[data_base]
        self.collection = self.db[collection]

        logger.info(f"Connected to database: {data_base} collection: {collection}")

    @catch_exception
    def insert(self, data: dict):
        self.collection.insert_one(data)

    @catch_exception
    def replace(self, data: dict):
        self.collection.find_one_and_replace({"name": data["name"]}, data)

    @catch_exception
    def get_by_name(self, name: str) -> dict:
        for network in self.collection.find({"name": name}):
            return network

    @catch_exception
    def get_all(self) -> list:
        return list(self.collection.find())

    @catch_exception
    def delete(self, name: str):
        self.collection.find_one_and_delete({"name": name})

    @catch_exception
    def drop_db(self):
        self.client.drop_database(self.db)
