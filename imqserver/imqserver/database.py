import sqlite3 as sql


class DATABASE(object):

    def __init__(self, DATABASE_NAME, default = True):

        self.DATABASE_NAME = DATABASE_NAME

        self.connection = sql.connect(self.DATABASE_NAME,check_same_thread=False)
        self.cursor = self.connection.cursor()

        if default == True:
            self.create_tables()


    def create_tables(self):


        # Creating root table
        root_cmd = """
                Create TABLE IF NOT EXISTS ROOT(
                client_id INTEGER PRIMARY KEY,
                client_ip VARCHAR
               );
               """
        self.cursor.execute(root_cmd)


        # Crate Message Table
        message_cmd = """

        Create TABLE IF NOT EXISTS PUBLISHER_MESSAGES (
        message_id INTEGER PRIMARY KEY,
        created_at VARCHAR,
        body TEXT,
        publisher_ip VARCHAR
        );
        """

        self.cursor.execute(message_cmd)
        #self.connection.commit()


        # Creating Topic Table
        cmd = """

        Create TABLE IF NOT EXISTS TOPIC (

        topic_id INTEGER PRIMARY KEY,
        topic_name VARCHAR
        );

        """
        self.cursor.execute(cmd)



        # Create Queue Table
        cmd = """

        Create TABLE IF NOT EXISTS QUEUE (

        queue_id INTEGER PRIMARY KEY,
        queue_status VARCHAR
        );

        """
        self.cursor.execute(cmd)


        # CREATE TOPICQUEUE MAPPING
        cmd = """
        Create TABLE IF NOT EXISTS TOPIC_QUEUE_MAPPING (
        id INTEGER PRIMARY KEY,
        queue_id INTEGER ,
        topic_id INTEGER,
        FOREIGN KEY (queue_id) REFERENCES QUEUE(queue_id) ON DELETE CASCADE,
        FOREIGN KEY (topic_id) REFERENCES TOPIC(topic_id) ON DELETE CASCADE
        );
        """
        self.cursor.execute(cmd)



        # CREATE ROOT_TOPPIC_MAPPING
        cmd = """
        Create TABLE IF NOT EXISTS ROOT_TOPIC_MAPPING (
        id INTEGER PRIMARY KEY,
        user_id INTEGER ,
        topic_id INTEGER,
        role VARCHAR,
        FOREIGN KEY (user_id) REFERENCES ROOT(client_id) ON DELETE CASCADE,
        FOREIGN KEY (topic_id) REFERENCES TOPIC(topic_id) ON DELETE CASCADE
        );
        """
        self.cursor.execute(cmd)



        # create Processed MESSAGE
        cmd = """

        Create TABLE IF NOT EXISTS SUBSCRIBER_MESSAGES (

        message_id INTEGER ,
        queue_id INTEGER,
        client_ip VARCHAR,

        FOREIGN KEY(message_id) REFERENCES PUBLISHER_MESSAGES(message_id) ,
        FOREIGN KEY(queue_id) REFERENCES QUEUE(queue_id) ON DELETE CASCADE,
        FOREIGN KEY(client_ip) REFERENCES ROOT(client_ip) ON DELETE CASCADE
        );

        """
        self.cursor.execute(cmd)

        self.connection.commit()




    def execute(self,command, data):
        if len(data) != 0:
            self.cursor.execute(command,data)
            response=self.cursor.fetchall()
            self.connection.commit()
            return response
        else:
            self.cursor.execute(command)
            response=self.cursor.fetchall()
            self.connection.commit()
            return response
