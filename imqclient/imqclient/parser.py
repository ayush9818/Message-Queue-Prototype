from imqclient.imqProtocol import  imqProtocol
from imqclient.request import Request
import jsonpickle
import json




class Parser():

    def encode_json(self,header):
        return json.dumps(jsonpickle.encode(header, unpicklable=False), indent=4)


    def decode_json(self,header):
        header = json.loads(header)
        return json.loads(header)
