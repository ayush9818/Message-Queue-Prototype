HOST = "127.0.0.1"
PORT_NO = 12397
RECV_BYTES = 4096
REGEX = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
BUFFER_SIZE=100

PUB_HELP_MESSAGE = "M___Connect : imq connect -r pub -t topic_name \nPublish : imq publish -m message_text \nTermiate : imq terminate"
SUB_HELP_MESSAGE = "M___Connect : imq connect -r sub -t topic_name \nPull  : imq pull\nTermiate : imq terminate"
ADMIN_HELP_MESSAGE = "M___Connect : imq connect -r admin \nRegister : imq register -t topic_name \nDelete Queue: imq delete -t topic_name \nTermiate : imq terminate"
IMQ_HELP_MESSAGE = "M___Topics: imq show_topics \nFor Client:imq help -r pub/sub/admin"
