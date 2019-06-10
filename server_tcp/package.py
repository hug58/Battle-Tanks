import json

def unpack(data):
    return json.loads(data)

def pack(data):
    data = json.dumps(data)
    return bytes(data,'utf-8')

