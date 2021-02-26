import sys
sys.path.append('..')


from imqserver import *
import time
import unittest
from imqclient.client_util import *
from imqserver.server import *
import threading
import multiprocessing
from imqserver.database import *
import imqserver.db_utils as du

import os
def func():
    sys.exit()

counter = 0

class TESTCASES(unittest.TestCase):

    def setUp(self):
        db_name="client_server.db"
        self.server_thread=threading.Thread(target=run_server,args=(db_name,))
        self.server_thread.start()
        time.sleep(0.1)
        self.client = ClientUtils()

    def test_connection(self):
        '''
        Check the Connection
        '''
        server_response=self.client.CONNECT_SERVER()
        print("Server response is {}".format(server_response))
        self.assertEqual(server_response,"Welcome")

    def test_admin_connection(self):
        server_response=self.client.CONNECT_SERVER()
        # # print("Server response is {}".format(server_response))

        commands = ["imq connect -r admin"]
        server_response = self.client.write(commands,debug=True).split(" ")[-1]
        self.assertEqual(server_response,"CONNECTED")

    # def test_admin(self):
    #     # client=ClientUtils()
    #     server_response=self.client.CONNECT_SERVER()
    #     # # print("Server response is {}".format(server_response))
    #
    #     commands = ["imq connect -r admin", "imq register -t sports"]
    #     server_response = self.client.write(commands,debug=True)
    #     self.assertEqual(server_response,"Topic Registered")



    def test_pub_connection(self):
        server_response=self.client.CONNECT_SERVER()
        # # print("Server response is {}".format(server_response))

        commands = ["imq connect -r pub -t sports"]
        server_response = self.client.write(commands,debug=True).split(" ")[-1]
        self.assertEqual(server_response,"CONNECTED")

    def test_sub_connection(self):
        server_response=self.client.CONNECT_SERVER()

        commands = ["imq connect -r sub -t sports"]
        server_response = self.client.write(commands,debug=True).split(" ")[-1]
        self.assertEqual(server_response,"CONNECTED")


    def test_publisher(self):
        #client=ClientUtils()
        time.sleep(0.1)
        server_response=self.client.CONNECT_SERVER()
        commands = ["imq connect -r pub -t sports", "imq publish -m Hello"]
        server_response = self.client.write(commands,debug=True)
        self.assertEqual(server_response,"Message Published")

    def test_connect_command(self):
        time.sleep(0.1)
        server_response=self.client.CONNECT_SERVER()
        commands = ["imq connect"]
        server_response = self.client.write(commands,debug=True)
        self.assertEqual(server_response,"Provide role. For ex :imq connect -r sub/pub/admin")

    def test_subscriber(self):
        time.sleep(0.1)
        server_response=self.client.CONNECT_SERVER()
        commands = ["imq connect -r sub -t sports", "imq pull"]
        server_response = self.client.write(commands,debug=True)
        self.assertEqual(server_response,"Hello")

    def test_show_command(self):
        time.sleep(0.1)
        server_response=self.client.CONNECT_SERVER()
        commands = ["imq show_topics"]
        server_response = self.client.write(commands,debug=True)
        self.assertEqual(server_response,"sports\n")

    def test_func(self):
        self.assertRaises(SystemExit, func)

    # def test_break(self):
    #     self.assertEqual(,3)

    def tearDown(self):
        global counter
        counter+=1

        if counter>=9:
            os._exit()
            # with self.assertRaises(SystemExit) as cm:
            #     sys.exit(0)
        print('TearDown')
        #self.assertEqual(2,3)
        self.server_thread.join()




def run_server(db_name):
    new_server = Server(db_name)
    new_server.run_server(debug=False)




if __name__=='__main__':
    # db_name="client_server.db"
    # server_thread=threading.Thread(target=run_server,args=(db_name,))
    # server_thread.start()
    # time.sleep(0.1)


    unittest.main(failfast=True)
    #server_thread.join()
    sys.exit(0)
