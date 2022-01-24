import os

from dotenv import load_dotenv
import pymongo
from datetime import datetime

load_dotenv()

class Database:
    def __init__(self):
        self.client = pymongo.MongoClient(os.getenv("database"))
        self.database = self.client["DenSec"]
        self.tasks = self.database["tasks"]
        self.servers = self.database["servers"]
    

    def create_task(self, task):
        return self.tasks.insert_one(task)
    

    def get_task_list(self):
        return list(self.tasks.find({}))


    def get_all_servers(self):
        return list(self.servers.find({}))


    def server_exist(self, uid):
        return bool(self.servers.find_one({"unique_id": uid}))


    def get_server(self, uid):
        return self.servers.find_one({"unique_id": uid})


    def active_server(self, logging, ip, port, uid):
        server_obj = self.get_server(uid)
        logging.info(f"{ip=} request active_serve")

        if not server_obj:
            logging.info(f"{ip=} not in our database, create record with him")
            return self.servers.insert_one({
                "_id": uid,
                "type": "server",
                "ip": ip,
                "socket_port": port,
                "last_ping": datetime.now().timestamp()
            })

        logging.info(f"{ip=} already in our database, update him last_ping timestamp")
        server_obj["unique_id"] = datetime.now().timestamp()
        return self.servers.update_one({"unique_id": uid}, {"$set": server_obj}, upsert=True)