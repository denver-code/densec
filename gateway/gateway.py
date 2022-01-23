#!/usr/bin/env python3

import os

import json
from dotenv import load_dotenv
from api.task_handler import Task
import socket
import selectors
import logging

load_dotenv()

class Server():
    def __init__(self, config):
        self.config = config
        self.selector = selectors.DefaultSelector()

        self.file_log = logging.FileHandler('gateway.log')
        self.console_out = logging.StreamHandler()

        logging.basicConfig(handlers=(self.file_log, self.console_out), 
                            format='[%(asctime)s | %(levelname)s]: %(message)s', 
                            datefmt='%m.%d.%Y %H:%M:%S',
                            level=logging.INFO)


    def server(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen()
        self.selector.register(fileobj = sock, events = selectors.EVENT_READ, data = self.accept_conn)


    def accept_conn(self, sock):
        cl_sock , connection_address = sock.accept()
        self.selector.register(fileobj = cl_sock, events = selectors.EVENT_READ, data = self.send_message)


    def send_message(self, socks):
        data = socks.recv(4096).decode("utf-8")
        try:
            parsed_data = json.loads(data) 
            logging.info(f"New message: from '{socks.getpeername()[0]}:{socks.getpeername()[1]}' info '{parsed_data}'")
            performance = Task().task_process(logging, socks, parsed_data)
            logging.info(f"Performance of request: {performance}")
            socks.sendall(json.dumps({"answer":performance}).encode("utf-8"))
        except Exception as e:
            print(e)
            try:
                logging.info(f"Close connection for address '{socks.getpeername()}'")
            except:
                logging.info(f"Close connection for unknow address")
            finally:
                self.selector.unregister(socks)
                socks.close()


    def env_loop(self):
        while True:
            events = self.selector.select()
            for key, _ in events:
                callback = key.data
                callback(key.fileobj)

    def run(self): 
        try:
            logging.info(f"'Server started at ip '{config['host']}' and port '{config['port']}', enter CTRL+C to stop.")
            self.server(
                host=self.config['host'],
                port=self.config['port']
            )
            self.env_loop()   
        except Exception as e:
            print(f"E:{e}")
            logging.info(f"Server has stopped!")
     

if __name__ == '__main__':
    config = {
        "host": os.getenv("host"),
        "port": int(os.getenv("port"))
    }
    Server(config=config).run()