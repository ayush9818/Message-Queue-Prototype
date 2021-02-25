
class CommandParser(object):



    def parse_commands(self,command):
        cmd_parts = command.split(" ")
        if "connect" in cmd_parts:

            if "-r" not in cmd_parts:
                return "Error___Provide role. For ex :imq connect -r sub/pub/admin"
            else:
                role = cmd_parts[cmd_parts.index("-r")+1]
                if role != "admin":
                    if "-t" not in cmd_parts:
                        return "Error___Topic Missing. Provide a Topic Name. For ex. imq connect -r pub -t sports"
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
                return "Error___Provide a message to publish For ex : imq publish -m hello world"
            else:
                message = " ".join(cmd_parts[cmd_parts.index("-m")+1:])
                response = {"publish" : {"message" : message}}
                return response

        if "pull" in cmd_parts:
            response = {"pull" : {}}
            return response

        if "register" in cmd_parts:
            if "-t" not in cmd_parts:
                return "Error___Provide a Topic to Register. For ex . imq register -t news"
            else:
                topic = cmd_parts[cmd_parts.index("-t")+1]
                response = {"register" : {"topic" : topic}}
                return response

        if "delete" in cmd_parts:
            if "-t" not in cmd_parts:
                return "Error___Provide a Topic to Delete. For ex . imq delete -t news"
            else:
                topic = cmd_parts[cmd_parts.index("-t")+1]
                response = {"delete" : {"topic" : topic}}
                return  response

        if "show_topics" in cmd_parts:
            response = {"show_topics" : {}}
            return response

        if "help" in cmd_parts:
            if "-r" not in cmd_parts:
                return "M___Topics: imq show_topics \nFor Client:imq help -r pub/sub/admin"
            else:
                role = cmd_parts[cmd_parts.index("-r")+1]
                if role == "pub":
                    return "M___Connect : imq connect -r pub -t topic_name \nPublish : imq publish -m message_text \nTermiate : imq terminate"
                if role == "sub":
                    return "M___Connect : imq connect -r sub -t topic_name \nPull  : imq pull\nTermiate : imq terminate"
                if role == "admin":
                    return "M___Connect : imq connect -r admin \nRegister : imq register -t topic_name \nDelete Queue: imq delete -t topic_name \nTermiate : imq terminate"



        return "Error___Not A valid Command."
