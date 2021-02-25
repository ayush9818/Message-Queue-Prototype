from imqclient.imqProtocol import imqProtocol




class Request(imqProtocol):

    def __init__(self,data):
        super().__init__(data)
        self.request_type = "Connect !!"


    def __str__(self):
        return f'data = {self.data} \ndata_format = {self.format} \ndata_version = {self.version}'







if __name__ == '__main__':

    header = Request(5)
    print(header)