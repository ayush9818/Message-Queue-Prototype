import sys
import os
sys.path.insert(1,os.path.dirname(os.getcwd()))
from imqserver.database import *


def InsertPublisherMessages(db, message):
    message_data = message.data
    created_at = message.created_at
    client_ip = message.address
    cmd="INSERT INTO PUBLISHER_MESSAGES(message_id,created_at,body,publisher_ip) VALUES(NULL,?,?,?)"
    db.execute(cmd,[created_at,message_data,str(client_ip),])

def GetMessageId(db,message):
    message_data = message.data
    created_at = message.created_at
    client_ip = message.address

    cmd="SELECT message_id FROM PUBLISHER_MESSAGES where publisher_ip=? and body=? and created_at=?"
    message_id=db.execute(cmd,[str(client_ip),message_data,created_at,])



    return message_id[0][0]

def GetUnprocessedMesssages(db,messages,address):
    unprocessed_messages = []
    for i in range(len(messages)):
        id,message_ob = messages[i]

        cmd="SELECT * FROM SUBSCRIBER_MESSAGES where message_id=? and client_ip=?"
        response=db.execute(cmd,[id,address,])
        if len(response) == 0:
            unprocessed_messages.append([id,message_ob])
    return unprocessed_messages

def ProccessMessages(db, messages,queue_id,address):
    for i in range(len(messages)):
        message_id,mesage_obj=messages[i]
        cmd="INSERT INTO SUBSCRIBER_MESSAGES(message_id,queue_id,client_ip) VALUES(?,?,?)"
        db.execute(cmd,[message_id,queue_id,address])



def DeleteTopic(db,topic_name):
    topic_mapping = fetch_topics(db,type_="dict")
    topic_id = topic_mapping[topic_name]
    topic_queue_mapping = GetTopicQueueMapping(db)
    queue_id = topic_queue_mapping[topic_id]

    cmd = "DELETE FROM TOPIC where topic_id = ?"
    db.execute(cmd,[topic_id,])
    cmd = "DELETE FROM QUEUE where queue_id = ?"
    db.execute(cmd,[queue_id,])


def fetch_topics(db, type_="list"):
    command="SELECT * from TOPIC"
    response=db.execute(command,[])
    if type_ == "list":
        topics = []
        for id,topic in response:
            topics.append(topic)
        return topics
    elif type_ == "dict":
        topics = {}
        for id,topic in response:
            topics[topic]=id
        return topics

def GetTopicQueueMapping(db):
    command="SELECT topic_id, queue_id FROM TOPIC_QUEUE_MAPPING"
    response=db.execute(command,[])
    topic_queue_mapping = {}
    for topic_id,queue_id in response:
        topic_queue_mapping[topic_id]=queue_id
    return topic_queue_mapping

def HandleNewClient(db, address, topic, role):
    command="Select * FROM ROOT WHERE client_ip = ?"
    root_response = db.execute(command, [str(address),])
    command="Select topic_id from TOPIC where topic_name=?"
    topic_id=db.execute(command,[topic,])[0][0]
    if len(root_response) > 0:
        command="Select * FROM ROOT_TOPIC_MAPPING WHERE user_id=? and topic_id=? and role=?"
        mapping_response = db.execute(command,[str(address),topic_id,role,])
        if len(mapping_response) == 0:
            command="INSERT INTO ROOT_TOPIC_MAPPING (id, user_id, topic_id, role) VALUES (NULL,?,?,?)"
            db.execute(command,[str(address),int(topic_id),str(role),])
        else:
            return True

    else:
        command="INSERT INTO ROOT (client_id, client_ip) VALUES (NULL,?)"
        db.execute(command,[str(address),])
        command="INSERT INTO ROOT_TOPIC_MAPPING (id, user_id, topic_id, role) VALUES (NULL,?,?,?)"
        db.execute(command,[str(address),int(topic_id),str(role),])

    return False


def CheckTopic(db,topic_name):
    command="SELECT * FROM TOPIC"
    response=db.execute(command, [])
    isExists = False
    for id,topic in response:
        if topic==topic_name:
            isExists=True
            break
    return isExists



def RegisterTopic(db,topic_name):

    command="SELECT * FROM TOPIC"
    response=db.execute(command, [])
    isExists = False
    for id,topic in response:
        if topic==topic_name:
            isExists=True
            break

    if isExists == False:
        command="INSERT INTO TOPIC (topic_id, topic_name) VALUES (NULL,?)"
        db.execute(command, [topic_name,])
        command="INSERT INTO QUEUE (queue_id, queue_status) VALUES (NULL,?)"
        db.execute(command, ["EMPTY",])


        command="SELECT * FROM TOPIC"
        response=db.execute(command, [])
        topic_id=response[-1][0]
        command="SELECT * FROM QUEUE"
        response=db.execute(command,[])
        queue_id=response[-1][0]

        command="INSERT INTO TOPIC_QUEUE_MAPPING (id,queue_id,topic_id) VALUES (NULL,?,?)"
        db.execute(command,[queue_id,topic_id])
    return isExists

def PrintAllTables(db):
    cmd = "SELECT name FROM sqlite_master WHERE type='table'"
    response = db.execute(cmd,[])
    for table in response:
        print(table[0])

def PrintTable(db, table_name):
    cmd = "SELECT * FROM {}".format(table_name)
    response = db.execute(cmd,[])
    for data in response:
        print(data)


if __name__ == "__main__":
    db = DATABASE(DATABASE_NAME="client_server.db")
    PrintAllTables(db)
    PrintTable(db,"ROOT")
    print("######################################")
    PrintTable(db,"PUBLISHER_MESSAGES")
    print("######################################")
    PrintTable(db,"TOPIC")
    print("######################################")
    PrintTable(db,"TOPIC_QUEUE_MAPPING")
    print("######################################")
    PrintTable(db,"ROOT_TOPIC_MAPPING")
    print("######################################")
    PrintTable(db,"SUBSCRIBER_MESSAGES")
    print("######################################")
