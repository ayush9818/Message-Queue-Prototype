from imqclient.imqProtocol import imqProtocol

class Request(imqProtocol):

    def __init__(self,data):
        super().__init__(data)
        self.request_type = "Connect !!"
