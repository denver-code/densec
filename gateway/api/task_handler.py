from api.database import Database

class Task():
    def __init__(self):
        self.avaible_tasks = ["serverping"]

    def dynamic_call(self, attribute_name, logging, socks, parsed_data):
        method_name = 'task_' + attribute_name
        func = getattr(self, method_name) 
        return func(logging, socks, parsed_data)  

    def new_task(self, method):
        if method == "test":
            return Database().create_task({"method":"test", "creator":"root"})
    
    def task_serverping(self, logging, socks, parsed_data):
        ''' 
        Sample of request - {"type":"client","task":"ping"}
        '''
        msg = {"statuscode":200,"message":"pong!"}
        logging.info(f"{socks.getpeername()[0]} - {msg=}")
        return msg

    def task_process(self, logging, socks, parsed_data):
        if "type" in parsed_data :
            if parsed_data["type"] == "client":
                if "task" in parsed_data:
                    if parsed_data["task"] in self.avaible_tasks: 
                        return self.dynamic_call(parsed_data['task'], logging, socks, parsed_data)
                    else:
                        errmsg = {"statuscode":404, "reason":"Command not found! Your client want use unknown task."}
                        logging.error(f"{socks.getpeername()[0]} - {errmsg=}")
                        return errmsg
                else:
                    errmsg = {"statuscode":404, "reason":"Your client don't have 'task' in parsed_data"}
                    logging.error(f"{socks.getpeername()[0]} - {errmsg=}")
                    return errmsg
            elif parsed_data["type"] == "server":
                pass
            else:
                return {"statuscode":400, "reason":"Your client have invalid 'type' in parsed_data"}
        else:
            errmsg = {"statuscode":400, "reason":"Your client don't have 'type' in parsed_data"}
            logging.error(f"{socks.getpeername()[0]} - {errmsg=}")
            return errmsg