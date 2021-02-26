
class MESSAGE(object):

    def __init__(self, address, data , timestamp):
        self.data = data
        self.created_at = timestamp
        self.address = address
