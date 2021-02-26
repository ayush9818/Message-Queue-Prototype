

class MessageQueue(object):

    def  __init__(self):
        print("Empty Queue initialized")
        self.queue = list()

    def PutMessages(self, message):
        self.queue.append(message)


    def FetchMessages(self):
        messages = []
        for i in range(len(self.queue)):
            messages.append(self.queue[i])
        return messages
