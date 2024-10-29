import json
import pickle

BUFFER_SIZE = 2024

def _unpack(data):
    return pickle.loads(data)

def _pack(data):
    return  pickle.dumps(data)

