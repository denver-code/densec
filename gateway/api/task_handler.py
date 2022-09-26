import uuid
import os

from api.database import Database
from api.middlewares import client_only, server_only
from dotenv import load_dotenv

load_dotenv()

class Task():
    def __init__(self):
        self.avaible_tasks = ["ping", "getservers", "generate_uuid"]
        self.SECRET_KEY = os.getenv("SECRET_KEY")


    def dynamic_call(self, attribute_name, logging, socks, parsed_data):
        method_name = 'task_' + attribute_name
        func = getattr(self, method_name) 
        return func(logging, socks, parsed_data)  


    # @client_only
    # def task_shutdown(self, logging, socks, parsed_data):
    #     '''
    #     Sample of request - {"type":"client","task":"shutdown","Authorization":"None"}
    #     '''


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


    def task_ping(self, logging, socks, parsed_data):
        ''' 
        Sample of request - {"type":"client","task":"serverping"}
        '''
        msg = {"statuscode":200,"message":"pong!"}
        logging.info(f"{socks.getpeername()[0]} - {msg=}")
        return msg


    def task_process(self, logging, socks, parsed_data):
        if "type" in parsed_data :
            if "task" in parsed_data:
                if parsed_data["task"] in self.avaible_tasks: 
                    return self.dynamic_call(parsed_data['task'], logging, socks, parsed_data)
                else:
                    errmsg = {"statuscode":404, "reason":"Command not found! You want use unknown task."}
                    logging.error(f"{socks.getpeername()[0]} - {errmsg=}")
                    return errmsg
            else:
                errmsg = {"statuscode":404, "reason":"You don't have 'task' in parsed_data"}
                logging.error(f"{socks.getpeername()[0]} - {errmsg=}")
                return errmsg
        else:
            errmsg = {"statuscode":400, "reason":"You don't have 'type' in parsed_data"}
            logging.error(f"{socks.getpeername()[0]} - {errmsg=}")
            return errmsg