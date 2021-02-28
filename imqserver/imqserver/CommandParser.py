from imqserver.errors import *
from imqserver.constant import *


class CommandParser(object):



    def parse_commands(self,command):
        cmd_parts = command.split(" ")
        if "connect" in cmd_parts:

            if "-r" not in cmd_parts:
                return PROVIDE_ROLE_ERROR
            else:
                role = cmd_parts[cmd_parts.index("-r")+1]
                if role != "admin":
                    if "-t" not in cmd_parts:
                        return CONNECT_TOPIC_ERROR
                    else:
                        topic = cmd_parts[cmd_parts.index("-t")+1]
                else:
                    topic = None
                response = {'connect' : {'role' : role, 'topic' : topic}}
                return response
        if "terminate" in cmd_parts:
            response = {'terminate' : {}}
            return response

        if "publish" in cmd_parts:
            if "-m" not in cmd_parts:
                return MISSING_MESSAGE_ERROR
            else:
                message = " ".join(cmd_parts[cmd_parts.index("-m")+1:])
                response = {"publish" : {"message" : message}}
                return response

        if "pull" in cmd_parts:
            response = {"pull" : {}}
            return response

        if "register" in cmd_parts:
            if "-t" not in cmd_parts:
                return REGISTER_TOPIC_ERROR
            else:
                topic = cmd_parts[cmd_parts.index("-t")+1]
                response = {"register" : {"topic" : topic}}
                return response

        if "delete" in cmd_parts:
            if "-t" not in cmd_parts:
                return DELETE_TOPIC_ERROR
            else:
                topic = cmd_parts[cmd_parts.index("-t")+1]
                response = {"delete" : {"topic" : topic}}
                return  response

        if "show_topics" in cmd_parts:
            response = {"show_topics" : {}}
            return response

        if "help" in cmd_parts:
            if "-r" not in cmd_parts:
                return IMQ_HELP_MESSAGE
            else:
                role = cmd_parts[cmd_parts.index("-r")+1]
                if role == "pub":
                    return PUB_HELP_MESSAGE
                if role == "sub":
                    return SUB_HELP_MESSAGE
                if role == "admin":
                    return ADMIN_HELP_MESSAGE



        return COMMAND_ERROR
