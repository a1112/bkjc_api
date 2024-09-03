from fastapi import FastAPI
from collections import defaultdict


class ForwarderServer:
    def __init__(self, ip, port):
        self.app = FastAPI()
        self.ip = ip
        self.port = port


default_forwarder_server_dict = defaultdict(lambda: ForwarderServer(None, None))


app = FastAPI()