import json
import pickle

BUFFER_SIZE = 324



def _unpack(data):



	try:
		return pickle.loads(data)
		#return json.loads(data)	
	except:
		print("FINIS PATRIA")
		#print("\n\n\n")
		#print(data)

	

def _pack(data):

	data = pickle.dumps(data)

	return data
	#return bytes(data,'utf-8')

