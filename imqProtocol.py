class imqProtocol(object):

    def __init__(self, data):
        self.data = data
        self.format = 'json'
        self.version = '1.0'

    # def __str__(self):
    #     print(f'data = {self.data} \n data_format = {self.format} \n data_version = {self.version}')
