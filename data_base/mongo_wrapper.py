import pymongo


class MongoWrapper:
    def __init__(self, url: str, data_base: str, collection: str):
        self.client = pymongo.MongoClient(url, serverSelectionTimeoutMS=5000)
        self.db = self.client[data_base]
        self.collection = self.db[collection]

    def insert(self, data: dict):
        self.collection.insert_one(data)

    def replace(self, data: dict):
        self.collection.find_one_and_replace({"name": data["name"]}, data)

    def get_by_name(self, name: str):
        for network in self.collection.find({}, {"name": name}):
            return network

    def get_all(self):
        return self.collection.find()

    def delete(self, name: str):
        self.collection.find_one_and_delete({"name": name})
