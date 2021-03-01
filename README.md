# Message-Queue-Prototype
This is a prototype of Publisher Subscriber Architecture and message queue.


## Clone Repository
    git clone https://github.com/ayush9818/Message-Queue-Prototype.git
    pip install -r requirements.txt

## Build imqserver : Run
    cd imqserver
    pip install wheel
    python setup.py sdist bdist_wheel
    python setup.py build
    python setup.py install
  
## Build imqclient : Run
    cd imqclient
    python setup.py sdist bdist_wheel
    python setup.py build
    python setup.py install
    
## Run Server
    python run_server.py

## Run Client
    python run_client.py
  
## Features
    Publisher, Subscriber and Admin functionalities for client
    Admin: 
      connect           : imq connect -r admin
      register topic    : imq register -t topic_name
      delete topic      : imq delete -t topic_name
      terminate session : imq terminate
    
    Publisher:
      connect           : imq connect -r pub -t topic_name
      publish messages  : imq publish -m message_text
      terminate session : imq terminate
    
    Subscriber: 
      connect           : imq connect -r sub -t topic_name
      pull messages     : imq pull
      terminate session : imq terminate
    
    Get Topics : 
        imq show_topics
    
    For help: 
        imq help
    

  
  
