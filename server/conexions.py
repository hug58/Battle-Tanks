from pymongo import MongoClient
from typing import Literal, Optional

import uuid

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
    def save(self, collection:str, data: dict):
        """ Implement save method """
        return data

    def find(self, collection:str, data: dict):
        """ Implement find method"""
        return {}

class ConnectMongo(BasicDb):
    def __init__(self, data:dict):
        self.client = MongoClient(host=data.get("host"), port=data.get("port"))
        self.db = self.client[data.get("db")]

    def save(self, collection:str, data: dict):
        collection = self.db[collection]
        return collection.insert_one(data)

    def find (self, collection:str, data: dict) -> list:
        collection = self.db[collection]
        return collection.find(data).to_list()

class DatabaseManager:
    _db:BasicDb = None

    @classmethod
    def configure(cls, data:dict=None):
        if isinstance(data, dict) :
            if data.get("database_name") in ["mongo","mongodb"]:
                cls._db = ConnectMongo(data)
        else:
            cls._db = BasicDb()


    @classmethod
    def get(cls) -> BasicDb:
        if cls._db is None:
            raise Exception("The database is not configured. Call `DatabaseManager.configure` first.")
        return cls._db
