from pymongo import MongoClient
from typing import List
import json

class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. Here we will use
    the metaclass method.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class BasicDb:
    def __init__(self, file_path: str):
        """
        Constructor to initialize the local JSON database.
        :param file_path: Path to the JSON file used for storing data.
        """
        self.file_path = file_path
        self._initialize_file()

    def _initialize_file(self):
        """
        Creates the JSON file if it does not exist, initializing it with an empty object.
        """
        try:
            with open(self.file_path, 'x') as file:
                json.dump({}, file)
        except FileExistsError:
            pass  # Do nothing if the file already exists.

    def _load_data(self) -> dict:
        """
        Loads data from the JSON file.
        :return: Dictionary with the loaded data.
        """
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def _save_data(self, data: dict):
        """
        Saves the data to the JSON file.
        :param data: Dictionary containing the data to save.
        """
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def save(self, collection: str, data: dict) -> dict:
        """
        Saves a document to the specified collection.
        :param collection: Name of the collection (key in the JSON).
        :param data: Document (dictionary) to save.
        :return: The saved document.
        """
        db = self._load_data()
        if collection not in db:
            db[collection] = []
        db[collection].append(data)
        self._save_data(db)
        return data

    def find(self, collection: str, query: dict) -> List[dict]:
        """
        Searches for documents in the collection that match the query.
        :param collection: Name of the collection.
        :param query: Dictionary representing the search criteria.
        :return: List of matching documents.
        """
        db = self._load_data()
        if collection not in db:
            return []
        return [item for item in db[collection] if all(item.get(k) == v for k, v in query.items())]


class ConnectMongo:
    def __init__(self, data:dict):
        self.client = MongoClient(host=data.get("host"), port=data.get("port"))
        self.db = self.client[data.get("db")]

    def save(self, collection:str, data: dict):
        collection = self.db[collection]
        collection.insert_one(data)
        return data

    def find(self, collection:str, data: dict) -> list:
        collection = self.db[collection]
        return collection.find(data).to_list()


class DatabaseManager:
    _db:BasicDb = None

    @classmethod
    def configure(cls, data:dict=None):
        # DatabaseManager.configure({"database_name":"mongo",
        #                            "db":"testing",
        #                            "host":"localhost",
        #                            "port":27017})

        if isinstance(data, dict) :
            if data.get("database_name") in ["mongo","mongodb"]:
                cls._db = ConnectMongo(data)
            else:
                cls._db = BasicDb(data.get("database_name"))



    @classmethod
    def get(cls) -> BasicDb:
        if cls._db is None:
            raise Exception("The database is not configured. Call `DatabaseManager.configure` first.")
        return cls._db
