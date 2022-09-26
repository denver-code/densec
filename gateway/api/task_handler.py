import uuid
import os

from api.database import Database
from api.middlewares import client_only, server_only
from dotenv import load_dotenv

load_dotenv()

class Task():
    def __init__(self):
        self.avaible_tasks = ["ping", "get_servers", "generate_uuid"]
        self.SECRET_KEY = os.getenv("SECRET_KEY")


    def dynamic_call(self, attribute_name, logging, socks, parsed_data):
        method_name = 'task_' + attribute_name
        func = getattr(self, method_name) 
        return func(logging, socks, parsed_data)  



    @client_only
    def task_get_servers(self, logging, socks, parsed_data):
        '''
        Sample of request - {"type":"client","task":"get_servers"}
        '''
        servers = Database().get_all_servers()
        if servers:
            msg = {"status_code":200,"data":{"servers":servers}}
        else:
            msg = {"status_code":204,"message":"No active servers"}
        logging.info(f"{socks.getpeername()[0]} - {msg=}")
        return msg


    def task_generate_uuid(self, logging, socks, parsed_data):
        '''
        Sample of request - {"type":"client","task":"generate_uuid"}
        '''
        uuid4 = str(uuid.uuid4())
        logging.info(f"{socks.getpeername()[0]} generate {uuid4=}")
        return {"status_code":200,"data":{"uuid":uuid4}}


    def task_ping(self, logging, socks, parsed_data):
        ''' 
        Sample of request - {"type":"client","task":"ping"}
        '''
        msg = {"status_code":200,"message":"pong!"}
        logging.info(f"{socks.getpeername()[0]} - {msg=}")
        return msg


    # def task_protected_ping()


    def task_process(self, logging, socks, parsed_data):
        if "type" in parsed_data :
            if "task" in parsed_data:
                if parsed_data["task"] in self.avaible_tasks: 
                    return self.dynamic_call(parsed_data['task'], logging, socks, parsed_data)
                else:
                    errmsg = {"status_code":404, "reason":"Command not found! You want use unknown task."}
                    logging.error(f"{socks.getpeername()[0]} - {errmsg=}")
                    return errmsg
            else:
                errmsg = {"status_code":404, "reason":"You don't have 'task' in request"}
                logging.error(f"{socks.getpeername()[0]} - {errmsg=}")
                return errmsg
        else:
            errmsg = {"status_code":400, "reason":"You don't have 'type' in request"}
            logging.error(f"{socks.getpeername()[0]} - {errmsg=}")
            return errmsg