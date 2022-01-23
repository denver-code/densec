import os

from dotenv import load_dotenv
import pymongo

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