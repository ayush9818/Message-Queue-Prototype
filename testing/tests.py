import sys
import os
from imqserver import *
import time
import unittest
import threading
from imqserver.server import *
from imqserver.database import *
import imqserver.db_utils as du
from imqserver.request import Request
from imqserver.imqProtocol import imqProtocol
from imqserver.CommandParser import *
from imqserver.errors import *



class TESTCASES(unittest.TestCase):

    def test_protocol(self):
        data = "hello"
        data_protocol = imqProtocol(data)
        self.assertEqual(data_protocol.data,data)
        self.assertEqual(data_protocol.format,"json")
        self.assertEqual(data_protocol.version,"1.0")

    def test_request(self):
        data = "hello"
        data_request = Request(data)
        self.assertEqual(data_request.data,data)
        self.assertEqual(data_request.format,"json")
        self.assertEqual(data_request.version,"1.0")

    def test_admin_connect_command(self):
        command = "imq connect -r admin"
        parser = CommandParser()
        response = parser.parse_commands(command)
        self.assertEqual(response['connect']['role'],'admin')

    def test_connect_validity(self):
        command = "imq connect"
        parser = CommandParser()
        response=parser.parse_commands(command)
        self.assertEqual(response,PROVIDE_ROLE_ERROR)

    def test_pub_connect_command(self):
        command = "imq connect -r pub -t sports"
        parser = CommandParser()
        response = parser.parse_commands(command)
        self.assertEqual(response['connect']['role'],'pub')
        self.assertEqual(response['connect']['topic'],'sports')

    def test_sub_connect_command(self):
        command = "imq connect -r sub -t sports"
        parser = CommandParser()
        response = parser.parse_commands(command)
        self.assertEqual(response['connect']['role'],'sub')
        self.assertEqual(response['connect']['topic'],'sports')

    def test_delete_command(self):
        command = "imq delete"
        parser=CommandParser()
        response=parser.parse_commands(command)
        self.assertEqual(response,DELETE_TOPIC_ERROR)

    def test_topic_existence(self):
        db_name = "test.db"
        if os.path.exists(db_name):
            os.remove(db_name)
        db = DATABASE("test.db")
        topic_name = "sports"
        isExists = du.CheckTopic(db,topic_name)
        self.assertEqual(isExists,False)

    def test_topic_register(self):
        db_name = "test.db"
        if os.path.exists(db_name):
            os.remove(db_name)
        db = DATABASE("test.db")
        topic_name = "sports"
        du.RegisterTopic(db,topic_name)
        isExists = du.CheckTopic(db,topic_name)
        self.assertEqual(isExists,True)

    def test_delete_topic(self):
        db_name = "test.db"
        if os.path.exists(db_name):
            os.remove(db_name)
        db = DATABASE("test.db")
        topic_name = "sports"
        du.RegisterTopic(db,topic_name)
        du.DeleteTopic(db,topic_name)
        isExists = du.CheckTopic(db,topic_name)
        self.assertEqual(isExists,False)

    def test_topic_list(self):
        db_name = "test.db"
        if os.path.exists(db_name):
            os.remove(db_name)
        db = DATABASE("test.db")
        topic_name_1 = "sports"
        du.RegisterTopic(db,topic_name_1)
        topic_name_2 = "news"
        du.RegisterTopic(db, topic_name_2)

        fetched_topics = du.fetch_topics(db,type_="list")
        fetched_topics_1 = fetched_topics[0]
        fetched_topics_2 = fetched_topics[1]

        self.assertEqual(topic_name_1,fetched_topics_1)
        self.assertEqual(topic_name_2,fetched_topics_2)

    def test_new_client(self):
        db_name = "test.db"
        if os.path.exists(db_name):
            os.remove(db_name)
        db = DATABASE("test.db")
        topic_name = "sports"
        du.RegisterTopic(db,topic_name)
        address = "172.1.0.1_1234"
        role = "pub"
        status = du.HandleNewClient(db,address,topic_name,role)
        self.assertEqual(status,False)
        status = du.HandleNewClient(db,address,topic_name,role)
        self.assertEqual(status,True)
