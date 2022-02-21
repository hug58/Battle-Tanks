import json
import pickle

BUFFER_SIZE = 2024



def _unpack(data):
	try:
		return pickle.loads(data)
	except:
		return None

def _pack(data):
	data = pickle.dumps(data)
	return data

