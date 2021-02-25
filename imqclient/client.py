import sys
import os



sys.path.insert(1,os.path.dirname(os.getcwd()))

from imqclient.client_util import ClientUtils
import threading

class Client(object):

    def run(self):
        client = ClientUtils()
        client.CONNECT_SERVER()
        # receive_thread = threading.Thread(target=client.receive)
        # receive_thread.start()

        write_thread = threading.Thread(target=client.write)
        write_thread.start()



if __name__ == '__main__':
    new_client = Client()
    new_client.run()
