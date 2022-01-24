import uuid

from api.database import Database
from api.middlewares import client_only, server_only

class Task():
    def __init__(self):
        self.avaible_tasks = ["serverping", "getservers", "activateserver", "generate_uuid"]


    def dynamic_call(self, attribute_name, logging, socks, parsed_data):
        method_name = 'task_' + attribute_name
        func = getattr(self, method_name) 
        return func(logging, socks, parsed_data)  


    def new_task(self, method):
        if method == "test":
            return Database().create_task({"method":"test", "creator":"root"})
    
    
    @client_only
    def task_getservers(self, logging, socks, parsed_data):
        '''
        Sample of request - {"type":"client","task":"getservers"}
        '''
        servers = Database().get_all_servers()
        if servers:
            msg = {"statuscode":200,"data":{"servers":servers}}
        else:
            msg = {"statuscode":204,"message":"No active servers :("}
        logging.info(f"{socks.getpeername()[0]} - {msg=}")
        return msg


    def task_generate_uuid(self, logging, socks, parsed_data):
        '''
        Sample of request - {"type":"client","task":"generate_uuid"}
        '''
        uuid4 = str(uuid.uuid4())
        logging.info(f"{socks.getpeername()[0]} generate {uuid4=}")
        return {"statuscode":200,"data":{"uuid":uuid4}}


    @server_only
    def task_activateserver(self, logging, socks, parsed_data):
        ''' 
        Sample of request - {"type":"server","task":"activateserver","uid":"ce13ddec-7c93-11ec-90d6-0242ac120003"}
        '''
        if "uid" not in parsed_data:
            errmsg = {"statuscode":400, "reason":"Your client don't have 'uid' in parsed_data!"}
            logging.error(f"{socks.getpeername()[0]} - {errmsg=}")
            return errmsg

        logging.info(f"Get request activateserver from server {socks.getpeername()[0]}")

        return Database().active_server(
            logging,
            socks.getpeername()[0],
            socks.getpeername()[1],
            parsed_data["uid"]
        )


    @client_only
    def task_serverping(self, logging, socks, parsed_data):
        ''' 
        Sample of request - {"type":"client","task":"serverping"}
        '''
        msg = {"statuscode":200,"message":"pong!"}
        logging.info(f"{socks.getpeername()[0]} - {msg=}")
        return msg


    def task_process(self, logging, socks, parsed_data):
        if "type" in parsed_data :
            if parsed_data["type"] in ["client", "server"]:
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
            else:
                return {"statuscode":400, "reason":"Your client have invalid 'type' in parsed_data"}
        else:
            errmsg = {"statuscode":400, "reason":"Your client don't have 'type' in parsed_data"}
            logging.error(f"{socks.getpeername()[0]} - {errmsg=}")
            return errmsg