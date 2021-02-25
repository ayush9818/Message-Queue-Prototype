import sys
import os
sys.path.insert(1,os.path.dirname(os.getcwd()))

import socket
import threading
from imqclient.constant import *
from request import Request
from parser import Parser

parser = Parser()

class ClientUtils():

    def __init__(self, host = HOST, port=PORT_NO):

        self.host = host
        self.port = port


    def CONNECT_SERVER(self,debug=False):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.host, self.port))
        except socket.error as errorMessage:
            raise Exception(errorMessage)

        message = self.client.recv(RECV_BYTES)
        parsed_message = parser.decode_json(message)
        server_ack = parsed_message['data']
        print(server_ack)
        return server_ack


    def rcv_msg(self):
        message = self.client.recv(RECV_BYTES)
        parsed_message = parser.decode_json(message)
        response_message = parsed_message['data']


        if response_message.split("___") == "Error":
            raise Exception(response_message.split("___")[1])
        else:
            if response_message.split("___")[1] == "terminated":
                self.client.close()
                return "exit"
            print(response_message.split("___")[1])
            return response_message.split("___")[1]




    def write(self,messages=None,debug=False):
        while True:
            if debug==False:
                message = input(">")
                message_header = Request(message)
                encoded_header = parser.encode_json(message_header)

                try:
                    self.client.send(str.encode(encoded_header))
                except Exception as e:
                    print(e)
                response = self.rcv_msg()
                if response == "exit":
                    break
            else:
                assert messages is not None, "While Debugging Message Cant be None"
                print("debugger")
                for message in messages:
                    message_header = Request(message)
                    encoded_header = parser.encode_json(message_header)
                    self.client.send(str.encode(encoded_header))
                    response = self.rcv_msg()
                    print(response)

                return response




if __name__ == "__main__":

    client = ClientUtils()

    client.CONNECT_SERVER()
    client.write(message="hello",debug=True)
    reply=client.receive(debug=True)
    print(reply.split(':')[-1])
