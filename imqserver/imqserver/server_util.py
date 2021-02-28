import sys
import os

sys.path.insert(1,os.path.dirname(os.getcwd()))


import socket
import threading
import os
import time
import datetime
import sqlite3 as sql
from imqserver.constant import *
from imqserver.database import *
from imqserver.MessageQueue import MessageQueue
from imqserver.message import *
import re
import imqserver.db_utils as du
from imqserver.request import Request
from imqserver.parser import Parser
from imqserver.CommandParser import CommandParser
from imqserver.errors import *
parser = Parser()
cmd_parser = CommandParser()

class ServerUtils(object):

    def __init__(self, db , host=HOST, port=PORT_NO):
        self.host = host
        self.port = port
        self.db = db
        self.IniializeMessageQueues(self.db)
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((host, port))
            self.server.listen(BUFFER_SIZE)
        except socket.error as errorMessage:
            raise Exception(errorMessage)
        self.client_connection = {}

    def getServerReply(self,server_reply):

        message_header = Request(server_reply)
        encoded_response = parser.encode_json(message_header)
        return str.encode(encoded_response)


    def DeleteQueue(self,db,topic):
        self.topic_mapping = du.fetch_topics(db,type_="dict")
        self.topic_queue_mapping = du.GetTopicQueueMapping(db)
        topic_id = self.topic_mapping[topic]

        queue_id = self.topic_queue_mapping[topic_id]
        # queue = self.message_queues[queue_id]
        del self.message_queues[queue_id]

        du.DeleteTopic(db,topic)
        self.topic_mapping = du.fetch_topics(db,type_="dict")
        self.topic_queue_mapping = du.GetTopicQueueMapping(db)

        return "M___{} deleted".format(topic)

    def DecodeClientData(self,message):
        try:
            decoded_message = parser.decode_json(message.decode("utf-8"))
            data = decoded_message['data']
        except:
            data = "Re-Enter"
        return data

    def StringiFy(self, messages):
        message_string=""
        for idx in range(len(messages)):
            message_id, message_ob = messages[idx]
            if idx == len(messages)-1:
                message_string+=message_ob.data
            else:
                message_string+=message_ob.data+'\n'
        return message_string


    def IniializeMessageQueues(self,db):

        print("Initializing Messaging Queues")

        #{topic_name : topic_id}
        self.topic_mapping = du.fetch_topics(db,type_="dict")
        #{topic_id : queue_id}
        self.topic_queue_mapping = du.GetTopicQueueMapping(db)
        self.message_queues = {}
        for topic, id in self.topic_mapping.items():
            print("hii {}  topic {} --> {} ".format(id,topic,self.topic_queue_mapping[id]))
            self.message_queues[self.topic_queue_mapping[id]] = MessageQueue()
            print("hi {}".format(self.message_queues))


    def UpdateMessageQueue(self,db,topic):
        print("updating Queue")
        self.topic_mapping = du.fetch_topics(db,type_="dict")
        self.topic_queue_mapping = du.GetTopicQueueMapping(db)
        topic_id = self.topic_mapping[topic]
        if self.topic_queue_mapping[topic_id] not in self.message_queues.keys():
            self.message_queues[self.topic_queue_mapping[topic_id]] = MessageQueue()



    def PublishMessages(self,client,address,db,topic,data):
        topic_id=self.topic_mapping[topic]
        message_queue=self.message_queues[self.topic_queue_mapping[topic_id]]
        curr_timestamp = datetime.datetime.now().strftime('%Y:%m:%d:%H_%M_%S')
        message_obj = MESSAGE(address, data, curr_timestamp)
        du.InsertPublisherMessages(db,message=message_obj)
        message_id = du.GetMessageId(db,message_obj)
        message_queue.PutMessages(message = (message_id,message_obj))
        print(message_queue)
        print("message published")



    def PullMessages(self,client,address,db,topic):
        topic_id=self.topic_mapping[topic]
        message_queue=self.message_queues[self.topic_queue_mapping[topic_id]]
        fetched_data=message_queue.FetchMessages()

        unprocessed_messages = du.GetUnprocessedMesssages(db,fetched_data,address)
        queue_id=self.topic_queue_mapping[topic_id]

        du.ProccessMessages(db,unprocessed_messages,queue_id,address)
        server_reply = self.StringiFy(unprocessed_messages)
        return server_reply


    def RegisterTopic(self,db,topic):
        isExists =du.RegisterTopic(db,topic)
        if isExists == True:
           return "M___Topic Already Exist. Try other name !"
        else:
           self.UpdateMessageQueue(db,topic)
           return "M___Topic Registered"



    def ManageQueue(self):

        while True:
            curr_time=datetime.datetime.now().strftime('%Y:%m:%d:%H_%M_%S')
            curr_time=datetime.datetime.now().strptime(curr_time,'%Y:%m:%d:%H_%M_%S')

            try:
                for message_queue in self.message_queues.values():
                    for message in message_queue.queue:
                        created_at=datetime.datetime.now().strptime(message[1].created_at,'%Y:%m:%d:%H_%M_%S')
                        diff=curr_time-created_at
                        if diff.seconds >= 120:
                            message_queue.queue.remove(message)
                            print("message deleted")
            except:
                continue


    def send_topics(self,client,db):
        topics=du.fetch_topics(db)
        if len(topics) > 0:
            topics.append("terminate")
            for topic in topics:
                client.send(self.getServerReply(topic))
        else:

            client.send(self.getServerReply("No Topics"))

    def handle(self,client,address,db):
        while True:
            try:
                command = self.DecodeClientData(client.recv(RECV_BYTES))
                cmd_response = cmd_parser.parse_commands(command)
                db_topic_list = du.fetch_topics(db)
                roles_list = ['pub', 'sub', 'admin']
                if type(cmd_response) is dict:

                    if "connect" in cmd_response.keys():
                        role = cmd_response['connect']["role"]
                        topic = cmd_response['connect']["topic"]
                        if role not in roles_list:
                            reply = INVALID_ROLE_ERROR
                            client.send(self.getServerReply(reply))
                        elif role != "admin" and topic not in db_topic_list:
                            reply = INVALID_TOPIC_ERROR
                            client.send(self.getServerReply(reply))

                        else:

                            if role != "admin":
                                database_response=du.HandleNewClient(db, address, topic, role)
                                if database_response == True:
                                    print("Client Exists")
                                else:
                                    print("New Client Created")
                            server_reply="M___Server:{}: Topic {} CONNECTED".format(address,topic)
                            client.send(self.getServerReply(server_reply))
                            self.client_connection[address]['status'] = True
                            self.client_connection[address]["topic"] = topic
                            self.client_connection[address]["role"] = role
                    elif "terminate" in cmd_response.keys():
                        client.send(self.getServerReply("M___terminated"))
                        client.close()
                        break
                    elif "show_topics" in cmd_response.keys():
                        topic_string = "M___"
                        for topic in db_topic_list:
                            topic_string+=topic+"\n"
                        client.send(self.getServerReply(topic_string))
                    else:
                        if self.client_connection[address]['status'] == False:
                            client.send(self.getServerReply(CONNECTION_ERROR))

                        elif "publish" in cmd_response.keys():
                            if self.client_connection[address]["role"] == "pub":
                                message = cmd_response["publish"]["message"]
                                topic = self.client_connection[address]["topic"]
                                self.PublishMessages(client,address,db,topic,message)
                                client.send(self.getServerReply("M___Message Published"))
                            else:
                                client.send(self.getServerReply(PUB_CONNECTION_ERROR))
                        elif "pull" in cmd_response.keys():
                            if self.client_connection[address]["role"] == "sub":
                                topic = self.client_connection[address]["topic"]
                                messages = self.PullMessages(client,address,db,topic)
                                client.send(self.getServerReply("M___{}".format(messages)))
                            else:
                                client.send(self.getServerReply(SUB_CONNECTION_ERROR))
                        elif "register" in cmd_response.keys():
                            if self.client_connection[address]['role']=="admin":
                                topic = cmd_response["register"]['topic']
                                response = self.RegisterTopic(db,topic)
                                client.send(self.getServerReply(response))
                            else:
                                client.send(self.getServerReply(ADMIN_CONNECTION_ERROR))

                        elif "delete" in cmd_response.keys():
                            current_topics = [ self.client_connection[key]['topic'] for key in self.client_connection]
                            current_topics = list(set(current_topics))
                            if self.client_connection[address]['role']=="admin":
                                topic = cmd_response["delete"]['topic']

                                if topic in current_topics:
                                    client.send(self.getServerReply(TOPIC_USED_ERROR))
                                else:
                                    response = self.DeleteQueue(db,topic)
                                    client.send(self.getServerReply(response))
                            else:
                                client.send(self.getServerReply(ADMIN_CONNECTION_ERROR))

                else:
                    client.send(self.getServerReply(cmd_response))
            except:
                break





    def receive(self,db):
        while True:
            try:
                client, addr = self.server.accept()
                client.send(self.getServerReply("Welcome"))
                address = str(addr[0])+'_'+str(addr[1])
                print(f'Connected to {str(addr)}')
                self.client_connection[address] = {}
                self.client_connection[address]['status'] = False
                thread = threading.Thread(target=self.handle, args=(client,address,db,))
                thread.start()

            except:
                print("Client Left")
                client.close()


if __name__ == '__main__':
    pass
