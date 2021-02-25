
import sys
import os

sys.path.insert(0,'..')
sys.path.insert(1,os.path.dirname(os.getcwd()))

import sqlite3 as sql
import imqserver.db_utils as du
#from imqserver.database import *
from imqserver.server_util import *

from database import *

class Server(object):

    def __init__(self,db_name):
        self.db = DATABASE(DATABASE_NAME=db_name)
        self.server = ServerUtils(self.db)

    def run_server(self,debug=False):
        print("Server is listening!!!")

        if debug == True:
            self.server.receive(self.db,debug)
        else:

            receive_thread=threading.Thread(target=self.server.receive,args=(self.db,debug,))
            receive_thread.start()

            manage_thread = threading.Thread(target=self.server.ManageQueue)
            manage_thread.start()

if __name__== "__main__":
    new_server = Server("client_server.db")
    new_server.run_server()
